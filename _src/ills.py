# -*- coding: utf-8 -*-
"""Concept illustrations (inline SVG, 480x270). Colours come from CSS classes in site.css,
so the same drawing works in dark and light themes. Text with class 'lbl' is hidden in card thumbnails."""
import math
from html import escape

W, H = 480, 270


def esc(s):
    return escape(s, quote=True)


def txt(x, y, en, ko=None, cls='t-l', anchor='start', lbl=True, extra=''):
    ko_attr = f' data-ko="{esc(ko)}"' if ko else ''
    c = cls + (' lbl' if lbl else '')
    return f'<text x="{x}" y="{y}" class="{c}" text-anchor="{anchor}"{ko_attr}{extra}>{esc(en)}</text>'


def arrow(x1, y1, x2, y2, cls='i-ln2', w=2, head=7, dash=None):
    ang = math.atan2(y2 - y1, x2 - x1)
    hx1 = x2 - head * math.cos(ang - 0.45)
    hy1 = y2 - head * math.sin(ang - 0.45)
    hx2 = x2 - head * math.cos(ang + 0.45)
    hy2 = y2 - head * math.sin(ang + 0.45)
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2:.1f}" y2="{y2:.1f}" class="{cls}" stroke-width="{w}" stroke-linecap="round"{d}/>'
            f'<path d="M{hx1:.1f} {hy1:.1f} L{x2:.1f} {y2:.1f} L{hx2:.1f} {hy2:.1f}" class="{cls}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" fill="none"/>')


def head_at(x, y, ang, cls, w=2, head=7):
    hx1 = x - head * math.cos(ang - 0.45)
    hy1 = y - head * math.sin(ang - 0.45)
    hx2 = x - head * math.cos(ang + 0.45)
    hy2 = y - head * math.sin(ang + 0.45)
    return f'<path d="M{hx1:.1f} {hy1:.1f} L{x} {y} L{hx2:.1f} {hy2:.1f}" class="{cls}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'


def svg(body, label_en, label_ko):
    return (f'<svg class="ill" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(label_en)}" data-ko-aria="{esc(label_ko)}" '
            f'preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">'
            f'<rect class="i-bg" x="0" y="0" width="{W}" height="{H}"/>' + body + '</svg>')


# ------------------------------------------------------------------------------------------------ GDTR
def ill_gdtr():
    b = []
    # double helix on the left
    cx, amp, y0, y1, period = 42, 15, 30, 240, 105
    ptsA, ptsB = [], []
    for i in range(0, 211, 3):
        y = y0 + i
        s = math.sin(2 * math.pi * i / period)
        ptsA.append(f'{cx + amp * s:.1f},{y}')
        ptsB.append(f'{cx - amp * s:.1f},{y}')
    for i in range(6, 211, 13):
        s = math.sin(2 * math.pi * i / period)
        if abs(s) > 0.2:
            b.append(f'<line x1="{cx + amp * s:.1f}" y1="{y0 + i}" x2="{cx - amp * s:.1f}" y2="{y0 + i}" class="i-ln" stroke-width="2.5"/>')
    b.append(f'<polyline points="{" ".join(ptsB)}" class="i-ln2 i-dim" stroke-width="3" stroke-linecap="round"/>')
    b.append(f'<polyline points="{" ".join(ptsA)}" class="i-accs" stroke-width="3" stroke-linecap="round"/>')
    # layer lanes
    x0, x1 = 128, 452
    lane_y = lambda i: 206 - i * 24
    for i in range(8):
        b.append(f'<rect x="{x0}" y="{lane_y(i)}" width="{x1 - x0}" height="16" rx="5" class="i-box" stroke-width="1"/>')
    b.append(txt(120, 50, 'layer 32', '32층', 't-s', 'end'))
    b.append(txt(120, 218, 'layer 1', '1층', 't-s', 'end'))
    # token columns with settling depth
    letters = 'CAGTAACT'
    settle = [5, 6, 2, 2, 5, 7, 6, 4]
    top_c = lane_y(7) + 8
    bot_c = lane_y(0) + 8
    for j in range(8):
        x = 150 + j * 42
        sy = lane_y(settle[j]) + 8
        b.append(f'<line x1="{x}" y1="{bot_c}" x2="{x}" y2="{sy}" class="i-ln2 i-dim" stroke-width="2" stroke-dasharray="2 4" stroke-linecap="round"/>')
        b.append(f'<line x1="{x}" y1="{sy}" x2="{x}" y2="{top_c}" class="i-accs" stroke-width="4" stroke-linecap="round"/>')
        splice = j in (2, 3)
        b.append(f'<circle cx="{x}" cy="{sy}" r="{7 if splice else 5.5}" class="i-acc"/>')
        b.append(f'<circle cx="{x}" cy="{sy}" r="{11 if splice else 0}" class="i-accs" stroke-width="1.5" opacity=".55"/>' if splice else '')
        cls = 't-m t-acc' if splice else 't-m'
        b.append(f'<text x="{x}" y="{242}" class="{cls}" text-anchor="middle" style="font-size:15px;font-weight:600">{letters[j]}</text>')
    # annotations
    b.append(f'<path d="M226 249 L226 255 L284 255 L284 249" class="i-accs lbl" stroke-width="1.5" fill="none"/>')
    b.append(txt(292, 264, 'splice site settles early', '스플라이스 자리는 일찍 정착', 't-s t-acc', 'start'))
    return svg(''.join(b), 'Layer stack of a DNA model: each DNA letter settles at a different depth; splice-site letters settle earlier.',
               'DNA 모델의 층: 글자마다 정착하는 깊이가 다르고, 스플라이스 자리는 더 일찍 정착합니다.')


