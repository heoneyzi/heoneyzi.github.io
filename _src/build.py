# -*- coding: utf-8 -*-
"""Build heoneyzi.github.io: index.html + projects/*.html + assets/.  Usage: python3 build.py <out_dir>"""
import os, re, sys, shutil, datetime
from html import escape
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import (PROJECTS, BY_SLUG, FEATURED, MORE, STUDY, REPO, EMAIL, GITHUB, LINKEDIN, CV, SITE, UPDATED, gh)
from ills import ILLS

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..'))  # default: the repo root (this file lives in _src/)
TODAY = '2026-09-28'


def e(s):
    return escape(s, quote=True)


NB = ' '
_SEP = re.compile(r' (·|—|–|→|×|/) ')
_WHEN = re.compile(r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|Spring|Summer|Fall|Autumn|Winter) (\d{4})\b')
_NUM = re.compile(r'(?<=\w) (\d{1,2})\b(?![.,]\d)')
_ACR = re.compile(r'\b([A-Z]{2,}) (\d{4})\b')
_HYPH = re.compile(r'(?<![\w-])([A-Za-z0-9]+(?:-[A-Za-z0-9]+)+)(?![\w-])')


def tidy(s):
    """Line-break hygiene for copy (text outside tags only): a separator stays with the word before it,
    so no line ever starts with '·', '—' or '→'; 'Nov 2023', 'Evo 2', 'season 1', 'IEIE 2025' never split,
    and hyphenated words ('held-out', 'training-free') never break at the hyphen."""
    out = []
    for part in re.split(r'(<[^>]+>)', s):
        if part.startswith('<'):
            out.append(part)
            continue
        part = _SEP.sub(lambda m: NB + m.group(1) + ' ', part)
        part = _WHEN.sub(lambda m: m.group(1) + NB + m.group(2), part)
        part = _ACR.sub(lambda m: m.group(1) + NB + m.group(2), part)
        part = _NUM.sub(lambda m: NB + m.group(1), part)
        part = _HYPH.sub(lambda m: '<span class="nw">' + m.group(1) + '</span>', part)
        out.append(part)
    return ''.join(out)


def t(pair, tag='span', cls=None, extra=''):
    """Bilingual text element: English inside, Korean in data-ko."""
    en, ko = tidy(pair[0]), tidy(pair[1])
    c = f' class="{cls}"' if cls else ''
    return f'<{tag}{c} data-ko="{e(ko)}"{extra}>{en}</{tag}>'


def ic(name, cls='ic'):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"/></svg>'


ICONS = {
    'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 7 8.5 6 8.5-6"/>',
    'file': '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
    'code': '<path d="m8 7-5 5 5 5M16 7l5 5-5 5"/>',
    'user': '<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/>',
    'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
    'ext': '<path d="M14 4h6v6M10 14 20 4M19 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h5"/>',
    'mic': '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>',
    'medal': '<circle cx="12" cy="9" r="6"/><path d="m8.5 14-1.5 7 5-3 5 3-1.5-7"/>',
    'papers': '<path d="M8 3h8l4 4v12a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z"/><path d="M16 3v4h4M4 7v12a2 2 0 0 0 2 2M10 12h6M10 16h6"/>',
    'users': '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.9-3.4 3.3-5.5 6.5-5.5s5.6 2.1 6.5 5.5M16 4.6a3.5 3.5 0 0 1 0 6.8M18 14.8c1.8.8 3 2.6 3.5 5.2"/>',
    'dna': '<path d="M8 3c0 5 8 5 8 9s-8 4-8 9M16 3c0 5-8 5-8 9s8 4 8 9M9.5 6.5h5M10 9.5h4M10 14.5h4M9.5 17.5h5"/>',
    'cell': '<circle cx="12" cy="12" r="9"/><circle cx="13" cy="11" r="3"/><circle cx="7.5" cy="15" r=".8"/><circle cx="16" cy="16.5" r=".8"/>',
    'protein': '<circle cx="6" cy="7" r="2.5"/><circle cx="17.5" cy="6" r="2.5"/><circle cx="12" cy="17.5" r="2.5"/><path d="M8.4 6.8 15 6.2M7.1 9.2l3.7 6M16.4 8.3 13.2 15"/>',
    'pill': '<rect x="2.8" y="8.3" width="18.4" height="7.4" rx="3.7" transform="rotate(-45 12 12)"/><path d="m8.6 8.6 6.8 6.8"/>',
    'pulse': '<path d="M3 12h4l3-7 4 14 3-7h4"/>',
    'film': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M7 5v14M17 5v14M3 9.5h4M3 14.5h4M17 9.5h4M17 14.5h4"/>',
    'route': '<circle cx="6" cy="18" r="2.5"/><circle cx="18" cy="6" r="2.5"/><path d="M8.5 18H15a3.5 3.5 0 0 0 0-7H9a3.5 3.5 0 0 1 0-7h6.5"/>',
    'compass': '<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2 5-5 2 2-5z"/>',
    'chat': '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9.5h8M8 12.5h5"/>',
    'pin': '<path d="M12 21s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/>',
    'book': '<path d="M3 5h6a3 3 0 0 1 3 3v12a2 2 0 0 0-2-2H3zM21 5h-6a3 3 0 0 0-3 3v12a2 2 0 0 1 2-2h7z"/>',
    'eye': '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    'pen': '<path d="M4 20h4L19 9a2.8 2.8 0 0 0-4-4L4 16z"/><path d="m13.5 6.5 4 4"/>',
    'check': '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    'cap': '<path d="M2 9.5 12 4.5l10 5-10 5z"/><path d="M6 11.5v5c3.5 2.7 8.5 2.7 12 0v-5"/>',
    'info': '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/>',
    'down': '<path d="M12 5v14M6 13l6 6 6-6"/>',
    'spark': '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/>',
    'github': '<path d="M9 19c-4.3 1.4-4.3-2.5-6-3m12 5v-3.5c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.2 4.2 0 0 0-.1-3.2s-1.1-.3-3.5 1.3a12.3 12.3 0 0 0-6.2 0C6.5 2.8 5.4 3.1 5.4 3.1a4.2 4.2 0 0 0-.1 3.2A4.6 4.6 0 0 0 4 9.5c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.2-.5 2V21"/>',
}


