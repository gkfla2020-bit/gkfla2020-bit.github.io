---
layout: page
title: "CodePathology — 코드 진단 웹 IDE"
permalink: /portfolio/projects/codepathology/
description: "정적분석과 LLM 진단을 결합한 코드 진단 웹 IDE."
---

[← 프로젝트 목록](/portfolio/projects/) · 공모전 페이지: [KIT 바이브코딩](/portfolio/competitions/kit-vibe-coding/)

데모: [/codepathology/](/codepathology/)

## 이 글이 다루는 것

Monaco 에디터 옆에 진단 패널을 띄워 정적분석과 LLM 코멘트를 한 줄에서 볼 수 있게 만든 도구. 도커 컴포즈 한 줄로 frontend / backend / static-analyzer를 동시 기동한다.

## 아키텍처

- **frontend/** — React + Tailwind + Monaco. 코드 입력과 진단 표시를 같은 줄/같은 색으로 매칭.
- **backend/** — FastAPI. 표준화된 진단 JSON을 반환. LLM 라우팅 레이어가 들어 있어 모델 교체 비용이 낮음.
- **static-analyzer/** — 언어별 분석 워커. Python AST + 휴리스틱 규칙 + 코드 메트릭(순환복잡도, 함수 길이).
- **docker-compose.yml** — 세 컨테이너를 묶어서 한 줄 기동.

## 특징

- **JSON 진단 표준.** 정적분석과 LLM 출력이 같은 스키마로 통합. UI는 출처를 가리지 않고 표시.
- **RAG 검증.** LLM 응답을 결함 패턴 지식베이스로 사후 검증. 환각이 "패턴에 없는 진단"으로 잡힘.
- **학습자 톤.** 진단 메시지는 "여기에 X 결함이 있다"가 아니라 "이 의도라면 어떤 부분이 약해지는가"로 작성.
