"""Shared loader for the resume source, so the phone number stays out of git.

`resume-src.html` is committed to a PUBLIC repo, so it carries a `{{PHONE}}`
placeholder rather than the number itself. The real number lives in
`tools/resume-private.json`, which is gitignored.

Two variants come out of the one source:

    load("full")  ->  placeholder replaced with the real number.
                      Needs resume-private.json. For direct applications.
    load("web")   ->  the whole <span class="phone"> element removed.
                      Needs nothing. This is what gets published.

Both `make-resume.py` and `resume-to-docx.py` go through here on purpose. They
generate different formats from the same source and have silently drifted apart
before, so the definition of each variant lives in exactly one place.
"""
import json
import os
import re

TOOLS = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(TOOLS, "resume-src.html")
PRIVATE = os.path.join(TOOLS, "resume-private.json")

PLACEHOLDER = "{{PHONE}}"
# the whole <span class="phone"> ... </span> element, separator and all
PHONE_SPAN = re.compile(r'<span class="phone">.*?</span>', re.S)


class MissingPrivateFile(RuntimeError):
    """resume-private.json is absent, so the full variant cannot be built."""


def read_source():
    with open(SRC, encoding="utf-8") as f:
        return f.read()


def phone():
    """The real number, from the gitignored private file."""
    if not os.path.exists(PRIVATE):
        raise MissingPrivateFile(
            f"{PRIVATE} not found.\n"
            "It is gitignored on purpose: the phone number must never be committed.\n"
            'Recreate it with a single line:  {"phone": "555-555-5555"}'
        )
    with open(PRIVATE, encoding="utf-8") as f:
        data = json.load(f)
    value = str(data.get("phone", "")).strip()
    if not value:
        raise MissingPrivateFile(f'{PRIVATE} has no non-empty "phone" key.')
    return value


def load(variant):
    """Return the source HTML for 'full' or 'web'."""
    html = read_source()
    if PLACEHOLDER not in html:
        raise RuntimeError(
            f"{SRC} no longer contains {PLACEHOLDER}. Refusing to guess where the "
            "phone number belongs -- restore the placeholder in the contact line."
        )

    if variant == "web":
        out = PHONE_SPAN.sub("", html)
        if PLACEHOLDER in out:
            raise RuntimeError(
                "the phone placeholder survived redaction -- the <span class=\"phone\"> "
                "wrapper in resume-src.html is malformed."
            )
        return out

    if variant == "full":
        return html.replace(PLACEHOLDER, phone())

    raise ValueError(f"unknown variant {variant!r} (expected 'full' or 'web')")
