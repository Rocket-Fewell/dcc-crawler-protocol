#!/home/box/.venvs/corebook/bin/python
"""Core Rulebook build: markdown -> HTML -> PDF (headless Chrome).

Usage: build/build.py [--version 0.1] [--html-only]
Reads  chapters/*.md (numeric prefix = book order), assets/css/book.css, assets/img/*
Writes build/book.html (intermediate), build/dcc-core-rulebook-v<ver>.pdf, build/pages.json
Two passes: pass 1 renders with placeholder TOC page numbers; pass 2 fills the real numbers
(found with pdftotext) and re-renders. Never hand edit anything in build/ except this script.
"""
import argparse, html, json, os, re, subprocess, sys, shutil
import markdown

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CH_DIR = os.path.join(ROOT, "chapters")
CSS = os.path.join(ROOT, "assets", "css", "book.css")
BOOK_TITLE = "Crawler Protocol: Season Zero"
BOOK_SUB = "Core Rulebook"

BOX_KINDS = {"system", "sidebar", "house", "inspired", "provisional", "readaloud", "cols2", "keep", "sheet"}


def inline_md(text):
    out = markdown.markdown(text.strip(), extensions=["smarty"])
    out = re.sub(r"^<p>|</p>$", "", out.strip())
    return out


def shortcodes(src):
    src = re.sub(r"\[VERIFY(?::\s*([^\]]*))?\]",
                 lambda m: '<span class="verify">VERIFY%s</span>' % ((": " + m.group(1)) if m.group(1) else ""), src)
    src = src.replace("{{HOUSE}}", '<span class="tag house">House</span>')
    src = src.replace("{{INSPIRED}}", '<span class="tag inspired">Inspired</span>')
    src = src.replace("{{PROVISIONAL}}", '<span class="tag provisional">Provisional</span>')
    return src


def preprocess_blocks(src):
    """Convert ::: kind Title ... ::: fenced blocks into HTML wrappers (md_in_html)."""
    lines = src.split("\n")
    out, i = [], 0
    while i < len(lines):
        m = re.match(r"^:::\s*(\w+)\s*(.*)$", lines[i])
        if not m:
            out.append(lines[i]); i += 1; continue
        kind, title = m.group(1), m.group(2).strip()
        body = []
        i += 1
        while i < len(lines) and lines[i].strip() != ":::":
            body.append(lines[i]); i += 1
        i += 1  # closing :::
        text = "\n".join(body).strip("\n")
        if kind == "achievement":
            paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
            reward = ""
            desc = []
            for p in paras:
                if p.lower().startswith("reward:"):
                    reward = p[len("reward:"):].strip()
                else:
                    desc.append(p)
            out.append('<div class="box achievement"><div class="ach-banner">New achievement!</div><div class="ach-body">'
                       '<div class="ach-title">%s</div>' % inline_md(title))
            for d in desc:
                out.append('<p class="ach-desc">%s</p>' % inline_md(d))
            out.append('<p class="ach-reward"><b>REWARD</b> %s</p></div></div>' % inline_md(reward))
            out.append("")
        elif kind == "epigraph":
            by = ""
            if title:
                by = '<span class="by">%s</span>' % html.escape(title)
            out.append('<div class="epigraph">%s%s</div>' % (inline_md(text), by))
            out.append("")
        elif kind in BOX_KINDS:
            cls = "box " + kind if kind not in ("cols2", "keep") else kind
            out.append('<div class="%s" markdown="1">' % cls)
            if title:
                out.append('<div class="box-title">%s</div>' % html.escape(title))
            out.append("")
            out.append(text)
            out.append("")
            out.append("</div>")
            out.append("")
        else:
            raise SystemExit("unknown block kind: " + kind)
    return "\n".join(out)


def render_md(src, ch_id):
    src = shortcodes(preprocess_blocks(src))
    md = markdown.Markdown(extensions=["tables", "attr_list", "md_in_html", "sane_lists", "smarty", "toc"],
                           extension_configs={"toc": {"slugify": lambda v, s: ch_id + "-" + re.sub(r"[^a-z0-9]+", "-", v.lower()).strip("-")}})
    body = md.convert(src)
    return body


