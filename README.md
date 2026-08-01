# nruth633.github.io

Personal portfolio site — plain HTML, CSS, and vanilla JS. No build step, no
dependencies, no package manager. Edit a file, refresh the browser.

Live at <https://nruth633.github.io>

## Layout

```
index.html            home — hero, skills, featured projects, contact
projects.html         all projects, filterable by tech
resume.html           experience, education, skills, coursework
projects/             project deep-dives
css/style.css         the entire stylesheet
js/main.js            theme toggle, filtering, scroll reveal
assets/img/           photos and board renders
assets/resume.pdf     resume download (add this file)
```

## Editing

**Add a project.** Copy an existing `<li>` block in `projects.html`, change the
text, and set `data-tags` to any of `stm32 pcb controls matlab arduino`. The
filter buttons pick it up automatically — no JS changes needed.

**Add a photo.** Drop the image in `assets/img/`, then replace the placeholder

```html
<div class="card-media" data-placeholder="robot photo → assets/img/"></div>
```

with

```html
<div class="card-media">
  <img src="assets/img/robot.jpg" alt="Describe what's in the photo" />
</div>
```

Alt text matters — it's what screen readers announce and what shows if the image
fails to load.

**Change colours.** Every colour is a custom property at the top of
`css/style.css`, under `:root` for light and `:root[data-theme="dark"]` for dark.
Change them in those two places and the whole site follows.

## Still to fill in

Search the source for `TODO` — each one marks a spot with placeholder text:

- `resume.html` — Arsenal Nexus start date and the three experience bullets
- `index.html` — LinkedIn URL (commented out until you add it)
- `projects/*.html` — measured results and build details (each page lists
  exactly what would strengthen it)
- `assets/img/` — no photos yet; every project shows a placeholder block

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
