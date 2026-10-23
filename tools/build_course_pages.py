"""Generate the per-course landing pages from the course data below."""

import html
import re
from pathlib import Path
from typing import TypedDict

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://hscmathstutor.com.au"
WHATSAPP_URL = "https://wa.me/61433011286?text=Hi%20Sachin%2C%20I%27m%20interested%20in%20HSC%20maths%20tutoring."
NEARBY = "Cherrybrook, Pennant Hills, Beecroft, Castle Hill, Carlingford, Thornleigh and Dural"


class Video(TypedDict, total=False):
    id: str
    playlist: str
    title: str
    note: str


class Course(TypedDict):
    slug: str
    name: str
    unit: str
    title: str
    description: str
    h1: str
    intro: list[str]
    topics: list[str]
    videos: list[Video]


COURSES: list[Course] = [
    {
        "slug": "maths-advanced-tutor",
        "name": "Mathematics Advanced",
        "unit": "2 unit",
        "title": "Maths Advanced Tutor (HSC 2 Unit) | West Pennant Hills & Online",
        "description": "HSC Mathematics Advanced tutoring for Years 11 and 12 with Sachin Abeywardana. 20+ years experience, worked video lessons, first lesson free. West Pennant Hills or online via Zoom.",
        "h1": "HSC Maths Advanced tutor",
        "intro": [
            "Mathematics Advanced (the old 2 unit course) is the course most HSC students take, and it's the foundation for Extension 1 and Extension 2. I've been tutoring it for more than 20 years.",
            "Lessons focus on understanding why each method works, not just memorising steps. That's what lets students handle the unfamiliar questions that separate a Band 5 from a Band 6.",
        ],
        "topics": [
            "Functions and graphs, including transformations",
            "Trigonometric functions and identities",
            "Exponential and logarithmic functions",
            "Differential calculus: rates of change, curve sketching and optimisation",
            "Integral calculus: areas under curves and the trapezoidal rule",
            "Series and financial mathematics: annuities and loan repayments",
            "Statistical analysis: random variables and the normal distribution",
        ],
        "videos": [
            {"id": "-4hwIgP7nms", "title": "Home loan repayments"},
            {"id": "UMu2_j5OMfI", "title": "Arithmetic and geometric series"},
            {"id": "c1vafF2mNnI", "title": "Change of base for logarithms"},
            {"id": "QqD3gD_Wpb0", "title": "Graphing parabolas"},
            {"id": "-DE87i3BwBg", "title": "Proof of the cosine rule"},
            {"id": "F4CazpRdI0A", "title": "Integration: a summary"},
            {"id": "340Skx6er48", "title": "Integrating trigonometric functions"},
            {"id": "k3quWmtXkF0", "title": "Acceleration and displacement"},
            {"id": "1Hj9YCz52u8", "title": "The normal distribution"},
            {"id": "TDJ5yV9jz9A", "title": "HSC 2012 Mathematics, Question 11", "note": "Past HSC paper walkthrough"},
            {"id": "XumT2RvVi4k", "title": "HSC 2012 Mathematics, Question 12", "note": "Past HSC paper walkthrough"},
        ],
    },
    {
        "slug": "extension-1-maths-tutor",
        "name": "Mathematics Extension 1",
        "unit": "3 unit",
        "title": "Extension 1 Maths Tutor (HSC 3 Unit) | West Pennant Hills & Online",
        "description": "HSC Mathematics Extension 1 tutoring for Years 11 and 12 with Sachin Abeywardana. 20+ years experience, worked video lessons, first lesson free. West Pennant Hills or online via Zoom.",
        "h1": "HSC Extension 1 maths tutor",
        "intro": [
            "Mathematics Extension 1 (the old 3 unit course) builds on Advanced with harder functions, proof and further calculus. I've been tutoring it for more than 20 years.",
            "Extension 1 questions often combine several topics at once, so lessons focus on recognising which tools a question needs and setting out clear, complete working.",
        ],
        "topics": [
            "Further functions and inequalities, including absolute values",
            "Polynomials: roots, factor theorem and graphing",
            "Inverse trigonometric functions and their derivatives",
            "Further trigonometry and trigonometric equations",
            "Proof by mathematical induction",
            "Combinatorics: permutations and combinations",
            "The binomial distribution and the normal approximation",
            "Vectors and projectile motion",
            "Further calculus: integration by substitution, volumes and differential equations",
        ],
        "videos": [
            {"id": "O4p9a-d6tIo", "title": "General solutions for sin, cos and tan"},
            {"id": "f_1wEVC8V4Q", "title": "Inverse tan (arctan)"},
            {"id": "2n2AKo4_ytQ", "title": "Differentiating inverse trigonometric functions"},
            {"id": "LHvQeBRLFn8", "title": "Polynomials"},
            {"id": "Yz2fcAx5Ufs", "title": "Graphing polynomials with known roots"},
            {"id": "6l4cAAx22SY", "title": "Inequalities with absolute values and polynomial fractions"},
            {"id": "Bg5SV-0UigM", "title": "Graphing sums of absolute values"},
            {"id": "ZeGdGKjz9pc", "title": "Permutations, part 1"},
            {"id": "vtac9u8mzK4", "title": "Permutations: arrangements"},
            {"id": "Sl2juYIftUs", "title": "Normal approximation to the binomial: visualisation"},
            {"id": "F1pE5sCZzaI", "title": "Normal approximation to the binomial: examples"},
            {"id": "w9Q6JOoA4ic", "title": "Projectile motion"},
            {"id": "lYdKnXbbZcs", "title": "Proof by induction (HSC 2005 Question 4d)", "note": "Past HSC paper walkthrough"},
        ],
    },
    {
        "slug": "extension-2-maths-tutor",
        "name": "Mathematics Extension 2",
        "unit": "4 unit",
        "title": "Extension 2 Maths Tutor (HSC 4 Unit) | West Pennant Hills & Online",
        "description": "HSC Mathematics Extension 2 tutoring for Year 12 with Sachin Abeywardana. 20+ years experience, worked video lessons, first lesson free. West Pennant Hills or online via Zoom.",
        "h1": "HSC Extension 2 maths tutor",
        "intro": [
            "Mathematics Extension 2 (the old 4 unit course) is the most demanding maths course in the HSC. I've been tutoring it for more than 20 years.",
            "Lessons focus on the reasoning behind each technique, so students can tackle the long, multi-step questions that make up much of the exam.",
        ],
        "topics": [
            "Complex numbers: Cartesian, polar and exponential forms, De Moivre's theorem and loci",
            "Vectors in three dimensions: lines and spheres",
            "Further integration: integration by parts, partial fractions and recurrence relations",
            "Mechanics: simple harmonic motion and resisted motion",
        ],
        "videos": [
            {"playlist": "PLIx9QCwIhuRSiGtRmZNvORkI9nVTzb1CQ", "id": "CNadwPOZINA", "title": "Complex numbers series", "note": "3-part playlist: locus of lines, locus of circles, and trigonometry"},
            {"id": "jvh-jWDAYd8", "title": "Integration by parts"},
            {"id": "jncLu10iAVc", "title": "Simple harmonic motion: introduction"},
            {"id": "0U7kLdcvmtU", "title": "Simple harmonic motion: examples, part 1"},
            {"id": "Y8wnwu_tHUI", "title": "Simple harmonic motion: examples, part 2"},
            {"id": "H8Wk_C0njpA", "title": "Motion and air resistance"},
        ],
    },
]


