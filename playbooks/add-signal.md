# Add a signal

A signal is one source that moves something: a claim, a lever, a tension or a
watchlist check. This is the most repeated job in the repository, and the one
where sloppiness compounds. Do it the same way every time.

## 1. Open the source yourself

Read the page, not a summary of it. If a research sub-agent reported it and you
have not opened it, it is `read: relayed`; say so and move on, or open it.

Take from the page, and only from the page:

- **The date.** `YYYY-MM-DD`, or `YYYY-MM` if only a month is shown, or `undated`.
  Never infer it from a URL or an arXiv number. arXiv numbers have been wrong
  about the month here before.
- **Who.** Organisation and authors as the page gives them. If affiliations are
  not shown, do not supply them.
- **What was actually done**, as distinct from what it is called. A system named
  for self-improvement that moves knobs with a controller is a controller.
- **Every number with its baseline.** Against what, on what hardware, measured by
  whom. A speed-up with no stated baseline is not recorded as a number; mention it
  in `caveats` instead.

## 2. Decide what it moves

If you cannot name a claim, lever, tension or check it bears on, it is not a
signal. Put it in the cycle record's `rejected` list with a one-line reason.

## 3. Write the file

`data/signals/<published>-<slug>.json`, where `<published>` is the date you took
from the page (or no prefix if undated). The `id` equals the file name.

```json
{
  "id": "2026-11-09-inferenceforge",
  "title": "The source's own title",
  "url": "https://the-exact-page-you-opened",
  "org": "Publisher or lab",
  "authors": "Optional, as shown",
  "published": "2026-11-09",
  "added": "today",
  "kind": "blog | paper | repo | product | benchmark | talk | critique | essay",
  "layers": ["loop", "kernels"],
  "mechanism": "agent",
  "venue": "cluster",
  "gist": "What it is. Three sentences, 85 words at most, your own words.",
  "changes": "What it does to the thesis. 55 words. Not what the source says about itself.",
  "caveats": "What to doubt. 70 words. Who measured, what is missing, what is planned not shipped.",
  "numbers": [
    {"metric": "What was measured", "value": "12.8k tok/s per GPU (+43%)",
     "baseline": "8.9k, best published run", "verification": "self-reported",
     "setup": "8x B300, one node"}
  ],
  "bears_on": [
    {"claim": "C1", "direction": "supports", "note": "One sentence saying how."}
  ],
  "also": [{"label": "Code", "url": "https://..."}],
  "read": "opened",
  "status": "active"
}
```

Field rules the build enforces:

- `layers`, `mechanism`, `venue` use the ids in `data/model.json`. Mechanism is
  how the optimisation is produced: `hand`, `rules`, `online` (the running system
  adjusts itself; no code is written), `agent` (agents write code, a harness
  measures), `frame` (benchmarks, critiques, essays).
- `verification`: `self-reported` (the author measured their own system),
  `public-run` (a public CI run or merged pull request anyone can inspect),
  `third-party` (measured by someone other than the system's author),
  `unverified`.
- `direction`: `supports`, `challenges`, or `complicates`. Use `complicates` when
  it is true but cuts both ways. Do not round a complication up to support.

## 4. Carry it through

A signal that only sits in its file changes nothing on the page. After writing it:

- If it changes what a lever has bought or how far along it is, update that lever
  in `data/map.json` and add the signal to its `signals`.
- If it is a team describing a loop, add or update its row in `data/roster.json`.
- If its numbers belong in an existing figure, add the row in `data/figures.json`.
- If it settles or opens a check, update `data/watchlist.json`.
- Then decide whether any confidence moves (playbook step 4).

## 5. Validate

```
python3 scripts/build.py --check
```

Zero errors. Read the warnings: a word-cap warning means cut the text, not that
the cap is wrong.

## The mistakes this procedure exists to prevent

- Taking a vendor's label for the mechanism.
- Recording a kernel speed-up as if it were an end-to-end gain. Kernel gains of
  several times have been worth about 1% inside a full engine.
- Comparing against another team's published run from a different date and
  calling it a like-for-like result. Say what the baseline was.
- Writing `opened` for a page only a sub-agent read.
- Adding a signal for something interesting that moves nothing.
