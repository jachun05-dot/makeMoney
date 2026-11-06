"""정적 사이트 생성기. 실행: python3 build.py  ->  dist/ 폴더 생성"""
import datetime
import html
import json
import shutil
from pathlib import Path

import config
from pages import PAGES

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
TODAY = datetime.date.today().isoformat()
BASE = config.SITE_URL.rstrip("/")


def esc(s):
    return html.escape(s, quote=True)


def page_url(slug=""):
    return f"{BASE}/{slug}/" if slug else f"{BASE}/"


def head(title, description, url, jsonld):
    verify = (
        f'<meta name="google-site-verification" content="{esc(config.GOOGLE_SITE_VERIFICATION)}">'
        if config.GOOGLE_SITE_VERIFICATION else ""
    )
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="{esc(config.SITE_NAME)}">
<meta property="og:locale" content="ko_KR">
{verify}
<link rel="stylesheet" href="{BASE}/style.css">
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
</head>
<body>
<header class="top"><a href="{BASE}/" class="brand">{esc(config.SITE_NAME)}</a></header>
"""


FOOT = f"""<footer class="foot">
<p>이 사이트의 일부 링크는 제휴 링크로, 링크를 통해 상담 신청·가입이 이루어지면 운영자가 일정 수수료를 받을 수 있습니다. 이용자에게 추가 비용은 없습니다.</p>
<p>본 사이트는 일반적인 정보를 제공하며, 구체적인 조건과 금액은 각 회사 및 상담을 통해 확인하세요.</p>
<p><a href="{BASE}/about/">운영 안내 · 개인정보</a></p>
</footer>
</body>
</html>
"""


def cta_block(p, variant=""):
    link = config.CPA_LINKS.get(p["offer"], "").strip()
    if link:
        btn = (f'<a class="btn" href="{esc(link)}" target="_blank" '
               f'rel="sponsored nofollow noopener">{esc(p["cta"])}</a>')
    else:
        btn = '<span class="btn btn-off">상담 링크 준비 중</span>'
    return f"""<div class="cta {variant}">
{btn}
<p class="cta-sub">{esc(p["cta_sub"])}</p>
<p class="ad">광고 · 제휴 링크</p>
</div>"""


def render_page(p):
    url = page_url(p["slug"])
    jsonld = [
        {
            "@context": "https://schema.org", "@type": "Article",
            "headline": p["h1"], "description": p["description"],
            "dateModified": TODAY, "mainEntityOfPage": url,
            "author": {"@type": "Organization", "name": config.SITE_NAME},
        },
        {
            "@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in p["faq"]
            ],
        },
        {
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "홈", "item": page_url()},
                {"@type": "ListItem", "position": 2, "name": p["h1"], "item": url},
            ],
        },
    ]
    sections = "\n".join(f"<section><h2>{esc(h)}</h2>{body}</section>" for h, body in p["sections"])
    faq = "\n".join(
        f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in p["faq"]
    )
    others = "\n".join(
        f'<li><a href="{page_url(o["slug"])}">{esc(o["title"])}</a></li>'
        for o in PAGES if o["slug"] != p["slug"]
    )
    body = f"""<main class="wrap">
<nav class="crumb"><a href="{BASE}/">홈</a> › {esc(p["category"])}</nav>
<article>
<h1>{esc(p["h1"])}</h1>
<p class="meta">업데이트 {TODAY}</p>
{p["intro"]}
{cta_block(p)}
{sections}
<section><h2>자주 묻는 질문</h2>{faq}</section>
{cta_block(p, "cta-end")}
</article>
<aside><h2>함께 보면 좋은 글</h2><ul>{others}</ul></aside>
</main>
{cta_block(p, "cta-sticky")}
"""
    return head(f'{p["title"]} | {config.SITE_NAME}', p["description"], url, jsonld) + body + FOOT


def render_index():
    jsonld = {"@context": "https://schema.org", "@type": "WebSite",
              "name": config.SITE_NAME, "url": page_url()}
    cards = "\n".join(
        f'<a class="card" href="{page_url(p["slug"])}"><span class="tag">{esc(p["category"])}</span>'
        f'<strong>{esc(p["title"])}</strong><span>{esc(p["description"])}</span></a>'
        for p in PAGES
    )
    body = f"""<main class="wrap">
<h1>{esc(config.SITE_NAME)}</h1>
<p class="lead">{esc(config.SITE_DESCRIPTION)}</p>
<div class="cards">{cards}</div>
</main>
"""
    return head(config.SITE_NAME, config.SITE_DESCRIPTION, page_url(), jsonld) + body + FOOT


def render_about():
    url = page_url("about")
    jsonld = {"@context": "https://schema.org", "@type": "WebPage", "name": "운영 안내", "url": url}
    body = """<main class="wrap"><article>
<h1>운영 안내 · 개인정보</h1>
<h2>사이트 소개</h2>
<p>생활 속 가입·계약을 앞둔 분들이 손해 보지 않도록 확인할 내용을 정리하는 정보 사이트입니다.</p>
<h2>제휴 및 광고 고지</h2>
<p>일부 페이지에는 제휴 마케팅 링크가 포함되어 있습니다. 해당 링크를 통해 상담 신청이나 가입이 이루어지면 운영자가 수수료를 받을 수 있으며, 이용자가 내는 비용에는 영향이 없습니다.</p>
<h2>개인정보</h2>
<p>이 사이트는 직접 개인정보를 수집하지 않습니다. 상담 신청 시 입력하는 정보는 연결된 각 제휴사(광고주)의 개인정보 처리방침에 따라 처리됩니다.</p>
</article></main>
"""
    return head(f"운영 안내 | {config.SITE_NAME}", "사이트 소개, 제휴 고지, 개인정보 안내", url, jsonld) + body + FOOT


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    shutil.copy(ROOT / "static" / "style.css", DIST / "style.css")

    write(DIST / "index.html", render_index())
    write(DIST / "about" / "index.html", render_about())
    for p in PAGES:
        write(DIST / p["slug"] / "index.html", render_page(p))
    write(DIST / "404.html", head("페이지를 찾을 수 없습니다", "", page_url(), {})
          + f'<main class="wrap"><h1>페이지를 찾을 수 없습니다</h1><p><a href="{BASE}/">홈으로</a></p></main>' + FOOT)

    urls = [page_url()] + [page_url(p["slug"]) for p in PAGES] + [page_url("about")]
    sitemap = "\n".join(f"<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls)
    write(DIST / "sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap}\n</urlset>\n')
    write(DIST / "robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    write(DIST / ".nojekyll", "")
    print(f"built {len(urls)} pages -> {DIST}")


if __name__ == "__main__":
    main()
