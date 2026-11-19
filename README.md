# The Recursive Stack

**What is happening to the inference layer now that coding agents can do
performance engineering?**

A living, opinionated tracker. It holds a thesis made of claims that can lose,
weighs every new source against them, and tells you where your own framing is
holding and where it is not. An agent re-runs it every three days.

> Inference optimisation is turning from a craft into a search. Agents rewrite the
> serving stack against replayed real traffic: one model, one workload, one chip
> at a time.

## Look at it

- **Interactive dashboard:** open [`index.html`](index.html) in a browser. It is
  one self-contained file; no server needed.
- **Plain-text version:** [`BRIEF.md`](BRIEF.md), which renders on GitHub.

What is on the dashboard:

| View | What it shows |
|---|---|
| Now | The shift as a flow diagram, five things to know, a verdict on your framing, confidence per claim, the optimisation loop, and the charts that carry the argument |
| Thesis | Each claim with its confidence, the evidence for and against, and what would move it |
| Stack map | Every source placed by stack layer, by what produces the optimisation, and by where it runs |
| Ledger | Every number with its baseline and who checked it |
| Tensions | Where credible sources do opposite things, and what would settle each |
| Watch | Dated checks written before the answer is known |
| Signals | The sources, searchable and filterable |
| Cycle log | What each sweep changed, and what it looked at and left out |

## Why this is not a literature review

- **It has a thesis that can be wrong.** Eight claims, each with a confidence that
  moves only with a written reason and conditions named in advance.
- **It hunts for the counter-case.** Every sweep must search for evidence against
  its strongest claim. Critiques and failed replications count as much as wins.
- **It keeps score on itself.** Dated checks are resolved as hit or miss before
  anything new is read.
- **It rewrites instead of piling up.** The front page holds five points. Sources
  that stop mattering are retired.
- **It checks your course.** Your own framing is recorded and judged part by part
  each cycle.

## How it updates

Every three days an agent runs one **sweep**, the procedure in
[`playbooks/sweep.md`](playbooks/sweep.md): settle due checks, hunt, triage,
adjudicate, redraw the figures, rebuild, commit, push.

It works with either agent:

```bash
scripts/sweep.sh claude
```

```bash
scripts/sweep.sh codex
```

Inside Claude Code, `/sweep` does the same. Codex reads [`AGENTS.md`](AGENTS.md)
directly; Claude Code reads it through [`CLAUDE.md`](CLAUDE.md).

## Steering it

Write in [`inbox.md`](inbox.md): links you want assessed, corrections to your
framing, answers to the questions the dashboard asks you. The next sweep reads it
first.

## Rebuilding by hand

```bash
python3 scripts/build.py
```

Everything in `data/` is the source of truth. `index.html` and `BRIEF.md` are
generated; never edit them directly. No dependencies beyond Python 3.8.