# ------------------------------------------------------------------------------------------------ VCC
def ill_vcc():
    b = []
    # reference cell lines
    for (x, y) in ((186, 58), (214, 50), (242, 58)):
        b.append(f'<circle cx="{x}" cy="{y}" r="12" class="i-soft2"/><circle cx="{x}" cy="{y}" r="12" class="i-accs" stroke-width="1.5" opacity=".6"/>')
    b.append(txt(214, 28, 'measured in other cell lines', '다른 세포주에서 측정된 효과', 't-s', 'middle'))
    b.append(arrow(214, 74, 214, 108, 'i-accs', 2, 7, '4 4'))
    # the unseen cell
    b.append('<circle cx="94" cy="134" r="56" class="i-soft2"/><circle cx="94" cy="134" r="56" class="i-accs" stroke-width="2.5"/>')
    b.append('<circle cx="102" cy="126" r="21" class="i-soft"/><circle cx="102" cy="126" r="21" class="i-accs" stroke-width="1.5"/>')
    for (x, y, r) in ((66, 110, 4), (70, 160, 5), (118, 164, 4), (60, 138, 3), (130, 108, 3)):
        b.append(f'<circle cx="{x}" cy="{y}" r="{r}" class="i-acc" opacity=".55"/>')
    b.append('<circle cx="140" cy="86" r="12" class="i-box" stroke-width="1.5"/>')
    b.append('<text x="140" y="91" class="t-b" text-anchor="middle" style="font-size:14px">?</text>')
    b.append(txt(94, 214, 'unseen cell line', '처음 보는 세포주', 't-s', 'middle'))
    # knockdown chip
    b.append(arrow(152, 134, 170, 134, 'i-ln2', 2, 6))
    b.append('<rect x="172" y="114" width="86" height="40" rx="10" class="i-box" stroke-width="1.5"/>')
    b.append('<text x="201" y="139" class="t-m" text-anchor="middle" style="font-size:13px;font-weight:600">gene X</text>')
    b.append('<path d="M238 126 L238 142 M232 136 L238 142 L244 136" class="i-accs" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    b.append(txt(215, 172, 'knock down', '유전자 억제', 't-s', 'middle'))
    b.append(arrow(260, 134, 282, 134, 'i-ln2', 2, 6))
    # predicted response chart
    b.append('<rect x="286" y="46" width="172" height="176" rx="12" class="i-box" stroke-width="1"/>')
    base = 134
    vals = [18, -10, 34, 8, -26, 12, 46, -6, 22, -38, 14, 28, -14, 6]
    for i, v in enumerate(vals):
        x = 298 + i * 11.2
        if v >= 0:
            b.append(f'<rect x="{x:.1f}" y="{base - v}" width="7" height="{v}" rx="2" class="i-acc"/>')
        else:
            b.append(f'<rect x="{x:.1f}" y="{base}" width="7" height="{-v}" rx="2" class="i-c3"/>')
    b.append(f'<line x1="294" y1="{base}" x2="450" y2="{base}" class="i-ln2" stroke-width="1.2" stroke-dasharray="3 3"/>')
    b.append(txt(298, 68, 'predicted response', '예측한 반응', 't-s', 'start'))
    b.append(txt(372, 244, '400 cells × 18,533 genes', '세포 400개 × 유전자 18,533개', 't-s', 'middle'))
    return svg(''.join(b), 'An unseen cell line, a gene knock-down, effects borrowed from other cell lines, and the predicted expression response.',
               '처음 보는 세포주, 유전자 억제, 다른 세포주에서 빌려 온 효과, 그리고 예측한 발현 반응.')


# ------------------------------------------------------------------------------------------------ CAFA 6
def ill_cafa():
    b = []
    b.append('<rect x="22" y="52" width="156" height="166" rx="12" class="i-box" stroke-width="1"/>')
    seq = ['MKTAYIAKQR', 'QISFVKSHFS', 'RQLEERLGLI', 'EVQAPILSRV', 'GDGTQDNLSG', 'AEKAVQVKVK', 'ALPDAQFEVV']
    for i, s in enumerate(seq):
        b.append(f'<text x="36" y="{80 + i * 20}" class="t-m" style="font-size:14px;letter-spacing:1px">{s}</text>')
    b.append(txt(100, 240, 'amino-acid sequence', '아미노산 서열', 't-s', 'middle'))
    b.append(arrow(182, 135, 204, 135, 'i-ln2', 2, 6))
    b.append('<rect x="206" y="100" width="58" height="70" rx="14" class="i-soft"/><rect x="206" y="100" width="58" height="70" rx="14" class="i-accs" stroke-width="1.5"/>')
    for r in range(3):
        for c in range(3):
            b.append(f'<circle cx="{221 + c * 14}" cy="{117 + r * 18}" r="4" class="i-acc"/>')
    b.append(txt(235, 190, 'protein LM', '단백질 LM', 't-s', 'middle'))
    b.append(arrow(266, 135, 284, 135, 'i-ln2', 2, 6))
    # GO tree (one ontology): predicted path highlighted
    nodes = {
        'root': (388, 46, 96, ('function', '기능'), 'on'),
        'bind': (352, 100, 86, ('binding', '결합'), 'on'),
        'cat': (438, 100, 76, ('catalysis', '촉매'), 'off'),
        'nab': (366, 154, 142, ('nucleic acid binding', '핵산 결합'), 'on'),
        'dna': (358, 208, 104, ('DNA binding', 'DNA 결합'), 'on'),
    }
    edges = [('root', 'bind'), ('root', 'cat'), ('bind', 'nab'), ('nab', 'dna')]
    for a, c in edges:
        ax, ay = nodes[a][0], nodes[a][1] + 13
        cx_, cy = nodes[c][0], nodes[c][1] - 13
        on = nodes[a][4] == 'on' and nodes[c][4] == 'on'
        b.append(f'<path d="M{ax} {ay} C{ax} {(ay + cy) / 2} {cx_} {(ay + cy) / 2} {cx_} {cy}" class="{"i-accs" if on else "i-ln"}" stroke-width="{2.2 if on else 1.5}" fill="none"/>')
    for k, (x, y, w, lab, st) in nodes.items():
        if st == 'on':
            b.append(f'<rect x="{x - w / 2}" y="{y - 13}" width="{w}" height="26" rx="13" class="i-acc"/>')
            b.append(f'<text x="{x}" y="{y + 4.5}" class="t-s lbl" text-anchor="middle" style="font-weight:700;fill:var(--bg)" data-ko="{esc(lab[1])}">{esc(lab[0])}</text>')
        else:
            b.append(f'<rect x="{x - w / 2}" y="{y - 13}" width="{w}" height="26" rx="13" class="i-box" stroke-width="1.2"/>')
            b.append(f'<text x="{x}" y="{y + 4.5}" class="t-s lbl" text-anchor="middle" data-ko="{esc(lab[1])}">{esc(lab[0])}</text>')
    # medal
    b.append('<path d="M444 206 L436 236 L448 230 L456 242 L460 212 Z" class="i-c4" opacity=".75"/>')
    b.append('<circle cx="450" cy="206" r="15" class="i-c3"/><circle cx="450" cy="206" r="9" class="i-box" stroke-width="0" opacity=".35"/>')
    return svg(''.join(b), 'A protein sequence goes into a protein language model, which predicts Gene Ontology functions along the ontology tree.',
               '단백질 서열을 단백질 언어모델에 넣어, 온톨로지 트리를 따라 Gene Ontology 기능을 예측합니다.')


# ------------------------------------------------------------------------------------------------ PhenoFocus
def hexagon(cx, cy, r, rot=0):
    pts = []
    for k in range(6):
        a = math.radians(60 * k + rot)
        pts.append(f'{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}')
    return ' '.join(pts)


def pentagon(cx, cy, r, rot=-90):
    pts = []
    for k in range(5):
        a = math.radians(72 * k + rot)
        pts.append(f'{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}')
    return ' '.join(pts)


def ill_pheno():
    b = []
    # query molecule
    b.append(f'<polygon points="{hexagon(62, 76, 22, 30)}" class="i-accs" stroke-width="2.6" fill="none" stroke-linejoin="round"/>')
    b.append('<polyline points="81,65 104,54 124,66 146,55" class="i-accs" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    b.append('<line x1="124" y1="66" x2="124" y2="90" class="i-accs" stroke-width="2.6" stroke-linecap="round"/>')
    b.append('<circle cx="146" cy="55" r="4" class="i-acc"/>')
    b.append(txt(86, 122, 'one hit', '효과가 확인된 화합물', 't-s', 'middle'))
    # cell painting tile
    b.append('<rect x="28" y="140" width="116" height="92" rx="10" style="fill:#0c1320"/>')
    for (x, y, r) in ((54, 164, 13), (92, 160, 11), (120, 190, 14), (62, 206, 12), (96, 214, 9), (128, 152, 7)):
        b.append(f'<circle cx="{x}" cy="{y}" r="{r}" style="fill:#2eb8ae" opacity=".35"/>')
        b.append(f'<circle cx="{x + 1}" cy="{y}" r="{r * .45:.1f}" style="fill:#57a9e6" opacity=".9"/>')
    b.append(txt(86, 252, 'cell images', '세포 이미지', 't-s', 'middle'))
    b.append(arrow(152, 72, 180, 96, 'i-ln2', 2, 6))
    b.append(arrow(150, 186, 180, 164, 'i-ln2', 2, 6))
    # learned space
    b.append('<rect x="184" y="44" width="150" height="186" rx="14" class="i-soft2"/><rect x="184" y="44" width="150" height="186" rx="14" class="i-ln" stroke-width="1.2" stroke-dasharray="4 4"/>')
    grey = [(204, 70), (226, 92), (300, 70), (318, 96), (214, 128), (298, 132), (204, 200), (236, 214), (312, 206), (284, 216), (320, 160), (206, 164), (296, 186), (230, 60)]
    for (x, y) in grey:
        b.append(f'<circle cx="{x}" cy="{y}" r="4.5" class="i-ink" opacity=".55"/>')
    b.append('<circle cx="258" cy="146" r="34" class="i-accs" stroke-width="1.6" stroke-dasharray="5 4"/>')
    for (x, y) in ((250, 140), (270, 132), (262, 162)):
        b.append(f'<circle cx="{x}" cy="{y}" r="6" class="i-acc"/>')
    b.append(txt(259, 36, 'learned biology space', '학습된 생물학 공간', 't-s', 'middle'))
    b.append(arrow(294, 146, 346, 128, 'i-accs', 2.2, 7))
    # candidate with a different skeleton
    b.append(f'<polygon points="{pentagon(386, 114, 20)}" class="i-c2s" stroke-width="2.6" fill="none" stroke-linejoin="round"/>')
    b.append(f'<polygon points="{pentagon(420, 124, 20, -54)}" class="i-c2s" stroke-width="2.6" fill="none" stroke-linejoin="round"/>')
    b.append('<polyline points="438,108 452,90 468,96" class="i-c2s" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    b.append('<circle cx="468" cy="96" r="4" class="i-c2"/>')
    b.append(txt(412, 170, 'new skeleton,', '다른 골격,', 't-s', 'middle'))
    b.append(txt(412, 187, 'same biology', '같은 작용', 't-s t-acc', 'middle'))
    return svg(''.join(b), 'One active compound and cell images map into a learned biology space; a neighbour with a different chemical skeleton is retrieved.',
               '효과가 확인된 화합물과 세포 이미지를 학습된 생물학 공간에 놓고, 골격이 다른 이웃 화합물을 찾아냅니다.')


# ------------------------------------------------------------------------------------------------ GeoFlowAgent
def ill_geoflow():
    b = []
    for i, r in enumerate((40, 72, 104, 136, 168, 200)):
        b.append(f'<ellipse cx="300" cy="118" rx="{r}" ry="{r * .62:.0f}" class="i-grid" opacity="{.9 - i * .1:.2f}"/>')
    for gx in range(30, 470, 30):
        for gy in range(24, 260, 30):
            b.append(f'<circle cx="{gx}" cy="{gy}" r="1.2" class="i-ink" opacity=".35"/>')
    # one-shot plan (fails)
    b.append('<path d="M70 212 C 170 206 300 206 420 176" class="i-ln2" stroke-width="2.2" fill="none" stroke-dasharray="6 6"/>')
    b.append('<path d="M414 168 L428 184 M428 168 L414 184" class="i-c4s" stroke-width="3" stroke-linecap="round"/>')
    b.append(txt(360, 232, 'one-shot plan', '한 번에 세운 계획', 't-s', 'middle'))
    # replanned route
    pts = [(70, 212), (150, 170), (238, 150), (316, 96), (404, 64)]
    d = f'M{pts[0][0]} {pts[0][1]} ' + ' '.join(f'L{x} {y}' for x, y in pts[1:])
    b.append(f'<path d="{d}" class="i-accs" stroke-width="3" fill="none" stroke-linejoin="round" stroke-linecap="round"/>')
    for (x, y) in pts[1:4]:
        b.append(f'<rect x="{x - 13}" y="{y - 13}" width="26" height="26" rx="7" class="i-box" stroke-width="1.5"/>')
        b.append(f'<rect x="{x - 13}" y="{y - 13}" width="26" height="26" rx="7" class="i-accs" stroke-width="1.5"/>')
    # tiny tool glyphs
    x, y = pts[1]
    b.append(f'<circle cx="{x - 2}" cy="{y - 2}" r="5" class="i-accs" stroke-width="1.8"/><line x1="{x + 2}" y1="{y + 2}" x2="{x + 6}" y2="{y + 6}" class="i-accs" stroke-width="1.8" stroke-linecap="round"/>')
    x, y = pts[2]
    b.append(f'<ellipse cx="{x}" cy="{y - 5}" rx="7" ry="3" class="i-accs" stroke-width="1.6"/><path d="M{x - 7} {y - 5} V{y + 5} A7 3 0 0 0 {x + 7} {y + 5} V{y - 5}" class="i-accs" stroke-width="1.6" fill="none"/>')
    x, y = pts[3]
    b.append(f'<path d="M{x - 7} {y + 6} V{y - 1} M{x} {y + 6} V{y - 7} M{x + 7} {y + 6} V{y + 1}" class="i-accs" stroke-width="2.2" stroke-linecap="round"/>')
    # start + goal
    b.append('<circle cx="70" cy="212" r="10" class="i-box" stroke-width="2"/><circle cx="70" cy="212" r="3.5" class="i-ink2"/>')
    b.append(txt(70, 242, 'start', '시작', 't-s', 'middle'))
    b.append('<circle cx="410" cy="60" r="18" class="i-soft"/><circle cx="410" cy="60" r="11" class="i-accs" stroke-width="2"/><circle cx="410" cy="60" r="4.5" class="i-acc"/>')
    b.append(txt(440, 36, 'goal', '목표', 't-s', 'middle'))
    b.append(txt(196, 128, 'act → observe → replan', '실행 → 관찰 → 재계획', 't-s t-acc', 'middle'))
    return svg(''.join(b), 'A planner in an embedding map: the one-shot plan misses the goal; acting, observing and replanning reaches it.',
               '임베딩 지도 위의 계획: 한 번에 세운 계획은 목표를 놓치고, 실행·관찰·재계획은 목표에 닿습니다.')


# ------------------------------------------------------------------------------------------------ BU-Net
def ill_bunet():
    b = []
    scan = 'style="fill:#0e1114"'
    # MRI
    b.append(f'<rect x="16" y="58" width="112" height="150" rx="12" {scan}/>')
    b.append('<ellipse cx="72" cy="133" rx="44" ry="55" style="fill:#5d646c"/>')
    b.append('<ellipse cx="72" cy="133" rx="34" ry="44" style="fill:#7b828b" opacity=".7"/>')
    b.append('<path d="M80 110 C94 102 106 114 100 126 C94 138 82 136 78 128 C72 120 72 114 80 110 Z" style="fill:#d9dde2" opacity=".9"/>')
    b.append(txt(72, 230, 'MRI slice', 'MRI 슬라이스', 't-s', 'middle'))
    # U-Net
    enc = [(156, 72, 16, 58), (180, 108, 16, 44), (204, 140, 16, 32)]
    dec = [(284, 140, 16, 32), (308, 108, 16, 44), (332, 72, 16, 58)]
    for (x, y, w, h) in enc + dec:
        b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" class="i-box" stroke-width="1.4"/>')
    b.append('<rect x="230" y="176" width="44" height="30" rx="7" class="i-soft"/><rect x="230" y="176" width="44" height="30" rx="7" class="i-accs" stroke-width="1.8"/>')
    b.append('<path d="M238 191 H266 M252 182 V200" class="i-accs" stroke-width="2" stroke-linecap="round"/>')
    for (a, c) in zip(enc, reversed(dec)):
        y = a[1] + a[3] / 2
        b.append(f'<line x1="{a[0] + a[2] + 4}" y1="{y}" x2="{c[0] - 4}" y2="{y}" class="i-ln2" stroke-width="1.4" stroke-dasharray="3 4"/>')
    b.append('<path d="M164 132 L188 152 M188 154 L212 174 M220 176 L230 186 M274 186 L286 176 M300 172 L310 154 M324 152 L336 132" class="i-ln2" stroke-width="1.6" stroke-linecap="round"/>')
    b.append(txt(252, 232, 'U-Net + wide context', 'U-Net + 넓은 맥락', 't-s', 'middle'))
    b.append(arrow(132, 100, 150, 100, 'i-ln2', 2, 6))
    b.append(arrow(352, 100, 368, 100, 'i-ln2', 2, 6))
    # mask
    b.append(f'<rect x="372" y="58" width="92" height="150" rx="12" {scan}/>')
    b.append('<ellipse cx="418" cy="133" rx="36" ry="55" style="fill:none;stroke:#5d646c;stroke-width:2"/>')
    b.append('<path d="M416 104 C438 94 454 116 447 134 C440 152 418 150 413 139 C406 126 402 110 416 104 Z" class="i-c3" opacity=".75"/>')
    b.append('<path d="M424 113 C437 107 444 121 440 131 C436 140 424 138 422 131 C418 123 418 117 424 113 Z" class="i-c4"/>')
    b.append('<circle cx="431" cy="123" r="5.5" class="i-acc"/>')
    b.append(txt(418, 230, 'tumour mask', '종양 마스크', 't-s', 'middle'))
    return svg(''.join(b), 'An MRI slice goes through a U-shaped network with a wide-context bottleneck and comes out as a coloured tumour mask.',
               'MRI 슬라이스가 넓은 맥락 블록을 가진 U자형 네트워크를 거쳐 색칠된 종양 마스크가 됩니다.')


# ------------------------------------------------------------------------------------------------ FTF-VTG
def ill_vtg():
    b = []
    b.append('<rect x="22" y="26" width="436" height="84" rx="8" style="fill:#101316"/>')
    for i in range(22):
        x = 30 + i * 19.6
        b.append(f'<rect x="{x:.1f}" y="31" width="9" height="6" rx="1.5" style="fill:#2a3036"/>')
        b.append(f'<rect x="{x:.1f}" y="99" width="9" height="6" rx="1.5" style="fill:#2a3036"/>')
    for i in range(8):
        x = 32 + i * 53.2
        hot = i in (3, 4, 5)
        b.append(f'<rect x="{x:.1f}" y="42" width="46" height="52" rx="4" style="fill:{"#20403d" if hot else "#1b2126"}"/>')
        # a tiny figure: head + body
        fx = x + 23 + (i - 3.5) * 1.5
        b.append(f'<circle cx="{fx:.1f}" cy="60" r="5" style="fill:{"#7fe0d6" if hot else "#56606a"}"/>')
        b.append(f'<rect x="{fx - 6:.1f}" y="67" width="12" height="18" rx="4" style="fill:{"#7fe0d6" if hot else "#56606a"}"/>')
        if i >= 4:
            b.append(f'<rect x="{x + 34:.1f}" y="48" width="8" height="40" rx="1.5" style="fill:#3c464f"/>')
        if hot:
            b.append(f'<rect x="{x:.1f}" y="42" width="46" height="52" rx="4" class="i-accs" stroke-width="2"/>')
    b.append('<line x1="186" y1="112" x2="186" y2="238" class="i-accs" stroke-width="1.2" stroke-dasharray="3 4"/>')
    b.append('<line x1="346" y1="112" x2="346" y2="238" class="i-accs" stroke-width="1.2" stroke-dasharray="3 4"/>')
    b.append('<rect x="130" y="120" width="220" height="32" rx="16" class="i-box" stroke-width="1.2"/>')
    b.append(txt(240, 141, '“a man opens the door”', '“남자가 문을 연다”', 't-s', 'middle', lbl=False, extra=' style="font-style:italic;font-size:13.5px;fill:var(--text-2)"'))
    # similarity curve
    b.append('<rect x="186" y="170" width="160" height="66" rx="6" class="i-soft"/>')
    import random
    random.seed(7)
    pts = []
    for i in range(0, 421, 6):
        x = 30 + i
        t = (x - 186) / 160
        base = 226 - (48 if 0 <= t <= 1 else 0) * (math.sin(math.pi * min(max(t, 0), 1)) ** 0.35)
        base += random.uniform(-4, 4)
        pts.append(f'{x},{base:.1f}')
    b.append(f'<polyline points="{" ".join(pts)}" class="i-accs" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>')
    b.append('<line x1="26" y1="238" x2="456" y2="238" class="i-ln2" stroke-width="1.2"/>')
    b.append(txt(266, 218, 'predicted moment', '찾아낸 순간', 't-s t-acc', 'middle'))
    b.append(txt(30, 256, 'frame-by-frame similarity', '프레임별 유사도', 't-s', 'start'))
    b.append(txt(456, 256, 'time →', '시간 →', 't-s', 'end'))
    return svg(''.join(b), 'Video frames scored against the sentence; the similarity curve rises and falls around the described moment.',
               '문장과 영상 프레임의 유사도 곡선이 설명된 장면 앞뒤로 오르내립니다.')


# ------------------------------------------------------------------------------------------------ Bi-CoT
def ill_bicot():
    b = []
    y = 96
    nodes = [(40, 70, 'Q', 'q'), (148, 84, 'hop 1', 'h'), (266, 84, 'hop 2', 'h'), (392, 58, 'A', 'a')]
    for (x, w, lab, kind) in nodes:
        if kind == 'a':
            b.append(f'<rect x="{x}" y="{y - 22}" width="{w}" height="44" rx="22" class="i-acc"/>')
            b.append(f'<text x="{x + w / 2}" y="{y + 6}" class="t-b" text-anchor="middle" style="fill:var(--bg);font-size:17px">{lab}</text>')
        else:
            b.append(f'<rect x="{x}" y="{y - 22}" width="{w}" height="44" rx="22" class="i-box" stroke-width="1.5"/>')
            b.append(f'<text x="{x + w / 2}" y="{y + 6}" class="t-b" text-anchor="middle" style="font-size:{17 if kind == "q" else 14}px">{lab}</text>')
    for (a, c) in ((110, 148), (232, 266), (350, 392)):
        b.append(arrow(a + 4, y, c - 4, y, 'i-accs', 2.4, 7))
    b.append(txt(246, 56, 'reason forwards, step by step', '한 단계씩 앞으로 추론', 't-s t-acc', 'middle'))
    # evidence
    for cx in (190, 308):
        b.append(f'<rect x="{cx - 16}" y="136" width="32" height="40" rx="5" class="i-box" stroke-width="1.3"/>')
        for k in range(4):
            b.append(f'<line x1="{cx - 9}" y1="{146 + k * 7}" x2="{cx + (9 if k < 3 else 2)}" y2="{146 + k * 7}" class="i-ln2" stroke-width="1.5" opacity=".7"/>')
        b.append(f'<circle cx="{cx + 16}" cy="136" r="9" style="fill:var(--good)"/>')
        b.append(f'<path d="M{cx + 11.5} 136 L{cx + 15} 139.5 L{cx + 20.5} 132.5" style="stroke:var(--bg);stroke-width:2;fill:none;stroke-linecap:round;stroke-linejoin:round"/>')
        b.append(f'<line x1="{cx}" y1="{y + 24}" x2="{cx}" y2="134" class="i-ln2" stroke-width="1.3" stroke-dasharray="2 3"/>')
    b.append(txt(249, 196, 'evidence checked at every step', '단계마다 근거 확인', 't-s', 'middle'))
    # backward verification arc
    b.append('<path d="M421 120 C 421 262, 75 262, 75 124" class="i-c2s" stroke-width="2.4" fill="none"/>')
    b.append(head_at(75, 122, -math.pi / 2, 'i-c2s', 2.4, 8))
    b.append(txt(248, 262, 'verify backwards', '거꾸로 검증', 't-s', 'middle', extra=' style="fill:var(--c-cell)"'))
    return svg(''.join(b), 'A question is answered hop by hop with evidence checks, then the chain is verified backwards from the answer.',
               '질문을 단계별로 근거를 확인하며 풀고, 마지막에 답에서 질문 쪽으로 거꾸로 검증합니다.')


# ------------------------------------------------------------------------------------------------ Persona chatbot
def ill_persona():
    b = []
    b.append('<path d="M34 56 H100 L118 74 V178 H34 Z" class="i-box" stroke-width="1.4"/>')
    b.append('<path d="M100 56 V74 H118" class="i-ln" stroke-width="1.4" fill="none"/>')
    b.append('<circle cx="56" cy="88" r="10" class="i-soft"/>')
    for k in range(6):
        b.append(f'<line x1="{46 if k > 0 else 72}" y1="{88 + k * 14 if k else 84}" x2="{106 if k % 2 else 96}" y2="{88 + k * 14 if k else 84}" class="i-ln2" stroke-width="2" opacity=".6" stroke-linecap="round"/>')
    b.append(txt(76, 200, 'profile page', '프로필 문서', 't-s', 'middle'))
    b.append(arrow(124, 116, 150, 116, 'i-ln2', 2, 6))
    b.append('<circle cx="192" cy="112" r="36" class="i-soft"/><circle cx="192" cy="112" r="36" class="i-accs" stroke-width="2"/>')
    b.append('<circle cx="180" cy="104" r="4" class="i-inkt"/><circle cx="204" cy="104" r="4" class="i-inkt"/>')
    b.append('<path d="M178 122 Q192 134 206 122" style="stroke:var(--text);stroke-width:2.4;fill:none;stroke-linecap:round"/>')
    b.append('<rect x="146" y="164" width="92" height="56" rx="9" class="i-box" stroke-width="1.3"/>')
    for k, w in enumerate((70, 58, 64)):
        b.append(f'<line x1="158" y1="{180 + k * 13}" x2="{158 + w}" y2="{180 + k * 13}" class="i-ln2" stroke-width="2" opacity=".6" stroke-linecap="round"/>')
    b.append(txt(192, 240, 'one reusable prompt', '재사용 프롬프트', 't-s', 'middle'))
    b.append(arrow(232, 112, 258, 112, 'i-ln2', 2, 6))
    bubbles = [(300, 40, 156, 34, 'u'), (262, 86, 176, 42, 'p'), (320, 140, 136, 30, 'u'), (262, 182, 188, 42, 'p')]
    for (x, y, w, h, who) in bubbles:
        if who == 'u':
            b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" class="i-box" stroke-width="1.2"/>')
            b.append(f'<line x1="{x + 14}" y1="{y + h / 2}" x2="{x + w - 30}" y2="{y + h / 2}" class="i-ln2" stroke-width="2.2" opacity=".6" stroke-linecap="round"/>')
        else:
            b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" class="i-soft"/><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" class="i-accs" stroke-width="1.4"/>')
            b.append(f'<line x1="{x + 14}" y1="{y + 15}" x2="{x + w - 24}" y2="{y + 15}" class="i-accs" stroke-width="2.2" stroke-linecap="round"/>')
            b.append(f'<line x1="{x + 14}" y1="{y + 27}" x2="{x + w - 60}" y2="{y + 27}" class="i-accs" stroke-width="2.2" stroke-linecap="round" opacity=".7"/>')
    return svg(''.join(b), 'A profile document and one reusable prompt let a general chat model answer in a character’s voice.',
               '프로필 문서와 재사용 프롬프트 하나로 범용 채팅 모델이 캐릭터의 말투로 답합니다.')


# ------------------------------------------------------------------------------------------------ Taste Trip
def pin(x, y, cls):
    return f'<path d="M{x} {y} C{x - 16} {y - 18} {x - 18} {y - 30} {x - 18} {y - 38} A18 18 0 1 1 {x + 18} {y - 38} C{x + 18} {y - 30} {x + 16} {y - 18} {x} {y} Z" class="{cls}"/>'


def ill_taste():
    b = []
    b.append('<rect x="20" y="26" width="300" height="218" rx="14" class="i-box" stroke-width="1"/>')
    b.append('<path d="M20 196 C 90 176 150 214 220 190 C 270 172 300 184 320 176" class="i-c2s" stroke-width="12" opacity=".28" fill="none"/>')
    for d in ('M20 120 H320', 'M110 26 V244', 'M20 70 C 120 80 200 60 320 88', 'M230 26 C 220 110 250 160 236 244'):
        b.append(f'<path d="{d}" class="i-ln" stroke-width="7" fill="none" stroke-linecap="round" opacity=".8"/>')
    b.append('<path d="M112 150 C 150 150 180 96 232 92" class="i-accs" stroke-width="2.6" stroke-dasharray="6 6" fill="none"/>')
    b.append(pin(112, 172, 'i-acc'))
    b.append('<path d="M106 126 V142 M112 126 V142 M118 126 V142 M106 138 H118 M112 142 V150" style="stroke:var(--bg);stroke-width:1.8;fill:none;stroke-linecap:round"/>')
    b.append(pin(234, 112, 'i-c3'))
    b.append('<path d="M226 68 H240 V78 A7 7 0 0 1 226 78 Z M240 70 H244 A3 3 0 0 1 244 76 H240" style="stroke:var(--bg);stroke-width:1.8;fill:none;stroke-linejoin:round"/>')
    b.append(txt(170, 262, 'meal → café nearby', '식당 → 근처 카페', 't-s', 'middle'))
    # rating matrix
    filled = {(0, 1), (1, 3), (2, 0), (2, 4), (3, 2), (4, 5), (5, 1), (6, 3), (7, 0), (1, 5), (6, 4)}
    guessed = {(0, 4), (3, 5), (5, 3), (7, 2)}
    for r in range(8):
        for c in range(6):
            x, y = 346 + c * 19, 44 + r * 23
            if (r, c) in filled:
                b.append(f'<rect x="{x}" y="{y}" width="15" height="15" rx="3" class="i-acc"/>')
            elif (r, c) in guessed:
                b.append(f'<rect x="{x}" y="{y}" width="15" height="15" rx="3" class="i-soft"/><rect x="{x}" y="{y}" width="15" height="15" rx="3" class="i-accs" stroke-width="1.2" stroke-dasharray="2 2"/>')
            else:
                b.append(f'<rect x="{x}" y="{y}" width="15" height="15" rx="3" class="i-box" stroke-width="1"/>')
    b.append(txt(398, 240, 'users × places', '사용자 × 장소', 't-s', 'middle'))
    return svg(''.join(b), 'A map with a restaurant pin and a café pin joined by a route, next to a sparse user-by-place rating grid.',
               '식당과 카페 핀을 잇는 동선 지도와, 듬성듬성 채워진 사용자 × 장소 평점 행렬.')


# ------------------------------------------------------------------------------------------------ Genomics study
def ill_genomics():
    b = []
    xs = [64, 180, 296, 412]
    y = 86
    for x in xs:
        b.append(f'<circle cx="{x}" cy="{y}" r="34" class="i-box" stroke-width="1.3"/>')
    for a, c in zip(xs, xs[1:]):
        b.append(arrow(a + 40, y, c - 40, y, 'i-ln2', 2, 6))
    # DNA icon
    x = xs[0]
    b.append(f'<path d="M{x - 12} {y - 20} C{x + 12} {y - 8} {x + 12} {y + 8} {x - 12} {y + 20}" class="i-accs" stroke-width="2.6" fill="none"/>')
    b.append(f'<path d="M{x + 12} {y - 20} C{x - 12} {y - 8} {x - 12} {y + 8} {x + 12} {y + 20}" class="i-ln2" stroke-width="2.6" fill="none"/>')
    for dy in (-12, 0, 12):
        b.append(f'<line x1="{x - 8}" y1="{y + dy}" x2="{x + 8}" y2="{y + dy}" class="i-ln2" stroke-width="1.6" opacity=".7"/>')
    # RNA single strand
    x = xs[1]
    b.append(f'<path d="M{x - 18} {y + 10} C{x - 10} {y - 18} {x - 2} {y + 18} {x + 6} {y - 8} S{x + 18} {y - 6} {x + 20} {y - 16}" class="i-c2s" stroke-width="2.8" fill="none" stroke-linecap="round"/>')
    for dx in (-14, -4, 6, 15):
        b.append(f'<line x1="{x + dx}" y1="{y + 2}" x2="{x + dx}" y2="{y + 12}" class="i-c2s" stroke-width="1.8" stroke-linecap="round" opacity=".7"/>')
    # protein blob
    x = xs[2]
    b.append(f'<path d="M{x - 16} {y - 4} C{x - 20} {y - 22} {x + 2} {y - 24} {x + 6} {y - 12} C{x + 22} {y - 16} {x + 22} {y + 6} {x + 10} {y + 10} C{x + 12} {y + 24} {x - 10} {y + 22} {x - 8} {y + 10} C{x - 24} {y + 10} {x - 22} {y} {x - 16} {y - 4} Z" class="i-c5s" stroke-width="2.6" fill="none" stroke-linejoin="round"/>')
    # cell
    x = xs[3]
    b.append(f'<circle cx="{x}" cy="{y}" r="20" class="i-c3s" stroke-width="2.6"/><circle cx="{x + 4}" cy="{y - 3}" r="7" class="i-c3"/>')
    for (lab, ko, x) in (('DNA', 'DNA', xs[0]), ('RNA', 'RNA', xs[1]), ('Protein', '단백질', xs[2]), ('Cell', '세포', xs[3])):
        b.append(txt(x, 140, lab, ko, 't-l', 'middle', lbl=False, extra=' style="font-size:14px"'))
    # seasons
    b.append('<rect x="30" y="166" width="300" height="34" rx="17" class="i-soft"/><rect x="30" y="166" width="300" height="34" rx="17" class="i-accs" stroke-width="1.4"/>')
    b.append(txt(46, 188, 'Season 1 · CAFA 6 · genome LMs', '시즌 1 · CAFA 6 · 유전체 LM', 't-s', 'start', extra=' style="fill:var(--text);font-weight:600"'))
    b.append('<rect x="150" y="212" width="300" height="34" rx="17" style="fill:color-mix(in srgb,var(--c-cell) 18%,transparent)"/><rect x="150" y="212" width="300" height="34" rx="17" class="i-c2s" stroke-width="1.4"/>')
    b.append(txt(166, 234, 'Season 2 · Perturbation · VCC 2026', '시즌 2 · Perturbation · VCC 2026', 't-s', 'start', extra=' style="fill:var(--text);font-weight:600"'))
    return svg(''.join(b), 'The central dogma — DNA, RNA, protein, cell — with the two study seasons spanning it.',
               '센트럴 도그마(DNA, RNA, 단백질, 세포)와 이를 나눠 다룬 두 공부 시즌.')


# ------------------------------------------------------------------------------------------------ Hallucination
def ill_halluc():
    b = []
    b.append('<rect x="24" y="34" width="224" height="156" rx="12" style="fill:#cfe6ea"/>')
    b.append('<path d="M24 130 H248 V178 Q248 190 236 190 H36 Q24 190 24 178 Z" style="fill:#9cc79a"/>')
    b.append('<path d="M112 190 L132 130 H142 L168 190 Z" style="fill:#7d858c"/>')
    b.append('<path d="M136 144 V152 M137 162 V172 M138 180 V188" style="stroke:#e9edf0;stroke-width:2;stroke-linecap:round"/>')
    b.append('<circle cx="208" cy="70" r="15" style="fill:#f2c14e"/>')
    b.append('<rect x="60" y="112" width="8" height="28" style="fill:#7a5a3a"/><circle cx="64" cy="100" r="20" style="fill:#3f9b6e"/>')
    b.append('<rect x="24" y="34" width="224" height="156" rx="12" class="i-ln" stroke-width="1" fill="none"/>')
    # attention blobs on an empty patch
    for (r, o) in ((30, .16), (20, .22), (11, .35)):
        b.append(f'<circle cx="196" cy="160" r="{r}" style="fill:#e05270;opacity:{o}"/>')
    # audio waveform
    import random
    random.seed(3)
    for i in range(44):
        h = 4 + abs(math.sin(i * .55)) * 18 * random.uniform(.4, 1)
        b.append(f'<rect x="{26 + i * 5.1:.1f}" y="{220 - h / 2:.1f}" width="3" height="{h:.1f}" rx="1.5" class="i-ink" opacity=".6"/>')
    b.append(txt(136, 252, 'image + audio in', '이미지 + 오디오 입력', 't-s', 'middle'))
    # caption bubble
    b.append('<rect x="266" y="52" width="196" height="112" rx="16" class="i-box" stroke-width="1.3"/>')
    b.append('<path d="M266 102 L252 112 L268 116" class="i-box" stroke-width="1.3"/>')
    b.append(txt(282, 84, '“A sunny road,', '“맑은 날의 길,', 't-l', 'start', lbl=False, extra=' style="font-size:16px;fill:var(--text)"'))
    b.append(txt(282, 108, 'a tree, and', '나무 한 그루,', 't-l', 'start', lbl=False, extra=' style="font-size:16px;fill:var(--text)"'))
    b.append(txt(282, 132, 'a barking dog.”', '짖는 강아지.”', 't-l', 'start', lbl=False, extra=' style="font-size:16px;fill:#e05270;font-weight:700"'))
    b.append('<path d="M282 138 H400" style="stroke:#e05270;stroke-width:2;stroke-dasharray:3 3"/>')
    b.append('<circle cx="452" cy="54" r="12" style="fill:#e05270"/><text x="452" y="59.5" text-anchor="middle" style="font:700 15px var(--font);fill:#fff">!</text>')
    b.append(txt(364, 190, 'no dog in the picture —', '사진에도 소리에도', 't-s', 'middle'))
    b.append(txt(364, 207, 'and no barking in the audio', '강아지는 없습니다', 't-s', 'middle'))
    return svg(''.join(b), 'A picture of a sunny road with a tree; the model’s caption adds a barking dog that is neither in the image nor in the audio.',
               '맑은 날의 길과 나무 사진인데, 모델의 설명에는 이미지에도 소리에도 없는 짖는 강아지가 등장합니다.')


# ------------------------------------------------------------------------------------------------ Writing
def ill_writing():
    b = []
    cards = [(-9, '#95'), (-3, '#109'), (3, '#125')]
    for k, (rot, num) in enumerate(cards):
        cx, cy = 140, 132
        b.append(f'<g transform="rotate({rot} {cx} {cy})">')
        b.append(f'<rect x="{cx - 88}" y="{cy - 70}" width="176" height="140" rx="12" class="i-box" stroke-width="1.3"/>')
        if k == 2:
            b.append(f'<rect x="{cx - 88}" y="{cy - 70}" width="176" height="36" rx="12" class="i-soft"/>')
            b.append(f'<text x="{cx - 74}" y="{cy - 46}" class="t-m" style="font-size:13px;font-weight:600;fill:var(--text)">위클리 딥 다이브 {num}</text>')
            for j, w in enumerate((140, 120, 132, 96)):
                b.append(f'<line x1="{cx - 74}" y1="{cy - 14 + j * 16}" x2="{cx - 74 + w}" y2="{cy - 14 + j * 16}" class="i-ln2" stroke-width="2.2" opacity=".6" stroke-linecap="round"/>')
        b.append('</g>')
    b.append(txt(140, 246, '9 newsletter issues', '뉴스레터 9편', 't-s', 'middle'))
    # magazine
    b.append('<rect x="300" y="30" width="138" height="192" rx="6" style="fill:#7d1428"/>')
    b.append('<text x="316" y="66" style="font:700 19px var(--font);fill:#fff">deep daiv.</text>')
    b.append('<text x="316" y="90" style="font:500 16px var(--font);fill:#fff;opacity:.85">vol.0</text>')
    for j in range(5):
        b.append(f'<line x1="378" y1="{130 + j * 14}" x2="{424 - (j % 2) * 10}" y2="{130 + j * 14}" style="stroke:#fff;stroke-width:1.6;opacity:.45"/>')
    b.append('<line x1="316" y1="120" x2="360" y2="120" style="stroke:#fff;stroke-width:1.6;opacity:.6"/>')
    b.append(txt(369, 246, 'magazine vol.0', '매거진 vol.0', 't-s', 'middle'))
    return svg(''.join(b), 'A stack of newsletter issues and the red cover of deep daiv. magazine vol.0.',
               '뉴스레터 호들과 deep daiv. 매거진 vol.0의 빨간 표지.')


ILLS = {
    'gdtr': ill_gdtr, 'vcc2026': ill_vcc, 'cafa6': ill_cafa, 'phenofocus': ill_pheno, 'geoflowagent': ill_geoflow,
    'bu-net': ill_bunet, 'ftf-vtg': ill_vtg, 'bi-cot': ill_bicot, 'persona-chatbot': ill_persona, 'taste-trip': ill_taste,
    'genomics-study': ill_genomics, 'hallucination': ill_halluc, 'writing': ill_writing,
}
