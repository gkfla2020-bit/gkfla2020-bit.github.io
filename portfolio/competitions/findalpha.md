---
layout: page
title: "Sprint 2 알파 — 파인드알파 델타"
permalink: /portfolio/competitions/findalpha/
description: "파인드알파 델타 스프린트 제출작. WorldQuant Brain 기반 알파 후보 자동 시뮬레이션 + 코드 리뷰 파이프라인."
---

[← 공모전 목록](/portfolio/competitions/)

**공모전**: 파인드알파 델타 스프린트 · **결과**: Sprint 2 제출 · **기간**: 2026

## 한 줄 요약

알파를 줍는 게 아니라, 알파를 깎아내는 파이프라인. WorldQuant Brain의 알파 후보 1만 개를 자동으로 시뮬레이션하고, 통과한 후보에 대해 5라운드 코드 리뷰를 다중 LLM에게 시켜 통과시킬 만한 알파만 남긴다.

## 주요 모듈

- **brain_api.py** — WQ Brain API 클라이언트. 시뮬레이션 큐잉/결과 수집.
- **alpha_ast.py** — 알파 표현식의 추상 구문 트리 검증기. 잘못된 연산 조합을 사전 컷.
- **code_review_5rounds.py** — 통과 후보를 5라운드에 걸쳐 LLM 코드 리뷰. 라운드별로 다른 평가 축(샤프 안정성 / 회귀 / 거래비용 / 산업 노출 / 데이터 시즌성).
- **dashboard.py** — 통과 알파 풀과 라운드별 코멘트를 시각화.

## Sprint 2 결과

- 1차 시뮬: 1만+ 후보 → 통계적으로 유의한 후보 약 7%로 축소
- 5라운드 리뷰 후 최종 알파 풀: 거래비용·집중 위험을 통과한 코어 후보로 축소
- 제출 자료 — FINDA_SPRINT2_ALPHA.pdf
