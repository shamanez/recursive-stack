# Check the page still renders

`scripts/build.py` proves the data has the right shape. It cannot see a figure
that overflows, a button that does nothing, or text that outgrew its box. Do this
after changing `site/template.html`, after adding a figure, lever or roster entry,
and on every weekly deep pass.

## 1. Build, then serve over HTTP

```
python3 scripts/build.py
python3 scripts/serve.py          # http://127.0.0.1:8765, Ctrl-C to stop
```

Serve it; do not open the file directly in an agent's preview pane. A preview of
a local file can be a static snapshot in which nothing responds to clicks, which
looks exactly like a broken page. `scripts/serve.py` sends no-cache headers and
works from any directory.

When reloading after a rebuild, change the query string
(`http://127.0.0.1:8765/?v=2#now`). Changing only the part after `#` does not
reload the file, so you would be looking at the old build.

## 2. Look at every tab

Now, Big picture, Build, Who, Thesis, Stack map, Evidence, Tensions, Watch,
Signals, Cycle log, Glossary. For each:

- The browser console shows no errors.
- Nothing is clipped, overlapping or spilling out of its box.
- The figure on that tab drew: the lever map has seven parts and a detail panel,
  the loop ring has five stages, the Who timeline has one mark per roster entry,
  the Watch timeline has one marker per check.

## 3. Try the things that respond

- Select a lever on the map: the selected part changes colour and the panel
  below changes with it.
- Select a stage in the loop ring: the panel beside it changes.
- Select a row in a chart, a mark on the stack map, a row in the roster: the
  source sheet opens, with a working "Read the source" link.
- On the Who tab, switch between the recent, all and providers lists.
- On Signals, a filter narrows the list; on Evidence, a segment of the bar
  filters the table.

## 4. Both themes, and a phone

- Switch theme with the button in the header. Check that text is readable and
  marks are visible in light and in dark.
- At a phone width (about 375 pixels) the page must not scroll sideways. In the
  console: `document.documentElement.scrollWidth <= window.innerWidth` must be
  `true`. Wide tables scroll inside their own box; the page does not.

## 5. If you used a browser tool with an emulated viewport

Reset it when you finish. A screenshot taken after scrolling an emulated viewport
can come back partly blank; scroll with
`element.scrollIntoView()` from the console and take the screenshot again before
concluding the page is broken.

## What to do when something is wrong

Fix it in `site/template.html` (never in `index.html`), rebuild, reload with a new
query string, and look again. If text is too long for its place, the fix is
usually in the data: the word caps in `scripts/build.py` exist for this.
