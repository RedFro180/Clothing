"""Build HTML + PDF for every tech pack in docs/ (docs/tech-pack-*.md).
Run: python3 tools/build_tech_packs.py
Needs python-markdown and Node Playwright (pre-installed here). Edit the .md files; this rebuilds the rest."""
import glob, os, re, subprocess, json
import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.normpath(os.path.join(HERE, "..", "docs"))
CSS = """@page { size: Letter; margin: 0.6in; }
body { font: 10.5pt/1.45 -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; color: #1a1714; }
h1 { font-size: 20pt; margin: 0 0 10px; border-bottom: 3px solid #1a1714; padding-bottom: 6px; }
h2 { font-size: 13.5pt; margin: 18px 0 6px; color: #8f2a25; page-break-after: avoid; }
table { border-collapse: collapse; width: 100%; margin: 6px 0 10px; page-break-inside: auto; }
tr { page-break-inside: avoid; }
th, td { border: 1px solid #b9b0a2; padding: 4px 6px; text-align: left; vertical-align: top; }
th { background: #ece6da; }
pre { background: #f4f0e8; border: 1px solid #ddd3c3; padding: 8px; font-size: 9.5pt; white-space: pre-wrap; }
hr { border: 0; border-top: 1px solid #ddd3c3; margin: 14px 0; }
li { margin: 2px 0; }"""

pages = []
for md in sorted(glob.glob(os.path.join(DOCS, "tech-pack-*.md"))):
    text = open(md).read()
    title = re.search(r"\(Style (\w+)\)", text)
    body = markdown.markdown(text, extensions=["tables", "fenced_code"])
    html = (f'<!DOCTYPE html><html><head><meta charset="utf-8"><title>Tech pack {title.group(1) if title else ""}</title>'
            f"<style>\n{CSS}\n</style></head><body>{body}</body></html>")
    out = md[:-3] + ".html"
    open(out, "w").write(html)
    pages.append([out, md[:-3] + ".pdf"])

js = """const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage();
  for (const [h, pdf] of %s) { await p.goto('file://' + h); await p.pdf({ path: pdf, format: 'Letter', printBackground: true }); }
  await b.close(); })();""" % json.dumps(pages)
subprocess.run(["node", "-e", js], check=True)
for h, pdf in pages:
    print(os.path.basename(pdf), os.path.getsize(pdf) // 1024, "KB")