def sprite():
    return ('<svg class="sprite" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg">'
            + ''.join(f'<symbol id="i-{k}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{v}</symbol>' for k, v in ICONS.items())
            + '</svg>')


NAV = [('work', ('Work', '연구·프로젝트')), ('papers', ('Papers', '논문')), ('study', ('Study & writing', '공부·글')),
       ('journey', ('Journey', '걸어온 길')), ('about', ('About', '소개'))]


def topbar(prefix, crumbs):
    base = '' if prefix == '' else prefix + 'index.html'
    nav_links = ''.join(
        f'<a href="{base}#{sid}"><span class="n">0{i + 1}</span>{t(lab)}</a>' for i, (sid, lab) in enumerate(NAV))
    strip_links = ''.join(
        f'<a href="{base}#{sid}"><span class="n">0{i + 1}</span>{t(lab)}</a>' for i, (sid, lab) in enumerate(NAV))
    return f'''<header class="topbar">
  <div class="tb-row">
    <a class="brand" href="{prefix}index.html" aria-label="Jiheon Kang — home" data-ko-aria="강지헌 — 홈"><span class="brand-mark">jk.</span></a>
    <div class="crumbs">{crumbs}</div>
    <nav class="nav" aria-label="Sections" data-ko-aria="섹션">{nav_links}</nav>
    <div class="tb-right">
      <a class="tb-btn" href="{prefix}{CV}" target="_blank" rel="noopener" aria-label="CV (PDF)">{ic('file')}<span class="t">CV</span></a>
      <a class="tb-btn" href="{GITHUB}" target="_blank" rel="noopener" aria-label="GitHub">{ic('code')}<span class="t">GitHub</span></a>
      <a class="tb-btn" href="mailto:{EMAIL}" aria-label="Email" data-ko-aria="이메일">{ic('mail')}<span class="t" data-ko="이메일">Email</span></a>
      <span class="tb-sep" aria-hidden="true"></span>
      <button class="lang-btn" type="button" data-lang-toggle aria-label="한국어로 보기" aria-pressed="false"><span class="l-en">EN</span><span class="l-ko">KR</span></button>
    </div>
  </div>
  <nav class="nav-strip" aria-label="Sections" data-ko-aria="섹션">{strip_links}</nav>
</header>'''


def page(prefix, title, title_ko, desc, canonical, body, crumbs):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="title-ko" content="{e(title_ko)}">
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#f4f8f8">
<meta name="color-scheme" content="light">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/svg+xml" href="{prefix}favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Sans+3:ital,wght@0,400;0,500;0,600;0,700;1,400&family=IBM+Plex+Mono:wght@400;500;600&family=Noto+Sans+KR:wght@400;500;700&display=swap">
<link rel="stylesheet" href="{prefix}assets/site.css?v=light-only-20260928">
<script src="{prefix}assets/site.js?v=light-only-20260928" defer></script>
</head>
<body>
<a class="skip" href="#main" data-ko="본문으로 건너뛰기">Skip to content</a>
{sprite()}
{topbar(prefix, crumbs)}
{body}
<footer class="foot">
  <div class="wrap">
    <span>© 2026 Jiheon Kang · {t(UPDATED)}</span>
    <span><a href="{REPO}" target="_blank" rel="noopener">github.com/heoneyzi</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></span>
  </div>
