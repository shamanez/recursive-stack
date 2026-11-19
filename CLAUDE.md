@AGENTS.md

## Claude Code specifics

- `/sweep` runs one update cycle. It loads `playbooks/sweep.md`.
- For the hunt step, parallel research sub-agents are fine. Anything a sub-agent
  reports and you have not opened yourself is `read: relayed`.
- To check the page, open `index.html` in the browser pane after building.
