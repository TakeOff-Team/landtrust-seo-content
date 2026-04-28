# Build log — v2 SEMRUSH brief drainer

**Built:** 2026-04-28 evening (Madrid)
**Status:** Routine live and scheduled. First fire at 2026-04-28 22:00 UTC / 00:00 Apr 29 Madrid. Drains 32 briefs over ~17 hourly fires.

## What this is

A `/schedule` recurring routine that finishes the v2 SEMRUSH content backlog (Weeks 17–33, 32 briefs total) unattended in the cloud. It clones this repo, picks 2 pending briefs from `briefs_backlog.md` per fire, composes them, commits, pushes, and self-terminates when the manifest is empty.

- **GitHub:** https://github.com/TakeOff-Team/landtrust-seo-content (private)
- **Routine ID:** `trig_018namShCPJmKCvKnn3HxAug`
- **Routine UI:** https://claude.ai/code/routines/trig_018namShCPJmKCvKnn3HxAug
- **Cron:** `0 * * * *` (hourly, top of hour, UTC)
- **Model:** `claude-sonnet-4-6`
- **Verbatim prompt:** `routine_prompt.md` in this repo

## Five decisions worth remembering

1. **Used `/schedule` routine, not Managed Agents.** Managed Agents (the productized Anthropic platform from the April 2026 PDF in repo root) is for shipping long-lived agents to clients with vaults, OAuth flows, custom tools, versioned configs — days of setup. This was a one-off internal task: drain a fixed backlog once and stop. Schedule routine + git repo got the same outcome (cloud execution, runs while laptop is off) in 30 minutes of setup. The cloud routine is set to write a final reflection on this in `DONE.md` when it finishes.

2. **Prefetched DataForSEO data locally instead of attaching as a connector.** claude.ai web custom connectors only support OAuth (or URL-embedded keys like Firecrawl); they don't support custom Authorization headers. DataForSEO requires Basic Auth → can't be a claude.ai connector. Workaround: ran ~160 DataForSEO API calls locally before commit, dumped to `seo_data/<slug>.json` (32 files, ~4 MB total), cloud agent reads from JSON instead of live API. Brief quality is preserved because the data is the same — just snapshot at prefetch time.

3. **Skipped Firecrawl on the routine.** User added it as a connector but it didn't show up in the schedule skill's connector list at routine-creation time (claude.ai backend lag, possibly). Rather than block, we shipped without it. Cloud agent falls back to built-in `web_fetch` and `web_search` for live competitor page reading. If a brief comes out thin, attach Firecrawl via routine update.

4. **Sonnet 4.6 not Opus.** Schedule skill default. ~3–4× cheaper across 17 fires. If brief quality is short of the Wyoming reference (Week 16), switch the routine's `model` field to `claude-opus-4-7` via `RemoteTrigger` update.

5. **2 briefs per fire, not 4 or 6.** Keeps each fire bounded (~5–10 min active per fire), keeps context fresh, makes failures resumable. Trade-off: ~17 hours wall-clock to drain. User accepted that vs. faster-but-fragile larger batches.

## Issues hit during build (and how they were resolved)

- **DataForSEO connector add failed** with `ofid_075c7fddedf80961`. Predicted — claude.ai sends no auth header during the connector probe; DataForSEO Basic-Auth-only endpoint rejects. **Fix:** skipped DataForSEO entirely, prefetched locally instead.
- **`gh auth login` via `! gh auth login` timed out.** Background-run commands have no TTY → device-code flow can't proceed. **Fix:** user manually created the GitHub repo at github.com/new; we pushed via existing macOS keychain credentials.
- **Agent batch 1 (DataForSEO prefetch) saved data as `persisted_file` pointers** to ephemeral `/tmp/` files that got cleaned up before commit. 7 of 8 JSONs were skeleton-only. **Fix:** spawned a re-run agent with explicit "filter responses to these specific fields, save inline, do NOT use persisted file storage" instructions. Worked.
- **Agent batches 2 and re-run agent #1 stalled** ("no progress for 600s"). Suspect cause: agents tried to Read existing broken files before re-fetching, hung. **Fix:** spawned narrower agents with "do NOT read existing files, just call the API and write fresh" prompts.
- **Co-Authored-By line in second commit was sandbox-blocked** because `routine_prompt.md` (which I wrote) says cloud-routine commits should not include Co-Authored-By. The policy enforcer can't tell that's instructions for a different agent. **Fix:** re-committed without the line. (Initial commit had it — that one was allowed.)