</footer>
</body>
</html>
'''


# ------------------------------------------------------------------------------------------------ index pieces
ID_DECO = '''<svg class="id-deco" viewBox="0 0 260 120" aria-hidden="true" focusable="false">
<g fill="none" stroke-linecap="round">
<path d="M4 112 C 70 110 110 64 170 52 S 230 44 250 44" stroke="var(--accent)" stroke-width="2" opacity=".75"/>
<path d="M4 88 C 64 92 116 58 176 50 S 232 44 250 44" stroke="var(--accent)" stroke-width="1.6" opacity=".55"/>
<path d="M4 64 C 80 76 122 52 182 47 S 236 44 250 44" stroke="var(--accent)" stroke-width="1.4" opacity=".42"/>
<path d="M4 40 C 84 58 132 46 188 45 S 238 44 250 44" stroke="var(--accent)" stroke-width="1.2" opacity=".3"/>
<path d="M4 16 C 90 38 140 42 194 44 S 240 44 250 44" stroke="var(--accent)" stroke-width="1.1" opacity=".22"/>
</g>
<circle class="halo" cx="250" cy="44" r="10" fill="none" stroke="var(--accent)" stroke-width="1.3" opacity=".45"/>
<circle cx="250" cy="44" r="4.5" fill="var(--accent)"/>
</svg>'''

HIGHLIGHTS = [
    dict(href='projects/gdtr.html', icon='mic', ctx='2026', v=('Oral', 'Oral'), l=('ICML 2026 GenBio Workshop', 'ICML 2026 GenBio 워크숍'),
         s=('GDTR paper · author', 'GDTR 논문 · 저자')),
    dict(href='projects/cafa6.html', icon='medal', ctx='2026', v=('Bronze', '동메달'), l=('CAFA 6 · protein function', 'CAFA 6 · 단백질 기능 예측'),
         s=('international challenge · team', '국제 대회 · 팀')),
    dict(href='#papers', icon='papers', ctx='2025–26', v=('3 papers', '논문 3편'), l=('2 as first author', '제1저자 2편'),
         s=('ICML GenBio · IEIE · KAIC', 'ICML GenBio · IEIE · KAIC')),
    dict(href='#journey', icon='users', ctx='YAI', v=('Vice President', '부회장'), l=('Yonsei AI (YAI)', 'Yonsei AI (YAI)'),
         s=('Team lead of 6 projects', '프로젝트 팀장 6회')),
]

STAGES = [
    dict(dom='dna', icon='dna', name=('DNA', 'DNA'), q=('Where inside a DNA model is each decision made?', 'DNA 모델 안 어디에서 판단이 이뤄질까?'),
         links=[('gdtr', 'GDTR', ('Oral', 'Oral')), ('geoflowagent', 'GeoFlowAgent', ('solo', '개인'))]),
    dict(dom='cell', icon='cell', name=('RNA · Cell', 'RNA · 세포'), q=('How will an unseen cell respond to a gene knockdown?', '처음 보는 세포는 유전자 억제에 어떻게 반응할까?'),
         links=[('vcc2026', 'VCC 2026', ('lead', '팀장'))]),
    dict(dom='protein', icon='protein', name=('Protein', '단백질'), q=('What does a protein do, from its sequence alone?', '서열만 보고 단백질의 기능을 알 수 있을까?'),
         links=[('cafa6', 'CAFA 6', ('Bronze', '동메달'))]),
    dict(dom='drug', icon='pill', name=('Drug', '약물'), q=('Can a new molecule do the same biology?', '구조가 다른 분자로 같은 효과를 낼 수 있을까?'),
         links=[('phenofocus', 'PhenoFocus', ('lead', '팀장'))]),
    dict(dom='clinic', icon='pulse', name=('Clinic', '임상'), q=('Can a model outline a brain tumour on MRI?', 'MRI에서 뇌종양을 자동으로 그려 낼 수 있을까?'),
         links=[('bu-net', 'BU-Net', ('lead', '팀장'))]),
]

ALSO = [('ftf-vtg', 'film', ('Video grounding · FTF-VTG', '비디오 그라운딩 · FTF-VTG')),
        ('bi-cot', 'route', ('Explainable reasoning · Bi-CoT', '설명 가능한 추론 · Bi-CoT')),
        ('hallucination', 'eye', ('Multimodal hallucination', '멀티모달 환각')),
        ('persona-chatbot', 'chat', ('RAG persona chatbot', 'RAG 페르소나 챗봇')),
        ('taste-trip', 'pin', ('Recommender system', '추천 시스템'))]

NOW = [('projects/vcc2026.html', 'VCC 2026', ('Team lead · 6 people', '팀장 · 6인 팀')),
       ('projects/phenofocus.html', 'PhenoFocus', ('competition main round', '대회 본선 진행 중')),
       ('projects/gdtr.html', 'GDTR', ('follow-up research', '후속 연구 중')),
       ('projects/genomics-study.html', 'YAI', ('Functional Genomics team lead', 'Functional Genomics 팀장'))]


def cover():
    hl = ''.join(f'''<a class="card hl tilt" data-tilt href="{h['href']}">
  <div class="hl-top"><span class="hl-ic">{ic(h['icon'])}</span><span class="hl-ctx">{h['ctx']}</span></div>
  {t(h['v'], 'p', 'hl-v')}
  <div class="hl-foot">{t(h['l'], 'p', 'hl-l')}{t(h['s'], 'p', 'hl-s')}</div>
  {ic('arrow', 'ic hl-go')}
</a>''' for h in HIGHLIGHTS)
    stages = []
    for s in STAGES:
        links = ''.join(f'<a class="st-link" href="projects/{slug}.html"><span>{name}</span>{t(tag, "small")}</a>' for slug, name, tag in s['links'])
        stages.append(f'''<li class="stage lift dom-{s['dom']}">
  <div class="st-top"><span class="st-ic">{ic(s['icon'])}</span>{t(s['name'], 'span', 'st-name')}</div>
  {t(s['q'], 'p', 'st-q')}
  <div class="st-links">{links}</div>
</li>''')
    also = ''.join(f'<a href="projects/{slug}.html">{ic(icn)}{t(lab)}</a>' for slug, icn, lab in ALSO)
    now = ''.join(f'<li><a href="{href}"><b>{name}</b>{t(lab)}</a></li>' for href, name, lab in NOW)
    return f'''<section class="cover" id="top" aria-labelledby="hero-name">
