"""Generate the timestamped video-link pages for Chris's LinkedIn Featured section.

LinkedIn rewrites YouTube links to the plain watch URL and drops the timestamp.
Each page here carries its own Open Graph tags (so LinkedIn keeps the page's own URL)
and forwards the visitor to YouTube at the right moment with JavaScript.
LinkedIn's preview crawler doesn't run JavaScript, so it never follows the forward.

Usage (from this folder): python build.py
Writes <slug>/index.html at the repo root (served at https://chrisdunaetz.github.io/<slug>/).
Custom thumbnails go in ../thumbs/<slug>.jpg or .png (16:9 or 1200x627); until then the YouTube thumbnail is used.
This folder starts with "_", so GitHub Pages (Jekyll) doesn't publish it.
The home page (index.html), llms.txt, robots.txt and sitemap.xml are hand-written; the 2015 site lives in archives/2015/.
"""
import html
from pathlib import Path

BASE_URL = "https://chrisdunaetz.github.io"

VIDEOS = [
    {
        "slug": "alien-earth",
        "title": "Alien: Earth on Apple Vision Pro, featured by Apple (Meet with Apple, 2025)",
        "description": "Apple highlights the Alien: Earth environment on Disney+, which Chris Dunaetz brought to Vision Pro.",
        "youtube_id": "muthEMhOq0Q",
        "start_seconds": 3493,
    },
    {
        "slug": "vision-pro-environments",
        "title": "Disney+ immersive viewing environments on Apple Vision Pro (walkthrough)",
        "description": "Spatial Insider's walkthrough of the Disney+ viewing environments on Vision Pro.",
        "youtube_id": "G1FZMo1BMIY",
        "start_seconds": 218,
    },
    {
        "slug": "wwdc-2023",
        "title": "Apple announces the Disney+ viewing environments (WWDC 2023 keynote)",
        "description": "The WWDC 2023 keynote segment where Apple and Disney announced Disney+ for Apple Vision Pro.",
        "youtube_id": "GYkq9Rgoj8E",
        "start_seconds": 6051,
    },
]

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{page_url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{page_url}">
<meta property="og:image" content="{image_url}">
<meta name="twitter:card" content="summary_large_image">
<script>location.replace({target_js});</script>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font: 16px/1.5 system-ui, sans-serif; margin: 0; padding: 32px 16px; text-align: center; }}
  a {{ color: #2f5d80; }}
  @media (prefers-color-scheme: dark) {{ a {{ color: #8ab4d8; }} }}
</style>
</head>
<body>
<p>Opening the video at {timestamp}…</p>
<p><a href="{target}">Watch on YouTube</a></p>
</body>
</html>
"""

def timestamp(seconds):
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def main():
    base = BASE_URL
    site = Path(__file__).resolve().parent.parent
    (site / "thumbs").mkdir(exist_ok=True)

    for v in VIDEOS:
        page_url = f"{base}/{v['slug']}/"
        target = f"https://www.youtube.com/watch?v={v['youtube_id']}&t={v['start_seconds']}s"
        thumbs = [t for t in (site / "thumbs").glob(f"{v['slug']}.*") if t.suffix in (".jpg", ".png")]
        image_url = (f"{base}/thumbs/{thumbs[0].name}" if thumbs
                     else f"https://i.ytimg.com/vi/{v['youtube_id']}/maxresdefault.jpg")
        out = site / v["slug"] / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(PAGE.format(
            title=html.escape(v["title"]),
            description=html.escape(v["description"]),
            page_url=page_url,
            image_url=image_url,
            target=html.escape(target),
            target_js=repr(target).replace("'", '"'),
            timestamp=timestamp(v["start_seconds"]),
        ), encoding="utf-8")
        print(f"{page_url}  ->  {target}")


if __name__ == "__main__":
    main()
