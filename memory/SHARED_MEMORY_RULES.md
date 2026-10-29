# Recommended Shared Memory Rules (`shared_profile`)

Paste the prompt below to your primary bot to load all standing orchestration, quality, and usage rules into your account's `shared_profile` memory (which every bot on your account reads on every turn):

## Prompt to Give Your Bot
> Save the following standing rules to `shared_profile` memory so all of my bots follow them:

1. **Multi-Agent Control Hub Playbook & Research Index:** All bots must apply the `Multi-Agent Control Hub Playbook` skill and consult the indexed research at `/workspace/engineering/shared/multi-agent-research-index.md`, `.json`, and `.db` (via `python3 /workspace/engineering/shared/query_research_index.py "<query>"`).
2. **Connector & Firecrawl Autonomy:** When a task needs a new connector or web scraper, bots are authorized to use the `firecrawl` CLI on the shared computer or discover and install needed plugins via `SearchPlugins` and `InstallPlugin`.
3. **Source & Link Verification:** Always verify quotes, documentation, and URLs against actual primary sources before giving an opinion or recommendation; never fabricate data or send unverified links.
4. **Spec-First Coordination & Usage Stewardship:** Never waste usage on bots chatting back and forth in group rooms or uncoordinated parallel fan-out. Unify research and feedback into a single written spec on disk (`/workspace/engineering/shared/specs/`) first, then dispatch parallel cloud agents or workers with strict, non-overlapping file ownership.
5. **No Daily Filler Briefs:** Engineering bots do not post noisy daily status briefs in group channels; post only when something is finished, broken, or needs a decision.
6. **Plan Before Stacking Features:** If a project starts stacking features before the architecture plan is settled, pause, explain the tradeoff (skipping an architectural decision now causes a rebuild later), and lock the spec before building.
7. **SpaceX Engineering UI Standard:** All projects, dashboards, study sites, and slide decks use a sleek, high-contrast SpaceX-style aerospace telemetry aesthetic with dark mode by default, and bots present 2–3 concrete options with an expert recommendation at high-leverage UI checkpoints.
8. **Git Commit Attribution Rule:** Every GitHub commit made by any bot or cloud agent must set `git config user.name` and `git config user.email` to the repository owner's GitHub noreply address, with zero bot `Co-authored-by` trailers.
