# Build log — v2 SEMRUSH brief drainer

**Built:** 2026-04-28 evening (Madrid)
**Status (2026-04-30 11:50 Madrid):** Routine v3 live after recovering from the W17a loop incident (see issues log). 1/32 briefs landed on main (W17a). Next hourly fire is the first proof-test of the PR-based landing pattern. Watchpoint: whether `gh` CLI is available in the cloud sandbox.

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

5. **1 brief per fire, not 2 or 4.** v1 said 2/fire; v2 dropped to 1/fire after a stream-idle-timeout in mid-generation. v3 keeps it at 1/fire. Trade-off: ~32 hours wall-clock to drain. Each fire stays bounded (~5–10 min active), context stays fresh, failures are resumable.

6. **PR-based landing with auto-merge enabled (v3, 2026-04-30).** `main` is branch-protected, so the routine cannot push directly. Each fire opens `brief/<ID>` → PR → `gh pr merge --squash --auto --delete-branch`. Auto-merge had to be turned on at the repo level (Settings → "Allow auto-merge") because otherwise every fire would dump a PR in the queue waiting for a human click — exact opposite of "unattended drain." See the W17a loop incident in the issues log for what happens when work doesn't land on main.

## Issues hit during build (and how they were resolved)

- **DataForSEO connector add failed** with `ofid_075c7fddedf80961`. Predicted — claude.ai sends no auth header during the connector probe; DataForSEO Basic-Auth-only endpoint rejects. **Fix:** skipped DataForSEO entirely, prefetched locally instead.
- **`gh auth login` via `! gh auth login` timed out.** Background-run commands have no TTY → device-code flow can't proceed. **Fix:** user manually created the GitHub repo at github.com/new; we pushed via existing macOS keychain credentials.
- **Agent batch 1 (DataForSEO prefetch) saved data as `persisted_file` pointers** to ephemeral `/tmp/` files that got cleaned up before commit. 7 of 8 JSONs were skeleton-only. **Fix:** spawned a re-run agent with explicit "filter responses to these specific fields, save inline, do NOT use persisted file storage" instructions. Worked.
- **Agent batches 2 and re-run agent #1 stalled** ("no progress for 600s"). Suspect cause: agents tried to Read existing broken files before re-fetching, hung. **Fix:** spawned narrower agents with "do NOT read existing files, just call the API and write fresh" prompts.
- **Co-Authored-By line in second commit was sandbox-blocked** because `routine_prompt.md` (which I wrote) says cloud-routine commits should not include Co-Authored-By. The policy enforcer can't tell that's instructions for a different agent. **Fix:** re-committed without the line. (Initial commit had it — that one was allowed.)
- **2026-04-30: 10-fire W17a loop — main is branch-protected.** The routine fired 10 times across Apr 29–30 and produced 10 complete W17a briefs, all stranded on `claude/gallant-tesla-*` sandbox branches. Root cause: branch protection on `main` rejects direct pushes ("Pushing directly to the repository's default branch bypasses PR review"); the predicted fallback in v2 was `git push origin main`, which was silently blocked. The cloud sandbox always starts on a fresh scratch branch, so each fire pulled `main` (which still showed W17a `pending`), regenerated the brief, pushed to sandbox, and exited — never updating `main`. **Fix (routine v3, commit 119a4b4):** routine now creates a deterministic `brief/<ID>` branch, force-pushes there, and uses `gh pr create` + `gh pr merge --squash --auto --delete-branch`. Step 3 also gained a sanity check — if the brief file already exists on `main`, the routine just marks the row `done` and exits, defending against PR-merge lag. Recovery: cherry-picked the most recent W17a brief (commit 42275ba) onto `main`, opened PR via `brief/W17a` branch.

## Operational state right now (2026-04-30 11:50 Madrid)

