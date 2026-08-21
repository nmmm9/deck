# -*- coding: utf-8 -*-
"""멈칫 발표 HTML → 공개 배포용 클린 빌드
원본(대본·Q&A 포함)에서 다음을 제거해 index.html 생성:
 - 발표 대본(⏱ note) 전체
 - 부록·Q&A 대비 슬라이드(파인튜닝/예상 질문 장)
 - 대본 편집 기능(contenteditable) 및 작업 도구(타이머·저장·복사) 표시
사용: python build_clean.py [원본경로] [출력경로]
"""
import sys, re, os

src = sys.argv[1] if len(sys.argv) > 1 else r'C:\Users\노명구\Downloads\멈칫_발표.html'
dst = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')

raw = open(src, encoding='utf-8').read()

# 1) 부록·Q&A 슬라이드 제거 (h2 키워드 기준)
DROP_KEYS = ['파인튜닝 파이프라인', '예상 질문 — 데이터·성능', '예상 질문 — 사업·법·운영']
out = []
pos = 0
dropped = 0
while True:
    s = raw.find('<section', pos)
    if s < 0:
        out.append(raw[pos:])
        break
    e = raw.find('</section>', s) + len('</section>')
    out.append(raw[pos:s])
    sec = raw[s:e]
    if any(k in sec for k in DROP_KEYS):
        dropped += 1
    else:
        out.append(sec)
    pos = e
raw = ''.join(out)

# 2) note div 제거 (중첩 안전 스캔)
res = []
pos = 0
notes = 0
while True:
    s = raw.find('<div class="note"', pos)
    if s < 0:
        res.append(raw[pos:])
        break
    res.append(raw[pos:s])
    i = raw.find('>', s) + 1
    depth = 1
    j = i
    while depth > 0:
        no = raw.find('<div', j)
        nc = raw.find('</div>', j)
        if 0 <= no < nc:
            depth += 1; j = no + 4
        else:
            depth -= 1; j = nc + 6
    notes += 1
    pos = j
raw = ''.join(res)

# 3) 편집 속성 제거 + 도구 숨김 CSS
raw = raw.replace(' contenteditable="true" spellcheck="false"', '')
raw = raw.replace('</head>', '<style>#tbar,#saveBtn,#laps{display:none !important}</style></head>', 1)

open(dst, 'w', encoding='utf-8').write(raw)
print(f'clean build -> {dst}')
print(f'  dropped slides: {dropped}, removed notes: {notes}, size: {os.path.getsize(dst)}')
