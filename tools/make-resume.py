#!/usr/bin/env python3
"""Build the resume PDFs from tools/resume-src.html.

Two variants come out of one source:

  assets/resume.pdf                  phone number stripped  (published)
  <desktop>/Nicolas_Ruth_Resume.pdf  phone number intact     (applications)

The redaction is done in code rather than by hand -- the old workflow exported
from Google Docs and redacted the export, so every re-export silently put the
phone number back.

The number is NOT in resume-src.html. That file is committed to a public repo,
so it carries a {{PHONE}} placeholder; the real number lives in the gitignored
tools/resume-private.json. See resume_source.py. The web variant needs no
private file at all, so a fresh clone can still build the published PDF.

It also *verifies* the result is one page and reports how much room is left, so
an edit that overflows fails loudly instead of quietly becoming a two-pager.
Tune the fit with the CSS custom properties at the top of resume-src.html
(--body, --lead, --gap-sec, --gap-entry, --bullet-gap).

Needs: Chrome (headless, for --print-to-pdf) and pymupdf (for verification).

    python tools/make-resume.py
"""
import os, re, shutil, subprocess, sys, tempfile

import resume_source

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = resume_source.SRC
WEB_OUT = os.path.join(ROOT, "assets", "resume.pdf")
FULL_OUT = os.path.join(os.path.expanduser("~"), "Desktop", "Nicolas_Ruth_Resume.pdf")

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome", "chromium",
]

def find_chrome():
    for c in CHROME_CANDIDATES:
        if os.path.sep in c or ":" in c:
            if os.path.exists(c):
                return c
        elif shutil.which(c):
            return shutil.which(c)
    sys.exit("Chrome not found -- add its path to CHROME_CANDIDATES.")


def render(chrome, html, out):
    """Render an HTML string to a PDF at `out`."""
    with tempfile.TemporaryDirectory() as td:
        page = os.path.join(td, "resume.html")
        with open(page, "w", encoding="utf-8") as f:
            f.write(html)
        subprocess.run([
            chrome, "--headless", "--disable-gpu", "--no-pdf-header-footer",
            "--run-all-compositor-stages-before-draw", "--virtual-time-budget=3000",
            f"--print-to-pdf={out}", "file:///" + page.replace("\\", "/"),
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


META = {
    "title": "Nicolas Ruth - Resume",
    "author": "Nicolas Ruth",
    "subject": "Electrical Engineering resume",
    "keywords": "electrical engineering, PCB design, KiCad, RF, embedded systems, STM32",
}


def stamp(path):
    """Chrome leaves its own producer metadata; give the file a real title so it
    shows up as a name, not a filename, in a recruiter's PDF viewer."""
    try:
        import fitz
    except ImportError:
        return
    doc = fitz.open(path)
    doc.set_metadata(META)
    tmp = path + ".tmp"
    doc.save(tmp)
    doc.close()
    os.replace(tmp, path)


def verify(path, label):
    """Assert one page; report the remaining room on it."""
    try:
        import fitz
    except ImportError:
        print(f"  {label}: pymupdf not installed, page count UNVERIFIED")
        return True
    doc = fitz.open(path)
    page = doc[0]
    bottoms = [b["bbox"][3] for b in page.get_text("dict")["blocks"] if b.get("lines")]
    end = max(bottoms) if bottoms else 0
    # bottom margin comes from the @page rule in the source
    margin_in = 0.34
    m = re.search(r"@page\s*\{[^}]*margin:\s*([\d.]+)in", open(SRC, encoding="utf-8").read())
    if m:
        margin_in = float(m.group(1))
    room = (page.rect.height - margin_in * 72) - end
    ok = doc.page_count == 1
    flag = "OK " if ok else "OVERFLOW"
    print(f"  {flag} {label}: {doc.page_count} page(s), {room:.0f}pt of room left")
    if ok and room < 8:
        print("       (that is very tight -- a font-metric shift could push it to two pages)")
    return ok


def main():
    chrome = find_chrome()

    # The published variant first: it needs no private file, so it always builds
    # -- a fresh clone of this repo can still produce the site's PDF.
    web = resume_source.load("web")
    print("Rendering:")
    render(chrome, web, WEB_OUT)
    stamp(WEB_OUT)
    ok = verify(WEB_OUT, f"redacted -> {WEB_OUT}")

    # The full variant carries the phone number, so it only builds when the
    # gitignored private file is present.
    try:
        full = resume_source.load("full")
    except resume_source.MissingPrivateFile as exc:
        print(f"\n  SKIP full variant -- {exc}")
        full = None
    else:
        # The guard compares against the value loaded at runtime, never a
        # literal, so this file never contains the number it is protecting.
        assert resume_source.phone() not in web, "phone survived the web redaction"
        render(chrome, full, FULL_OUT)
        stamp(FULL_OUT)
        ok &= verify(FULL_OUT, f"full     -> {FULL_OUT}")

    if not ok:
        sys.exit("\nResume no longer fits on one page. Tune the fit knobs in resume-src.html.")
    print("\nBuilt. `git add assets/resume.pdf` to publish the redacted one.")
    if full is None:
        print("The phone-bearing copy was NOT rebuilt -- restore tools/resume-private.json first.")


if __name__ == "__main__":
    main()
