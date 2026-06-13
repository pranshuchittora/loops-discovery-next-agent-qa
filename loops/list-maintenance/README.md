# list-maintenance loop

**This is the loop that maintains awesome-agent-loops.** It runs weekly, discovers
new loop-engineering resources from compliant sources, drafts them as awesome
entries, verifies them, and opens a PR. A human approves every merge.

It's also the reference example of the pattern this whole list is about:
`discover → act → verify → human approve → persist`.

## Why it's not fully automated (on purpose)

An awesome list's value is curation. A bot that auto-merges scraped links destroys
the trust that makes the list worth anything — and "verify" is the core idea of
loop engineering, so the maintenance loop can't skip it either. So: discovery and
drafting are automated; **taste and the merge stay human.**

## Files

- `list-maintenance.loop.md` — the prompt. Feed to Claude Code `/schedule`, a
  Routine, or system cron with `claude -p`.
- `verify.py` — the gate: HTTP-200 check, dedupe against README, blacklist,
  format + category validation. Caps output at 8/run.
- `sources.txt` — the (short, high-signal) source allowlist. No open scraping.
- `rejected.txt` — blacklist of declined hosts. Add to it when you delete a PR line.
- `seen.txt` — auto-maintained; URLs already considered, so nothing repeats.

## Run it

```bash
# one-off, locally
claude -p "$(cat loops/list-maintenance/list-maintenance.loop.md)" \
  --allowedTools "Bash,WebFetch,Write"

# or schedule weekly (cloud, survives laptop-off)
/schedule every Monday 14:00 UTC, run loops/list-maintenance/list-maintenance.loop.md
```

## Your weekly job (~5 min)

Open the PR it files. Delete anything off-topic or low-quality. Merge the rest.
Paste any deleted URL into `rejected.txt`. Done.

## Verify the loop converges (no agent needed)

```bash
python loops/list-maintenance/verify.py candidates.json
```
