"""Build the paper-selection page from configured solution content."""
from pathlib import Path
import html
import json
root=Path(__file__).resolve().parent.parent
from build_practice_page import PAPERS


def main() -> None:
    groups = [
        ("Mathematics Advanced", ["2026-maths-advanced", "2025-maths-advanced"]),
        ("Mathematics Extension 1", ["2025-maths-extension-1"]),
        ("Mathematics Extension 2", ["2026-maths-extension-2"]),
    ]
    cards = []
    for course, keys in groups:
        years = []
        for key in keys:
            paper = PAPERS[key]
            parts = json.loads(s=(root / "content" / f"{key}.json").read_text())
            note = '<p>2026 official paper not yet available.</p>' if key == "2025-maths-extension-1" else ""
            years.append(f'''<div class="paper-year"><h3>{paper["year"]} HSC exam</h3>{note}<p>{len({part["number"] for part in parts})} questions · {len(parts)} parts · {paper["total_marks"]} marks</p><a class="btn" href="{paper["slug"]}">Open {paper["year"]} solutions &rarr;</a></div>''')
        cards.append(f'''<article class="card"><h2>{html.escape(s=course)}</h2><p>Original worked solutions, topic filters and study timers.</p>{"".join(years)}</article>''')
    s='''<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>HSC Maths Past Paper Worked Solutions | Advanced &amp; Extension</title><meta name="description" content="Original HSC maths worked solutions for Advanced, Extension 1 and Extension 2. Filter by topic and track your study time."><link rel="canonical" href="https://hscmathstutor.com.au/practice/"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/styles.css?v=8"><link rel="stylesheet" href="/assets/practice/practice.css?v=1"><style>.paper-year + .paper-year { margin-top: 28px; padding-top: 24px; border-top: 1px solid #dde3ea; }</style></head><body><a class="skip-link" href="#papers">Skip to papers</a><header class="site-header"><div class="container nav"><a href="/" class="brand">Sachin Abeywardana <span>HSC Maths Tutoring</span></a><nav aria-label="Main"><a href="/practice/" aria-current="page">Past paper solutions</a><a href="/#contact" class="btn btn-small">Free trial lesson</a></nav></div></header><main><section class="section"><div class="container"><p class="eyebrow">Free HSC practice</p><h1>Past paper worked solutions</h1><p class="section-lead">Choose your course and year. Try the official questions, then reveal a short explanation when you’re ready. Filter by topic and track the time you spend reviewing.</p><p>Opening a solution starts its timer and pauses the previous one. Total study time adds up active time across the paper. Timers pause when you leave the tab and reset when the page reloads.</p><div class="card-grid" id="papers">'''+''.join(cards)+'''</div><p>These independently written solutions are unofficial. Each paper links to NESA’s original questions. For Extension 1, the 2025 paper is provided while the 2026 official paper is awaiting release.</p></div></section></main><footer class="site-footer"><div class="container footer-grid"><p>&copy; 2026 Sachin Abeywardana</p><p><a href="/">HSC Maths Tutoring</a></p></div></footer><script src="/site.js?v=8"></script></body></html>'''
    (root/'practice/index.html').write_text(s)


if __name__ == "__main__":
    main()
