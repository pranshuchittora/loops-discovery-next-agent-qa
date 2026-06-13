# list-maintenance.loop

Discovers new loop-engineering resources, drafts them as awesome-list entries,
verifies them, and opens a PR for human review. Never merges on its own.

This is the loop that maintains awesome-agent-loops. It is also the reference
example of "discover → act → verify → human approve → persist" running in
production.

---

## GOAL

The repo's `candidates.md` holds 0–8 freshly discovered, verified, correctly
categorized loop-engineering resources that are NOT already in README.md, each
drafted in awesome single-line format and bundled into one open PR for the
maintainer to approve. The loop never writes to README.md or main directly.

## TRIGGER

`0 14 * * 1`  — every Monday 14:00 UTC (weekly). Run via Claude Code Routine,
`/schedule`, or system cron with `claude -p`.

## DISCOVER

Pull candidate resources from compliant, structured sources only. Do NOT scrape
X/Twitter HTML or violate any ToS.

1. GitHub search (primary, free, structured):
   - `gh search repos --topic loop-engineering --topic agent-loops --sort updated --limit 30`
   - new repos with >3 stars created/pushed in the last 7 days
   - also diff competitor lists for entries we lack:
     serenakeyitan/awesome-agent-loops, and the loops.elorm.xyz catalog
2. RSS / Atom feeds (compliant, zero-risk) — read the URLs in `sources.txt`:
   - blogs that cover loop engineering (Addy Osmani's Substack, Pulumi blog, devrel blogs)
   - official changelogs: Claude Code, Codex, OpenClaw release notes
3. If X coverage is wanted, use an RSS bridge (e.g. Nitter RSS) for a SHORT
   allowlist of accounts in `sources.txt` only (steipete, bcherny, addyosmani).
   Never do open-ended web scraping.

Collect: title, canonical URL, one-line description, and where it was found.

## ACT

For each raw candidate:
1. Write it as an awesome single-line entry:
   `- [Name](canonical-url) - One concise, technical sentence. No marketing adjectives.`
2. Assign exactly one category from README.md's existing sections:
   Concepts & Guides | Origin Posts & Talks | Loop Patterns | Templates |
   Runtimes & Harnesses | Scheduling & Triggers | Verification & Guardrails |
   State & Memory | Cost Control | Related Lists | Communities
3. Prefer the canonical/original source (author's blog, the repo, official docs)
   over aggregators or reposts.

## VERIFY  (the gate — nothing passes without this)

Run `python loops/list-maintenance/verify.py candidates.json`. A candidate is
REJECTED unless ALL hold:
- URL returns HTTP 200 (follow redirects; dead links are dropped, not queued)
- URL host is not already present anywhere in README.md (dedupe)
- URL is not in `rejected.txt` (the blacklist of previously-declined items)
- the drafted line matches awesome format (`- [text](url) - sentence.`)
- the assigned category is one of the README sections above
Cap the output at 8 candidates per run. If more pass, keep the 8 with the
strongest signal (stars / author authority / recency) and discard the rest.

## PERSIST

- Write the surviving entries to `candidates.md`, grouped by target category.
- Open ONE pull request titled `Weekly loop discovery: N candidates (YYYY-MM-DD)`,
  body = the drafted lines + their source-found notes, base `main`, head a new
  branch `discovery/YYYY-MM-DD`.
- Append every URL you considered (accepted or rejected) to `seen.txt` so next
  week's run won't re-surface them.

## EXIT  (hard stops — non-negotiable)

- The loop STOPS at "PR opened." It must NEVER merge, NEVER push to main,
  NEVER edit README.md directly. Merging is a human action.
- If 0 candidates survive verify, open no PR; just update `seen.txt` and exit.
- One PR per run. Do not reopen or amend last week's PR.

## COST

~8–15k tokens/cycle (mostly the discovery + drafting; verify is shell/HTTP, cheap).
Weekly cadence keeps this trivial. Declare it; kill the cycle if it blows past 30k.

---

## Human step (you, ~5 min/week)

Open the PR. Delete any line that's off-topic, low-quality, or a dupe the
dedupe missed. Merge what's left. Anything you delete: paste its URL into
`rejected.txt` so the loop never suggests it again.

That's the whole maintenance burden. Discover + draft + verify is automated;
taste and the merge stay with you — which is exactly what keeps an awesome list
trustworthy.
