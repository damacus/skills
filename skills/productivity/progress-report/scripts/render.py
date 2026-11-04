#!/usr/bin/env python3
"""Render the machine-readable JSON progress report using only Python's standard library."""

import argparse
import html
import re
from pathlib import Path
from string import Template
from urllib.parse import quote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
IDENTIFIER = r"[A-Za-z][A-Za-z0-9_-]*"
STATES = {
    "Implementation": {"complete", "in-progress", "not-started"},
    "Local checks": {"passed", "pending", "failed", "not-required"},
    "Publication": {"published", "unpublished"},
    "Hosted checks": {"passed", "pending", "failed", "not-required"},
    "Acceptance": {"passed", "pending", "failed", "not-required"},
    "Merge": {"merged", "unmerged"},
    "Deployment": {"deployed", "not-deployed"},
}
LABELS = {
    "complete": "Implemented", "in-progress": "In progress",
    "not-started": "Not started", "passed": "Passed", "pending": "Pending",
    "failed": "Failed", "not-required": "Not required", "published": "Published",
    "unpublished": "Unpublished", "merged": "Merged", "unmerged": "Unmerged",
    "deployed": "Deployed", "not-deployed": "Not deployed",
}


def escape(value):
    return html.escape(str(value), quote=True)


def url(value):
    """Allow evidence links, including local paths; reject active URL schemes."""
    scheme = urlsplit(value).scheme.lower()
    if scheme not in {"", "http", "https", "file"}:
        raise ValueError(f"Unsupported link scheme: {scheme}")
    if value.startswith("//"):
        raise ValueError("Use an explicit https URL instead of a protocol-relative link")
    return escape(value)


def inline(value):
    # Deliberately small Markdown subset. All text and attributes are escaped.
    parts = re.split(r"(\[[^\]\n]+\]\([^\s)]+\)|\*\*[^*\n]+\*\*|`[^`\n]+`)", value)
    result = []
    for part in parts:
        link = re.fullmatch(r"\[([^\]]+)\]\(([^)]+)\)", part)
        if link:
            result.append(f'<a href="{url(link[2])}">{escape(link[1])}</a>')
        elif part.startswith("**") and part.endswith("**"):
            result.append(f"<strong>{escape(part[2:-2])}</strong>")
        elif part.startswith("`") and part.endswith("`"):
            result.append(f"<code>{escape(part[1:-1])}</code>")
        else:
            result.append(escape(part))
    return "".join(result)


def prose(value):
    blocks = []
    for block in re.split(r"\n\s*\n", value.strip()):
        if not block:
            continue
        lines = block.splitlines()
        if all(line.startswith("- ") for line in lines):
            blocks.append("<ul>" + "".join(f"<li>{inline(line[2:])}</li>" for line in lines) + "</ul>")
        else:
            blocks.append(f"<p>{inline(' '.join(lines))}</p>")
    return "".join(blocks)


