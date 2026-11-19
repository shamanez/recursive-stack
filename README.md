# The Recursive Stack

**Inference is becoming load-aware: the stack now fits itself to the traffic. What
does that do to the layer that serves the models, and how do you build for it?**

A living, opinionated tracker. It maps the levers that adapt inference to the load
and how they connect, holds a thesis made of claims that can lose, weighs every
new source against them, lays out a build order, and tells you where your own
framing is holding and where it is not. An agent re-runs it every day.

> Six levers move with the load, from which model answers to which kernel runs.
> Coding agents are what make re-tuning them affordable.

## Look at it

- **Live dashboard:** <https://shamanez.github.io/recursive-stack/>
- **Offline:** open [`index.html`](index.html) in a browser. It is one
  self-contained file; no server needed.
- **Plain-text version:** [`BRIEF.md`](BRIEF.md), which renders on GitHub.

What is on the dashboard:

| Tab | What it shows |
|---|---|
| Now | The lever map, five things to know, a verdict on your framing, what it means for a provider, confidence per claim |
| Big picture | Before and after, the six levers side by side, how they connect, the optimisation loop stage by stage |
| Build | A build order for a provider: what each step has bought others, what to watch out for, and open-source parts to reuse |
| Who | Every team found that has described the loop, on a timeline, with what each one actually did |
| Thesis | Each claim with its confidence, the evidence for and against, and what would move it |
| Stack map | Every source placed by stack layer, by what produces the optimisation, and by where it runs |
| Evidence | The charts that carry the argument, then every number with its baseline and who checked it |
| Tensions | Where credible sources do opposite things, and what would settle each |
| Watch | Dated checks written before the answer is known |
| Signals | The sources, searchable and filterable |
| Cycle log | What each sweep changed, and what it looked at and left out |

## Why this is not a literature review

- **It has a thesis that can be wrong.** Each claim has a confidence that moves
  only with a written reason and conditions named in advance. Claims get retired.
- **It hunts for the counter-case.** Every sweep must search for evidence against
  one of its claims. Critiques and failed replications count as much as wins.
- **It keeps score on itself.** Dated checks are resolved as hit or miss before
  anything new is read.
- **It rewrites instead of piling up.** The front page holds five points. Sources
  that stop mattering are retired.
- **It checks your course.** Your own framing is recorded and judged part by part.

## How it updates

Every day an agent runs one **sweep**, the procedure in
[`playbooks/sweep.md`](playbooks/sweep.md): settle due checks, hunt, triage,
adjudicate, redraw what changed, rebuild, commit, push. Most days little moves.
Once a week it goes deeper: a full check for missing teams, first-hand reads of
relayed sources, pruning.

It works with either agent:

```bash
scripts/sweep.sh claude
```

```bash
scripts/sweep.sh codex
```

The repeated jobs are skills, available to both agents (`.claude/skills/` for
Claude Code, `.agents/skills/` for Codex), each backed by a plain playbook:

| Skill | What it does |
|---|---|
| `sweep` | The daily update, start to finish |
| `add-signal` | Turn one source into a signal and carry it through to the map, roster and figures |
| `steer` | Act on something you said: restate your framing, re-judge it, follow the change through |
| `roster-check` | Look for teams building the loop that are missing from the Who tab |
| `check-page` | Serve the page and check every tab, both themes and a phone width |

## Steering it

Write in [`inbox.md`](inbox.md): links you want assessed, corrections to your
framing, answers to the questions the dashboard asks you. The next sweep reads it
first. What you have said so far is kept at the top of
[`playbooks/steer.md`](playbooks/steer.md).

## Rebuilding and checking by hand

```bash
python3 scripts/build.py
```

```bash
python3 scripts/serve.py
```

Everything in `data/` is the source of truth. `index.html` and `BRIEF.md` are
generated; never edit them directly. No dependencies beyond Python 3.8.
