# Check the roster for missing teams

`data/roster.json` lists every team found that has described an optimisation loop
for inference: agents (or, flagged separately, a controller) re-tuning part of the
serving stack. The reader asked that no team be missed and that each one's gist be
stated. The first version of the front page named five teams where there were ten;
this procedure exists so that does not happen again.

Run it in full on the weekly deep pass, and add single entries any day one turns
up.

## 1. Search by kind of team, not by topic

A topic search returns the teams you already have. Search each kind separately,
restricted to the time since the last deep pass:

| Kind | What to look for |
|---|---|
| Inference providers | Together, Fireworks, Baseten, Modal, Anyscale, Groq, Cerebras, SambaNova, Nebius, DeepInfra, Crusoe, hyperscalers: any post about agents tuning their serving stack |
| Open engines | vLLM blog and RFC issues, the SGLang (LMSYS) blog, llm-d, TensorRT-LLM, llama.cpp: agent-written or agent-assisted performance work |
| Model labs | Posts from labs about a model building or tuning its own serving (Z.ai did; check Moonshot, MiniMax, DeepSeek, Alibaba, and the closed labs) |
| Chip vendors | NVIDIA, AMD, Qualcomm, and accelerator start-ups: agent loops that write kernels for their chips |
| Workload owners | Companies that are not providers running the loop on their own traffic (Decagon and Unity so far) |
| Academics | arXiv, searched for: agents plus inference engine, serving system, kernel generation, self-evolving, autoresearch |
| The public board | New entrants at the top of the AgentX results, and how their kernels were produced |

Also follow the citations out of the newest two roster entries; teams cite their
rivals.

## 2. Confirm before adding

Open the page. A roster entry needs three things you can only get there:

- **When it was first described** (`when`), from the page.
- **What the team actually did**, in one line of 28 words: the `gist`. Not what
  they call it. "Agents rewrite the forward pass per traffic shape, model and
  chip" is a gist. "A recursive self-improvement loop" is a label.
- **How far along it is** (`stage`): `production` (serving real traffic),
  `upstream` (merged into an open engine), `research` (a measured result outside
  production), `claimed` (asserted, no way to check), `retracted`.

## 3. Write the entry

```json
{
  "who": "Team or organisation",
  "system": "What they call it",
  "kind": "Inference provider | Open engine | Model lab | Chip vendor | Workload owner | Academic group | Startup",
  "when": "2026-11-09",
  "updated": "2026-11-17",
  "means": "agent",
  "stage": "research",
  "gist": "One line on what they actually did.",
  "signal": "2026-11-09-inferenceforge",
  "read": "opened"
}
```

- `means` is `agent` for an agent loop. Use `online` for a system that adapts
  with a controller and writes no code; it is listed so the difference is visible.
- Give `signal` if the source has been weighed against the thesis
  (`playbooks/add-signal.md`), otherwise `url`. An entry with only a `url` is
  noted, not weighed. Promote it to a signal when it moves a claim.
- `updated` is a later post that matters; it keeps the team in the recent view.
- Keep `kind` containing the word "provider" for providers: the Who tab's
  providers filter matches on it.

## 4. Keep the count honest

Point 1 on the front page (`picture[0]` in `data/thesis.json`) states how many
teams have announced since `recent_from`. After adding or removing entries,
recount and fix that sentence. On a deep pass, move `recent_from` forward so the
default view covers about the last six weeks.

## 5. Record what you could not see

Some teams cannot be found by searching: closed labs publish nothing on this, and
pages time out. List what you tried and could not open in the cycle record's
`rejected` list, so the next pass tries again.