<div class="wrap cover-grid">
  <div class="card id-card">
    <p class="id-stamp">{t(('Portfolio', '포트폴리오'), 'span', 'pill')}<span data-ko="2026.09">Sep 2026</span></p>
    <h1 id="hero-name">Jiheon Kang<span class="h1-ko" lang="ko">강지헌</span></h1>
    {t(('Biomedical AI Researcher · Electrical &amp; Electronic Engineering, Yonsei University', 'Biomedical AI 연구자 · 연세대학교 전기전자공학부'), 'p', 'id-role')}
    <div class="id-tagrow">
      {t(('Beyond artificial tasks,<br><em>toward the rules of nature.</em>', '인공적인 과제를 넘어,<br><em>자연의 규칙을 찾아서.</em>'), 'p', 'id-tag')}
      {ID_DECO}
    </div>
    {t(('I started asking biological questions to move beyond artificial tasks toward real ones, where the rules are nature’s own. Finding those rules is what excites me.', '인공적인 과제에서 벗어나 자연의 규칙을 찾는 진짜 과제로 나아가고 싶어 생물학의 질문을 시작했습니다. 그 규칙을 찾아가는 일에 가장 큰 흥미를 느낍니다.'), 'p', 'id-intro')}
    <div class="id-links">
      <a class="btn btn-primary" href="mailto:{EMAIL}">{ic('mail')}{t(('Email', '이메일'))}</a>
      <a class="btn" href="{CV}" target="_blank" rel="noopener">{ic('file')}<span>CV</span></a>
      <a class="btn" href="{GITHUB}" target="_blank" rel="noopener">{ic('code')}<span>GitHub</span></a>
      <a class="btn" href="{LINKEDIN}" target="_blank" rel="noopener">{ic('user')}<span>LinkedIn</span></a>
    </div>
  </div>
  <div class="hl-grid">{hl}</div>
  <div class="card map-card">
    <div class="map-head">
      <div>{t(('What I study', '연구 지도'), 'p', 'eyebrow')}{t(('Following biological information from DNA to the clinic', 'DNA에서 임상까지, 생물학 정보의 흐름을 따라갑니다'), 'h2')}</div>
      <div class="interests">{t(('Research interests', '연구 관심사'), 'span', 'lbl')}<div class="chips"><span class="chip">{ic('dna')}{t(('Genomics AI', '유전체 AI'))}</span><span class="chip">{ic('eye')}{t(('Multimodal AI', '멀티모달 AI'))}</span><span class="chip">{ic('spark')}{t(('Model interpretability', '모델 해석'))}</span></div></div>
    </div>
    <ol class="stages">{''.join(stages)}</ol>
    <div class="also">{t(('Also from AI', 'AI 쪽 경험'), 'span', 'lbl')}<div class="chips">{also}</div></div>
  </div>
  <div class="card now-bar">
    {t(('Now', '지금'), 'span', 'now-h')}
    <ul class="now-items">{now}</ul>
    <a class="scroll-cue" href="#work">{t(('Selected work', '대표 작업'))}{ic('down')}</a>
  </div>
</div>
</section>'''


def status_badge(p):
    return t(p.get('live_label', ('Ongoing', '진행 중')), 'span', 'badge b-live') if p['status'] == 'live' else ''


def card_value(p, ko=False):
    return p.get('card_v_ko', p['card_v']) if ko else p['card_v']


def wcard(p, prefix=''):
    v_en, v_ko = p['card_v'], p.get('card_v_ko', p['card_v'])
    v = f'<span class="w-v" data-ko="{e(v_ko)}">{e(v_en)}</span>' if v_ko != v_en else f'<span class="w-v">{e(v_en)}</span>'
    return f'''<a class="card wcard tilt dom-{p['dom']}" data-tilt href="{prefix}projects/{p['slug']}.html">
  <div class="thumb">{ILLS[p['slug']]()}</div>
  <div class="w-body">
    <div class="w-meta">{t(p.get('badge', p['outcome']), 'span', 'badge b-acc')}{status_badge(p)}</div>
    <p class="w-kicker"><span class="dot"></span>{e(p['short'])}</p>
    {t(p['title'], 'h3')}
    {t(p['card_q'], 'p', 'w-q')}
    <div class="w-res"><div class="w-res-inner">{v}{t(p['card_l'], 'span', 'w-l')}</div></div>
    <div class="w-foot">{t(p['role'])}<span class="go">{t(('Read', '자세히'))}{ic('arrow')}</span></div>
  </div>
</a>'''


def mcard(p):
    return f'''<a class="card mcard tilt dom-{p['dom']}" data-tilt href="projects/{p['slug']}.html">
  <div class="thumb">{ILLS[p['slug']]()}</div>
  <div class="m-body">
    <p class="w-kicker"><span class="dot"></span>{e(p['short'])}</p>
    {t(p['title'], 'h3')}
    {t(p['card_q'], 'p', 'm-q')}
    <p class="m-foot">{t(p['role'])}{NB}· {t(p['period'])}</p>
  </div>
</a>'''


PAPERS = [
    dict(slug='gdtr', venue=('ICML GenBio ’26 · Oral', 'ICML GenBio ’26 · Oral'), note=('Workshop · author', '워크숍 · 저자'),
         title='Layer-wise Settling Depth Reveals Biological Grammar in Genomic Foundation Models',
         authors='Y. Cho, <b>J. Kang</b>, S. Park, S. Kim',
         links=[('OpenReview', 'https://openreview.net/forum?id=Z9h1jiPbus'), ('bioRxiv', 'https://www.biorxiv.org/content/10.64898/2026.07.14.738370v1'),
                ('Code', 'https://github.com/YAICON-8th-Think-Deep-in-Genome/TDiG')]),
    dict(slug='ftf-vtg', venue=('IEIE ’25', 'IEIE ’25'), note=('Summer Annual Conference · first author', '하계종합학술대회 · 제1저자'),
         title='Frame-Level Understanding for Lightweight and Explainable Video Temporal Grounding',
         authors='<b>J. Kang</b>, S. Kim, H. Noh, H. Yang',
         links=[('Code', gh('02_Paper/FTFVTG/code')), ('PDF', 'https://github.com/heoneyzi/Paper/blob/main/FTFVTG/Frame-Level%20Understanding%20for%20Lightweight%20and%20Explainable%20Video%20Temporal%20Grounding.pdf')]),
    dict(slug='bi-cot', venue=('KAIC ’25', 'KAIC ’25'), note=('6th Korea AI Conference · first author', '제6회 한국인공지능학술대회 · 제1저자'),
         title='Plug-and-Play Bi-CoT: Self-Aware Forward Reasoning and Reverse Verification for Explainable Multi-Hop QA',
         authors='<b>J. Kang</b>, S. Jung',
         links=[('Code', gh('02_Paper/Bi-CoT/code')), ('PDF', 'https://github.com/heoneyzi/Paper/blob/main/Bi-CoT/Plug-and-Play%20Bi-CoT%20-%20Self-Aware%20Forward%20Reasoning%20and%20Reverse%20Verification%20for%20Explainable%20Multi-Hop%20QA.pdf')]),
]


def papers():
    """One grid for every paper: venue column | title · authors · links. Links sit under the authors so the
    rows line up no matter how many links a paper has."""
    items = []
    for pp in PAPERS:
        links = f'<a class="is-story" href="projects/{pp["slug"]}.html">{ic("arrow")}{t(("Story", "소개"))}</a>' + ''.join(
            f'<a href="{u}" target="_blank" rel="noopener">{ic("ext")}<span>{lab}</span></a>' for lab, u in pp['links'])
        # 'ICML GenBio ’26 · Oral' -> venue badge + a solid 'Oral' badge
        v_en, v_ko = [x.split(' · ') for x in pp['venue']]
        badges = t((v_en[0], v_ko[0]), 'span', 'badge b-acc') + ''.join(
            t((a, b), 'span', 'badge b-solid') for a, b in zip(v_en[1:], v_ko[1:]))
        # 'Summer Annual Conference · first author' -> name line + role line
        n_en, n_ko = [x.rsplit(' · ', 1) for x in pp['note']]
        first = 'first' in n_en[1].lower()
        role = (n_en[1][:1].upper() + n_en[1][1:], n_ko[1])
        items.append(f'''<li class="card paper lift">
  <div class="venue"><div class="v-badges">{badges}</div>{t((n_en[0], n_ko[0]), 'span', 'v-name')}{t(role, 'span', 'v-role is-first' if first else 'v-role')}</div>
  <div class="p-main"><h3><a href="projects/{pp['slug']}.html">{tidy(e(pp['title']))}</a></h3><p class="authors">{pp['authors']}</p>
  <div class="p-links">{links}</div></div>
