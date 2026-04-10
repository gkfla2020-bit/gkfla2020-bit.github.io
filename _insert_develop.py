#!/usr/bin/env python3
"""기존 HTML에 디벨롭 섹션 삽입 + 결론 번호 9→10 변경"""

html_path = 'research/vol-integrated-kr/index.html'
insert_path = '_develop_insert.html'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

with open(insert_path, 'r', encoding='utf-8') as f:
    insert = f.read()

# 삽입 지점: 기존 "<!-- 9. 결론 -->" 바로 위의 section-divider부터
# 그 section-divider + 결론 제목을 새 내용으로 교체
old_marker = '<div class="section-divider">\u2022 \u2022 \u2022</div>\n\n<!-- 9. \uacb0\ub860 -->\n<h2>9. \uacb0\ub860 \ubc0f \uc2dc\uc0ac\uc810</h2>'

if old_marker not in html:
    # 줄바꿈 차이 시도
    old_marker = '<div class="section-divider">• • •</div>\n\n<!-- 9. 결론 -->\n<h2>9. 결론 및 시사점</h2>'

if old_marker in html:
    # insert 내용의 마지막에 이미 "10. 결론 및 시사점" 제목이 있음
    html = html.replace(old_marker, insert.strip())
    
    # 기존 결론 하위 번호 9.x → 10.x 변경
    html = html.replace('<h3>9.1 주요 발견</h3>', '<h3>10.1 주요 발견</h3>')
    html = html.replace('<h3>9.2 이론적 기여</h3>', '<h3>10.2 이론적 기여</h3>')
    html = html.replace('<h3>9.3 실무적 시사점</h3>', '<h3>10.3 실무적 시사점</h3>')
    html = html.replace('<h3>9.4 연구의 한계 및 향후 과제</h3>', '<h3>10.4 연구의 한계 및 향후 과제</h3>')
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ 삽입 완료! 파일 크기: {len(html)} bytes")
else:
    print("❌ 삽입 지점을 찾지 못함")
    # 디버깅
    idx = html.find('<!-- 9. 결론 -->')
    if idx >= 0:
        print(f"  '<!-- 9. 결론 -->' found at position {idx}")
        print(f"  Context: {repr(html[idx-100:idx+100])}")
    else:
        print("  '<!-- 9. 결론 -->' not found at all")