- Repo: main is at `d87306e` (PR #1 merged — recovers W17a + ships routine v3).
- Manifest: `briefs_backlog.md` — 1/32 rows `done` (W17a), 31/32 rows `pending`.
- GitHub: `main` is branch-protected (cause of the W17a loop). `Allow auto-merge` is now enabled at repo level so the routine's PRs land themselves.
- Stranded sandbox branches from the loop: 10 `claude/gallant-tesla-*` branches still on origin (kept until v3 is proven; cleanup commands in the chat thread or Issues log).
- Prefetched SEO: `seo_data/` — 32 JSON files, all inline-clean (no persisted_file refs).
- Routine: enabled, next run scheduled. v3 prompt deployed.

## Watchpoints — proving routine v3 actually works

The next hourly fire is the first proof-test of the PR-based pattern. The thing we don't know yet is whether `gh` CLI is available + authenticated in the cloud sandbox env.

- **Success signal:** new PR opens for W17b → auto-merges → main shows W17b `done` within a few minutes of the fire. Repeat for W18a, W18b, etc. on subsequent fires.
- **Failure signal — gh not authed:** routine aborts with "ERROR: gh not authenticated — routine cannot land work to main." This is the v3 prompt's clean-fail path. Fix: rewrite the routine to use the GitHub REST API via `curl` with a PAT (the GitHub Integration connector should expose one to the sandbox env), or have it push to `brief/<ID>` and rely on a human merge.
- **Failure signal — auto-merge falls through:** PR opens, `gh pr merge --squash --auto` errors, fallback `gh pr merge --squash` runs immediate merge. Fine if there are no required checks. If both fail, the PR sits open and you merge by hand. The next fire's step-3 sanity check (file already on main → mark `done` and exit) will then unblock the loop without redoing the brief.
- **Failure signal — looping again:** any row's brief gets generated more than once. If you see a second commit for the same `<ID>` on main or in PRs, something is wrong with the sanity check or the auto-merge path. Stop the routine immediately and ping for a debug.
- **Brief quality:** spot-check W17b against the Wyoming reference (Week 16) once it lands. Switch to Opus via `RemoteTrigger update` if it feels thin.
- **Routine doesn't see CLAUDE.md or auto-memory.** Each cloud fire starts with zero conversational context — only the routine prompt + the cloned repo. Anything the human-mode Claude Code knows from `MEMORY.md` or chat history isn't there.

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
| Fire aborts with "ERROR: gh not authenticated" | Cloud sandbox doesn't have `gh` CLI auth. Rewrite the PR step in `routine_prompt.md` to use GitHub REST API via `curl` (POST to `/repos/{owner}/{repo}/pulls` to create, PUT to `/repos/{owner}/{repo}/pulls/{n}/merge` to merge). Token comes from `GH_TOKEN` / GitHub Integration connector if exposed; otherwise add a PAT secret to the routine config. |
| Routine generates the same `<ID>` more than once | Check `briefs_backlog.md` on main — the row should be `done` after merge. If it's still `pending`, the merge step silently failed. Manually mark `done`, push (via PR), then trigger the routine. The step-3 sanity check (file already on main → mark `done` and exit) is the safety net. |
| 10 stranded `claude/gallant-tesla-*` branches from the W17a loop | Once v3 is proven on a few fires, delete with `git push origin --delete <branch1> <branch2> ...`. Branch list is in the chat history of 2026-04-30. |

## File map

- `briefs_backlog.md` — manifest (work queue)
- `seo_data/<slug>.json` — prefetched DataForSEO data, one per topic
- `routine_prompt.md` — verbatim cloud agent prompt (keep in sync if you update the routine)
- `SETUP.md` — original setup doc, three manual steps (now done)
- `Research/*.md` — marketing reports (cloud agent greps these for blog idea context)
- `.claude/skills/blog-brief-generator/SKILL.md` — authoritative brief structure (cloud agent reads this)
- `Finished Content/v2 - SEMRUSH/Week 1-16/` — existing briefs (cloud agent uses Week 16 as style reference)
- `Finished Content/v2 - SEMRUSH/Week 17-33/` — created on first fire that needs each one