def read_chapters():
    files = sorted(f for f in os.listdir(CH_DIR) if f.endswith(".md") and re.match(r"\d\d-", f))
    chapters = []
    for f in files:
        with open(os.path.join(CH_DIR, f), encoding="utf-8") as fh:
            raw = fh.read()
        # strip the file header block (lines before the first '---' line that starts the content) - header = first lines until a line == '<!-- BEGIN -->'
        if "<!-- BEGIN -->" in raw:
            raw = raw.split("<!-- BEGIN -->", 1)[1]
        chapters.append((f, raw))
    return chapters


def pyramid_svg():
    """Inverted pyramid of 18 floors: wide top, narrow bottom. Stairwell notches shrink toward the tip."""
    W, H = 560, 420
    layers = 18
    top_w, bot_w = 520, 14
    x0 = W / 2
    y_top, y_bot = 10, H - 6
    lh = (y_bot - y_top) / layers
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W, H, W, H)]
    for i in range(layers):
        t0, t1 = i / layers, (i + 1) / layers
        w0 = top_w + (bot_w - top_w) * t0
        w1 = top_w + (bot_w - top_w) * t1
        y0 = y_top + i * lh
        y1 = y0 + lh - 2.5
        # color ramps from steel-grey to hot orange toward the bottom
        r = int(60 + (232 - 60) * t0); g = int(66 + (83 - 66) * t0); b = int(82 + (26 - 82) * t0)
        pts = "%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" % (x0 - w0 / 2, y0, x0 + w0 / 2, y0, x0 + w1 / 2, y1, x0 - w1 / 2, y1)
        parts.append('<polygon points="%s" fill="rgb(%d,%d,%d)" fill-opacity="0.92" stroke="#0f1015" stroke-width="0.8"/>' % (pts, r, g, b))
        if i < layers - 1:
            # stairwell marker: smaller and rarer toward the bottom
            n = max(1, int(round(9 * (1 - t0) ** 1.6)))
            span = (w0 + w1) / 2 - 40
            for k in range(n):
                cx = x0 - span / 2 + span * (k + 0.5) / n
                parts.append('<rect x="%.1f" y="%.1f" width="5" height="%.1f" fill="#fbf7ee" fill-opacity="0.85"/>' % (cx - 2.5, y0 + 4, lh - 10))
    parts.append("</svg>")
    return "".join(parts)


def cover_html(version):
    return f"""
<section class="cover">
  <div class="kicker">Season Zero</div>
  <div class="art">{pyramid_svg()}</div>
  <h1 class="cover-title">Crawler Protocol<span>Core Rulebook</span></h1>
  <div class="subtitle">Eighteen floors. Fewer ways down each time.<br>A tabletop RPG of the Crawl, built on the 5e (2024) System Reference Document.</div>
  <div class="byline"><b>Valtay Corp</b> &nbsp;·&nbsp; Draft v{version} &nbsp;·&nbsp; Chapters 1, 2 &amp; 4</div>
</section>
"""