</li>''')
    return '<ol class="papers">' + ''.join(items) + '</ol>'


JOURNEY = [
    dict(y='2023–24', t=('deep daiv. · first team projects', 'deep daiv. · 첫 팀 프로젝트'), items=[
        (('Nov 2023 – Jan 2024', '2023.11 – 2024.01'), ('Persona chatbot (RAG)', '페르소나 챗봇 (RAG)'), ('Team Lead · NLP', '팀장 · NLP'), 'persona-chatbot'),
        (('Spring 2024', '2024 봄'), ('Lightweight BU-Net', '경량 BU-Net'), ('Team Lead · Medical AI', '팀장 · 의료 AI'), 'bu-net'),
        (('Summer 2024', '2024 여름'), ('Taste Trip recommender', 'Taste Trip 추천 시스템'), ('Team Lead · RecSys', '팀장 · 추천 시스템'), 'taste-trip'),
        (('Aug – Dec 2024', '2024.08 – 12'), ('Magazine vol.0', '매거진 vol.0'), ('AI Magazine Editor', 'AI 매거진 에디터'), 'writing'),
    ]),
    dict(y='2025', t=('First papers', '첫 논문'), items=[
        (('Nov 2024 – 2025', '2024.11 – 2025'), ('Video grounding → IEIE 2025 paper', '비디오 그라운딩 → IEIE 2025 논문'), ('Team Lead · first author', '팀장 · 제1저자'), 'ftf-vtg'),
        (('2025', '2025'), ('Bi-CoT → KAIC 2025 paper', 'Bi-CoT → KAIC 2025 논문'), ('First author', '제1저자'), 'bi-cot'),
        (('Mar 2025 – Jan 2026', '2025.03 – 2026.01'), ('Weekly AI newsletter · 9 issues', '주간 AI 뉴스레터 · 9편'), ('Newsletter Writer', '뉴스레터 필진'), 'writing'),
        (('May 2025 – May 2026', '2025.05 – 2026.05'), ('Multimodal hallucination study', '멀티모달 환각 공부'), ('Individual study', '개인 공부'), 'hallucination'),
    ]),
    dict(y='2026', t=('Into genomics', '유전체로'), items=[
        (('Jan 2026', '2026.01'), ('Joined Yonsei AI (YAI)', 'Yonsei AI(YAI) 합류'), ('Functional Genomics study', 'Functional Genomics 스터디'), 'genomics-study'),
        (('Feb 2026', '2026.02'), ('CAFA 6 · Bronze Medal', 'CAFA 6 · 동메달'), ('Team member', '팀원'), 'cafa6'),
        (('Apr – Jun 2026', '2026.04 – 06'), ('GDTR → ICML GenBio Oral', 'GDTR → ICML GenBio Oral'), ('Author', '저자'), 'gdtr'),
        (('Jun 2026', '2026.06'), ('Functional Genomics Team Lead', 'Functional Genomics 팀장'), ('Yonsei AI', 'Yonsei AI'), 'genomics-study'),
        (('Sep 2026', '2026.09'), ('GeoFlowAgent', 'GeoFlowAgent'), ('Independent research · completed', '개인 연구 · 완료'), 'geoflowagent'),
    ]),
    dict(y='Now', y_ko='지금', t=('Leading', '이끄는 중'), items=[
        (('Jul 2026 –', '2026.07 –'), ('Vice President, YAI', 'YAI 부회장'), ('Yonsei AI', 'Yonsei AI'), None),
        (('Aug 2026 –', '2026.08 –'), ('Virtual Cell Challenge 2026', 'Virtual Cell Challenge 2026'), ('Team Lead · 6 people', '팀장 · 6인'), 'vcc2026'),
        (('2026 –', '2026 –'), ('PhenoFocus · main round', 'PhenoFocus · 본선 진출'), ('Team Lead · 4 people', '팀장 · 4인'), 'phenofocus'),
        (('Sep 2026 –', '2026.09 –'), ('GDTR follow-up research', 'GDTR 후속 연구'), ('Ongoing · own paper project', '진행 중 · 개인 논문 프로젝트'), 'gdtr'),
    ]),
]


def journey():
    cols = []
    for c in JOURNEY:
        lis = []
        for when, what, role, slug in c['items']:
            dom = BY_SLUG[slug]['dom'] if slug else 'dna'
            what_html = f'<a href="projects/{slug}.html" data-ko="{e(what[1])}">{what[0]}</a>' if slug else t(what)
            lis.append(f'<li class="dom-{dom}">{t(when, "span", "j-when")}<span class="j-what">{what_html}</span>{t(role, "span", "j-role")}</li>')
        yk = c.get('y_ko')
        y = f'<b data-ko="{e(yk)}">{c["y"]}</b>' if yk else f'<b>{c["y"]}</b>'
        cols.append(f'<div class="card j-col"><h3>{y}{t(c["t"])}</h3><ul class="j-list">{"".join(lis)}</ul></div>')
    return '<div class="journey">' + ''.join(cols) + '</div>'


def about():
    bring = [
        ('Real biological questions turned into AI experiments that can be checked and reproduced', '자연의 규칙을 묻는 생물학 질문을 검증 · 재현 가능한 AI 실험으로 설계'),
        ('Careful evaluation — held-out chromosomes, unseen cell lines, pre-registered tests', '꼼꼼한 평가 설계 — 보지 않은 염색체, 처음 보는 세포주, 사전등록한 테스트'),
        ('Leading teams of three to six and explaining research to broad audiences', '3–6인 팀을 이끌고, 연구를 누구나 이해할 수 있게 전달'),
    ]
    kit = ['Python', 'PyTorch', 'Hugging Face', 'NumPy · SciPy', 'scikit-learn', 'Scanpy · AnnData', 'Evo 2', 'ESM · ProtT5', 'RDKit', 'Slurm · GPU clusters', 'Git · pytest']
    return f'''<div class="about">
  <div class="card vision-card">
    {t(('From tasks we design<br>to rules nature wrote.', '사람이 만든 과제에서,<br>자연이 쓴 규칙으로.'), 'h3')}
    {t(('Most AI tasks are designed by people, and so are their answers. In biology the rules were written by nature, and no one hands them over: a DNA model trained only to predict the next base picks up the grammar of splicing, and a cell that loses a gene responds by laws we are still learning. I started asking biological questions to work on real tasks like these — finding those rules is what excites me most.', '대부분의 AI 과제는 사람이 설계하고, 정답도 사람이 정합니다. 생물학에서는 규칙을 자연이 썼고, 아무도 그 규칙을 미리 알려 주지 않습니다. 다음 염기만 맞히도록 학습한 DNA 모델이 유전자가 이어 붙는 문법을 스스로 익히고, 유전자를 잃은 세포는 아직 우리가 다 알지 못하는 법칙에 따라 반응합니다. 저는 이런 진짜 과제를 풀고 싶어 생물학의 질문을 시작했고, 그 규칙을 찾아가는 일에 가장 큰 흥미를 느낍니다.'), 'p', 'vq')}
    {t(('I am an Electrical &amp; Electronic Engineering student at Yonsei University, focused on medical AI — genomics and AI-driven drug discovery. My projects follow biological information from DNA to cells, proteins and drugs: what a DNA model has learned about the genome, how an unseen cell responds to a knockdown, which compounds share a mechanism.', '연세대학교 전기전자공학부에서 공부하며 의료 AI, 특히 유전체와 AI 신약 개발에 집중하고 있습니다. DNA 모델이 유전체에 대해 무엇을 배웠는지, 처음 보는 세포가 유전자 억제에 어떻게 반응하는지, 어떤 화합물이 같은 작용 기전을 공유하는지처럼, DNA에서 세포·단백질·약물로 이어지는 생물학 정보의 흐름을 따라 프로젝트를 이어 왔습니다.'), 'p')}
    {t(('Leading teams and writing about AI for a general audience taught me to explain ideas clearly and to build with others. The same habit — show every step and check it — runs through all of my work.', '팀을 이끌고 일반 독자를 위한 AI 글을 쓰면서, 아이디어를 명확하게 설명하고 함께 만드는 법을 배웠습니다. 모든 단계를 보여 주고 확인하는 습관이 제 모든 작업에 이어져 있습니다.'), 'p')}
  </div>
  <div class="card side-card">
    {t(('What I bring', '함께 연구할 때의 강점'), 'h3')}
    <ul class="bring">{''.join(f'<li>{ic("check")}{t(b)}</li>' for b in bring)}</ul>
    {t(('Research toolkit', '연구 도구'), 'h3')}
    <ul class="kit">{''.join(f'<li>{k}</li>' for k in kit)}</ul>
    {t(('Education', '학력'), 'h3')}
    <div class="edu">{ic('cap')}<div><b data-ko="연세대학교">Yonsei University</b>{t(('B.S. candidate, Electrical &amp; Electronic Engineering · expected Feb 2028', '전기전자공학부 학사과정 · 2028년 2월 졸업 예정'))}</div></div>
  </div>
