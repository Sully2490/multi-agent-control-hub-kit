# Multi-Agent Control Hub Kit

A complete, battle-tested starter kit to configure a multi-agent AI control hub (Grok Bot / Cursor Agents) with:
1. **Automated Friday Multi-Agent Orchestration Research Routine (`3–5` primary-source papers/week)** that deduplicates against a local JSON/Markdown/SQLite FTS5 index and self-updates your bots' operating rules.
2. **The `Multi-Agent Control Hub Playbook` Skill** enforcing empirical findings from recent multi-agent research (`arXiv:2610.31709`, `arXiv:2610.34467`, `arXiv:2610.21063`, `arXiv:2610.28425`, `arXiv:2610.34777`, `arXiv:2610.36108`, `arXiv:2610.31974`, `arXiv:2610.23449`, `arXiv:2610.35950`, `arXiv:2610.32060`, `arXiv:2610.32155`).
3. **Reusable Global Skills (`skills/`)** including `spacex-ui-veneer-and-tactful-checkpoints`, `read-a-gemini-notebook-source`, and the Product Idea Stress Test (`pist-*`) suite.
4. **Shared Memory & Team Ethos (`memory/`)** for token stewardship, primary-source verification, spec-first parallel cloud agent orchestration, and zero-trust mechanical QA.
5. **Bot Blueprints (`bots/`)** including the **Engineering Team Roster** (`Keel`, `Forge`, `Atlas`, `Scout`, `Helm`, `Orchard`, `Aegis`, `Warden`) and the **COVENANT & REPUBLIC** Constitutional Originalist scholar bot with its 44-item verified Founding Canon and SQLite FTS5 search index.

---

## Quick Start (One-Prompt Setup for Your Bot)

Paste this single message into your primary bot chat:

```text
Set up my computer and bots from https://github.com/Sully2490/multi-agent-control-hub-kit :
1. Run scripts/bootstrap_box.sh on your computer so the research index, SQLite FTS5 search, Firecrawl CLI, ETHOS, Constitution Bot canon, and skills are installed.
2. Save the skills in skills/ (especially Multi-Agent Control Hub Playbook and SpaceX UI Veneer and Tactful Checkpoints) via UpdateSkill.
3. Add the standing rules in memory/SHARED_MEMORY_RULES.md to shared_profile via UpdateMemory.
4. Create the Friday 9:00 AM routine in routines/friday-multi-agent-orchestration-research-digest.json via UpdateRoutine.
```

---

## Repository Structure

```text
multi-agent-control-hub-kit/
├── README.md
├── routines/
│   ├── FRIDAY_ROUTINE_PROMPT.md                          # Exact prompt & schedule for the Friday 3-5 paper digest
│   └── friday-multi-agent-orchestration-research-digest.json
├── skills/
│   ├── multi-agent-control-hub-playbook/SKILL.md         # Enforces the 6 core orchestration, security & QA rules
│   ├── spacex-ui-veneer-and-tactful-checkpoints/SKILL.md # High-contrast SpaceX telemetry UI + decision checkpoints
│   ├── read-a-gemini-notebook-source/SKILL.md            # Reads sources from Google NotebookLM
│   ├── pist-evidence-investigator/SKILL.md               # Product Idea Stress Test — graded evidence packets
│   ├── pist-experiment-designer/SKILL.md                 # Product Idea Stress Test — bottleneck experiment design
│   ├── pist-method-codifier/SKILL.md                     # Product Idea Stress Test — methodology lens codifier
│   ├── family-calendar-briefs/SKILL.md                   # 14-day family calendar collision & prep scanner
│   ├── kitchen-table-newspaper/SKILL.md                  # Printable one-page morning household newspaper
│   └── monthly-parent-note/SKILL.md                      # Monthly local events & age-adjusted parenting brief
├── research-index/
│   ├── multi-agent-research-index.md                     # Human-readable research index & standing rules
│   └── multi-agent-research-index.json                   # Machine-readable deduplication log (6 indexed clusters)
├── memory/
│   ├── ETHOS.md                                          # Shared Christian & engineering team ethos
│   └── SHARED_MEMORY_RULES.md                            # Standing `shared_profile` memory rules for all bots
├── scripts/
│   ├── bootstrap_box.sh                                  # One-command installer for the shared Linux box
│   └── query_research_index.py                           # SQLite FTS5 indexer & CLI search over research digests
└── bots/
    ├── engineering-roster/
    │   └── ENGINEERING_BOT_ROSTER_PROMPTS.md             # Role prompts for Keel, Forge, Atlas, Scout, Helm, Orchard, Aegis, Warden
    └── covenant-and-republic/
        ├── COVENANT_AND_REPUBLIC_PROMPT.md               # Full Conservative Originalist & Biblical Philosophy bot prompt
        ├── founding-canon.md                             # 44-entry verified Founding Canon with primary URLs
        ├── founding-canon.json                           # Structured JSON manifest of the Founding Canon
        ├── build_canon.py                                # URL verifier + SQLite FTS5 builder for the Founding Canon
        └── query_canon.py                                # Fast CLI FTS5 search over the Founding Canon
```

