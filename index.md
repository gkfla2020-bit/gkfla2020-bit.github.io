---
layout: default
title: Home
---

# 👋 안녕하세요, 윤민혁입니다

서울경제신문 인턴 / 컴퓨터공학 전공

데이터 분석과 웹 개발에 관심이 많습니다.

---

## 🚀 프로젝트

### 기자 정량평가 시스템
서울경제신문 기자들의 KPI를 관리하는 웹 시스템

- **기간**: 2026.01
- **기술스택**: HTML/CSS/JS, AWS Lambda, S3, EventBridge
- **주요 기능**:
  - XML 데이터 자동 파싱 및 동기화
  - 기자별 기사 통계 (기사수, 글자수, 면별 분포)
  - 정성 평가 입력 (취재유형, 임팩트 등급)
  - 기간별 조회 (일별/주별/월별/분기별)
  - 엑셀 내보내기
  - 대시보드 시각화

🔗 [GitHub](https://github.com/gkfla2020-bit/journalist-evaluation) | [Live Demo](https://kpi.sedaily.ai)

---

## 📝 블로그 포스트

{% for post in site.posts %}
- [{{ post.title }}]({{ post.url }}) - {{ post.date | date: "%Y-%m-%d" }}
{% endfor %}

---

## 📫 Contact

- GitHub: [gkfla2020-bit](https://github.com/gkfla2020-bit)
