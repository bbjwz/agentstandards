#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
test_root="$(mktemp -d /tmp/agentstandards-speckit.XXXXXX)"
trap 'rm -rf -- "$test_root"' EXIT
version="$(python3 -c 'import sys, tomllib; print(tomllib.load(open(sys.argv[1], "rb"))["project"]["version"])' "$repo_root/pyproject.toml")"
spec_kit_version="${SPEC_KIT_VERSION:-1.0.8}"

python3 "$repo_root/scripts/build_release.py" --output "$test_root/release"
mkdir -p "$test_root/extension" "$test_root/preset"
unzip -q "$test_root/release/agentstandards-${version}.zip" -d "$test_root/extension"
unzip -q "$test_root/release/agentstandards-gate-${version}.zip" -d "$test_root/preset"

uvx --from "specify-cli==${spec_kit_version}" specify init "$test_root/project" \
  --non-interactive \
  --integration codex \
  --script py \
  --ignore-agent-tools \
  --extension "$test_root/extension"

cd "$test_root/project"
uvx --from "specify-cli==${spec_kit_version}" specify preset add --dev "$test_root/preset"
uvx --from "specify-cli==${spec_kit_version}" specify workflow add \
  "$repo_root/workflows/agentstandards-architecture" --dev

test -f .agents/skills/speckit-agentstandards-init/SKILL.md
test -f .agents/skills/speckit-agentstandards-architect/SKILL.md
test -f .agents/skills/speckit-agentstandards-resume/SKILL.md
test -f .agents/skills/speckit-agentstandards-status/SKILL.md
test -f .agents/skills/speckit-agentstandards-gate/SKILL.md
python3 .specify/extensions/agentstandards/scripts/python/agentstandards.py --help >/dev/null

uvx --from "specify-cli==${spec_kit_version}" specify bundle validate \
  --path "$repo_root/bundles/agentstandards" --offline
