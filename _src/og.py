"""Render assets/og.png (1200x630 social preview) from the built site's CSS. Usage: python3 og.py <site_dir>"""
import sys, os, asyncio, pathlib
from playwright.async_api import async_playwright
site = os.path.abspath(sys.argv[1])
html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700&family=IBM+Plex+Mono:wght@500;600&family=Noto+Sans+KR:wght@500&display=swap">
<link rel="stylesheet" href="file://{site}/assets/site.css">
<style>
body{{margin:0;width:1200px;height:630px;overflow:hidden;background:var(--bg)}}
.og{{position:relative;width:1200px;height:630px;padding:64px 72px;box-sizing:border-box;display:flex;flex-direction:column}}
.og::before{{content:"";position:absolute;right:-160px;top:-200px;width:760px;height:760px;border-radius:50%;background:radial-gradient(closest-side,rgba(46,184,174,.28),transparent 70%)}}
.top{{display:flex;align-items:center;gap:14px;position:relative}}
.mark{{display:grid;place-items:center;width:52px;height:52px;border-radius:13px;background:var(--teal-fill);color:var(--teal-ink);font:700 24px/1 var(--font);letter-spacing:-.05em}}
.site{{font:500 22px var(--mono);color:var(--text-3)}}
h1{{position:relative;margin:46px 0 0;font:700 84px/1 var(--font);letter-spacing:-.02em;color:var(--text)}}
h1 span{{font:500 40px var(--font);font-family:"Noto Sans KR";color:var(--text-3);margin-left:14px}}
.role{{position:relative;margin:16px 0 0;font:400 27px var(--font);color:var(--text-2)}}
.tag{{position:relative;margin:30px 0 0;font:700 36px/1.3 var(--font);color:var(--text)}}
.tag em{{font-style:normal;color:var(--teal-text)}}
.oghl{{position:relative;display:flex;flex-direction:row;gap:12px;margin-top:auto}}
.oghl span{{display:inline-flex;align-items:center;height:46px;padding:0 18px;border-radius:12px;border:1px solid var(--line-2);background:var(--panel);font:600 21px var(--font);color:var(--text)}}
.oghl span b{{color:var(--teal-text);margin-right:8px}}
</style></head><body><div class="og">
<div class="top"><span class="mark">jk.</span><span class="site">heoneyzi.github.io</span></div>
<h1>Jiheon Kang<span>강지헌</span></h1>
<p class="role">Biomedical AI Researcher · Yonsei University</p>
<p class="tag">Beyond artificial tasks,<br><em>toward the rules of nature.</em></p>
<div class="oghl"><span><b>Oral</b>ICML 2026 GenBio</span><span><b>Bronze</b>CAFA 6</span><span><b>3</b>papers</span><span><b>VP</b>Yonsei AI</span></div>
</div></body></html>'''
tmp = pathlib.Path(site) / '_og_tmp.html'
tmp.write_text(html, encoding='utf-8')
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1200, 'height': 630})
        await pg.goto(tmp.as_uri()); await pg.wait_for_timeout(1500)
        await pg.screenshot(path=os.path.join(site, 'assets', 'og.png'))
        await b.close()
asyncio.run(main()); tmp.unlink()
print('og.png written')
