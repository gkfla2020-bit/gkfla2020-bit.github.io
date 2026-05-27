---
layout: page
title: "WorldQuant Brain Alpha Survey"
permalink: /portfolio/research/wq-alpha/
description: "WorldQuant Brain에서 1만+ 알파 후보를 시뮬레이션하고 5라운드 코드 리뷰로 통과 풀의 공통 구조를 추출한 서베이."
---

[← 리서치 목록](/portfolio/research/)

전체 페이지: [/research/wq-alpha-evolution/](/research/wq-alpha-evolution/)

## 이 글이 다루는 것

WorldQuant Brain에서 1만+ 알파를 자동 시뮬레이션하고, 통과한 후보에 대해 5라운드 LLM 코드 리뷰를 적용해 통과 풀의 공통 구조와 자주 무너지는 패턴을 정리한 서베이.

## 주요 관찰

- 통과 알파의 약 60%는 "횡단면 정규화 + 시간 평활"의 합성으로 환원 가능.
- 거래비용 컷을 강제하면 풀 크기는 90% 이상 줄어듦.
- 시즌성 의존 알파는 라운드 4(데이터 시즌성)에서 가장 많이 탈락.

## 코드 흐름

1. `brain_api.py` — 시뮬 큐잉, 결과 수집.
2. `alpha_ast.py` — 알파 AST 검증.
3. `code_review_5rounds.py` — 5라운드 평가 루프.
4. 리포트 자동 생성 → 라운드별 통과율과 코멘트 정리.
