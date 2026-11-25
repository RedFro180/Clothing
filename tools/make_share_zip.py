"""Make a private, link-only copy of the shop to show a friend.

    python3 tools/make_share_zip.py [output.zip]

Copies ONLY site/ (shop page, scripts, pictures, fonts). Nothing else from the project goes in:
no research, costs, tech pack, designs, tools or notes. In the copy (not in site/ itself) it tells
search engines and AI crawlers not to index, list or archive it, so only people with the link find it.
Upload the zip at Cloudflare: Workers & Pages > Create > Pages > Upload assets.
Not a lock: anyone who has the link can open and forward it. See docs/owner-guide.md.
"""
import pathlib, re, shutil, sys, tempfile, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "site-share.zip"
NOINDEX = "noindex, nofollow, noarchive, noai, noimageai"

with tempfile.TemporaryDirectory() as tmp:
    dst = pathlib.Path(tmp) / "site"
    shutil.copytree(SITE, dst)
    # 1. page tag: don't index / list / archive
    html = (dst / "index.html").read_text()
    html, n = re.subn(r'<meta name="robots" content="[^"]*">', f'<meta name="robots" content="{NOINDEX}">', html)
    if n != 1:
        sys.exit("index.html: robots meta tag not found; not making the zip.")
    (dst / "index.html").write_text(html)
    # 2. every response: same instruction as a header (Cloudflare Pages reads _headers)
    hdr = (dst / "_headers").read_text()
    hdr, n = re.subn(r"X-Robots-Tag: [^\n]*", f"X-Robots-Tag: {NOINDEX}", hdr)
    if n != 1:
        sys.exit("_headers: X-Robots-Tag line not found; not making the zip.")
    (dst / "_headers").write_text(hdr)
    # 3. robots.txt: no crawler may read any page
    (dst / "robots.txt").write_text("# Private preview: not for search engines or AI crawlers.\nUser-agent: *\nDisallow: /\n")
    # zip with index.html at the top level
    OUT.unlink(missing_ok=True)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(dst.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(dst).as_posix())
    count = sum(1 for f in dst.rglob("*") if f.is_file())
print(f"Made {OUT} ({OUT.stat().st_size // 1024} KB, {count} files). Only site/ is inside; marked noindex.")