def read_report(path):
    import json
    from datetime import datetime
    from zoneinfo import ZoneInfo
    data = json.loads(path.read_text(encoding="utf-8"))
    if data["schema_version"] != 1:
        raise ValueError("Unsupported report schema version")
    snapshot = datetime.fromisoformat(data["snapshot_at"])
    if snapshot.utcoffset() is None:
        raise ValueError("snapshot_at must include a UTC offset")
    snapshot = snapshot.astimezone(ZoneInfo(data["snapshot_timezone"]))
    meta = {key: data[key] for key in ("project", "report", "headline")}
    meta["updated"] = snapshot.strftime("%d %B %Y at %H:%M %Z")
    sections = {"Overview":data["summary"], "Release boundary":data["release_boundary"], "Limitations":data["limitations"]}
    evidence = {key:{"title":row["title"], "Observed":row["observed_at"], "Revision":row["revision"], "Source":row["source"], "Note":row["note"]} for key,row in data["evidence"].items()}
    for record in evidence.values():
        url(record["Source"])
    if not data["slices"]:
        raise ValueError("Add at least one slice")
    for key in ("project", "report", "headline", "summary", "release_boundary", "limitations"):
        if not isinstance(data[key], str) or not data[key].strip():
            raise ValueError("Expected nonempty text: " + key)
    for key, record in evidence.items():
        if not re.fullmatch(IDENTIFIER, key) or any(not isinstance(value, str) or not value.strip() for value in record.values()):
            raise ValueError("Invalid evidence record: " + key)
    ids = set()
    def identify(record):
        if not re.fullmatch(IDENTIFIER, record["id"]) or record["id"] in ids:
            raise ValueError("Invalid or duplicate ID: " + record["id"])
        if not isinstance(record["title"], str) or not record["title"].strip():
            raise ValueError("Expected record title")
        ids.add(record["id"])
    def checked(entry, allowed):
        if not isinstance(entry, dict) or set(entry) != {"status", "evidence_ids"} or not isinstance(entry["evidence_ids"], list):
            raise ValueError("States require status and evidence_ids")
        status, references = entry["status"], entry["evidence_ids"]
        if not isinstance(status, str) or status not in allowed:
            raise ValueError(f"Invalid state: {status!r}; expected one of {', '.join(sorted(allowed))}")
        if any(not isinstance(ref, str) or ref not in evidence for ref in references):
            raise ValueError(f"Unknown evidence reference in: {references!r}")
        if status in {"complete", "passed", "not-required", "published", "merged", "deployed"} and not references:
            raise ValueError(f"{status}: add an evidence_ids reference")
        return status, references
    slices = []
    for row in data["slices"]:
        identify(row)
        if not isinstance(row["acceptance_criteria"], str) or not row["acceptance_criteria"].strip():
            raise ValueError(f"{row['id']}: acceptance_criteria must be nonempty text")
        result = {"id":row["id"], "title":row["title"], "Closes":row["acceptance_criteria"], "accepted":checked(row["acceptance"], {"passed","pending","failed"}), "items":[]}
        for item in row["items"]:
            identify(item)
            if item["scope"] not in {"first-release","full-goal"}:
                raise ValueError("Invalid item scope")
            if set(item["states"]) != {key.lower().replace(" ", "_") for key in STATES}:
                raise ValueError("Each item needs exactly seven delivery states")
            for key in ("works", "remaining", "next_action"):
                if item[key] is not None and (not isinstance(item[key], str) or not item[key].strip()):
                    raise ValueError("Use text or null for " + key)
            states = {key: checked(item["states"][key.lower().replace(" ","_")], allowed) for key,allowed in STATES.items()}
            done = states["Implementation"][0] == "complete" and states["Publication"][0] == "published" and all(states[key][0] in {"passed","not-required"} for key in ("Local checks","Hosted checks"))
            result["items"].append({"id":item["id"], "title":item["title"], "Scope":item["scope"], "states":states, "done":done, "Works":item["works"], "Remaining":item["remaining"], "Next":item["next_action"]})
        if not result["items"] or result["accepted"][0] == "passed" and not all(item["done"] for item in result["items"]):
            raise ValueError("Invalid accepted or empty slice")
        slices.append(result)
    return meta, sections, slices, evidence


def badge(entry):
    status, references = entry
    colour = ("published" if status in {"complete", "passed", "published", "merged", "deployed"}
              else "missing" if status in {"failed", "not-started"}
              else "partial")
    links = " ".join(f'<a href="#evidence-{escape(ref)}">{escape(ref)}</a>' for ref in references)
    return f'<span class="badge {colour}">{LABELS[status]}</span> {links}'


def item_badge(item):
    states = {key: entry[0] for key, entry in item["states"].items()}
    if item["done"]:
        label, colour = "Published; checks passed", "published"
    elif states["Implementation"] != "complete" and states["Publication"] == "published":
        label, colour = "Partly implemented; published", "partial"
    elif states["Publication"] == "published":
        failed = any(states[key] == "failed" for key in ["Local checks", "Hosted checks"])
        label, colour = ("Published; checks failed", "missing") if failed else ("Published; checks pending", "partial")
    elif states["Local checks"] == "passed":
        label, colour = "Passing locally", "local"
    elif states["Implementation"] == "in-progress":
        label, colour = "In progress", "partial"
    elif states["Implementation"] == "complete":
        label, colour = "Implemented; checks remain", "partial"
    else:
        label, colour = "Not yet verified", "missing"
    return f'<span class="badge {colour}">{label}</span>'


def section(id_, title, body, kind="summary"):
    return f'<section class="{kind}" id="{id_}" aria-labelledby="{id_}-title"><h2 id="{id_}-title">{title}</h2>{body}</section>'