## Operational state right now

- Repo: 3 commits, 130 files, 9.2 MB. Branch `main`, tracking `origin/main`.
- Manifest: `briefs_backlog.md` — all 32 rows `status: pending`.
- Prefetched SEO: `seo_data/` — 32 JSON files, all inline-clean (no persisted_file refs).
- Routine: enabled, next run scheduled.

## Watchpoints during the first 1–2 fires

- **Push permissions:** the cloud routine needs write access to the private repo. claude.ai's GitHub integration usually handles this via the user's account-level GitHub OAuth, but if fire #1 produces a brief and fails the push step, the symptom will be a row staying `status: pending` despite the file existing in the routine logs. Fix path: connect GitHub at https://claude.ai/customize/connectors with write scope, or attach a PAT-based credential.
- **Brief quality:** spot-check first 2 briefs against `Finished Content/v2 - SEMRUSH/Week 16/Wyoming_Hunting_Fishing_Regulations_Non_Resident_Blog_Brief_2026.md`. If they feel thinner, options below.
- **Routine doesn't see CLAUDE.md or auto-memory.** Each cloud fire starts with zero conversational context — only the routine prompt + the cloned repo. Anything the human-mode Claude Code knows from `MEMORY.md` or chat history isn't there. Currently the only relevant saved feedback is "briefs not articles," which is already baked into the prompt.

## How to fix common things without rebuilding

| Symptom | Fix |
|---|---|
| Briefs are thin / off-voice | `RemoteTrigger update` the routine, change `job_config.ccr.session_context.model` to `claude-opus-4-7`. Or sharpen `routine_prompt.md` and update the routine's `events[0].data.message.content`. |
| Routine push fails | Connect GitHub with write scope at https://claude.ai/customize/connectors, then `RemoteTrigger run` to re-fire. |
| Want faster drain | `RemoteTrigger update` to bump briefs-per-fire from 2 to 4 in the prompt. (Don't drop cron — minimum is 1 hour.) |
| Want Firecrawl after all | Verify it's listed by re-invoking `/schedule`. Then `RemoteTrigger update` with `mcp_connections: [{connector_uuid, name: "Firecrawl", url: "..."}]`. |
| One brief comes out broken | Manually edit the brief locally, set its row in `briefs_backlog.md` back to `status: pending`. Routine will redo it next fire. |
| Want to stop the routine | Toggle off at https://claude.ai/code/routines, or `RemoteTrigger update` with `enabled: false`. |
| Backlog drained but routine still firing | The routine is designed to no-op when `DONE.md` exists (~30 sec, pennies). Disable manually when convenient. |

## File map

- `briefs_backlog.md` — manifest (work queue)
- `seo_data/<slug>.json` — prefetched DataForSEO data, one per topic
- `routine_prompt.md` — verbatim cloud agent prompt (keep in sync if you update the routine)
- `SETUP.md` — original setup doc, three manual steps (now done)
- `Research/*.md` — marketing reports (cloud agent greps these for blog idea context)
- `.claude/skills/blog-brief-generator/SKILL.md` — authoritative brief structure (cloud agent reads this)
- `Finished Content/v2 - SEMRUSH/Week 1-16/` — existing briefs (cloud agent uses Week 16 as style reference)
- `Finished Content/v2 - SEMRUSH/Week 17-33/` — created on first fire that needs each one
