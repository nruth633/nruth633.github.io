# nruth633.github.io

Personal portfolio site — plain HTML, CSS, and vanilla JS. No build step, no
dependencies, no package manager. Edit a file, refresh the browser.

Live at <https://nruth633.github.io>

## Layout

```
index.html            home — hero, skills, featured projects, contact
projects.html         all projects, filterable by tech
resume.html           experience, education, skills, coursework
404.html              not-found page (GitHub Pages serves this automatically)
projects/             project deep-dives
css/style.css         the entire stylesheet
js/main.js            theme toggle, filtering, scroll reveal
assets/img/           photos and board renders
assets/resume.pdf     resume download (add this file)
tools/                one-off generators; not part of the published site
```

## Editing

**Add a project.** Copy an existing `<li>` block in `projects.html`, change the
text, and set `data-tags` to any of `stm32 pcb controls matlab arduino`. The
filter buttons pick it up automatically — no JS changes needed.

**Add a photo.** Drop the image in `assets/img/` (≤ 1500 px on the long edge —
JPEG for photos and 3D renders, palette PNG for schematics and layouts), then:

```html
<div class="card-media">
  <img src="assets/img/robot.jpg" alt="Describe what's in the photo" />
</div>
```

Alt text matters — it's what screen readers announce and what shows if the image
fails to load.

Card images are cropped to fill a 16:9 frame. A full schematic sheet shrunk to
that size is unreadable, so for documents make a cropped detail for the card and
keep the whole sheet on the detail page (see `battery-tester-card.png` next to
`battery-tester-schematic.png`).

**Add a figure to a detail page.** Put `<figure class="figure">` *outside* the
`<div class="prose">` block — prose is capped at 68 characters for readability,
and a schematic squeezed into that column can't be read. Add `figure-tall` to
anything roughly square or taller so it doesn't swallow the viewport.

**Social preview.** Every page carries Open Graph tags. Project pages point at
their own lead image; home, projects, and resume share a generated card,
`assets/img/og-card-v2.png`, built by `tools/make-og-card.py`.

That card does **not** follow the stylesheet — the colours are baked into the
pixels. Change the site's look and the thumbnail keeps showing the old one until
the script is re-run:

```sh
python tools/make-og-card.py
```

Bump `VERSION` in the script and update the three `og:image` tags to match, then
delete the old file. Publishing under a *new filename* is the point: iMessage,
Slack, and LinkedIn cache previews keyed on the image URL, so overwriting the
same name leaves everyone looking at the stale thumbnail. To check a link
preview yourself before sharing it, append `?v=2` — that is a new URL to the
cache and the site serves identically.

**Change colours.** Every colour is a custom property at the top of
`css/style.css`, under `:root` for light and `:root[data-theme="dark"]` for dark.
Change them in those two places and the whole site follows.

## Still to fill in

No `TODO` markers or placeholder cards remain. Open questions that need you
rather than an edit:

- **LinkedIn** — no URL on the site. Add a button next to the email one in the
  contact section of `index.html` if you want it.
- **Balancing robot control loop** — the page describes the hardware but says
  nothing about the controller (PID? gains? loop rate? complementary filter on
  the IMU?). That's the most interesting part of the project and the biggest
  remaining gap on the site.
- **LPKF milling** — `index.html`'s "PCB design & fabrication" skill card claims
  custom footprints and drill specs for in-house LPKF milling. That claim used to
  hang off the battery tester, which never got past schematic, so it now has no
  project backing it. Either point it at the board it actually belongs to, or
  drop it.
- **IEEE board, SRCLR** — see the note below.

## A design issue worth checking

On the IEEE LED matrix board, pin 10 (`SRCLR`, the active-low shift-register
clear) carries a no-connect flag on all three 74HCT595s. That input wants to be
tied to VCC; left floating it can clear the registers spuriously, and a floating
CMOS input sits mid-rail and burns current. Worth a look before another slice is
fabricated. Nothing on the site claims the board is flawless, so there's no
correction needed there — this is just a heads-up.

## Image sources

Everything in `assets/img/` is Nic's own work — coursework documents, the
`arduino-shield-pcb` and `3-wheel-balancing-robot` repositories, and the FM
receiver course presentation — re-encoded for the web. Deliberately *excluded*,
because they weren't ours to publish: a stock photo of a naval railgun, a
textbook diagram of rail physics, and the Adafruit product shots of the DemoSat
sensors.

If you add photos, keep to that rule — your own work only.

## Before you publish

`assets/resume.pdf` contains your phone number. The site itself deliberately
shows email only, but the downloadable PDF does not — so pushing this publishes
the number. Either accept that, or put a phone-free version at
`assets/resume.pdf` and keep the full one for direct applications.

## Local preview

Open `index.html` in a browser. That's it.

For a stricter check that matches how GitHub Pages serves it:

```sh
python -m http.server 8000
# then open http://localhost:8000
```

## Deploying

Pushing to `main` publishes automatically via GitHub Pages (Settings → Pages →
Source: `main`, root). Live about a minute after the push.
