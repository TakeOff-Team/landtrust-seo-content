# Setup — finishing the v2 SEMRUSH brief drainer

Local repo is ready (commit `935c142`, 129 files, 9.2 MB). Three manual steps remain to start the cloud routine. Each takes <5 minutes.

## Step 1 — push to private GitHub repo `landtrust-content`

Two paths; pick whichever is easier.

**Path A: gh CLI (if you can run interactive shell)**

In a real Terminal.app window (not the `!` prefix in Claude Code — that runs without a TTY and the device-code flow times out):
```bash
cd "~/Downloads/TakeOff - LandTrust"
gh auth login                     # GitHub.com → HTTPS → Yes → Browser
gh repo create landtrust-content --private --source=. --remote=origin --push
```

**Path B: manual via web UI (no gh required)**

1. Open https://github.com/new
2. Repo name: `landtrust-content`. Visibility: **Private**. Do NOT initialize with README/license/.gitignore (we already have history).
3. Click "Create repository". Copy the HTTPS clone URL.
4. Back in this Claude Code session, tell me the URL and I'll run:
   ```bash
   git remote add origin <url>
   git push -u origin main
   ```
   macOS keychain will prompt for GitHub credentials (use a Personal Access Token if your account has 2FA — passwords don't work for git push anymore).

## Step 2 — add Firecrawl as a claude.ai connector

The cloud routine needs Firecrawl for live SERP page scraping during gap analysis. claude.ai web connectors only support OAuth or URL-embedded keys; Firecrawl uses the latter.

1. Go to https://claude.ai/customize/connectors → Add custom connector
2. Name: `Firecrawl`
3. URL: `https://mcp.firecrawl.dev/<YOUR_FIRECRAWL_API_KEY>/v2/mcp`
   (paste your real API key in place of `<YOUR_FIRECRAWL_API_KEY>` — get one at https://firecrawl.dev/app/api-keys if you don't have it handy; the local CLI MCP key is reusable)
4. Leave OAuth fields blank
5. Save — should connect in a second or two

(Skip DataForSEO. claude.ai doesn't support Basic Auth for connectors and DataForSEO requires it. The 32 prefetched JSONs in `seo_data/` are a static replacement.)

## Step 3 — create the recurring routine

Once Steps 1 & 2 are done, tell me "ready" and I'll fire one `RemoteTrigger.create` call with this config:

- **Name:** `landtrust-briefs-drainer`
- **Cron:** `0 * * * *` (every hour, top of the hour, UTC) — minimum interval claude.ai allows
- **Environment:** `env_01Q28jtqXq8ddQddJjZUh6aV` (Anthropic Cloud default)
- **Model:** `claude-sonnet-4-6`
- **Source:** the `landtrust-content` repo from Step 1
- **MCP connections:** Firecrawl from Step 2
- **Allowed tools:** `Bash`, `Read`, `Write`, `Edit`, `Glob`, `Grep`, plus built-in `web_search` and `web_fetch`
- **Prompt:** verbatim contents of `routine_prompt.md` in this repo

Each fire processes 2 briefs and pushes to `main`. ~17 hours wall-clock to drain the full 32-brief backlog (you can sleep, work, travel — it just keeps firing). When the manifest is empty it writes `DONE.md` and stops doing real work; you can then disable the routine in https://claude.ai/code/routines.

**Cost ballpark:** ~17 fires × 5–10 min active each ≈ 1.5–3 hours of session runtime at $0.08/hr = ~$0.15–0.25. Plus tokens (~$10–20 at Sonnet rates across 32 briefs). Plus a handful of Firecrawl scrapes per brief. Under $30 total.

---

## What I already did

- ✅ Built `briefs_backlog.md` — manifest of 32 pending briefs (Weeks 17–33)
- ✅ Prefetched DataForSEO data for all 32 → `seo_data/<slug>.json` (volumes, CPC, monthly trends, keyword suggestions, top 20 organic SERP, PAA boxes, related searches, secondary SERPs)
- ✅ Drafted `routine_prompt.md` — the verbatim cloud-agent prompt
- ✅ Wrote `.gitignore` excluding `.claude/settings.local.json`, `.claude/plans/`, `.DS_Store`
- ✅ Initial git commit (`935c142`, 129 files, 9.2 MB)
