"""Build the 2025 Advanced practice page from original solution content."""

import html
import json
import math
import pathlib
import subprocess
from collections.abc import Callable
from typing import NotRequired, TypedDict

ROOT = pathlib.Path(__file__).resolve().parent.parent
SLUG = "/practice/2025-maths-advanced/"
PAPER = "https://www.nsw.gov.au/sites/default/files/noindex/2025-10/2025-hsc-maths-advanced.pdf"
PACK = "https://www.nsw.gov.au/education-and-training/nesa/curriculum/hsc-exam-papers/mathematics-advanced/2025"


class Part(TypedDict):
    number: int
    part: str
    marks: int
    page: int
    title: str
    tags: list[str]
    steps: list[str]
    answer: str
    figure: NotRequired[str]


def _escape(*, text: str) -> str:
    return html.escape(s=text, quote=True)


def _render_texts(*, parts: list[Part]) -> dict[str, str]:
    texts = list(dict.fromkeys(text for part in parts for text in [*part["steps"], part["answer"]]))
    result = subprocess.run(
        args=["node", str(ROOT / "tools/render_math.cjs")],
        input=json.dumps(obj=texts), text=True, capture_output=True, check=True,
    )
    return dict(zip(texts, json.loads(s=result.stdout), strict=True))


def _part_id(*, part: Part) -> str:
    return f'q{part["number"]}{part["part"]}'


def _card(*, part: Part, rendered: dict[str, str]) -> str:
    key = _part_id(part=part)
    label = f'Question {part["number"]}' + (f'({part["part"]})' if part["part"] else "")
    section = "I" if part["number"] <= 10 else "II"
    tags = "".join(f'<span class="topic-label">{_escape(text=tag)}</span>' for tag in part["tags"])
    steps = "".join(f'<li>{rendered[step]}</li>' for step in part["steps"])
    figure = ""
    if "figure" in part:
        figure = f'<figure><img src="/assets/practice/{part["figure"]}" alt="Solution sketch for {label}; key values and curve behaviour are described in the steps above." width="680" height="350" loading="lazy"><figcaption>Original solution sketch; see the steps for key values.</figcaption></figure>'
    return f'''<article class="question-card" id="{key}" data-section="{section}" data-tags="{_escape(text=json.dumps(obj=part["tags"]))}">
      <div class="question-heading">
        <div><p class="question-number"><a href="#{key}">{label}</a><span>{part["marks"]} {"mark" if part["marks"] == 1 else "marks"}</span></p>
          <h3>{_escape(text=part["title"])}</h3></div>
        <a class="paper-link" href="{PAPER}#page={part["page"]}" target="_blank" rel="noopener">Read question <span aria-hidden="true">↗</span><span class="sr-only"> in NESA PDF, new tab</span></a>
      </div>
      <div class="question-tags" aria-label="Topics">{tags}</div>
      <details class="solution" id="solution-{key}">
        <summary><span class="when-closed">Show solution</span><span class="when-open">Hide solution</span><span class="sr-only"> for {label}</span><span class="expand-icon" aria-hidden="true">+</span></summary>
        <div class="solution-body"><ol>{steps}</ol>{figure}<div class="answer"><strong>Answer</strong><div>{rendered[part["answer"]]}</div></div></div>
      </details>
      <div class="timer-controls" hidden>
        <span class="timer-label">Solution time <output aria-label="Time spent on {label}" class="timer-value">00:00</output></span>
        <span class="timer-status">Not started</span>
        <button type="button" class="timer-toggle" aria-label="Pause timer for {label}" disabled>Pause</button>
        <button type="button" class="timer-reset" aria-label="Reset timer for {label}">Reset</button>
      </div>
    </article>'''


