# Friday Multi-Agent Orchestration Research Digest Routine

- **Routine Name:** `Friday multi-agent orchestration research digest`
- **Routine ID:** `friday-multi-agent-orchestration-research-digest`
- **Schedule:** Every Friday at 9:00 AM Local Time (`CRON_TZ=America/New_York 0 9 * * 5`, flexible ±30 min)

## One-Line Prompt to Give Your Primary Bot to Create This Routine

> Create a Friday 9:00 AM routine called "Friday multi-agent orchestration research digest" using the prompt in `routines/FRIDAY_ROUTINE_PROMPT.md`.

## Exact Routine Prompt Saved on the Bot

```text
Run @Multi-Agent Control Hub Playbook. First read /workspace/engineering/shared/multi-agent-research-index.json so you skip any paper, report, or article already covered. Find 3 to 5 worthwhile new papers, technical reports, or engineering articles published recently about multi-agent AI orchestration across Grok, Claude, and ChatGPT (using WebSearch, WebFetch, or the firecrawl CLI). Prioritize coordination frameworks, agent security, tool permissions, approval gates, and automated QA, and skip minor announcements. Verify each primary source link before including it. Append the new entries (with id, date, title, url, key_findings, and applied_rule) to /workspace/engineering/shared/multi-agent-research-index.json and /workspace/engineering/shared/multi-agent-research-index.md, rebuild the SQLite FTS5 index via `python3 /workspace/engineering/shared/query_research_index.py --rebuild`, and update the Multi-Agent Control Hub Playbook skill if a finding introduces a new operational rule worth enforcing across all bots. Send the digest to the user in this chat with each item's verified markdown link, key findings, and practical implications for the agent control hub, plus a one-line note confirming the index and playbook skill were updated; if nothing notable was published this week, send a brief note saying so.
```

## How the Routine Self-Improves the Bot Team Every Week
1. **Deduplication Check:** Reads `/workspace/engineering/shared/multi-agent-research-index.json` first so it never repeats a paper or engineering post already covered.
2. **Primary-Source Research & Scraping (`3–5` items):** Searches and scrapes arXiv (`cs.MA`, `cs.CR`, `cs.AI`, `cs.SE`), OpenAI Engineering, Anthropic Engineering, and xAI Docs using `WebSearch`, `WebFetch`, and `firecrawl` CLI, and verifies every link (`HTTP 200`) before citing it.
3. **Persistent Indexing:** Appends new findings + an explicit `applied_rule` for each paper to `multi-agent-research-index.json` and `multi-agent-research-index.md`, then rebuilds the SQLite FTS5 full-text search database (`multi-agent-research-index.db`).
4. **Live Skill Enforcement:** Updates the global `Multi-Agent Control Hub Playbook` skill (`UpdateSkill`) whenever a paper introduces a new coordination, security, approval-gate, or QA rule, so every bot on the account automatically enforces it on subsequent turns.
