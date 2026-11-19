#!/usr/bin/env python3
"""Validate data/ and render index.html + BRIEF.md.

Stdlib only, Python 3.8+. Deterministic: the same data always produces the
same output, so git diffs show real changes only.

    python3 scripts/build.py           # validate, then write index.html and BRIEF.md
    python3 scripts/build.py --check   # validate only

Exit code 1 if any error is found. Warnings never fail the build; they are the
discipline checks an update cycle is expected to clear or consciously accept.
"""
import datetime
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

KINDS = {"blog", "paper", "repo", "product", "benchmark", "talk", "critique", "essay"}
DIRECTIONS = {"supports", "challenges", "complicates"}
VERIFICATION = {"self-reported", "public-run", "third-party", "unverified"}
SIGNAL_STATUS = {"active", "superseded", "retired"}
READ = {"opened", "relayed"}
CLAIM_STATUS = {"active", "retired", "merged"}
TENSION_STATUS = {"open", "leaning", "settled"}
WATCH_STATUS = {"open", "hit", "miss", "dropped"}
VERDICTS = {"holding", "sharpen", "unsupported", "wrong"}
CHANGE_TYPES = {"added", "revised", "retired", "confidence", "tension", "watch", "course", "model"}
LOOP_STATUS = {"working", "bottleneck", "unproven"}
FIGURE_TYPES = {"pairs", "bars"}
ROSTER_STAGES = {"production", "upstream", "research", "claimed", "retracted"}

# Word caps. The page is figure-first; prose that outgrows these belongs behind a link.
CAPS = {"intro": 120, "roster.gist": 28, "picture.head": 9, "picture.text": 34, "verdict.short": 18, "figure.takeaway": 22,
        "signal.gist": 85, "signal.changes": 55, "signal.caveats": 70}

errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def load(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        err(f"{path.relative_to(ROOT)}: file is missing")
    except json.JSONDecodeError as exc:
        err(f"{path.relative_to(ROOT)}: invalid JSON ({exc})")
    return None


def is_date(value):
    try:
        datetime.date.fromisoformat(value)
        return True
    except (TypeError, ValueError):
        return False


def is_published(value):
    """A full date, a month (YYYY-MM) when the page gives no day, or 'undated'."""
    if value == "undated" or is_date(value):
        return True
    return isinstance(value, str) and len(value) == 7 and is_date(value + "-01")


def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def need(obj, fields, where):
    """Every field must be present and non-empty."""
    ok = True
    for field in fields:
        if obj.get(field) in (None, "", []):
            err(f"{where}: '{field}' is missing or empty")
            ok = False
    return ok


def cap(text, key, where):
    n = len(str(text or "").split())
    if n > CAPS[key]:
        warn(f"{where}: {n} words, cap is {CAPS[key]}. Cut it; the detail belongs behind the link.")


def main():
    check_only = "--check" in sys.argv

    meta = load(DATA / "meta.json") or {}
    model = load(DATA / "model.json") or {}
    thesis = load(DATA / "thesis.json") or {}
    tensions = load(DATA / "tensions.json") or []
    watch = load(DATA / "watchlist.json") or {}
    course = load(DATA / "course.json") or {}
    glossary = load(DATA / "glossary.json") or []
    figures = load(DATA / "figures.json") or []
    roster = load(DATA / "roster.json") or {}

    signals = []
    for path in sorted((DATA / "signals").glob("*.json")):
        sig = load(path)
        if sig is not None:
            sig["_file"] = path.stem
            signals.append(sig)

    cycles = []
    for path in sorted((DATA / "cycles").glob("*.json")):
        cyc = load(path)
        if cyc is not None:
            cyc["_file"] = path.stem
            cycles.append(cyc)

    layer_ids = {x["id"] for x in model.get("layers", [])}
    mech_ids = {x["id"] for x in model.get("mechanisms", [])}
    venue_ids = {x["id"] for x in model.get("venues", [])}
    claim_ids = {c.get("id") for c in thesis.get("claims", [])}

    # ---- meta
    need(meta, ["title", "tagline", "started", "cadence_days", "repo"], "meta.json")

    # ---- signals (first, so everything else can point at them)
    signal_ids = set()
    evidence = {cid: {d: 0 for d in DIRECTIONS} for cid in claim_ids}
    for sig in signals:
        sid = sig.get("id", "?")
        where = f"signals/{sig['_file']}.json"
        if sid != sig["_file"]:
            err(f"{where}: id '{sid}' must equal the file name")
        if sid in signal_ids:
            err(f"{where}: duplicate id")
        signal_ids.add(sid)
        need(sig, ["id", "title", "url", "org", "published", "added", "kind", "layers", "mechanism", "venue", "gist", "changes", "caveats", "read", "status"], where)
        if not str(sig.get("url", "")).startswith("http"):
            err(f"{where}: url must be absolute")
        if not is_published(sig.get("published")):
            err(f"{where}: published must be YYYY-MM-DD, YYYY-MM or 'undated'. Never guess a date.")
        for link in sig.get("also") or []:
            if not link.get("label") or not str(link.get("url", "")).startswith("http"):
                err(f"{where}: each 'also' entry needs a label and an absolute url")
        if not is_date(sig.get("added")):
            err(f"{where}: added must be YYYY-MM-DD")
        if sig.get("kind") not in KINDS:
            err(f"{where}: kind must be one of {sorted(KINDS)}")
        for layer in sig.get("layers") or []:
            if layer not in layer_ids:
                err(f"{where}: unknown layer '{layer}' (see data/model.json)")
        if sig.get("mechanism") not in mech_ids:
            err(f"{where}: unknown mechanism '{sig.get('mechanism')}'")
        if sig.get("venue") not in venue_ids:
            err(f"{where}: unknown venue '{sig.get('venue')}'")
        if sig.get("status") not in SIGNAL_STATUS:
            err(f"{where}: status must be one of {sorted(SIGNAL_STATUS)}")
        if sig.get("read") not in READ:
            err(f"{where}: read must be 'opened' (the cycle agent read the page itself) or 'relayed'")
        for bear in sig.get("bears_on") or []:
            if bear.get("claim") not in claim_ids:
                err(f"{where}: bears_on names unknown claim '{bear.get('claim')}'")
            elif bear.get("direction") not in DIRECTIONS:
                err(f"{where}: direction must be one of {sorted(DIRECTIONS)}")
            elif sig.get("status") == "active":
                evidence[bear["claim"]][bear["direction"]] += 1
            if not bear.get("note"):
                err(f"{where}: bears_on entry for {bear.get('claim')} needs a 'note' saying how")
        for num in sig.get("numbers") or []:
            need(num, ["metric", "value", "baseline", "verification"], f"{where} numbers")
            if num.get("verification") not in VERIFICATION:
                err(f"{where}: number verification must be one of {sorted(VERIFICATION)}")
        if sig.get("status") == "active" and not sig.get("bears_on"):
            warn(f"{where}: bears on no claim. Say what it changes, or retire it.")
        if sig.get("status") == "superseded" and not sig.get("superseded_by"):
            err(f"{where}: superseded signals need 'superseded_by'")
        for field in ("gist", "changes", "caveats"):
            cap(sig.get(field), f"signal.{field}", f"{where} {field}")

    def known_signals(ids, where):
        for sid in ids or []:
            if sid not in signal_ids:
                err(f"{where}: names unknown signal '{sid}'")

    active_signals = [s for s in signals if s.get("status") == "active"]
    if len(active_signals) > 60:
        warn(f"{len(active_signals)} active signals. Retire or merge until the set is something a person can hold in their head.")

    # ---- model
    for stage in model.get("loop", []):
        where = f"model.json loop '{stage.get('id')}'"
        need(stage, ["id", "name", "does", "hard", "status"], where)
        if stage.get("status") not in LOOP_STATUS:
            err(f"{where}: status must be one of {sorted(LOOP_STATUS)}")
        known_signals(stage.get("signals"), where)
    shift = model.get("shift") or {}
    for side in ("then", "now"):
        need(shift.get(side) or {}, ["label", "steps"], f"model.json shift.{side}")

    # ---- thesis
    need(thesis, ["headline", "subhead", "intro", "picture", "claims"], "thesis.json")
    cap(thesis.get("intro"), "intro", "thesis.json intro")
    picture = thesis.get("picture") or []
    if len(picture) > 5:
        err("thesis.json: 'picture' holds at most 5 points. Replace one; do not add a sixth.")
    for i, point in enumerate(picture):
        where = f"thesis.json picture[{i}]"
        if not isinstance(point, dict):
            err(f"{where}: must be an object with head, text and signals")
            continue
        need(point, ["head", "text", "signals"], where)
        cap(point.get("head"), "picture.head", f"{where} head")
        cap(point.get("text"), "picture.text", f"{where} text")
        known_signals(point.get("signals"), where)
    seen_claims = set()
    for claim in thesis.get("claims", []):
        cid = claim.get("id", "?")
        where = f"thesis.json claim {cid}"
        if cid in seen_claims:
            err(f"{where}: duplicate id")
        seen_claims.add(cid)
        need(claim, ["id", "short", "statement", "plain", "confidence", "history", "raise_if", "lower_if", "status"], where)
        conf = claim.get("confidence")
        if not is_number(conf) or not 0 <= conf <= 1:
            err(f"{where}: confidence must be a number between 0 and 1")
        if claim.get("status") not in CLAIM_STATUS:
            err(f"{where}: status must be one of {sorted(CLAIM_STATUS)}")
        hist = claim.get("history") or []
        for point in hist:
            if not is_date(point.get("cycle")):
                err(f"{where}: history entry has a bad 'cycle' date")
            if not point.get("why"):
                err(f"{where}: history entry {point.get('cycle')} needs a 'why'")
        if hist and hist[-1].get("confidence") != conf:
            err(f"{where}: confidence {conf} does not match the last history entry {hist[-1].get('confidence')}")
        if claim.get("status") == "active":
            ev = evidence.get(cid, {})
            if ev.get("supports", 0) and not (ev.get("challenges", 0) or ev.get("complicates", 0)):
                warn(f"claim {cid}: only supporting evidence is logged. Go and look for the counter-case.")
            if not sum(ev.values()):
                warn(f"claim {cid}: no evidence attached at all.")

    # ---- roster
    need(roster, ["recent_from", "entries"], "roster.json")
    if not is_date(roster.get("recent_from")):
        err("roster.json: recent_from must be YYYY-MM-DD")
    seen_systems = set()
    for entry in roster.get("entries") or []:
        where = f"roster.json '{entry.get('who')}'"
        need(entry, ["who", "system", "kind", "when", "means", "stage", "gist", "read"], where)
        key = (entry.get("who"), entry.get("system"))
        if key in seen_systems:
            err(f"{where}: listed twice")
        seen_systems.add(key)
        for field in ("when", "updated"):
            if entry.get(field) is not None and (entry[field] == "undated" or not is_published(entry[field])):
                err(f"{where}: {field} must be YYYY-MM-DD or YYYY-MM")
        if entry.get("means") not in mech_ids:
            err(f"{where}: unknown means '{entry.get('means')}'")
        if entry.get("stage") not in ROSTER_STAGES:
            err(f"{where}: stage must be one of {sorted(ROSTER_STAGES)}")
        if entry.get("read") not in READ:
            err(f"{where}: read must be 'opened' or 'relayed'")
        if entry.get("signal"):
            known_signals([entry["signal"]], where)
        elif not str(entry.get("url", "")).startswith("http"):
            err(f"{where}: needs a 'signal' id or an absolute 'url'")
        cap(entry.get("gist"), "roster.gist", f"{where} gist")

    # ---- figures
    figure_ids = set()
    for fig in figures:
        fid = fig.get("id", "?")
        where = f"figures.json {fid}"
        if fid in figure_ids:
            err(f"{where}: duplicate id")
        figure_ids.add(fid)
        need(fig, ["id", "type", "title", "takeaway", "rows", "caption"], where)
        cap(fig.get("takeaway"), "figure.takeaway", f"{where} takeaway")
        if fig.get("type") not in FIGURE_TYPES:
            err(f"{where}: type must be one of {sorted(FIGURE_TYPES)}")
        group_ids = {g.get("id") for g in fig.get("groups") or []}
        if len(group_ids) > 3:
            err(f"{where}: at most 3 groups. Past that, split the figure.")
        for row in fig.get("rows") or []:
            need(row, ["label"], f"{where} row")
            keys = ("from", "to") if fig.get("type") == "pairs" else ("value",)
            for key in keys:
                if not is_number(row.get(key)):
                    err(f"{where} row '{row.get('label')}': '{key}' must be a number")
            if row.get("group") and row["group"] not in group_ids:
                err(f"{where} row '{row.get('label')}': unknown group '{row['group']}'")
            if not row.get("signal"):
                err(f"{where} row '{row.get('label')}': every row cites the signal its number comes from")
            known_signals([row.get("signal")] if row.get("signal") else [], where)
        for cid in fig.get("claims") or []:
            if cid not in claim_ids:
                err(f"{where}: names unknown claim '{cid}'")
    if sum(1 for f in figures if f.get("featured")) > 4:
        warn("figures.json: more than 4 featured figures. The front page is for the few that carry the argument.")

    # ---- tensions
    tension_ids = set()
    for ten in tensions:
        tid = ten.get("id", "?")
        where = f"tensions.json {tid}"
        if tid in tension_ids:
            err(f"{where}: duplicate id")
        tension_ids.add(tid)
        need(ten, ["id", "question", "sides", "settles_when", "status"], where)
        if ten.get("status") not in TENSION_STATUS:
            err(f"{where}: status must be one of {sorted(TENSION_STATUS)}")
        if len(ten.get("sides") or []) < 2:
            err(f"{where}: a tension needs at least two sides")
        for side in ten.get("sides") or []:
            known_signals(side.get("signals"), where)

    # ---- watchlist
    today = datetime.date.today()
    watch_ids = set()
    for chk in watch.get("checks", []):
        wid = chk.get("id", "?")
        where = f"watchlist.json {wid}"
        if wid in watch_ids:
            err(f"{where}: duplicate id")
        watch_ids.add(wid)
        need(chk, ["id", "what", "why", "opened", "due", "status"], where)
        if not is_date(chk.get("due")) or not is_date(chk.get("opened")):
            err(f"{where}: opened and due must be YYYY-MM-DD")
        elif chk.get("status") == "open" and datetime.date.fromisoformat(chk["due"]) < today:
            warn(f"{where}: due {chk['due']} and still open. Resolve it (hit / miss / dropped) or move the date with a reason.")
        if chk.get("status") not in WATCH_STATUS:
            err(f"{where}: status must be one of {sorted(WATCH_STATUS)}")
        if chk.get("status") in {"hit", "miss", "dropped"} and not chk.get("resolution"):
            err(f"{where}: closed checks need a 'resolution'")
        for cid in chk.get("claims") or []:
            if cid not in claim_ids:
                err(f"{where}: names unknown claim '{cid}'")
    for feed in watch.get("feeds", []):
        need(feed, ["name", "url", "why"], "watchlist.json feed")

    # ---- course
    need(course, ["as_of", "reader_framing", "verdicts", "reframe"], "course.json")
    for ver in course.get("verdicts", []):
        need(ver, ["part", "verdict", "short", "note"], "course.json verdict")
        cap(ver.get("short"), "verdict.short", f"course.json verdict '{ver.get('part')}' short")
        if ver.get("verdict") not in VERDICTS:
            err(f"course.json: verdict must be one of {sorted(VERDICTS)}")
    read_next = course.get("read_next") or []
    if len(read_next) > 3:
        err("course.json: read_next is capped at 3. Choosing is the point.")
    known_signals([item.get("signal") for item in read_next], "course.json read_next")

    # ---- cycles
    for cyc in cycles:
        where = f"cycles/{cyc['_file']}.json"
        need(cyc, ["id", "n", "agent", "summary", "changes", "next_due"], where)
        if cyc.get("id") != cyc["_file"] or not is_date(cyc.get("id")):
            err(f"{where}: id must be the YYYY-MM-DD file name")
        for change in cyc.get("changes") or []:
            if change.get("type") not in CHANGE_TYPES:
                err(f"{where}: change type must be one of {sorted(CHANGE_TYPES)}")
            if not change.get("text"):
                err(f"{where}: every change needs 'text'")
    cycles.sort(key=lambda c: c.get("id", ""), reverse=True)
    if cycles and course.get("as_of") and course["as_of"] < cycles[0].get("id", ""):
        warn("course.json: as_of is older than the latest cycle. The course check must be re-judged every cycle.")

    # ---- glossary
    for entry in glossary:
        need(entry, ["term", "def"], "glossary.json entry")

    for line in warnings:
        print(f"warning: {line}")
    for line in errors:
        print(f"ERROR:   {line}")
    if errors:
        print(f"\n{len(errors)} error(s). Nothing written.")
        return 1
    if check_only:
        print(f"ok: {len(signals)} signals, {len(claim_ids)} claims, {len(figures)} figures, {len(cycles)} cycle(s), {len(warnings)} warning(s)")
        return 0

    # Newest first; undated sources go last.
    signals.sort(key=lambda s: ("" if s.get("published") == "undated" else s.get("published", ""), s.get("id", "")), reverse=True)
    for item in signals + cycles:
        item.pop("_file", None)

    bundle = {
        "meta": meta,
        "model": model,
        "thesis": thesis,
        "signals": signals,
        "figures": figures,
        "roster": roster,
        "tensions": tensions,
        "watch": watch,
        "course": course,
        "cycles": cycles,
        "glossary": sorted(glossary, key=lambda g: g["term"].lower()),
    }
    payload = json.dumps(bundle, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    template = (ROOT / "site" / "template.html").read_text(encoding="utf-8")
    if "/*__DATA__*/null" not in template:
        print("ERROR:   site/template.html has no /*__DATA__*/null placeholder")
        return 1
    page = template.replace("/*__DATA__*/null", payload, 1)
    page = page.replace("<!--__GENERATED__-->", "<!-- GENERATED by scripts/build.py from data/. Edit site/template.html or data/, never this file. -->", 1)
    (ROOT / "index.html").write_text(page, encoding="utf-8")
    (ROOT / "BRIEF.md").write_text(brief(bundle, evidence), encoding="utf-8")
    print(f"built index.html and BRIEF.md: {len(signals)} signals, {len(claim_ids)} claims, {len(figures)} figures, {len(cycles)} cycle(s), {len(warnings)} warning(s)")
    return 0


def brief(b, evidence):
    """A plain-markdown digest: what GitHub shows, and what an agent reads first."""
    meta, thesis, course = b["meta"], b["thesis"], b["course"]
    latest = b["cycles"][0] if b["cycles"] else {}
    by_id = {s["id"]: s for s in b["signals"]}
    link = lambda sid: f"[{by_id[sid]['org'].split(',')[0].split('(')[0].strip()}]({by_id[sid]['url']})"
    out = []
    add = out.append
    add("<!-- GENERATED by scripts/build.py. Do not edit; change data/ and rebuild. -->")
    add(f"# {meta['title']}: current brief")
    add("")
    add(f"Cycle {latest.get('n', '?')} · as of {latest.get('id', '?')} · next sweep due {latest.get('next_due', '?')} · "
        f"{sum(1 for s in b['signals'] if s['status'] == 'active')} active signals")
    add("")
    add(f"> **{thesis['headline'].replace('*', '')}** {thesis['subhead']}")
    add("")
    add(thesis["intro"])
    add("")
    add("## Five things to know")
    add("")
    for point in thesis["picture"]:
        add(f"- **{point['head']}.** {point['text']} ({', '.join(link(s) for s in point['signals'])})")
    add("")
    entries = sorted(b["roster"].get("entries", []), key=lambda e: e.get("updated") or e["when"], reverse=True)
    if entries:
        add("## Who is building the loop")
        add("")
        add("| First described | Who | What they did | Stage |")
        add("|---|---|---|---|")
        for e in entries:
            url = by_id[e["signal"]]["url"] if e.get("signal") else e["url"]
            add(f"| {e['when']} | [{e['who']}: {e['system']}]({url}) | {e['gist']} | {e['stage']} |")
        add("")
    add("## Course check")
    add("")
    add(f"**Your working framing:** {course['reader_framing']}")
    add("")
    add("| Part of the framing | Verdict | In one line |")
    add("|---|---|---|")
    for ver in course["verdicts"]:
        add(f"| {ver['part']} | {ver['verdict']} | {ver['short']} |")
    add("")
    add(f"**Sharper version:** {course['reframe']}")
    add("")
    if course.get("read_next"):
        add("**Read next:**")
        add("")
        for item in course["read_next"]:
            sig = by_id[item["signal"]]
            add(f"- [{sig['title']}]({sig['url']}): {item['why']}")
        add("")
    add("## Claims")
    add("")
    add("| | Claim | Confidence | For / mixed / against |")
    add("|---|---|---|---|")
    for claim in thesis["claims"]:
        if claim["status"] != "active":
            continue
        ev = evidence.get(claim["id"], {})
        add(f"| {claim['id']} | {claim['statement']} | {round(claim['confidence'] * 100)}% | "
            f"{ev.get('supports', 0)} / {ev.get('complicates', 0)} / {ev.get('challenges', 0)} |")
    add("")
    if b["figures"]:
        add("## The numbers that carry the argument")
        add("")
        for fig in b["figures"]:
            add(f"**{fig['title']}.** {fig['takeaway']}")
            add("")
            for row in fig["rows"]:
                unit = fig.get("unit", "")
                value = f"{row['from']}{unit} → {row['to']}{unit}" if fig["type"] == "pairs" else f"{row['value']}{unit}"
                add(f"- {row['label']}: {value} ({link(row['signal'])})")
            add("")
    if latest:
        add(f"## What changed in cycle {latest.get('n')}")
        add("")
        add(latest.get("summary", ""))
        add("")
        for change in latest.get("changes", []):
            ref = f" `{change['ref']}`" if change.get("ref") else ""
            add(f"- **{change['type']}**{ref}: {change['text']}")
        add("")
    open_tensions = [t for t in b["tensions"] if t["status"] != "settled"]
    if open_tensions:
        add("## Open tensions")
        add("")
        for ten in open_tensions:
            add(f"- **{ten['id']}** {ten['question']} _Settles when:_ {ten['settles_when']}")
        add("")
    open_checks = sorted((c for c in b["watch"].get("checks", []) if c["status"] == "open"), key=lambda c: c["due"])
    if open_checks:
        add("## Watchlist")
        add("")
        add("| Due | Check |")
        add("|---|---|")
        for chk in open_checks:
            add(f"| {chk['due']} | {chk['what']} |")
        add("")
    add("Open `index.html` for the interactive version: flow diagrams, stack map, evidence ledger, every signal.")
    add("")
    return "\n".join(out)


if __name__ == "__main__":
    sys.exit(main())