def _page(*, parts: list[Part], rendered: dict[str, str]) -> str:
    tags = sorted({tag for part in parts for tag in part["tags"]})
    filters = "".join(f'<button type="button" class="tag-filter" data-tag="{_escape(text=tag)}" aria-pressed="false">{_escape(text=tag)}</button>' for tag in tags)
    sections = []
    for section, name in [("I", "Multiple choice"), ("II", "Written responses")]:
        matching = [part for part in parts if (part["number"] <= 10) == (section == "I")]
        cards = "\n".join(_card(part=part, rendered=rendered) for part in matching)
        sections.append(f'<section class="question-section" data-section="{section}" aria-labelledby="section-{section}"><h2 id="section-{section}">Section {section} <span>{name}</span></h2>{cards}</section>')
    return f'''<!doctype html>
<html lang="en-AU">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>2025 HSC Maths Advanced Worked Solutions | HSC Maths Tutor</title>
  <meta name="description" content="Original worked solutions for every question in the 2025 HSC Mathematics Advanced exam. Filter by topic, reveal each solution and time your review.">
  <link rel="canonical" href="https://hscmathstutor.com.au{SLUG}">
  <meta property="og:title" content="2025 HSC Maths Advanced worked solutions">
  <meta property="og:description" content="31 questions. 50 parts. Clear working, topic filters and a timer for every solution.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://hscmathstutor.com.au{SLUG}">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,600;8..60,700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css?v=8">
  <link rel="stylesheet" href="/assets/vendor/katex/katex.min.css">
  <link rel="stylesheet" href="/assets/practice/practice.css?v=1">
  <script src="/assets/practice/practice.js?v=1" defer></script>
</head>
<body class="practice-page">
  <a class="skip-link" href="#questions">Skip to solutions</a>
  <header class="site-header"><div class="container nav">
    <a href="/" class="brand">Sachin Abeywardana <span>HSC Maths Tutoring</span></a>
    <nav aria-label="Main"><a href="/maths-advanced-tutor/">Advanced</a><a href="{SLUG}" aria-current="page">Past paper solutions</a><a href="/#contact" class="btn btn-small">Free trial lesson</a></nav>
  </div></header>
  <main>
    <section class="practice-hero"><div class="container practice-width">
      <p class="eyebrow">Past paper practice · Mathematics Advanced</p>
      <h1>2025 HSC<br>worked solutions</h1>
      <p class="lead">A clear method for every question. Find a topic, try it on paper, then open the working when you’re ready.</p>
      <div class="paper-stats"><span><strong>31</strong> questions</span><span><strong>50</strong> parts</span><span><strong>100</strong> marks</span></div>
      <div class="cta-row"><a class="btn" href="{PAPER}" target="_blank" rel="noopener">Open official exam paper <span aria-hidden="true">↗</span><span class="sr-only"> (PDF, new tab)</span></a><a class="text-link" href="{PACK}" target="_blank" rel="noopener">NESA exam pack <span class="sr-only">(new tab)</span></a></div>
      <p class="source-note">Use these independently written solutions alongside the official NESA questions. This is an unofficial study resource, not endorsed by NESA.</p>
    </div></section>
    <div class="container practice-width practice-content">
      <aside class="how-to"><strong>Make it a focused study session.</strong> Open a solution to start its timer and pause the previous one. Close it to pause, or use Pause and Reset. Switching tabs pauses timing. All timers reset on page reload.</aside>
      <div id="total-time-panel" class="total-time-panel" hidden><div><strong>Total study time</strong><p>Active time across all solutions. Resetting a question keeps this total.</p></div><output id="total-time" aria-label="Total study time" aria-live="off">00:00</output></div>
      <form class="filter-panel" hidden aria-label="Filter questions">
        <div class="filter-heading"><h2>Choose your topics</h2><button type="button" id="clear-filters">Clear filters</button></div>
        <p id="tag-help">Select one or more topics. Questions matching any selected topic will appear.</p>
        <div class="tag-filters" role="group" aria-label="Topics" aria-describedby="tag-help">{filters}</div>
        <div class="filter-bottom"><label for="section-filter">Exam section</label><select id="section-filter"><option value="all">All questions</option><option value="I">Section I · Multiple choice</option><option value="II">Section II · Written responses</option></select><p id="result-count" role="status" aria-live="polite" aria-atomic="true">Showing all 50 question parts</p></div>
      </form>
      <noscript><p class="how-to">All solutions are available below. Enable JavaScript for topic filters and timers.</p></noscript>
      <div id="questions" tabindex="-1">{"".join(sections)}</div>
      <div id="empty-state" hidden><h2>No matching question parts</h2><p>Try another topic or exam section.</p><button type="button" class="btn btn-ghost" id="empty-clear">Clear filters</button></div>
      <aside class="study-footer"><h2>Want to work through it together?</h2><p>Bring the questions you’re finding tricky to a lesson.</p><a class="btn" href="/#contact">Book a free trial lesson</a></aside>
    </div>
  </main>
  <footer class="site-footer"><div class="container footer-grid"><p>&copy; <span id="year">2026</span> Sachin Abeywardana</p><p><a href="/">HSC Maths Tutoring</a></p><p><a href="{PACK}" target="_blank" rel="noopener">Official source: NESA 2025 exam pack</a></p></div></footer>
  <script src="/site.js?v=8"></script>
</body>
</html>
'''


def _curve(*, function: Callable[[float], float], xmin: float, xmax: float, ymin: float, ymax: float, colour: str, dash: bool = False) -> str:
    points = []
    for index in range(401):
        x = xmin + (xmax - xmin) * index / 400
        y = function(x)
        px = 64 + 580 * (x - xmin) / (xmax - xmin)
        py = 285 - 250 * (y - ymin) / (ymax - ymin)
        points.append(f"{px:.2f},{py:.2f}")
    pattern = ' stroke-dasharray="7 5"' if dash else ""
    return f'<polyline points="{" ".join(points)}" fill="none" stroke="{colour}" stroke-width="3"{pattern} clip-path="url(#plot)"/>'


