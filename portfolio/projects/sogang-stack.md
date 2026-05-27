---
layout: page
title: "Sogang Stack — 학내 도구 3종"
permalink: /portfolio/projects/sogang-stack/
description: "학내 행정·강의계획서·교내 자료 검색을 같은 디자인 토큰 위에 묶은 학생용 도구 스위트."
---

[← 프로젝트 목록](/portfolio/projects/) · 공모전 페이지: [서강 생성형 AI](/portfolio/competitions/sogang-genai/)

## 이 글이 다루는 것

학사 행정, 교내 자료 검색, 강의계획서 탐색을 별도 제품 3개로 분리하면서도 같은 디자인 토큰 위에 묶어 한 제품처럼 동작하도록 설계.

## 구성

| 도구 | 역할 | 데모 |
|:-----|:-----|:-----|
| Sogang Copilot | 학사 코파일럿 | [/sogang-copilot/](/sogang-copilot/) |
| Sogang Scout | 교내 자료 스카우트 | [/sogang-scout/](/sogang-scout/) |
| Syllabus Navigator | 강의계획서 네비게이터 | [/syllabus-navigator/](/syllabus-navigator/) |

## 설계 결정

- **인덱스 분리.** 강의계획서 / 행정 문서 / 교내 공지 별도 인덱스. 질의 분류기가 인덱스를 라우팅.
- **실패 케이스.** "모르면 모른다" 응답 비율을 KPI로 둠. 환각을 줄이기 위함.
- **디자인 토큰 공유.** 한 컬러 팔레트, 한 카드 시스템, 한 타이포그래피.
