---
name: sweep
description: Run one update cycle of The Recursive Stack. Settles due watchlist checks, hunts for new evidence, adjudicates the claims, rewrites the front page, rebuilds, commits and pushes. Use when asked to sweep, update, refresh, or run a cycle of this repository.
---

Run one sweep of this repository.

1. Read `playbooks/sweep.md` in the repository root. It is the whole procedure.
2. Follow it in order, start to finish, without asking questions. Where something
   is ambiguous, make the conservative choice and record it in the cycle summary.
3. `AGENTS.md` holds the data rules and the writing style. Both apply.

If the playbook's early-stop condition holds (the last cycle is under two days old
and `inbox.md` has nothing open), say so and change nothing.
