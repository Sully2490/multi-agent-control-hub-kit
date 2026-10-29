#!/usr/bin/env bash
set -euo pipefail

echo "=== 1. Creating shared engineering & constitution-bot directories ==="
mkdir -p /workspace/engineering/shared/specs
mkdir -p /workspace/constitution-bot
mkdir -p /home/box/agent-data/workflows

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=== 2. Installing Multi-Agent Research Index & FTS5 Search Tool ==="
cp "$REPO_ROOT/research-index/multi-agent-research-index.md" /workspace/engineering/shared/
cp "$REPO_ROOT/research-index/multi-agent-research-index.json" /workspace/engineering/shared/
cp "$REPO_ROOT/scripts/query_research_index.py" /workspace/engineering/shared/
chmod +x /workspace/engineering/shared/query_research_index.py
python3 /workspace/engineering/shared/query_research_index.py --rebuild

echo "=== 3. Installing Shared ETHOS ==="
cp "$REPO_ROOT/memory/ETHOS.md" /workspace/engineering/shared/ETHOS.md

echo "=== 4. Installing Global Reusable Skills ==="
for skill_dir in "$REPO_ROOT/skills/"*; do
  if [ -d "$skill_dir" ]; then
    slug="$(basename "$skill_dir")"
    mkdir -p "/home/box/agent-data/workflows/$slug"
    cp "$skill_dir/SKILL.md" "/home/box/agent-data/workflows/$slug/SKILL.md"
    echo "  Installed skill: $slug"
  fi
done

echo "=== 5. Installing COVENANT & REPUBLIC Constitution Bot Canon ==="
cp "$REPO_ROOT/bots/covenant-and-republic/"* /workspace/constitution-bot/
python3 /workspace/constitution-bot/build_canon.py

echo "=== 6. Installing Firecrawl CLI globally ==="
if ! command -v firecrawl >/dev/null 2>&1; then
  npm install -g firecrawl-cli
fi
firecrawl --version || true

echo "=== Bootstrap Complete! ==="
