---
layout: page
title: "CodePathology — KIT 바이브코딩 공모전"
permalink: /portfolio/competitions/kit-vibe-coding/
description: "FastAPI · React · Docker로 만든 코드 진단 웹 IDE. KIT 바이브코딩 공모전 제출작."
---

[← 공모전 목록](/portfolio/competitions/)

**팀명**: 제노닉스 · **결과**: 제출 · **기간**: 2026

데모: [/codepathology/](/codepathology/)

## 한 줄 요약

코드를 X-ray 찍듯이 분석한다. 정적 분석기로 구조적 결함을 짚어내고, LLM이 그 결함을 학습자 입장에서 다시 설명해 주는 웹 IDE.

## 왜 ‘병리학’인가

초보가 코드에서 막히는 지점은 문법이 아니라 *구조적 의도가 무너지는 자리*다. 의사가 환자의 X-ray를 보며 "여기, 이 부분이 약하다"라고 짚어 주듯이, 학습자에게 "이 함수의 책임이 너무 많다", "이 분기의 종료 조건이 모호하다" 같은 구조 차원의 진단을 준다. LLM 단독이 아니라 정적 분석과의 합으로 진단하는 게 핵심이다.

## 구성

- **Frontend.** Monaco 에디터 기반 웹 IDE, Tailwind UI. 진단 결과를 코드 옆 사이드 패널에 인라인 표시.
- **Backend.** FastAPI. 정적 분석 워커(언어별 plugin) + LLM 라우팅. 결과를 표준화된 JSON 진단 리포트로 통일.
- **Container.** docker-compose로 frontend / backend / static-analyzer를 한 줄 명령으로 기동.
- **RAG.** 코드 결함 패턴을 지식베이스로 두고 LLM 답변을 패턴 기반으로 검증해 환각 줄임.

## 제출 자료

- 참가 각서, 개인정보 동의서, AI 리포트 (KIT 양식 3종)
- 제품 기획서 — CodePathology_기획서.html
- 개발 명세서 — CodePathology_개발명세서.html
- 웹 IDE 명세서 — CodePathology_웹IDE_명세서.html
- 실행 데모 — [/codepathology/](/codepathology/)

## 회고

혼자 만들었지만 모듈 경계가 깔끔해 팀이 붙어도 그대로 확장 가능하다. 학습 도메인이지만 동일 아키텍처를 사내 코드 리뷰 보조 도구로 옮기기 쉬운 점이 평가에서 살았다.
