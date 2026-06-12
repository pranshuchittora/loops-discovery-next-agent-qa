# Awesome Agent Loops [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> Loops, not prompts. A curated list of patterns, tools, templates and writing on **loop engineering** — designing systems that prompt your AI agents for you.

In June 2026, the way people work with coding agents shifted: instead of prompting an agent turn by turn, you design a loop that discovers work, hands it to agents, verifies the result, persists state, and decides what happens next. This list collects everything worth reading and running on that shift.

Maintained by [agentloophub.com](https://agentloophub.com) — the loop template library. *This list updates itself via an agent loop; humans approve every merge.*

## Contents

- [Concepts & Guides](#concepts--guides)
- [Origin Posts & Talks](#origin-posts--talks)
- [Loop Patterns](#loop-patterns)
- [Templates](#templates)
- [Runtimes & Harnesses](#runtimes--harnesses)
- [Scheduling & Triggers](#scheduling--triggers)
- [Verification & Guardrails](#verification--guardrails)
- [State & Memory](#state--memory)
- [Cost Control](#cost-control)
- [Communities](#communities)

## Concepts & Guides

- [What Is Loop Engineering?](https://www.mindstudio.ai/blog/what-is-loop-engineering-ai-coding-agents) - Plain-language introduction: act, observe, decide, repeat — and when loops beat single-shot prompting.
- [Loop Engineering: The Complete Guide](https://linas.substack.com/p/loop-engineering-complete-guide) - Long-form walkthrough written for both engineers and non-engineers.
- [Loop Engineering: Design Coding Agent Loops That Run While You Sleep](https://explainx.ai/blog/loop-engineering-coding-agents-claude-code-guide-2026) - From ReAct and ralph to `/goal` and `/loop` in Claude Code, with cron-driven examples.
- [Loop Engineering: The Guide for AI Agents](https://lushbinary.com/blog/loop-engineering-ai-coding-agents-guide/) - The five building blocks of a loop (plus memory), mapped to Claude Code and Codex.
- [Loop Engineering (Cobus Greyling)](https://cobusgreyling.medium.com/loop-engineering-62926dd6991c) - How loops relate to prompt, context and harness engineering.

## Origin Posts & Talks

- [Peter Steinberger's loop tweet](https://x.com/steipete) - The two sentences that named the trend: design loops that prompt your agents.
- Boris Cherny on loops - "I don't prompt Claude anymore. I have loops running. My job is to write loops." Talk clips circulating from June 2026.
- Addy Osmani on loop engineering - Framing loops as one level above agent harness engineering.

## Loop Patterns

- **Ralph loop** - The brute-force `while true` pattern: same prompt, fresh agent, until the verify step passes.
- **Maker–checker loop** - One agent acts, a separate model judges whether the goal is met; Claude Code's `/goal` applies this at the exit condition.
- **Queue-drain loop** - Discover tasks into a queue (issues, briefs, failing tests), pop one per cycle, exit when empty.
- **Cron refresh loop** - Scheduled wake-up, diff current state against desired state, act only on drift.
- **Subagent fan-out loop** - A coordinator loop that spawns scoped subagents per task and merges verified results.

## Templates

- [Agent Loop Hub templates](https://agentloophub.com) - Copy-paste loops in a seven-field format (goal, trigger, discover, act, verify, persist, exit) with measured token cost per cycle.
- Test-fix loop, content refresh loop, dependency upgrade loop, scrape-and-validate loop - see the library for runnable specs.

## Runtimes & Harnesses

- [Claude Code](https://docs.claude.com) - Agentic CLI with `/goal` loops and scheduled runs; the reference runtime for most loop writing today.
- [OpenClaw](https://github.com) - Open-source agent runtime by the author of the tweet that named the trend.
- [obra/superpowers](https://github.com/obra/superpowers) - Composable skills that give loops engineering discipline: TDD, subagent review, git worktrees.

## Scheduling & Triggers

- cron - Still the backbone of most production loops.
- CI triggers (on push / on schedule) - Loops that live in GitHub Actions.
- Event triggers - Webhooks, new-issue events, GSC data drops.

## Verification & Guardrails

- Test suites as verify steps - The strongest signal: exit 0 or loop again.
- Second-model judges - A separate model evaluating "is the goal met?" to avoid self-grading.
- Diff budgets & change caps - Bounding how much a single cycle is allowed to touch.

## State & Memory

- Markdown state files - A `state.md` the loop reads and rewrites each cycle; agents forget, the repo doesn't.
- Issue/board-backed state - Linear, GitHub Projects or a plain table as the loop's queue and memory.

## Cost Control

- Token budgets per cycle - Declare expected cost up front; kill cycles that exceed it.
- Exit conditions - No exit, no loop — just a bill.

## Communities

- r/ClaudeAI - Loop threads and Claude Code automation discussion.
- Hacker News - Search "loop engineering" for the ongoing debate.

## Contributing

One line is enough. Open a PR adding a resource in the format `- [Name](link) - One-sentence description.` See [CONTRIBUTING.md](CONTRIBUTING.md). Self-promotion is fine if the thing is genuinely useful and runnable.

## License

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](https://creativecommons.org/publicdomain/zero/1.0/)
