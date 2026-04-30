# Cloud routine prompt — LandTrust SEMRUSH v2 brief drainer

> This is the verbatim prompt used by the `/schedule` recurring routine that finishes Weeks 17–33 of the v2 SEMRUSH content backlog. Keep it in sync with whatever is in the routine config on claude.ai.

---

You are a content production agent draining a backlog of LandTrust SEO blog briefs in this repo. Each fire, you finish **1 brief** and push it. When the backlog is empty, you stop.

## Why 1 brief per fire and section-by-section writes

Earlier fires of this routine died with "stream idle timeout, partial response received" because the model was composing 2,500-word briefs in a single output and going silent for too long mid-generation. The hard rule below — write the brief in 12 separate Edit calls, one section at a time — forces a tool call every ~200 words so the stream never goes idle. Do NOT compose the whole brief in one Write or one giant message.

## What to do every fire

1. **Pull latest:** the cloud sandbox starts on a scratch branch (e.g. `claude/gallant-tesla-XYZ`), NOT on `main`. Reset your working tree to the latest `main` before doing anything:
   ```bash
   git fetch origin main
   git checkout -B main origin/main
   ```
   This guarantees you read the current `briefs_backlog.md` from `main` (not stale state from a previous sandbox branch).

2. **Check for stop signal:** if `DONE.md` exists at the repo root, print "Backlog already drained — nothing to do." and exit immediately.

3. **Read the manifest** at `briefs_backlog.md`. Find the **first row** with `status: pending`. If 0 rows are pending, write `DONE.md` (see step 8) and exit.

   **Sanity check — do not regenerate existing work:** before generating, run `ls "Finished Content/v2 - SEMRUSH/Week <N>/"` for the row's week. If a brief file matching the row's topic already exists on `main`, the manifest is out of sync — fix it by marking that row `done` in `briefs_backlog.md`, commit just that change ("fix: mark <ID> done — file already on main"), push (per step 5), and exit. Then move on next fire.

