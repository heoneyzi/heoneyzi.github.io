# Jiheon Kang · 강지헌

Biomedical AI research portfolio for **https://heoneyzi.github.io/**.

연세대학교 전기전자공학부 강지헌의 연구 포트폴리오 사이트입니다. 첫 화면(표지)에서 관심 분야와 대표 성과를 한눈에 보여 주고, 프로젝트 카드를 누르면 **주제 → 한 일 → 결과 → 비전**을 짧게 정리한 페이지가 열립니다. 코드와 실험의 세부 내용은 각 페이지의 GitHub 버튼으로 [Medical](https://github.com/heoneyzi/Medical) · [Paper](https://github.com/heoneyzi/Paper) · [Study](https://github.com/heoneyzi/Study) · [Deep_Daiv](https://github.com/heoneyzi/Deep_Daiv) 저장소에 연결됩니다.

## 구성

| 경로 | 내용 |
|---|---|
| `index.html` | 표지(이름·대표 성과·연구 지도·지금 하는 일) → 대표 작업 → 논문 → 공부·글 → 걸어온 길 → 소개·연락 |
| `projects/*.html` | 프로젝트 13개 페이지 (GDTR, VCC 2026, CAFA 6, PhenoFocus, FTF-VTG, Bi-CoT, GeoFlowAgent, BU-Net, Persona chatbot, Taste Trip, Genomics study, Hallucination study, Newsletter & Magazine) |
| `assets/site.css`, `assets/site.js` | 항상 밝은 화면의 스타일(메인 색 CV 청록 `#008080`)과 언어 전환 |
| `assets/og.png` | 링크 공유 미리보기 이미지 |
| `Jiheon_Kang_CV.pdf` | CV (파일명을 유지한 채 교체하면 됩니다) |
| `_src/` | 사이트를 만드는 원본: `content.py`(영문·한국어 문구), `ills.py`(프로젝트 그림), `build.py`, `og.py` |

## 수정하기

1. 문구·수치·링크는 `_src/content.py`, 표지·논문·타임라인은 `_src/build.py`, 그림은 `_src/ills.py`, 색과 레이아웃은 `_src/site.css`에서 고칩니다. 모든 문구는 `(영문, 한국어)` 쌍입니다.
2. 저장소 최상위에서 `python3 _src/build.py`를 실행하면 `index.html`, `projects/`, `assets/`, `sitemap.xml`이 다시 만들어집니다. Python 3.9 이상이면 되고 추가 패키지는 필요 없습니다.
3. 공유 미리보기 이미지를 다시 만들려면 `python3 _src/og.py .`를 실행합니다. Playwright가 필요하며, 이 단계는 선택입니다.

로컬 미리보기: `python3 -m http.server 4173` 실행 후 http://127.0.0.1:4173/ 접속.

## 게시

저장소 **Settings → Pages → Deploy from a branch**에서 `main`, `/ (root)`를 선택합니다. 정적 HTML/CSS/JS라서 서버나 빌드 과정이 필요 없습니다. `.nojekyll`은 Jekyll 처리를 생략하게 합니다.

## 내용 기준

2026년 9월 CV와 Portfolio 저장소를 기준으로 썼습니다. 수치는 원자료에 적힌 그대로이고, 범위를 함께 적었습니다.

- GDTR: ICML 2026 GenBio **워크숍** Oral입니다. TDiG는 팀 후속 연구이며, YAICON 1등은 팀 저장소에 적힌 내용입니다.
- VCC 2026: 0.5794는 **공개 대리 시험**(Jiang24 IFNG, BxPC3 제외) 결과이고, 공식 리더보드 점수가 아닙니다.
- PhenoFocus: 31개 화합물, 질의 1개로 한 **탐색적 MVP** 결과입니다.
- Bi-CoT·FTF-VTG: 논문 원고와 결과 노트에 보고된 수치입니다.

JavaScript가 꺼져 있어도 영어 본문과 모든 링크가 동작합니다. 언어 선택만 브라우저에 저장하며, 방문자 데이터 수집이나 외부 분석 스크립트는 없습니다.

## Published sources

The GitHub profile is the portfolio entry point. Source material is organized in [Medical](https://github.com/heoneyzi/Medical), [Paper](https://github.com/heoneyzi/Paper), [Study](https://github.com/heoneyzi/Study), and [Deep_Daiv](https://github.com/heoneyzi/Deep_Daiv). Historical repositories are preserved in [Portfolio-Archive](https://github.com/heoneyzi/Portfolio-Archive).

`Jiheon_Kang_CV.pdf` is the exact user-provided September 2026 `Jiheon_CV_updated_web.pdf` (SHA-256: `6ba07da961cdc43c327f5ca5f5baaeb1a75e81567fbda2093d58e353ae36fa56`).

Published from the reviewed September 28, 2026 source snapshot. The site is served from the root of the `main` branch with `.nojekyll`.
