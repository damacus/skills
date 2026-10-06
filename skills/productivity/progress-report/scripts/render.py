#!/usr/bin/env python3
"""Render the fixed progress-report Markdown format using only Python's standard library."""

import argparse
import html
import re
from pathlib import Path
from string import Template
from urllib.parse import urlsplit

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


def fields(lines, required, where):
    result = {}
    for line in lines:
        if not line.strip():
            continue
        key, separator, value = line.partition(": ")
        if not separator or key not in required or key in result or not value.strip():
            raise ValueError(f"{where}: unexpected, repeated or empty field: {line}")
        result[key] = value.strip()
    if set(result) != set(required):
        raise ValueError(f"{where}: missing fields: {', '.join(sorted(set(required) - set(result)))}")
    return result


def chunks(text, pattern):
    matches = list(re.finditer(pattern, text, re.M))
    if not matches or text[:matches[0].start()].strip():
        raise ValueError("Expected the documented headings")
    return [(match, text[match.end():matches[i + 1].start() if i + 1 < len(matches) else len(text)])
            for i, match in enumerate(matches)]


def read_report(path):
    text = path.read_text(encoding="utf-8")
    front = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not front:
        raise ValueError("Start with the documented metadata block")
    meta = fields(front[1].splitlines(), {"project", "report", "headline", "updated"}, "Metadata")
    sections = {}
    slices = []
    for heading, body in chunks(text[front.end():], r"^## (.+)\n"):
        title = heading[1]
        if title.startswith("Slice "):
            match = re.fullmatch(rf"Slice ({IDENTIFIER}) \| (.+)", title)
            if not match:
                raise ValueError(f"Invalid slice heading: {title}")
            blocks = chunks(body, r"^### (.+)\n")
            if blocks[0][0][1] != "Details":
                raise ValueError(f"{title}: first heading must be ### Details")
            detail = fields(blocks[0][1].splitlines(), {"Accepted", "Closes"}, title)
            items = []
            for item_heading, item_body in blocks[1:]:
                item_match = re.fullmatch(rf"({IDENTIFIER}) \| (.+)", item_heading[1])
                if not item_match:
                    raise ValueError(f"Invalid item heading: {item_heading[1]}")
                item = fields(item_body.splitlines(), {*STATES, "Scope", "Works", "Remaining", "Next"}, item_heading[1])
                item.update(id=item_match[1], title=item_match[2])
                items.append(item)
            if not items:
                raise ValueError(f"{title}: add named checklist items")
            slices.append(dict(id=match[1], title=match[2], items=items, **detail))
        elif title in sections:
            raise ValueError(f"Repeated section: {title}")
        else:
            sections[title] = body.strip()
    if set(sections) != {"Overview", "Release boundary", "Evidence", "Limitations"} or not slices:
        raise ValueError("Include Overview, Release boundary, at least one Slice, Evidence and Limitations")
    if any(not value for value in sections.values()):
        raise ValueError("Required sections must not be empty")
    evidence = {}
    for heading, body in chunks(sections["Evidence"], rf"^### ({IDENTIFIER}) \| (.+)\n"):
        if heading[1] in evidence:
            raise ValueError(f"Repeated evidence ID: {heading[1]}")
        evidence[heading[1]] = dict(title=heading[2], **fields(body.splitlines(), {"Observed", "Revision", "Source", "Note"}, heading[1]))
        url(evidence[heading[1]]["Source"])
    ids = set()
    for slice_ in slices:
        for record in [slice_, *slice_["items"]]:
            if record["id"] in ids:
                raise ValueError(f"Repeated slice/item ID: {record['id']}")
            ids.add(record["id"])
        slice_["accepted"] = state(slice_["Accepted"], {"passed", "pending", "failed"}, evidence)
        for item in slice_["items"]:
            if item["Scope"] not in {"first-release", "full-goal"}:
                raise ValueError(f"{item['id']}: Scope must be first-release or full-goal")
            item["states"] = {key: state(item[key], allowed, evidence) for key, allowed in STATES.items()}
            statuses = {key: entry[0] for key, entry in item["states"].items()}
            item["done"] = (statuses["Implementation"] == "complete"
                            and statuses["Publication"] == "published"
                            and all(statuses[key] in {"passed", "not-required"} for key in ["Local checks", "Hosted checks"]))
        if slice_["accepted"][0] == "passed" and not all(item["done"] for item in slice_["items"]):
            raise ValueError(f"{slice_['id']}: an accepted full slice must have every item complete")
    return meta, sections, slices, evidence