</div>
<div class="card contact" id="contact">
  <div>
    {t(('Let’s start with a good question.', '좋은 질문으로 연결되고 싶습니다.'), 'h3')}
    {t(('For conversations about biomedical AI, research projects and ideas. Based in Seoul, Republic of Korea.', 'Biomedical AI 연구, 프로젝트, 아이디어에 관해 편하게 연락해 주세요. 서울, 대한민국.'), 'p')}
    <a class="mail" href="mailto:{EMAIL}">{ic('mail')}{EMAIL}</a>
  </div>
  <div class="c-links">
    <a class="btn" href="{GITHUB}" target="_blank" rel="noopener">{ic('code')}<span>GitHub</span></a>
    <a class="btn" href="{LINKEDIN}" target="_blank" rel="noopener">{ic('user')}<span>LinkedIn</span></a>
    <a class="btn" href="{CV}" target="_blank" rel="noopener">{ic('file')}<span>CV (PDF)</span></a>
    <a class="btn btn-primary" href="{REPO}" target="_blank" rel="noopener">{ic('github')}{t(('GitHub projects', 'GitHub 프로젝트'))}</a>
  </div>
</div>'''


def sec_head(num, sid, label, title, desc):
    return f'''<header class="sec-head">
  <div><p class="eyebrow">{num} · {t(label)}</p>{t(title, 'h2', extra=f' id="{sid}-h"')}</div>
  {t(desc, 'p')}
