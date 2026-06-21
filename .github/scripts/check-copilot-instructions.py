#!/usr/bin/env python3
"""Report Copilot instruction drift from sibling repositories.

The workflow searches repositories owned by OWNER for files named
copilot-instructions.md, compares them with this repository's baseline file,
and opens or updates a GitHub issue with diffs and merge commands.
"""

from __future__ import annotations

import base64
import difflib
import json
import os
import pathlib
import shlex
import sys
import textwrap
import urllib.error
import urllib.parse
import urllib.request


GITHUB_API_BASE_URL = "https://api.github.com"
ISSUE_TITLE = "Weekly Copilot instructions changes detected"
MAX_ISSUE_BODY = 60_000
MAX_DIFF_CHARS = 12_000
MAX_SEARCH_PAGES = 10


class GitHubApiError(RuntimeError):
    """Raised when the GitHub API returns an unexpected response."""


def env_required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise GitHubApiError(f"Missing required environment variable: {name}")
    return value


def request_json(
    method: str,
    path: str,
    token: str,
    *,
    body: dict[str, object] | None = None,
    accept: str = "application/vnd.github+json",
) -> dict[str, object] | list[object]:
    data = None
    headers = {
        "Accept": accept,
        "Authorization": "Bearer " + token,
        "User-Agent": "agentstandards-copilot-instructions-sync",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(
        f"{GITHUB_API_BASE_URL}{path}",
        data=data,
        headers=headers,
        method=method,
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            response_body = response.read()
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise GitHubApiError(f"GitHub API {method} {path} failed: {error.code} {detail}") from error

    if not response_body:
        return {}
    return json.loads(response_body.decode("utf-8"))


def owner_qualifier(owner: str, token: str) -> str:
    user = request_json("GET", f"/users/{urllib.parse.quote(owner)}", token)
    if isinstance(user, dict) and user.get("type") == "Organization":
        return f"org:{owner}"
    return f"user:{owner}"


def search_instruction_files(owner: str, token: str) -> list[dict[str, str]]:
    qualifier = owner_qualifier(owner, token)
    query = f"filename:copilot-instructions.md {qualifier}"
    encoded_query = urllib.parse.quote(query)
    files: list[dict[str, str]] = []

    for page in range(1, MAX_SEARCH_PAGES + 1):
        result = request_json(
            "GET",
            f"/search/code?q={encoded_query}&per_page=100&page={page}",
            token,
        )
        if not isinstance(result, dict):
            raise GitHubApiError("Unexpected GitHub code search response")
        items = result.get("items", [])
        if not isinstance(items, list) or not items:
            break

        for item in items:
            if not isinstance(item, dict):
                continue
            repository = item.get("repository", {})
            if not isinstance(repository, dict):
                continue
            full_name = repository.get("full_name")
            path = item.get("path")
            url = item.get("url")
            if isinstance(full_name, str) and isinstance(path, str) and isinstance(url, str):
                files.append({"repository": full_name, "path": path, "url": url})

        if len(items) < 100:
            break

    return sorted(files, key=lambda entry: (entry["repository"], entry["path"]))


def fetch_file_text(contents_url: str, token: str) -> str:
    parsed_url = urllib.parse.urlparse(contents_url)
    content = request_json("GET", parsed_url.path, token)
    if not isinstance(content, dict):
        raise GitHubApiError("Unexpected GitHub contents response")
    encoded = content.get("content")
    if not isinstance(encoded, str):
        raise GitHubApiError("GitHub contents response did not include file content")
    return base64.b64decode(encoded).decode("utf-8", errors="replace")


def unified_diff(
    baseline_repository: str,
    baseline_path: str,
    source_path: str,
    baseline: str,
    candidate: str,
) -> str:
    diff = difflib.unified_diff(
        baseline.splitlines(keepends=True),
        candidate.splitlines(keepends=True),
        fromfile=f"{baseline_repository}/{baseline_path}",
        tofile=source_path,
    )
    return "".join(diff)


def merge_command(repository: str, source_path: str, baseline_path: str) -> str:
    quoted_repository = shlex.quote(repository)
    quoted_source_path = shlex.quote(source_path)
    quoted_baseline_path = shlex.quote(baseline_path)
    return textwrap.dedent(
        f"""\
        SOURCE_REPO={quoted_repository}
        SOURCE_PATH={quoted_source_path}
        BASELINE_PATH={quoted_baseline_path}
        BRANCH="sync-copilot-instructions-${{SOURCE_REPO##*/}}"
        if [ -n "$(git status --porcelain)" ]; then
          echo "Working directory is not clean. Commit, stash, or discard changes first."
          exit 1
        fi
        git checkout -b "${{BRANCH}}"
        gh api "repos/${{SOURCE_REPO}}/contents/${{SOURCE_PATH}}" --jq .content | base64 --decode > "${{BASELINE_PATH}}"
        git add "${{BASELINE_PATH}}"
        git commit -m "Sync Copilot instructions from ${{SOURCE_REPO}}"
        git push --set-upstream origin "${{BRANCH}}"
        gh pr create --title "Sync Copilot instructions from ${{SOURCE_REPO}}" --body "Updates ${{BASELINE_PATH}} from ${{SOURCE_REPO}}/${{SOURCE_PATH}}."
        """
    ).strip()


def build_issue_body(
    baseline_path: str,
    current_repository: str,
    changes: list[dict[str, str]],
) -> str:
    body_parts = [
        "Weekly check found repositories with `copilot-instructions.md` content that differs from this repository.",
        "",
        f"Baseline: `{current_repository}/{baseline_path}`",
        "",
        "Review each diff below. To merge one source into this repository, run the command block for that source locally, then open a pull request.",
        "",
    ]

    for change in changes:
        diff = change["diff"]
        truncated = ""
        if len(diff) > MAX_DIFF_CHARS:
            diff = diff[:MAX_DIFF_CHARS]
            truncated = "\n\n_Diff truncated. Open the source file for the full content._"

        body_parts.extend(
            [
                f"## {change['repository']} `{change['path']}`",
                "",
                "Prerequisites: `gh` CLI installed and authenticated, and a clean git working directory.",
                "",
                "Merge command:",
                "",
                "```bash",
                merge_command(change["repository"], change["path"], baseline_path),
                "```",
                "",
                "Diff:",
                "",
                "```diff",
                diff.rstrip(),
                "```",
                truncated,
                "",
            ]
        )

        if sum(len(part) for part in body_parts) > MAX_ISSUE_BODY:
            body_parts.append("_Report truncated because the generated issue body reached the GitHub issue size limit._")
            break

    return "\n".join(body_parts)[:MAX_ISSUE_BODY]


def find_open_issue(repository: str, token: str) -> int | None:
    issues = request_json("GET", f"/repos/{repository}/issues?state=open&per_page=100", token)
    if not isinstance(issues, list):
        raise GitHubApiError("Unexpected GitHub issues response")
    for issue in issues:
        if not isinstance(issue, dict):
            continue
        if issue.get("pull_request"):
            continue
        if issue.get("title") == ISSUE_TITLE and isinstance(issue.get("number"), int):
            return int(issue["number"])
    return None


def upsert_issue(repository: str, token: str, body: str) -> None:
    existing_issue = find_open_issue(repository, token)
    payload = {"title": ISSUE_TITLE, "body": body}
    if existing_issue is None:
        request_json("POST", f"/repos/{repository}/issues", token, body=payload)
        print(f"Created issue: {ISSUE_TITLE}")
        return

    request_json("PATCH", f"/repos/{repository}/issues/{existing_issue}", token, body=payload)
    print(f"Updated issue #{existing_issue}: {ISSUE_TITLE}")


def main() -> int:
    owner = env_required("OWNER")
    current_repository = env_required("CURRENT_REPOSITORY")
    write_token = env_required("GITHUB_TOKEN")
    read_token = os.environ.get("COPILOT_SYNC_TOKEN", "").strip() or write_token
    baseline_path = os.environ.get("BASELINE_PATH", ".github/copilot-instructions.md")
    baseline = pathlib.Path(baseline_path).read_text(encoding="utf-8")

    changes: list[dict[str, str]] = []
    for candidate in search_instruction_files(owner, read_token):
        if candidate["repository"] == current_repository and candidate["path"] == baseline_path:
            continue

        candidate_text = fetch_file_text(candidate["url"], read_token)
        if candidate_text == baseline:
            continue

        changes.append(
            {
                "repository": candidate["repository"],
                "path": candidate["path"],
                "diff": unified_diff(
                    current_repository,
                    baseline_path,
                    f"{candidate['repository']}/{candidate['path']}",
                    baseline,
                    candidate_text,
                ),
            }
        )

    if not changes:
        print("No Copilot instruction changes detected.")
        return 0

    body = build_issue_body(baseline_path, current_repository, changes)
    upsert_issue(current_repository, write_token, body)
    print(f"Reported {len(changes)} changed Copilot instruction file(s).")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except GitHubApiError as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(1)