def state(value, allowed, evidence):
    parts = value.split()
    status = parts[0]
    references = [part[1:] for part in parts[1:] if part.startswith("@")]
    if status not in allowed or len(references) != len(parts) - 1:
        raise ValueError(f"Invalid state: {value}")
    if any(reference not in evidence for reference in references):
        raise ValueError(f"Unknown evidence reference in: {value}")
    if status in {"complete", "passed", "not-required", "published", "merged", "deployed"} and not references:
        raise ValueError(f"{value}: add an @evidence reference")
    return status, references


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
    rows, cards, actions, navigation = [], [], [], []
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
        rows.append(f"<tr><th scope=\"row\">{link}</th><td><strong>{done}/{len(items)}</strong></td><td>{local}</td><td>{progress}</td><td>{release_done}/{len(required)}</td><td>{badge(slice_['accepted'])}</td></tr>")
        checklist = []
        works = []
        for item in items:
            item_anchor = f"item-{item['id']}"
            if item["Works"] != "None":
                works.append(f"<li><strong>{escape(item['title'])}:</strong> {inline(item['Works'])}</li>")
            delivery = "".join(f"<dt>{escape(key)}</dt><dd>{badge(entry)}</dd>" for key, entry in item["states"].items())
            scope = "Required for first release" if item["Scope"] == "first-release" else "Deferred from first release; retained in the full goal"
            score = "Earns one point" if item["done"] else "No completed point yet"
            notes = "".join(f'<p><strong>{label}:</strong> {inline(item[key])}</p>'
                            for key, label in [("Works", "What works"), ("Remaining", "Remaining work"), ("Next", "Next action")]
                            if item[key] != "None")
            refs = dict.fromkeys(ref for _, references in item["states"].values() for ref in references)
            links = " · ".join(f'<a href="#evidence-{escape(ref)}">{escape(ref)}</a>' for ref in refs)
            if links:
                notes += f'<p class="note">Evidence: {links}</p>'
            checklist.append(f'<tr id="{item_anchor}"><th scope="row">{escape(item["id"])}: {escape(item["title"])}<p class="note">{scope}</p></th><td>{item_badge(item)}<p class="note">{score}</p><details class="delivery-details"><summary>Delivery states</summary><dl class="delivery">{delivery}</dl></details></td><td>{notes}</td></tr>')
            if item["Remaining"] != "None" or item["Next"] != "None":
                actions.append(f'<li><a href="#{item_anchor}">{escape(item["title"])}</a> — {inline(item["Remaining"])} <strong>Next:</strong> {inline(item["Next"])} <span class="note">({scope})</span></li>')
        remaining = "".join(f"<li><strong>{escape(item['title'])}:</strong> {inline(item['Remaining'])}</li>" for item in items if item["Remaining"] != "None")
        if not remaining:
            remaining = ("<li>Every named item earns a completed point.</li>" if done == len(items)
                         else "<li>Some checklist items remain unfinished. Remaining work has not been recorded; see their delivery states below.</li>")
        checklist_table = '<div class="table-wrap"><table class="checklist"><thead><tr><th scope="col">Item</th><th scope="col">State</th><th scope="col">Evidence or remaining work</th></tr></thead><tbody>' + "".join(checklist) + '</tbody></table></div>'
        cards.append(f'<section class="section slice-card" id="{anchor}" aria-labelledby="{anchor}-title"><div class="section-head"><div><span class="number">Slice {number:02}</span><h2 id="{anchor}-title">{escape(slice_["title"])}</h2></div><div class="slice-score">{done}/{len(items)}<small>completed checklist items</small></div></div><progress value="{done}" max="{len(items)}" aria-label="{escape(slice_["title"])}: {done} of {len(items)} items complete"></progress><p class="note">{local} additional items pass locally · {progress} items in progress.</p><p><strong>Whole-slice acceptance:</strong> {badge(slice_["accepted"])}</p><h3>What works</h3><ul>{"".join(works) or "<li>No working behaviour recorded yet.</li>"}</ul><h3>What remains</h3><ul>{remaining}</ul><div class="acceptance"><strong>What closes this slice</strong>{prose(slice_["Closes"])}</div><details><summary>Show all {len(items)} checklist items</summary>{checklist_table}</details></section>')
    scoring = '<p>An item earns one point when it is implemented, published and its recorded checks have passed. A check marked “not required” needs evidence explaining why. Partial progress earns no point. Every full-goal item stays in the denominator, including work deferred from first release.</p><p>Items differ in size. These scores must not be averaged into an overall percentage or used to estimate time remaining. Acceptance, merging and deployment are recorded separately in each checklist.</p>'
    table = '<div class="table-wrap"><table><thead><tr><th scope="col">Slice</th><th scope="col">Completed / full goal</th><th scope="col">Additional locally passing</th><th scope="col">In progress</th><th scope="col">Completed / first release</th><th scope="col">Whole-slice acceptance</th></tr></thead><tbody>' + "".join(rows) + '</tbody></table></div>'
    overview = section("overview", "The position at a glance", f'<p><strong>{accepted}/{len(slices)} whole slices accepted.</strong></p>' + table + scoring)
    boundary = section("release", "First release and the full goal", prose(sections["Release boundary"]))
    all_done = all(item["done"] for slice_ in slices for item in slice_["items"])
    empty_actions = ('<p>Every named item earns a completed point. Check the recorded acceptance and deployment states before making a release decision.</p>'
                     if all_done else '<p>Some checklist items remain unfinished. Remaining work and next actions have not been recorded; see the slice checklists for their delivery states.</p>')
    next_actions = section("remaining", "Remaining work and concrete next actions", '<ol class="route">' + "".join(actions) + '</ol>' if actions else empty_actions)
    records = "".join(f'<li id="evidence-{escape(id_)}"><strong>{escape(id_)} · {escape(record["title"])}</strong><p>Observed: {escape(record["Observed"])} · Revision: {escape(record["Revision"])}</p><p><a href="{url(record["Source"])}">Open evidence</a> · {inline(record["Note"])}</p></li>' for id_, record in evidence.items())
    sources = section("evidence", "Evidence and limitations", '<ul>' + records + '</ul><h3>Limitations</h3>' + prose(sections["Limitations"]), "evidence")
    nav = '<a href="#report">Overall position</a><a href="#overview">At a glance</a><a href="#release">First release and full goal</a><span class="nav-label">Slices</span>' + "".join(navigation) + '<span class="nav-label">Completion</span><a href="#remaining">Remaining work and next actions</a><a href="#evidence">Evidence and limitations</a>'
    return Template((ROOT / "assets/report.html").read_text(encoding="utf-8")).substitute(
        page_title=escape(f"{meta['project']} — {meta['report']}"), project=escape(meta["project"]),
        report_name=escape(meta["report"]), headline=escape(meta["headline"]), updated=escape(meta["updated"]),
        overview=prose(sections["Overview"]), styles="\n".join((ROOT / name).read_text(encoding="utf-8") for name in ["assets/report.css", "assets/checklist.css"]),
        navigation=nav, content=overview + boundary + "".join(cards) + next_actions + sources)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Structured Markdown report")
    parser.add_argument("output", type=Path, help="Standalone HTML output")
    args = parser.parse_args()
    try:
        document = render(args.input)
        if args.input.resolve() == args.output.resolve():
            raise ValueError("Input and output must be different files")
        args.output.write_text(document, encoding="utf-8")
    except (ValueError, OSError) as error:
        parser.exit(2, f"Cannot render report: {error}\n")
    print(f"Rendered {args.output}")


if __name__ == "__main__":
    main()