def render(path):
    meta, sections, slices, evidence = read_report(path)
    rows, cards, navigation, actions = [], [], [], []
    accepted = sum(slice_["accepted"][0] == "passed" for slice_ in slices)
    for number, slice_ in enumerate(slices, 1):
        items = slice_["items"]
        done = sum(item["done"] for item in items)
        local = sum(not item["done"] and item["states"]["Local checks"][0] == "passed" for item in items)
        progress = sum(not item["done"] and item["states"]["Implementation"][0] == "in-progress" for item in items)
        required = [item for item in items if item["Scope"] == "first-release"]
        release_done = sum(item["done"] for item in required)
        anchor = f"slice-{slice_['id']}"
        name = f"{number:02}. {escape(slice_['title'])}"
        link = f'<a href="#{anchor}">{name}</a>'
        navigation.append(link)
        rows.append(f'<tr><th scope="row">{link}</th><td data-label="Completed / full goal"><strong>{done}/{len(items)}</strong></td><td data-label="Additional locally passing">{local}</td><td data-label="In progress">{progress}</td><td data-label="Completed / first release">{release_done}/{len(required)}</td><td data-label="Whole-slice acceptance">{badge(slice_["accepted"])}</td></tr>')
        checklist = []
        for item in items:
            item_anchor = f"item-{item['id']}"
            delivery = "".join(f"<dt>{escape(key)}</dt><dd>{badge(entry)}</dd>" for key, entry in item["states"].items())
            scope = "Required for first release" if item["Scope"] == "first-release" else "Deferred from first release; retained in the full goal"
            score = "Earns one point" if item["done"] else "No completed point yet"
            notes = "".join(f'<p><strong>{label}:</strong> {inline(item[key])}</p>'
                            for key, label in [("Works", "What works"), ("Remaining", "Remaining work"), ("Next", "Next action")]
                            if item[key] is not None)
            refs = dict.fromkeys(ref for _, references in item["states"].values() for ref in references)
            links = " · ".join(f'<a href="#evidence-{escape(ref)}">{escape(ref)}</a>' for ref in refs)
            if links:
                notes += f'<p class="note">Evidence: {links}</p>'
            checklist.append(f'<tr id="{item_anchor}"><th scope="row">{escape(item["id"])}: {escape(item["title"])}<p class="note">{scope}</p></th><td>{item_badge(item)}<p class="note">{score}</p><details class="delivery-details"><summary>Delivery states</summary><dl class="delivery">{delivery}</dl></details></td><td>{notes}</td></tr>')
            if item["Remaining"] is not None or item["Next"] is not None:
                action_notes = "".join(f'<p><strong>{label}:</strong> {inline(item[key])}</p>' for key, label in [("Remaining", "Remaining work"), ("Next", "Next action")] if item[key] is not None)
                actions.append(f'<li><a href="#{item_anchor}">{escape(item["title"])}</a><span class="note"> · {scope}</span>{action_notes}</li>')
        checklist_table = '<div class="table-wrap"><table class="checklist"><thead><tr><th scope="col">Item</th><th scope="col">State</th><th scope="col">Evidence or remaining work</th></tr></thead><tbody>' + "".join(checklist) + '</tbody></table></div>'
        works = "".join(f'<li><strong>{escape(item["title"])}:</strong> {inline(item["Works"])}</li>' for item in items if item["Works"] is not None)
        remaining = "".join(f'<li><strong>{escape(item["title"])}:</strong> {inline(item["Remaining"])}</li>' for item in items if item["Remaining"] is not None)
        works = works or '<li>No working behaviour recorded yet.</li>'
        remaining = remaining or ('<li>Every named item earns a completed point.</li>' if done == len(items) else '<li>Unfinished items remain; see their delivery states. Remaining work has not been recorded.</li>')
        noun = "item" if len(items) == 1 else "items"
        cards.append(f'<section class="section slice-card" id="{anchor}" aria-labelledby="{anchor}-title"><div class="section-head"><div><span class="number">Slice {number:02}</span><h2 id="{anchor}-title">{escape(slice_["title"])}</h2></div><div class="slice-score">{done}/{len(items)}<small>completed items</small></div></div><progress value="{done}" max="{len(items)}" aria-label="{escape(slice_["title"])}: {done} of {len(items)} items complete"></progress><p class="note">{local} additional items pass locally · {progress} in progress.</p><p><strong>Whole-slice acceptance:</strong> {badge(slice_["accepted"])}</p><div class="slice-summary"><div><h3>What works</h3><ul>{works}</ul></div><div><h3>What remains</h3><ul>{remaining}</ul></div></div><div class="acceptance"><strong>What closes this slice</strong>{prose(slice_["Closes"])}</div><details class="checklist-details"><summary>Show all {len(items)} checklist {noun}</summary>{checklist_table}</details></section>')

    table = '<div class="table-wrap"><table class="score-table"><thead><tr><th scope="col">Slice</th><th scope="col">Completed / full goal</th><th scope="col">Additional locally passing</th><th scope="col">In progress</th><th scope="col">Completed / first release</th><th scope="col">Whole-slice acceptance</th></tr></thead><tbody>' + "".join(rows) + '</tbody></table></div>'
    scoring = '<details><summary>How scores work</summary><p>An item earns one point when implemented, published and its local and hosted checks have passed. A check marked “not required” needs evidence explaining why. Partial work earns no point. Deferred work stays in the full-goal count.</p><p>Items differ in size. Counts do not estimate effort, time remaining or release readiness. Whole-slice acceptance, merging and deployment are separate states.</p></details>'
    overview = section("overview", "At a glance", f'<p><strong>{accepted}/{len(slices)} whole slices accepted.</strong></p>' + table + scoring)
    boundary = section("release", "First release and the full goal", prose(sections["Release boundary"]))
    all_done = all(item["done"] for slice_ in slices for item in slice_["items"])
    empty_actions = '<p>Every named item earns a completed point. Check acceptance and deployment before a release decision.</p>' if all_done else '<p>Unfinished items remain. Next actions have not been recorded; see the slice checklists.</p>'
    next_actions = section("remaining", "Remaining work and next actions", '<ol class="route">' + "".join(actions) + '</ol>' if actions else empty_actions)
    records = "".join(f'<li id="evidence-{escape(id_)}"><strong>{escape(id_)} · {escape(record["title"])}</strong><p>Observed: {escape(record["Observed"])} · Revision: {escape(record["Revision"])}</p><p><a href="{url(record["Source"])}">Open evidence</a> · {inline(record["Note"])}</p></li>' for id_, record in evidence.items())
    sources = section("evidence", "Evidence and limitations", '<h3>Limitations</h3>' + prose(sections["Limitations"]) + '<details><summary>Source evidence</summary><ul>' + records + '</ul></details>', "evidence")
    nav = '<a href="#report">Overall position</a><a href="#overview">At a glance</a><a href="#release">First release and full goal</a><span class="nav-label">Slices</span>' + "".join(navigation) + '<span class="nav-label">Completion</span><a href="#remaining">Remaining work and next actions</a><a href="#evidence">Evidence and limitations</a>'
    return Template((ROOT / "assets/report.html").read_text(encoding="utf-8")).substitute(
        page_title=escape(f"{meta['project']} — {meta['report']}"), project=escape(meta["project"]), data_source=url(quote(path.name, safe="")),
        report_name=escape(meta["report"]), headline=escape(meta["headline"]), updated=escape(meta["updated"]),
        overview=prose(sections["Overview"]), styles="\n".join((ROOT / name).read_text(encoding="utf-8") for name in ["assets/report.css", "assets/checklist.css"]),
        navigation=nav, content=overview + boundary + "".join(cards) + next_actions + sources)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Authoritative JSON report")
    parser.add_argument("output", type=Path, nargs="?", help="Standalone HTML output")
    parser.add_argument("--check", action="store_true", help="Validate JSON and template rendering without writing HTML")
    args = parser.parse_args()
    if args.check and args.output is not None:
        parser.error("--check does not accept an output path")
    if not args.check and args.output is None:
        parser.error("provide an output path or use --check")
    try:
        if args.check:
            render(args.input)
            print(f"Valid report: {args.input}")
            return
        if args.input.resolve() == args.output.resolve():
            raise ValueError("Input and output must be different files")
        if args.input.parent.resolve() != args.output.parent.resolve():
            raise ValueError("Keep JSON and HTML in the same directory")
        document = render(args.input)
        args.output.write_text(document, encoding="utf-8")
    except (ValueError, OSError, KeyError, TypeError, AttributeError) as error:
        parser.exit(2, f"Cannot render report (check required JSON fields and types): {error}\n")
    print(f"Rendered {args.output}")


if __name__ == "__main__":
    main()
