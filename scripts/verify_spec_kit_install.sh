#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
test_root="$(mktemp -d /tmp/agentstandards-speckit.XXXXXX)"
trap 'rm -rf -- "$test_root"' EXIT

python3 "$repo_root/scripts/build_release.py" --output "$test_root/release"
mkdir -p "$test_root/extension" "$test_root/preset"
unzip -q "$test_root/release/agentstandards-0.1.0.zip" -d "$test_root/extension"
unzip -q "$test_root/release/agentstandards-gate-0.1.0.zip" -d "$test_root/preset"

uvx --from specify-cli==1.0.8 specify init "$test_root/project" \
  --non-interactive \
  --integration codex \
  --script py \
  --ignore-agent-tools \
  --extension "$test_root/extension"

cd "$test_root/project"
uvx --from specify-cli==1.0.8 specify preset add --dev "$test_root/preset"
uvx --from specify-cli==1.0.8 specify workflow add \
  "$repo_root/workflows/agentstandards-architecture" --dev

test -f .agents/skills/speckit-agentstandards-init/SKILL.md
test -f .agents/skills/speckit-agentstandards-architect/SKILL.md
test -f .agents/skills/speckit-agentstandards-resume/SKILL.md
test -f .agents/skills/speckit-agentstandards-status/SKILL.md
test -f .agents/skills/speckit-agentstandards-gate/SKILL.md
python3 .specify/extensions/agentstandards/scripts/python/agentstandards.py --help >/dev/null

uvx --from specify-cli==1.0.8 specify bundle validate \
  --path "$repo_root/bundles/agentstandards" --offline