---

## The 6 Standing Multi-Agent Orchestration Rules Enforced by This Kit

1. **Shared-State Spec First, Never Uncoordinated Fan-Out (`arXiv:2610.31709`, `arXiv:2610.34467`):** Across 28,568 evaluated workflows, raw parallel `Star-first` fan-out hurts accuracy ($\Delta = -0.045$), while writing to persistent `SharedMemory` first beats free-form bot chat `Debate` ($\Delta = +0.143$) and cuts token burn. Coordinators always write a unified spec to disk first and assign strict, non-overlapping file slices to workers.
2. **Canonical Payload Approval Binding (`arXiv:2610.21063`, Anthropic Auto Mode, OpenAI Agents SDK):** Strip subagent persuasive narration when evaluating risky tool calls; bind approvals strictly to the raw `[tool, target, arguments]` tuple and the user's explicit instruction.
3. **Persistent Memory, Skill & Worklist Hygiene (`arXiv:2610.28425`, `arXiv:2610.34777`):** Planted payloads in durable memory or routine prompts trigger with $\Pr(\text{trig}\mid\text{plant}) \approx 1.0$ across future wakes, and hiding malicious targets inside external worklists bypasses single-file `SKILL.md` audits (`78%` vs. `23%` acceptance). Treat memory, skills, and routine prompts as privileged sinks and audit helper files alongside prompts.
4. **Least-Privilege MCP Discovery & Post-Read Sink Blocking (`arXiv:2610.36108`, `arXiv:2610.31974`, `arXiv:2610.23449`):** Defend against `Log-To-Leak` post-task MCP exfiltration (`62.64%–100%` ASR) by using hierarchical tool discovery (`GetDynamicTools`) and blocking any external write/send/logging MCP sink after reading untrusted content unless pre-authorized by the user.
5. **Cross-Skill Capability-Flow Hygiene (`arXiv:2610.32155` — KnotScryer):** `13.7%` of exploitable multi-skill chains consist entirely of skills rated clean by single-skill scanners. Never pipe raw output from an upstream scraping/search skill (`firecrawl`, `WebFetch`) directly into a downstream skill or tool that runs shell commands, edits configs, or sends external messages without structured validation.
6. **Mechanical Zero-Trust QA (`arXiv:2610.35950`, `arXiv:2610.32060`):** "PASS is a claim, not an observation" (`50%` of self-asserted coordinator `PASS` claims in live multi-agent audits failed AST/call-site checks). Every coordinator and QA lead must run deterministic mechanical verification (`git diff` / `git apply --check`, build/test exit codes, CSV row/sum scripts, and live HTTP checks) before reporting `done`.

---

## Querying the Indexes Locally

```bash
# Rebuild and query the Multi-Agent Orchestration Research FTS5 index
python3 /workspace/engineering/shared/query_research_index.py --rebuild
python3 /workspace/engineering/shared/query_research_index.py "SharedMemory OR KnotScryer"

# Query the COVENANT & REPUBLIC Founding Canon FTS5 index
python3 /workspace/constitution-bot/query_canon.py "Deuteronomy OR Rutherford OR Tucker"
```
