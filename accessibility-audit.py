from pathlib import Path
from urllib.parse import urlsplit

from lxml import html


ROOT = Path(__file__).resolve().parent
issues = []
pages = sorted(ROOT.glob("*.html"))


def issue(page, message):
    issues.append(f"{page.name}: {message}")


for page in pages:
    source = page.read_text(encoding="utf-8")
    doc = html.fromstring(source)

    if doc.get("lang") != "en":
        issue(page, "missing or unexpected document language")
    if len(doc.xpath("//title[normalize-space()]")) != 1:
        issue(page, "must have exactly one nonempty title")
    if len(doc.xpath("//meta[@charset]")) != 1:
        issue(page, "must have one charset declaration")
    if len(doc.xpath("//meta[@name='viewport']")) != 1:
        issue(page, "must have a viewport declaration")
    if len(doc.xpath("//h1")) != 1:
        issue(page, "must have exactly one h1")
    for landmark in ("nav", "main", "footer"):
        if len(doc.xpath(f"//{landmark}")) != 1:
            issue(page, f"must have exactly one {landmark} landmark")

    skip_links = doc.xpath(
        "//a[@href='#main-content' and "
        "contains(concat(' ', normalize-space(@class), ' '), ' skip-link ')]"
    )
    if len(skip_links) != 1:
        issue(page, "missing the main-content skip link")
    targets = doc.xpath("//*[@id='main-content']")
    if len(targets) != 1:
        issue(page, "missing or duplicate main-content target")

    ids = [value for value in doc.xpath("//*[@id]/@id") if value]
    duplicates = sorted({value for value in ids if ids.count(value) > 1})
    if duplicates:
        issue(page, f"duplicate IDs: {', '.join(duplicates)}")

    for image in doc.xpath("//img"):
        if "alt" not in image.attrib:
            issue(page, f"image missing alt: {image.get('src', '(no src)')}")
    for frame in doc.xpath("//iframe"):
        if not (frame.get("title") or "").strip():
            issue(page, "iframe missing a descriptive title")

    for anchor in doc.xpath("//a[@href]"):
        name = (anchor.get("aria-label") or " ".join(anchor.itertext())).strip()
        image_alts = " ".join(anchor.xpath(".//img/@alt")).strip()
        if not name and not image_alts:
            issue(page, f"link has no accessible name: {anchor.get('href')}")
        if anchor.get("target") == "_blank":
            rel = set((anchor.get("rel") or "").split())
            if "noopener" not in rel:
                issue(page, f"new-tab link missing noopener: {anchor.get('href')}")
            if "opens in a new tab" not in (anchor.get("aria-label") or "").lower():
                issue(page, f"new-tab link does not announce behavior: {anchor.get('href')}")

    for node in doc.xpath("//*[@tabindex]"):
        try:
            if int(node.get("tabindex")) > 0:
                issue(page, "positive tabindex changes the natural focus order")
        except ValueError:
            issue(page, f"invalid tabindex value: {node.get('tabindex')}")

    headings = []
    for heading in doc.xpath("//h1|//h2|//h3|//h4|//h5|//h6"):
        headings.append(int(heading.tag[1]))
    for previous, current in zip(headings, headings[1:]):
        if current > previous + 1:
            issue(page, f"heading level skips from h{previous} to h{current}")

    for section in doc.xpath("//section"):
        if not section.xpath(".//h2|.//h3|.//h4|.//h5|.//h6"):
            issue(page, "section has no heading")

    for details in doc.xpath("//details"):
        if len(details.xpath("./summary")) != 1:
            issue(page, "details element must have one direct summary")

    for table in doc.xpath("//table"):
        if len(table.xpath("./caption[normalize-space()]")) != 1:
            issue(page, "table must have one nonempty caption")
        if table.xpath(".//thead//th[not(@scope='col')]"):
            issue(page, "column header missing scope=col")
        if table.xpath(".//tbody/tr/th[1][not(@scope='row')]"):
            issue(page, "row header missing scope=row")
        wrap = table.getparent()
        if wrap is None or "table-wrap" not in (wrap.get("class") or "").split():
            issue(page, "table is not inside a table-wrap region")
        elif not (
            wrap.get("tabindex") == "0"
            and wrap.get("role") == "region"
            and (wrap.get("aria-label") or "").strip()
        ):
            issue(page, "table-wrap needs focusability, region role, and label")

    for node in doc.xpath("//*[@href] | //*[@src]"):
        attribute = "href" if node.get("href") is not None else "src"
        value = node.get(attribute)
        parsed = urlsplit(value)
        if parsed.scheme or value.startswith(("#", "mailto:", "tel:")):
            continue
        local_path = parsed.path
        if local_path and not (page.parent / local_path).resolve().exists():
            issue(page, f"broken local {attribute}: {value}")

    if 'scope="col"ead' in source:
        issue(page, "malformed thead markup")

css = (ROOT / "assets" / "styles.css").read_text(encoding="utf-8")
for required in (
    ".skip-link",
    ":focus-visible",
    "@media (prefers-reduced-motion: reduce)",
    "text-decoration-line: underline",
):
    if required not in css:
        issues.append(f"assets/styles.css: missing required rule {required}")

print(f"Audited {len(pages)} HTML pages.")
if issues:
    print(f"Found {len(issues)} issue(s):")
    for item in issues:
        print(f"- {item}")
    raise SystemExit(1)
print("No issues found by the source-level accessibility audit.")