</header>'''


def index_page():
    work = ''.join(wcard(BY_SLUG[s]) for s in FEATURED)
    more = ''.join(mcard(BY_SLUG[s]) for s in MORE)
    study = ''.join(wcard(BY_SLUG[s]) for s in STUDY)
    body = f'''<main id="main">
{cover()}
<section class="section" id="work" aria-labelledby="work-h">
<div class="wrap">
{sec_head('01', 'work', ('Work', '연구·프로젝트'), ('Selected work', '대표 작업'), ('Each card opens a short story: the question, what I did, what we found — and where it leads next.', '카드를 누르면 짧은 이야기가 열립니다. 질문, 한 일, 결과, 그리고 다음 방향까지.'))}
<div class="work-grid">{work}</div>
{t(('More projects', '다른 프로젝트'), 'h3', 'sub-h')}
<div class="more-grid">{more}</div>
</div>
</section>
<section class="section" id="papers" aria-labelledby="papers-h">
<div class="wrap">
{sec_head('02', 'papers', ('Papers', '논문'), ('Publications', '논문'), ('Three accepted papers — two as first author.', '채택 논문 3편, 그중 2편은 제1저자입니다.'))}
{papers()}
</div>
</section>
<section class="section" id="study" aria-labelledby="study-h">
<div class="wrap">
{sec_head('03', 'study', ('Study & writing', '공부·글'), ('Study &amp; writing', '공부와 글'), ('How I learn a field: read, write it up, argue about it in a team — then turn the open questions into experiments.', '새 분야는 이렇게 익힙니다. 논문을 읽고, 정리하고, 팀에서 토론한 뒤, 남은 질문을 실험으로 옮깁니다.'))}
<div class="study-grid">{study}</div>
</div>
</section>
<section class="section" id="journey" aria-labelledby="journey-h">
<div class="wrap">
{sec_head('04', 'journey', ('Journey', '걸어온 길'), ('From a club project to genomics research', '동아리 프로젝트에서 유전체 연구까지'), ('Team lead in six projects since 2023; Vice President of Yonsei AI since July 2026.', '2023년부터 여섯 개 프로젝트의 팀장을 맡았고, 2026년 7월부터 Yonsei AI 부회장입니다.'))}
{journey()}
</div>
</section>
<section class="section" id="about" aria-labelledby="about-h">
<div class="wrap">
{sec_head('05', 'about', ('About', '소개'), ('About &amp; vision', '소개와 비전'), ('Who I am, what I want to build, and how to reach me.', '제가 누구인지, 무엇을 만들고 싶은지, 그리고 연락처.'))}
{about()}
</div>
</section>
</main>'''
    crumbs = '<a href="index.html">heoneyzi</a><span class="sep">/</span><span aria-current="page" data-ko="포트폴리오">portfolio</span>'
    return page('', 'Jiheon Kang · Biomedical AI Researcher', '강지헌 · Biomedical AI 연구자',
                'Jiheon Kang (강지헌), Yonsei University — moving beyond artificial AI tasks toward real ones: finding nature’s rules in DNA, cells and proteins. Papers, projects and study notes.',
                SITE, body, crumbs)


# ------------------------------------------------------------------------------------------------ project page
def project_page(i):
    p = PROJECTS[i]
    prev_p = PROJECTS[i - 1]
    next_p = PROJECTS[(i + 1) % len(PROJECTS)]
    g = p['glance']
    steps = ''.join(f'<li><b data-ko="{e(ti[1])}">{ti[0]}</b>{t(tx)}</li>' for ti, tx in p['steps'])
    kpi_ko = p.get('kpi_ko', {})
    kpis = ''.join(
        f'<div class="kpi"><p class="kpi-v"{(" data-ko=" + chr(34) + e(kpi_ko[v]) + chr(34)) if v in kpi_ko else ""}>{e(v)}</p>{t(l, "p", "kpi-l")}{t(n, "p", "kpi-n")}</div>'
        for v, l, n in p['kpis'])
    scope = f'<p class="scope">{ic("info")}{t(p["scope"])}</p>' if p.get('scope') else ''
    question = ''.join(t(q, 'p') for q in p['question'])
    facts = f'''<dl class="facts">
  <div><dt data-ko="역할">Role</dt><dd data-ko="{e(p['role'][1])}">{p['role'][0]}</dd></div>
  <div><dt data-ko="기간">Period</dt><dd data-ko="{e(p['period'][1])}">{p['period'][0]}</dd></div>
  <div class="full"><dt data-ko="성과">Outcome</dt><dd data-ko="{e(p['outcome'][1])}">{p['outcome'][0]}</dd></div>
  <div class="full"><dt data-ko="팀">Team</dt><dd data-ko="{e(p['team'][1])}">{p['team'][0]}</dd></div>
</dl>'''
    issues = ''
    if p.get('issues'):
        rows = ''.join(
            f'<div><dt>{num} · {date}</dt><dd><a href="{u}" target="_blank" rel="noopener" lang="ko">{e(ko)}</a><br><span style="color:var(--text-3);font-size:14px">{e(en)}</span></dd></div>'
            for num, date, ko, en, u in p['issues'])
        issues = f'''<section class="st-row"><h2>{t(('05 · Read', '05 · 읽기'), 'small')}{t(('The nine issues', '뉴스레터 9편'))}</h2>
