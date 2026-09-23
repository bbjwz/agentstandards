from __future__ import annotations

import argparse
import json
import re
import tomllib
from pathlib import Path

VERSION_PATTERN = re.compile(r'^\s+version:\s*["\']([^"\']+)["\']\s*$', re.MULTILINE)


def project_version(root: Path) -> str:
    with (root / "pyproject.toml").open("rb") as handle:
        return str(tomllib.load(handle)["project"]["version"])


def declared_versions(root: Path) -> dict[str, str]:
    versions: dict[str, str] = {}
    yaml_paths = [
        root / "extension.yml",
        root / "presets" / "agentstandards-gate" / "preset.yml",
        root / "workflows" / "agentstandards-architecture" / "workflow.yml",
        root / "bundles" / "agentstandards" / "bundle.yml",
    ]
    for path in yaml_paths:
        match = VERSION_PATTERN.search(path.read_text(encoding="utf-8"))
        if not match:
            raise ValueError(f"missing version in {path.relative_to(root)}")
        versions[path.relative_to(root).as_posix()] = match.group(1)

    init_text = (root / "runtime" / "agentstandards" / "__init__.py").read_text(
        encoding="utf-8"
    )
    match = re.search(r'^__version__\s*=\s*["\']([^"\']+)["\']', init_text, re.MULTILINE)
    if not match:
        raise ValueError("missing __version__ in runtime/agentstandards/__init__.py")
    versions["runtime/agentstandards/__init__.py"] = match.group(1)

    for path in sorted((root / "catalogs").glob("*.json")):
        catalog = json.loads(path.read_text(encoding="utf-8"))
        entries = catalog.get("entries") or catalog.get("extensions") or catalog.get("presets")
        entries = entries or catalog.get("workflows") or catalog.get("bundles")
        if not entries:
            raise ValueError(f"missing catalog entries in {path.relative_to(root)}")
        entry = next(iter(entries.values())) if isinstance(entries, dict) else entries[0]
        versions[path.relative_to(root).as_posix()] = str(entry["version"])
    return versions


def validate(root: Path) -> str:
    expected = project_version(root)
    mismatches = {
        path: value for path, value in declared_versions(root).items() if value != expected
    }
    if mismatches:
        details = ", ".join(f"{path}={value}" for path, value in mismatches.items())
        raise ValueError(f"release version {expected} does not match {details}")
    return expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--print-version", action="store_true")
    args = parser.parse_args()
    version = validate(args.root.resolve())
    if args.print_version:
        print(version)
    else:
        print(f"Release metadata is consistent at version {version}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