def _chart(*, name: str, title: str, description: str, xmin: float, xmax: float, ymin: float, ymax: float, xticks: list[float], yticks: list[float], curves: list[tuple[Callable[[float], float], str, bool]], xlabel: str, ylabel: str, legend: str) -> None:
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 350" role="img" aria-labelledby="title desc"><title id="title">{_escape(text=title)}</title><desc id="desc">{_escape(text=description)}</desc><defs><clipPath id="plot"><rect x="64" y="35" width="580" height="250"/></clipPath></defs><rect width="680" height="350" fill="white"/><g font-family="system-ui,sans-serif" font-size="13" fill="#13294b">']
    for x in xticks:
        px = 64 + 580 * (x - xmin) / (xmax - xmin)
        svg.append(f'<path d="M{px} 35V285" stroke="#dde3ea"/><text x="{px}" y="306" text-anchor="middle">{x:g}</text>')
    for y in yticks:
        py = 285 - 250 * (y - ymin) / (ymax - ymin)
        svg.append(f'<path d="M64 {py}H644" stroke="#dde3ea"/><text x="52" y="{py+4}" text-anchor="end">{y:g}</text>')
    xzero = 64 + 580 * (0 - xmin) / (xmax - xmin)
    yzero = 285 - 250 * (0 - ymin) / (ymax - ymin)
    svg.append(f'<path d="M64 {yzero}H644 M{xzero} 35V285" stroke="#13294b" stroke-width="1.5"/>')
    for function, colour, dash in curves:
        svg.append(_curve(function=function, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, colour=colour, dash=dash))
    svg.append(f'<text x="650" y="306">{xlabel}</text><text x="12" y="22">{ylabel}</text><text x="64" y="334">{_escape(text=legend)}</text></g></svg>')
    (ROOT / "assets/practice" / name).write_text(data="".join(svg), encoding="utf-8")


def _first_wave(t: float) -> float:
    return 2 * math.sin(2 * math.pi * t / 5)


def _second_wave(t: float) -> float:
    return 4 * math.sin(math.pi * t / 10)


def _stationary_curve(x: float) -> float:
    return x * x * math.exp(-x)


def _arc_curve(theta: float) -> float:
    return math.sin(theta) + math.pi / 2


def _identity(x: float) -> float:
    return x


def _write_charts() -> None:
    _chart(name="sine-waves.svg", title="Solution sketch: the two sound waves", description="The solid teal half-wave rises from (0,0) to (5,4) and falls to (10,0). The dashed navy wave oscillates twice with amplitude 2.", xmin=0, xmax=10, ymin=-3, ymax=5, xticks=[0, 2.5, 5, 7.5, 10], yticks=[-2, 0, 2, 4], curves=[(_first_wave, "#13294b", True), (_second_wave, "#167a78", False)], xlabel="t (ms)", ylabel="Pressure (Pa)", legend="Solid teal: P₂(t) · Dashed navy: P₁(t)")
    _chart(name="stationary-curve.svg", title="Solution sketch: stationary points", description="The curve has a minimum at (0,0), a local maximum at (2,4/e squared), and approaches zero from above as x increases.", xmin=-1, xmax=7, ymin=-0.15, ymax=1.2, xticks=[-1, 0, 1, 2, 3, 4, 5, 6, 7], yticks=[0, 0.5, 1], curves=[(_stationary_curve, "#167a78", False)], xlabel="x", ylabel="f(x)", legend="Minimum (0, 0) · Local maximum (2, 4/e²) ≈ (2, 0.541)")
    _chart(name="arc-intersection.svg", title="Solution sketch: finding the intersection", description="The line y equals theta intersects y equals sin theta plus pi over 2 near theta equals 2.31 radians.", xmin=0, xmax=3.2, ymin=0, ymax=3.3, xticks=[0, 1, 2, 2.31, 3], yticks=[0, 1, 2, 3], curves=[(_arc_curve, "#167a78", False), (_identity, "#13294b", True)], xlabel="θ", ylabel="y", legend="Solid teal: sin θ + π/2 · Dashed navy: θ (radians)")


def main() -> None:
    parts = json.loads(s=(ROOT / "content/2025-maths-advanced.json").read_text(encoding="utf-8"))
    if len(parts) != 50 or sum(part["marks"] for part in parts) != 100:
        raise ValueError("Expected all 50 question parts and all 100 marks")
    if len({_part_id(part=part) for part in parts}) != len(parts):
        raise ValueError("Duplicate question part")
    rendered = _render_texts(parts=parts)
    _write_charts()
    (ROOT / SLUG.strip("/") / "index.html").write_text(data=_page(parts=parts, rendered=rendered), encoding="utf-8")
    print(f"Built {SLUG}: {len(parts)} parts, 100 marks, original solution sketches")


if __name__ == "__main__":
    main()