def build_html(chapters, version, toc_pages=None, return_meta=False):
    toc_pages = toc_pages or {}
    css = open(CSS, encoding="utf-8").read()
    named_css = []
    sections = []
    toc_entries = []   # (level, id, number, title)
    for idx, (fname, raw) in enumerate(chapters):
        m = re.match(r"(\d\d)-", fname)
        num = int(m.group(1))
        is_front = (num == 0)
        ch_id = "ch%d" % num if not is_front else "front"
        body = render_md(raw, ch_id)
        title_m = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
        title = re.sub(r"<[^>]+>", "", title_m.group(1)).strip() if title_m else fname
        title = html.unescape(title)
        if is_front:
            sections.append('<section class="frontmatter" id="front">%s</section>' % body)
            continue
        # decorate h1 with data-num and id
        body = re.sub(r"<h1([^>]*)>", lambda mm: '<h1 id="%s-top" data-num="%s"%s>' % (ch_id, num_words(num), mm.group(1)), body, count=1)
        body = body.replace('data-num="%s" data-num="%s"' % (num_words(num), num_words(num)), 'data-num="%s"' % num_words(num))
        toc_entries.append((1, ch_id + "-top", num, title))
        for hm in re.finditer(r'<h2 id="([^"]+)">(.*?)</h2>', body, re.S):
            toc_entries.append((2, hm.group(1), num, html.unescape(re.sub(r"<[^>]+>", "", hm.group(2))).strip()))
        sections.append('<section class="chapter ch%d" id="%s" style="page: ch%d">%s</section>' % (num, ch_id, num, body))
        short = title.upper()
        named_css.append(f"""
@page ch{num}:left {{
  @top-left {{ content: "CRAWLER PROTOCOL: SEASON ZERO"; font-family: "Barlow Condensed"; font-size: 8.5pt; letter-spacing: 0.22em; color: #8a8497; border-bottom: 1px solid #d9cfb4; padding-bottom: 4pt; width: 100%; vertical-align: bottom; }}
  @bottom-left {{ content: counter(page); font-family: "Barlow Condensed"; font-weight: 700; font-size: 10pt; color: #2b2f3a; }}
  @bottom-center {{ content: "DRAFT v{version}"; font-family: "Barlow Condensed"; font-size: 7.5pt; letter-spacing: 0.25em; color: #b4ad9b; }}
}}
@page ch{num}:right {{
  @top-right {{ content: "{short}"; font-family: "Barlow Condensed"; font-size: 8.5pt; letter-spacing: 0.22em; color: #8a8497; border-bottom: 1px solid #d9cfb4; padding-bottom: 4pt; width: 100%; text-align: right; vertical-align: bottom; }}
  @bottom-right {{ content: counter(page); font-family: "Barlow Condensed"; font-weight: 700; font-size: 10pt; color: #2b2f3a; }}
  @bottom-center {{ content: "DRAFT v{version}"; font-family: "Barlow Condensed"; font-size: 7.5pt; letter-spacing: 0.25em; color: #b4ad9b; }}
}}
""")
    # front matter toc
    toc = ['<section class="toc"><h1 class="toc-title">Contents</h1><ol>']
    toc.append('<li class="l0"><span class="t">Front Matter</span><span class="dots"></span><span class="pg">%s</span></li>' % toc_pages.get("front", "0"))
    for level, hid, num, title in toc_entries:
        pg = toc_pages.get(hid, "0")
        if level == 1:
            toc.append('<li class="l1"><span class="num">%d</span><span class="t">%s</span><span class="dots"></span><span class="pg">%s</span></li>' % (num, html.escape(title), pg))
        else:
            toc.append('<li class="l2"><span class="t">%s</span><span class="dots"></span><span class="pg">%s</span></li>' % (html.escape(title), pg))
    toc.append("</ol></section>")
    named_css.append("""
@page toc:left { @top-left { content: "CRAWLER PROTOCOL: SEASON ZERO"; font-family: "Barlow Condensed"; font-size: 8.5pt; letter-spacing: 0.22em; color: #8a8497; } @bottom-left { content: counter(page); font-family: "Barlow Condensed"; font-weight: 700; font-size: 10pt; } }
@page toc:right { @top-right { content: "CONTENTS"; font-family: "Barlow Condensed"; font-size: 8.5pt; letter-spacing: 0.22em; color: #8a8497; } @bottom-right { content: counter(page); font-family: "Barlow Condensed"; font-weight: 700; font-size: 10pt; } }
@page frontmatter:left { @bottom-left { content: counter(page); font-family: "Barlow Condensed"; font-weight: 700; font-size: 10pt; } }
@page frontmatter:right { @bottom-right { content: counter(page); font-family: "Barlow Condensed"; font-weight: 700; font-size: 10pt; } }
""")
    doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>{BOOK_TITLE} - {BOOK_SUB} v{version}</title>