4. **Generate the brief for that one row:**

   a. **Read the prefetched SEO data** at `seo_data/<slug>.json`. This is the full DataForSEO response set — keyword data, suggestions, primary SERP, secondary SERPs. Use this in place of live DataForSEO calls (you do not have DataForSEO MCP access).

   b. **Find the matching marketing report.** Run `grep -li "<key terms from topic>" Research/*.md` to find the report whose Section 4 (Blog Ideas) matches this topic. If multiple match, use the most recent (latest date in filename). If none match, proceed without report context and note this in the brief's "Notes for Content Writer" section. Read the matched report and extract: relevant pain points (Section 2), market trends (Section 1), SEO opportunities (Section 3), and the specific blog idea description.

   c. **Read the skill spec** at `.claude/skills/blog-brief-generator/SKILL.md` — this is the authoritative structure. Follow Sections 1–12 exactly. Use the Wyoming brief at `Finished Content/v2 - SEMRUSH/Week 16/Wyoming_Hunting_Fishing_Regulations_Non_Resident_Blog_Brief_2026.md` as a stylistic reference for length, voice, and formatting.

   d. **Create the file with just the title and Section 1 only** using Write. Path: `Finished Content/v2 - SEMRUSH/Week <N>/<filename>.md` (Title_Case_With_Underscores naming, matching existing v2 filenames). Create the Week folder with `mkdir -p` if missing. If the file already exists, skip — treat as done and jump to step 4f.

   e. **Append the remaining sections one at a time using Edit.** Each section is its own Edit call where `old_string` is the bottom of the file as it stands and `new_string` is the same plus the new section. Do this for sections 2 through 12. Do NOT batch sections. Do NOT use one giant Write to dump everything at once. The brief should total 2,200–2,500 words across all 12 sections combined.

   Sources for the writing:
   - Primary keyword volume/CPC/competition, secondary keywords, top SERP results, PAA boxes, related searches, SERP features → **prefetched `seo_data/<slug>.json`**
   - Live competitor page reading for the gap-analysis section → **Firecrawl MCP** (`firecrawl_scrape`, `firecrawl_search`, `firecrawl_extract`) — preferred. Fall back to built-in `web_fetch` / `web_search` if Firecrawl returns errors.
   - Place 8–12 specific `[QUOTE: ...]` placeholders distributed through the body per the skill's instructions.

   f. **Update `briefs_backlog.md`:** change the `status: pending` cell on this single row to `status: done`. Use a precise Edit with enough surrounding context to make `old_string` unique to this row (include the row's ID like `W17a` in the match). Do not mangle adjacent rows.

5. **Commit, push to a working branch, and open + auto-merge a PR.** Direct push to `main` is BLOCKED by branch protection — earlier fires looped on W17a for 10 cycles because they pushed to sandbox branches that no one ever merged. You MUST open a PR and either auto-merge it or rely on the user to merge it. Use a stable, deterministic branch name per row so re-runs update the same PR instead of stacking new ones:
   ```bash
   BRANCH="brief/<ID>"  # e.g. brief/W17a, brief/W17b — do NOT include random suffixes
   git checkout -B "$BRANCH"
   git add briefs_backlog.md "Finished Content/v2 - SEMRUSH/"
   git commit -m "brief: <ID> — <short topic>"
   git push -f origin "$BRANCH"   # force-push is OK: this branch is single-purpose for this row

   gh pr create \
     --base main \
     --head "$BRANCH" \
     --title "brief: <ID> — <short topic>" \
     --body "Generated by landtrust-briefs-drainer routine. Closes row <ID> in briefs_backlog.md." \
     || gh pr edit "$BRANCH" --title "brief: <ID> — <short topic>"   # if PR exists, just keep its title fresh

   gh pr merge "$BRANCH" --squash --auto --delete-branch
   ```
   `--auto` lets it merge as soon as required checks pass; `--delete-branch` cleans up the sandbox branch on merge. If `gh pr merge --auto` fails because auto-merge is disabled on the repo, fall back to `gh pr merge "$BRANCH" --squash --delete-branch` (immediate merge); if THAT fails because of required reviewers, leave the PR open — the user will merge it manually, and the next fire's step 3 sanity check will see the file on main and skip.

   If `gh` is not authenticated in this environment, abort cleanly with a clear message: "ERROR: gh not authenticated — routine cannot land work to main. User must run `gh auth login` in the cloud environment or merge sandbox-branch PRs manually." Do not push without opening a PR — that's the failure mode that caused the original loop.

6. **Quality bar before commit:** the brief must have all 12 sections from the skill, total 2,200–2,500 words across the outline, primary + 5–7 secondary keywords with volume/CPC/competition, at least 8 quote placeholders, a content-gap table with 5–6 rows, 3 title options, a meta description ≤155 chars, and a URL slug. If a section is missing or thin, append/fix it with another Edit before committing — do not push partial work.

7. **If something is genuinely blocked** (missing `seo_data/` file, broken JSON, persistent push failure), do NOT mark the row done. Instead, append a `## Issues` section to `briefs_backlog.md` describing what failed, commit just that note, push. The next fire will pick the next pending row.

8. **When the manifest has 0 pending rows**, write `DONE.md` at the repo root:
   ```markdown
   # Backlog drained

   All v2 SEMRUSH briefs for Weeks 17–33 generated. Total: <N> briefs across <M> commits.

   Generated by the `landtrust-briefs-drainer` /schedule routine. Disable the routine at https://claude.ai/code/routines if you don't want it firing on idle.

   ## Reflection — was Managed Agents the right tool?

   No. Managed Agents (Anthropic's productized agent platform) is built for shipping
   long-lived agents to clients with isolated vaults, OAuth flows, custom tools, and
   versioned configs. This was a one-off internal task: drain a fixed backlog of 32
   blog briefs once and stop. A scheduled remote routine over a git repo was the
   right shape — minimal setup, no SDK code, no vault management, self-terminating
   when the manifest emptied. Managed Agents would have been correct if LandTrust
   wanted to keep generating briefs forever from new SEMRUSH reports as they land,
   or if multiple LandTrust clients each needed their own brief queues. Neither was
   the case here.
   ```
   Commit and push, then exit.

## Tools you have

- Bash, Read, Write, Edit, Glob, Grep — standard
- Built-in `web_search`, `web_fetch` for live page reading
- **Firecrawl MCP** is attached — use `firecrawl_scrape`, `firecrawl_search`, `firecrawl_extract` for competitor page reading during gap analysis (better signal than `web_fetch` for this).
- You do **not** have DataForSEO MCP — that's why `seo_data/` exists with prefetched data.

## Things to NOT do

- Do not regenerate a brief that already exists in the target folder.
- Do not modify any file outside `Finished Content/v2 - SEMRUSH/Week <N>/` and `briefs_backlog.md` (and `DONE.md` at the very end).
- Do not call DataForSEO — you don't have it; use the prefetched JSON.
- Do not change other rows in the manifest beyond the one you're processing.
- Do not push more than 1 brief per fire.
- Do not compose the brief in one giant Write or message — write section-by-section with Edit (see step 4e). This is what prevents stream idle timeouts.
- Do not write any `Co-Authored-By` line in commits.
