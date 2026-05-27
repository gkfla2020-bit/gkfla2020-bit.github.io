---
layout: page
title: "Sogang Stack — 서강대 생성형 AI 공모전"
permalink: /portfolio/competitions/sogang-genai/
description: "서강대 생성형 AI 공모전 제출작. 학내 행정·강의계획서·자료 검색 자동화 3종."
---

[← 공모전 목록](/portfolio/competitions/)

**공모전**: 2026 서강대학교 생성형 AI 기반 아이디어 공모전 · **결과**: 제출

## 한 줄 요약

학생이 매일 부딪히는 정보 격차를 한 화면으로 줄이는 학내 도구 3종. 같은 디자인 토큰 위에 묶어 한 제품처럼 동작하도록 설계.

## 3종 도구

### Sogang Copilot — 학사 코파일럿

데모: [/sogang-copilot/](/sogang-copilot/)

학사 일정, 졸업 요건, 학적 변경 절차를 자연어로 묻고 답한다. 행정 문서 RAG 위에서 동작.

### Sogang Scout — 교내 자료 스카우트

데모: [/sogang-scout/](/sogang-scout/)

학생들이 흩어진 공지·신청 양식·연구실 정보를 키워드 한 줄로 끌어 모은다. 검색·추천이 한 화면.

### Syllabus Navigator — 강의계획서 네비게이터

데모: [/syllabus-navigator/](/syllabus-navigator/)

"머신러닝 다루는 학부 과목 중 평가가 30/30/40인 강의" 같은 자연어 질의를 강의계획서 데이터셋에서 풀어준다.

## 공통 설계

- **같은 디자인 토큰.** 서강 컬러 + 시스템 폰트로 3종 모두 동일한 톤.
- **데이터 격리.** 강의계획서·행정 문서·교내 공지 각각 별도 인덱스. 검색 권한·캐시 전략이 다르다.
- **실패 케이스 우선.** "모르면 모른다" 응답 비율을 측정 지표로 잡고 환각을 줄이는 데 우선순위.