<style>{css}</style><style id="named-pages">{''.join(named_css)}</style></head>
<body>
{cover_html(version)}
{''.join(s for s in sections if 'class="frontmatter"' in s)}
{''.join(toc)}
{''.join(s for s in sections if 'class="chapter' in s)}
</body></html>"""
    if return_meta:
        return doc, toc_entries
    return doc


NUM_WORDS = ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen"]
def num_words(n):
    return NUM_WORDS[n] if n < len(NUM_WORDS) else str(n)


def chrome_pdf(html_path, pdf_path):
    cmd = ["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage",
           "--no-pdf-header-footer", "--run-all-compositor-stages-before-draw", "--virtual-time-budget=20000",
           "--print-to-pdf=" + pdf_path, "file://" + html_path]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if not os.path.exists(pdf_path):
        raise SystemExit("chrome failed:\n" + r.stderr[-2000:])


def pdf_pages_text(pdf_path):
    n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", pdf_path], capture_output=True, text=True).stdout).group(1))
    pages = []
    for p in range(1, n + 1):
        t = subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), "-layout", pdf_path, "-"], capture_output=True, text=True).stdout
        pages.append(t)
    return pages


def norm(s):
    s = html.unescape(s)
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"').replace("\u2013", "-").replace("\u2014", "-")
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def locate(pages, entries):
    """entries: list of (level, id, num, title). Returns {id: page_number(1-based)}.
    Compares with all spaces removed because letter-spaced headings can extract with gaps."""
    found = {}
    def ns(s):
        return re.sub(r"\s+", "", norm(s))
    first_chapter_page = 0
    for i, t in enumerate(pages):
        if i >= 2 and re.search(r"C\s?H\s?A\s?P\s?T\s?E\s?R\s+O\s?N\s?E", t):
            first_chapter_page = i
            break
    cursor = first_chapter_page
    for level, hid, num, title in entries:
        key = ns(title)[:34]
        hit = None
        for i in range(cursor, len(pages)):
            for l in pages[i].split("\n"):
                nl = ns(l)
                if nl and len(nl) >= 5 and (nl == key or (len(key) >= 10 and nl.startswith(key)) or (len(nl) >= 10 and key.startswith(nl) and len(nl) >= 0.6 * len(key))):
                    hit = i
                    break
            if hit is not None:
                break
        if hit is None:
            print("WARN: heading not found in PDF:", title, file=sys.stderr)
            hit = cursor
        found[hid] = hit + 1
        cursor = hit
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", default="0.1")
    ap.add_argument("--html-only", action="store_true")
    a = ap.parse_args()
    chapters = read_chapters()
    out_html = os.path.join(ROOT, "build", "book.html")
    out_pdf = os.path.join(ROOT, "build", "dcc-core-rulebook-v%s.pdf" % a.version)
    tmp_pdf = os.path.join(ROOT, "build", ".pass1.pdf")
    doc, entries = build_html(chapters, a.version, return_meta=True)
    open(out_html, "w", encoding="utf-8").write(doc)
    if a.html_only:
        return
    chrome_pdf(out_html, tmp_pdf)
    pages = pdf_pages_text(tmp_pdf)
    found = locate(pages, entries)
    # front matter page = first page after cover that carries the copyright title
    front_page = 2
    for i, t in enumerate(pages):
        if "Legal" in t and ("SRD" in t or "System Reference" in t):
            front_page = i + 1
            break
    found["front"] = front_page
    doc2, _ = build_html(chapters, a.version, toc_pages=found, return_meta=True)
    open(out_html, "w", encoding="utf-8").write(doc2)
    chrome_pdf(out_html, out_pdf)
    pages2 = pdf_pages_text(out_pdf)
    found2 = locate(pages2, entries)
    if any(found2[k] != found[k] for k in found2):
        # TOC length changed layout (unlikely): one more pass
        found2["front"] = found["front"]
        doc3, _ = build_html(chapters, a.version, toc_pages=found2, return_meta=True)
        open(out_html, "w", encoding="utf-8").write(doc3)
        chrome_pdf(out_html, out_pdf)
        pages2 = pdf_pages_text(out_pdf)
        found2 = locate(pages2, entries)
        found = found2
    else:
        found = found2
    # per-chapter page counts
    ch_starts = [(hid, found[hid], title, num) for (lvl, hid, num, title) in entries if lvl == 1]
    total = len(pages2)
    stats = []
    for i, (hid, start, title, num) in enumerate(ch_starts):
        end = (ch_starts[i + 1][1] - 1) if i + 1 < len(ch_starts) else total
        stats.append({"chapter": num, "title": title, "start": start, "end": end, "pages": end - start + 1})
    meta = {"total_pages": total, "chapters": stats, "toc": found}
    json.dump(meta, open(os.path.join(ROOT, "build", "pages.json"), "w"), indent=1)
    if os.path.exists(tmp_pdf):
        os.remove(tmp_pdf)
    print(json.dumps(meta, indent=1))


if __name__ == "__main__":
    main()
