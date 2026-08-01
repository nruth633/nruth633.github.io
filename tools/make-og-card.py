#!/usr/bin/env python3
"""Generate the site's social-preview card (assets/img/og-card-*.png).

This is the image that shows as the thumbnail when the site is linked in
iMessage, Slack, LinkedIn, and so on. It is a *generated* image, so it does not
follow the stylesheet — if the site's colours change, this has to be re-run or
the preview keeps showing the old look.

    python tools/make-og-card.py

Two things to know before running it:

1. Bump VERSION and update the three <meta property="og:image"> tags to match.
   Scrapers cache previews keyed on the image URL, so overwriting the same
   filename leaves everyone looking at the old thumbnail — sometimes for weeks.
   A new filename is the only reliable way to force a refetch. Delete the old
   file once the tags point at the new one.

2. Keep ACCENT in step with --accent in css/style.css (dark theme) and the
   bolt in favicon.svg.

Needs Pillow: pip install pillow
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

VERSION = 2

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img", f"og-card-v{VERSION}.png")

# --- palette: mirrors the dark theme in css/style.css ---
BG = (16, 18, 22)  # --bg
RAISED = (24, 27, 33)  # --bg-raised
TEXT = (232, 233, 236)  # --text
SOFT = (164, 169, 180)  # --text-soft
ACCENT = (156, 163, 175)  # --accent  (#9ca3af, same grey as the favicon bolt)
BORDER = (38, 42, 50)  # --border
GRID = (20, 23, 28)

W, H = 1200, 630  # the size every scraper expects
PAD = 78

# --- content ---
BRAND = "> nic ruth"
NAME = "Nicolas Ruth"
LINES = [
    "Electrical Engineering · University of Denver",
    "Power electronics · PCB design · RF · Embedded systems",
]
CHIPS = ["330 J capacitor bank", "KiCad", "STM32", "R-2R DAC", "VNA"]
URL = "nruth633.github.io"

# Segoe UI and Consolas ship with Windows. On another OS, point these at any
# sans and any monospace face.
FONT_DIRS = ["C:\\Windows\\Fonts", "/usr/share/fonts", "/Library/Fonts"]
SANS_BOLD, SANS, MONO, MONO_BOLD = "segoeuib.ttf", "segoeui.ttf", "consola.ttf", "consolab.ttf"


def font(name, size):
    for d in FONT_DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    sys.exit(f"Font not found: {name}. Looked in {FONT_DIRS}. Edit FONT_DIRS above.")


def main():
    f_name = font(SANS_BOLD, 82)
    f_line = font(SANS, 33)
    f_mono = font(MONO, 27)
    f_brand = font(MONO_BOLD, 29)

    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)

    # faint grid, like a schematic sheet
    for x in range(0, W, 40):
        d.line([(x, 0), (x, H)], fill=GRID)
    for y in range(0, H, 40):
        d.line([(0, y), (W, y)], fill=GRID)

    d.rectangle([0, 0, 8, H], fill=ACCENT)  # accent rule down the left edge

    d.text((PAD, 92), BRAND, font=f_brand, fill=ACCENT)
    d.text((PAD, 168), NAME, font=f_name, fill=TEXT)
    for i, line in enumerate(LINES):
        d.text((PAD, 286 + i * 50), line, font=f_line, fill=SOFT)

    x, y = PAD, 470
    for c in CHIPS:
        w = d.textlength(c, font=f_mono) + 40
        d.rounded_rectangle([x, y, x + w, y + 54], radius=27, fill=RAISED, outline=BORDER)
        d.text((x + 20, y + 14), c, font=f_mono, fill=SOFT)
        x += w + 14

    d.text((PAD, 566), URL, font=f_mono, fill=ACCENT)

    im.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT}  ({os.path.getsize(OUT) // 1024} KB, {W}x{H})")
    print("reminder: og:image tags in index.html, projects.html, and resume.html "
          f"must point at og-card-v{VERSION}.png")


if __name__ == "__main__":
    main()
