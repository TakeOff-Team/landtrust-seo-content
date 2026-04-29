# Cloud Routines Playbook

Lessons + checklists for building Anthropic `/schedule` cloud routines that actually run to completion. Cumulative — append as we learn.

---

## Symptom → cause → fix cookbook

| Symptom in the routine UI | Cause | Fix |
|---|---|---|
| `API error, stream idle timeout, partial response received` | Model went silent for >N minutes mid-fire — usually composing a long output in one shot or thinking too long between tool calls | Force a tool call every ~200 words. For long writes: build the file section-by-section with `Edit`, not one giant `Write`. Reduce work-per-fire if needed. |
| Fire ends, no commit lands | Push permission missing, or agent silently failed mid-write | Check claude.ai → Settings → Connectors → GitHub has *write* scope. Inspect the routine UI fire log for the actual exit message. |
| Connector exists in claude.ai but isn't visible in `/schedule` skill at create time | claude.ai connector-list lag (sometimes minutes, sometimes hours) | Create the routine without it, then `RemoteTrigger update` later with `mcp_connections: [{...}]` once it appears. Don't block the build. |
| Connector requires Basic Auth (e.g. DataForSEO) | claude.ai connectors only support OAuth or URL-embedded keys | Pre-fetch the data locally, dump to JSON in the repo, point the agent at the JSON. |
| `Co-Authored-By` line in agent commits gets sandbox-blocked | Local Claude Code policy in this session forbids it; the prompt told the cloud agent the same | Make sure the prompt explicitly says "do not write Co-Authored-By." |
| `RemoteTrigger update` returns 400 `missing ccr.environment_id` | "Partial update" isn't fully partial — `job_config.ccr` requires `environment_id` every time | Re-pass the full `ccr` block on every update (`environment_id`, `events`, `session_context.outcomes`, `session_context.sources`). |
| `RemoteTrigger update` returns 400 `unknown field "persist_session"` | `persist_session` lives at the `trigger` root, not inside `session_context` | Drop it from `session_context` when copying the response back into an update body. |

---

## Pre-flight checklist for building a new routine

Run through this before clicking go.

**Repo & manifest**
- [ ] Repo private, GitHub OAuth has *write* scope on it
- [ ] Manifest file (work queue) at repo root, one row per unit of work, explicit `status: pending|done` column
- [ ] Stop signal defined (e.g. `DONE.md` at repo root) — agent must check for this first thing every fire

**Prompt structure**
- [ ] First action every fire: `git pull origin main`
- [ ] Second action: check stop signal
- [ ] Hard cap on work per fire (1 unit, not "as much as you can")
- [ ] Quality bar listed explicitly (word count, required sections, etc.)
- [ ] Exit cleanly on errors — append `## Issues` to manifest, never push partial work
- [ ] Commit message format spelled out
- [ ] Explicit "do not" list (don't touch unrelated files, don't regenerate completed work, don't write Co-Authored-By)

**Anti-idle-timeout rules** (the big one)
- [ ] If output >500 words: instruct agent to build via incremental `Edit` calls, not one `Write`
- [ ] If reasoning is long: insert checkpoint Bash calls (`echo "section 4 done"`) to keep the stream alive
- [ ] Cap context loads — agent reading 5 MB before writing anything is a stall risk

**Tools & connectors**
- [ ] `allowed_tools` includes every MCP tool you reference (format: `mcp__<ConnectorName>__<tool>`; case matches the connector's `name` field)
- [ ] Built-in fallbacks named when MCP could fail (e.g. "use Firecrawl, fall back to `web_fetch`")
- [ ] Pre-fetched data committed to repo for any API the routine can't reach (Basic Auth, rate limits, etc.)

**Model choice**
- [ ] Default to Sonnet 4.6 for cost. Only escalate to Opus 4.7 if Sonnet produces thin output or stalls repeatedly.

**Mirror & docs**
- [ ] Verbatim prompt mirrored at `routine_prompt.md` in the repo, kept in sync via `RemoteTrigger update`
- [ ] Build log in `PROGRESS.md` covering decisions, watchpoints, common-fix table

---

## What worked / didn't on the LandTrust briefs drainer

`trig_018namShCPJmKCvKnn3HxAug` — Weeks 17–33 SEMRUSH brief drainer.

| Attempt | Date (UTC) | Change | Outcome |
|---|---|---|---|
| v1 | 2026-04-28 21:03 | Initial: Sonnet 4.6, 2 briefs/fire, monolithic Write per brief, no Firecrawl | ❌ All ~19 fires failed with `stream idle timeout, partial response received`. Zero commits. |
| v2 | 2026-04-29 16:13 | 1 brief/fire, section-by-section `Edit` (12 calls), Firecrawl MCP added | ⏳ Manual fire triggered 16:13 UTC — pending verification. |

When v2 (or whatever finally works) confirms green: update the corresponding row's outcome, add a "✅ Verified" line, and move the working pattern up into the playbook above.

---

## Open questions to resolve once we have a green run

- Does `mcp__Firecrawl__*` (capital F, matching the connector name) resolve, or does the cloud sandbox normalize to lowercase `mcp__firecrawl__*`? The successful fire log will show it.
- Does Sonnet 4.6 + section-by-section actually finish without timeout, or do we still need Opus 4.7?
- How long does a single brief take wall-clock with the new pattern? Determines whether 1 brief/fire is sustainable for a 32-row backlog (≈32 hours) or whether we want to bump cron to every 30 min.
