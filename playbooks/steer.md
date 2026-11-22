# Act on something the reader said

The reader steers this repository in two ways: by writing in `inbox.md`, and by
saying things in conversation. Either way the handling is the same. It has
happened several times already, and each time it changed the thesis more than any
new source did, so treat it as the highest-priority input there is.

## What the reader has said so far (keep this in mind)

- The page should be figure-first: flow charts, diagrams and colour over
  paragraphs, with links for depth. Text is fine where it explains.
- "Local" means the stack fits what you have (your models, chips, traffic). It
  does not mean on-device hardware, and hardware itself is not the point.
- They are reading this as a **provider**, serving **many model families**. Work that
  repeats per model matters most to them.
- The frame is wider than agents optimising engines: it is inference becoming
  load-aware and adaptive, and how the parts connect (open and frontier models
  side by side, routing, speculative decoding, tuning for a domain).
- No team building the loop should be missing from the roster, and each should
  have its gist stated.
- They want to know how to build such a system.
- They would build the **measuring rig first**. That matches the build order; keep
  the rig steps the best evidenced.
- The tracker serves three purposes at once: **building a system** (weight tooling,
  costs and how others built theirs), **positioning research** (weight gaps and
  what nobody has shown: `open_ground` in `data/map.json`), and **placing a bet**
  (weight who keeps the gains and which leads last).
- The repository and the page are **public**, at their request, so they can share
  the link.
- They want **X (Twitter) searched** alongside blogs and papers: maintainers,
  providers and labs often post there first. Sweeps reach it through a web search
  limited to x.com and open single posts directly; X's own search needs a sign-in,
  and sweeps never sign in.

The current wording of their framing lives in `data/course.json`
(`reader_framing`, `position`).

## Procedure

1. **Work out what kind of input it is.**
   - *A link.* Treat it as a candidate: `playbooks/add-signal.md`. Tell them in
     the Processed note what it moved, or that it moved nothing and why.
   - *A correction to their framing* ("by X I meant Y"). Go to step 2.
   - *A change of scope* ("we do not need to go into Z", "also cover W"). Go to
     step 3.
   - *A request about the page* (more figures, less text, a new section). Change
     `site/template.html` or the data shape, then `playbooks/check-page.md`, and
     record the preference in `AGENTS.md` so it survives.
   - *An answer to a question the page asked them.* Record it in
     `data/course.json`, remove the question, and go to step 2.

2. **Restate, then re-judge.**
   - Rewrite `reader_framing` in `data/course.json` in close to their own words.
     Only they change what it says; you only keep it accurate.
   - Re-judge every verdict against the evidence as it stands. A verdict can go
     from `unsupported` to `holding` purely because the claim being judged
     changed. That is correct; say so in the note.
   - Re-derive `implications` for their `position`.

3. **Follow the scope change all the way through.** Half-applied scope changes
   are the main way this repository goes stale.
   - *Narrowing:* retire the claims that only tested the dropped reading
     (`status: retired`, `retired_why`), retire signals that only bore on them,
     re-point signals that still matter to a surviving claim, remove tensions
     premised on it, and mark its watchlist checks `dropped` with a `resolution`.
     Then search the data for leftovers: `grep -rn "<the dropped idea>" data/`.
   - *Widening:* add or extend the lever in `data/map.json`, research the new
     area before writing about it, add claims only where there is evidence to
     test them against, and open dated checks for what is still unknown.

4. **Leave a trail.**
   - Move the inbox entry to "Processed" with the date and one line on what was
     done. Summarise; never paste the reader's words. The repository is public.
   - Add a `course` change to today's cycle record.
   - If it is a standing preference about how to work or how the page should
     look, add it to the list at the top of this file and to `AGENTS.md`.

5. **Build, check, commit, push** as in `playbooks/sweep.md` steps 7 and 8.

## What not to do

- Do not argue the reader out of their scope. If the evidence contradicts their
  framing, the verdict says `wrong` and explains; the scope is still theirs.
- Do not keep tracking something they said to drop because it is interesting.
- Do not put words in `reader_framing` that they did not say or clearly mean.
