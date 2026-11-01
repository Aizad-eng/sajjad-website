# SurgiSource

Static site for SurgiSource: medical equipment and surgical disposables, imported on order and supplied across Pakistan.

- Build: `python3 tools/build.py` (categories live in the script, guides in `content/guides/*.json`, writing rules in `tools/GUIDE_BRIEF.md`).
- Quote form: Tally form `zEjKDE`, submissions emailed to the owner.
- Deploy: Cloudflare Workers static assets, `npx wrangler deploy` (config in `wrangler.jsonc`). Change `SITE` in `tools/build.py` when a custom domain is attached.
