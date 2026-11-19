@AGENTS.md

## Claude Code specifics

- The procedures are skills: `/sweep`, `/add-signal`, `/steer`, `/roster-check`,
  `/check-page`. Each loads the playbook of the same name.
- For research, parallel sub-agents are fine. Anything a sub-agent reports and you
  have not opened yourself is `read: relayed`.
- To check the page, follow `playbooks/check-page.md`: serve it with
  `python3 scripts/serve.py` and open that address in the browser pane. A preview
  of the local file can be a static snapshot that does not respond to clicks.