def _whatsapp_svg(*, size: int) -> str:
    index = (ROOT / "index.html").read_text()
    path = re.search(r'<path fill="currentColor" d="([^"]+)"', index).group(1)
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="{path}"/></svg>'


def _video_card(*, video: Video) -> str:
    title = html.escape(video["title"])
    attr = f'data-list="{video["playlist"]}"' if "playlist" in video else f'data-id="{video["id"]}"'
    note = f'\n            <p class="video-note">{html.escape(video["note"])}</p>' if "note" in video else ""
    return f"""          <article class="video-card">
            <button class="video-facade" type="button" {attr} aria-label="Play: {title}">
              <img src="https://i.ytimg.com/vi/{video["id"]}/hqdefault.jpg" alt="" loading="lazy" width="480" height="360">
              <span class="play" aria-hidden="true"></span>
            </button>
            <h3>{title}</h3>{note}
          </article>"""


def _other_courses(*, current: Course) -> str:
    links = [f'<a href="/{c["slug"]}/">{c["name"]}</a>' for c in COURSES if c["slug"] != current["slug"]]
    return " and ".join(links)


def _page(*, course: Course) -> str:
    url = f'{SITE}/{course["slug"]}/'
    intro = "\n".join(f"        <p>{html.escape(p)}</p>" for p in course["intro"])
    topics = "\n".join(f"              <li>{html.escape(t)}</li>" for t in course["topics"])
    videos = "\n".join(_video_card(video=v) for v in course["videos"])
    practice = f"""
    <section class="section">
      <div class="container narrow">
        <p class="eyebrow">Free past paper practice</p>
        <h2>{html.escape(course["name"])} worked solutions</h2>
        <p>Original explanations for every question, topic filters and solution timers with a total study time counter.</p>
        <a class="btn" href="/practice/">Explore past paper solutions &rarr;</a>
      </div>
    </section>
"""
    return f"""<!doctype html>
<html lang="en-AU">
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-6GRSXV2JGM"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-6GRSXV2JGM');
  </script>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(course["title"])}</title>
  <meta name="description" content="{html.escape(course["description"])}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{html.escape(course["title"])}">
  <meta property="og:description" content="{html.escape(course["description"])}">
  <meta property="og:image" content="{SITE}/assets/sachin.jpg">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,600;8..60,700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css?v=8">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{"@type": "ListItem", "position": 1, "name": "HSC Maths Tutor", "item": "{SITE}/"}},
      {{"@type": "ListItem", "position": 2, "name": "{course["name"]} tutor", "item": "{url}"}}
    ]
  }}
  </script>
</head>
<body>
  <header class="site-header">
    <div class="container nav">
      <a href="/" class="brand">Sachin Abeywardana <span>HSC Maths Tutoring</span></a>
      <nav aria-label="Main">
        <a href="/maths-advanced-tutor/">Advanced</a>
        <a href="/extension-1-maths-tutor/">Extension 1</a>
        <a href="/extension-2-maths-tutor/">Extension 2</a>
        <a href="/#contact" class="btn btn-small">Free trial lesson</a>
      </nav>
    </div>
  </header>

  <main>
    <section class="hero course-hero">
      <div class="container narrow">
        <p class="eyebrow">{course["name"]} ({course["unit"]}) &middot; West Pennant Hills and online</p>
        <h1>{html.escape(course["h1"])}</h1>
        <p class="lead">1-on-1 and small group lessons for {course["name"]}, at my home in West Pennant Hills or online via Zoom. Your first lesson is free.</p>
        <div class="cta-row">
          <a href="/#contact" class="btn">Book your free trial lesson</a>
          <a href="{WHATSAPP_URL}" class="btn btn-whatsapp" target="_blank" rel="noopener">{_whatsapp_svg(size=18)}Message me on WhatsApp</a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container narrow">
        <h2>About {course["name"]} tutoring</h2>
{intro}
      </div>
    </section>

{practice}    <section class="section alt">
      <div class="container narrow">
        <h2>Topics I cover</h2>
        <ul class="topic-list">
{topics}
        </ul>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <h2>Worked video lessons</h2>
        <p class="section-lead">Some of my {course["name"]} lessons on YouTube, so you can see how I explain things before booking.</p>
        <div class="video-grid three">
{videos}
        </div>
      </div>
    </section>

    <section class="section alt">
      <div class="container narrow">
        <h2>Lesson details</h2>
        <ul class="checks details">
          <li><strong>First lesson free</strong>, then $60 per hour for 1-on-1 lessons</li>
          <li>60 minute lessons, 1-on-1 or in a small group</li>
          <li>At my home in West Pennant Hills (2125), a short drive from {NEARBY}</li>
          <li>Or online via Zoom, with a tablet, a stylus and a free Canva account</li>
          <li>20+ years tutoring HSC maths, James Ruse graduate (99.25 UAI), PhD in AI and statistics</li>
          <li>Current NSW Working With Children Check (WWC2744827E)</li>
        </ul>
        <div class="cta-row">
          <a href="/#contact" class="btn">Book your free trial lesson</a>
        </div>
        <p class="also">I also tutor {_other_courses(current=course)}.</p>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container footer-grid">
      <p>&copy; <span id="year">2026</span> Sachin Abeywardana</p>
      <p>ABN 80 539 711 268 &middot; NSW WWCC WWC2744827E</p>
      <p>West Pennant Hills NSW 2125</p>
    </div>
    <nav class="container footer-links" aria-label="Courses">
      <a href="/maths-advanced-tutor/">Maths Advanced tutor</a>
      <a href="/extension-1-maths-tutor/">Extension 1 maths tutor</a>
      <a href="/extension-2-maths-tutor/">Extension 2 maths tutor</a>
    </nav>
    <p class="container privacy">This site uses Google Analytics to understand how visitors use it. Details you send through the contact form go only to me and are never shared.</p>
  </footer>

  <a href="{WHATSAPP_URL}" class="whatsapp-float" target="_blank" rel="noopener" aria-label="Message me on WhatsApp">{_whatsapp_svg(size=28)}</a>
  <script src="/site.js?v=8"></script>
</body>
</html>
"""


def _write_page(*, course: Course) -> Path:
    out = ROOT / course["slug"] / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(_page(course=course))
    return out


def _write_sitemap() -> None:
    urls = [f"{SITE}/"] + [f'{SITE}/{c["slug"]}/' for c in COURSES]
    urls.append(f"{SITE}/practice/")
    urls.extend(f"{SITE}/practice/{path.stem}/" for path in sorted((ROOT / "content").glob("*.json")))
    entries = "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}\n</urlset>\n'
    )


def main() -> None:
    for path in [_write_page(course=c) for c in COURSES]:
        print(f"wrote {path.relative_to(ROOT)}")
    _write_sitemap()
    print("wrote sitemap.xml")


if __name__ == "__main__":
    main()