<div class="st-body"><dl class="facts">{rows}</dl></div></section>'''
    gh_path, gh_label = p['gh']
    link_btns = ''.join(
        f'<a class="btn" href="{u}" target="_blank" rel="noopener">{ic("ext")}{t(lab)}</a>' for kind, u, lab in p['links'])
    body = f'''<main id="main" class="proj dom-{p['dom']}">
<div class="wrap">
  <a class="back" href="../index.html#work">{ic('arrow')}{t(('All work', '전체 작업'))}</a>
  <div class="p-head">
    <div>
      <p class="p-kicker"><span class="dot"></span>{t(p['kicker'])}</p>
      <p class="p-short">{e(p['short'])}</p>
      {t(p['title'], 'h1')}
      {t(p['lede'], 'p', 'p-lede')}
      <div class="p-badges">{t(p['outcome'], 'span', 'badge b-acc')}{status_badge(p)}{t(p['role'], 'span', 'badge')}{t(p['period'], 'span', 'badge')}</div>
    </div>
    <figure class="card p-hero" style="margin:0">{ILLS[p['slug']]()}</figure>
  </div>
  <div class="glance">
    <section class="card g-card"><h2><span class="k">1</span>{t(('Topic', '주제'))}</h2>{t(g['topic'], 'p')}</section>
    <section class="card g-card"><h2><span class="k">2</span>{t(('What I did', '한 일'))}</h2>{t(g['did'], 'p')}</section>
    <section class="card g-card"><h2><span class="k">3</span>{t(('Result', '결과'))}</h2>{t(g['result'], 'p')}</section>
  </div>
  <div class="p-story">
    <section class="st-row"><h2>{t(('Vision', '비전'), 'small')}{t(('Why it matters to me', '이 연구가 제게 중요한 이유'))}</h2>
      <div class="st-body"><blockquote class="vision" style="margin:0">{t(p['vision'], 'span')}</blockquote><p class="vision-by">— Jiheon Kang</p></div></section>
    <section class="st-row"><h2>{t(('01 · Background', '01 · 배경'), 'small')}{t(('The question', '질문'))}</h2><div class="st-body">{question}</div></section>
    <section class="st-row"><h2>{t(('02 · Approach', '02 · 방법'), 'small')}{t(('How it works', '어떻게 했나'))}</h2><div class="st-body"><ol class="steps">{steps}</ol></div></section>
    <section class="st-row"><h2>{t(('03 · Results', '03 · 결과'), 'small')}{t(('What we found', '무엇을 알아냈나'))}</h2><div class="st-body"><div class="kpis">{kpis}</div>{scope}</div></section>
    <section class="st-row"><h2>{t(('04 · Team', '04 · 팀'), 'small')}{t(('Role &amp; credits', '역할과 팀'))}</h2><div class="st-body">{facts}</div></section>
    {issues}
  </div>
  <aside class="card cta">
    <div>{t(('Want the details?', '더 자세히 보고 싶다면'), 'h2')}{t(p.get('cta', ('Experiments, figures, notes and code live in the project repositories on GitHub.', '실험, 그림, 노트, 코드는 GitHub의 각 프로젝트 저장소에 정리되어 있습니다.')), 'p')}</div>
    <div class="cta-links"><a class="btn btn-primary" href="{gh(gh_path)}" target="_blank" rel="noopener">{ic('github')}{t(gh_label)}</a>{link_btns}</div>
  </aside>
  <nav class="pn" aria-label="More projects" data-ko-aria="다른 프로젝트">
    <a class="card tilt dom-{prev_p['dom']}" data-tilt href="{prev_p['slug']}.html"><small data-ko="← 이전">← Previous</small><b>{e(prev_p['short'])}</b></a>
    <a class="card tilt next dom-{next_p['dom']}" data-tilt href="{next_p['slug']}.html"><small data-ko="다음 →">Next →</small><b>{e(next_p['short'])}</b></a>
  </nav>
</div>
</main>'''
    crumbs = f'<a href="../index.html">heoneyzi</a><span class="sep">/</span><a href="../index.html#work" data-ko="작업">work</a><span class="sep">/</span><span aria-current="page">{e(p["slug"])}</span>'
    title = f"{p['short']} · Jiheon Kang"
    title_ko = f"{p['short']} · 강지헌"
    desc = p['lede'][0]
    return page('../', title, title_ko, desc, f"{SITE}projects/{p['slug']}.html", body, crumbs)


FAVICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#008080"/><text x="9" y="45" font-family="Arial,Helvetica,sans-serif" font-size="40" font-weight="700" letter-spacing="-4" fill="#ffffff">jk.</text></svg>\n'


def main():
    os.makedirs(os.path.join(OUT, 'assets'), exist_ok=True)
    os.makedirs(os.path.join(OUT, 'projects'), exist_ok=True)
    shutil.copy(os.path.join(HERE, 'site.css'), os.path.join(OUT, 'assets', 'site.css'))
    shutil.copy(os.path.join(HERE, 'site.js'), os.path.join(OUT, 'assets', 'site.js'))
    with open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_page())
    for i, p in enumerate(PROJECTS):
        with open(os.path.join(OUT, 'projects', p['slug'] + '.html'), 'w', encoding='utf-8') as f:
            f.write(project_page(i))
    with open(os.path.join(OUT, 'favicon.svg'), 'w') as f:
        f.write(FAVICON)
    urls = [SITE] + [f'{SITE}projects/{p["slug"]}.html' for p in PROJECTS]
    with open(os.path.join(OUT, 'sitemap.xml'), 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                + ''.join(f'  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n' for u in urls) + '</urlset>\n')
    with open(os.path.join(OUT, 'robots.txt'), 'w') as f:
        f.write(f'User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n')
    open(os.path.join(OUT, '.nojekyll'), 'w').close()
    print('built', OUT, len(PROJECTS), 'project pages')


if __name__ == '__main__':
    main()
