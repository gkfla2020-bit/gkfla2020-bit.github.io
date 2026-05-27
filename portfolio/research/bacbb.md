---
layout: page
title: "BACBB — Bad-Beta against Crypto"
permalink: /portfolio/research/bacbb/
description: "Asness Leverage Aversion 프레임을 가상자산에 적용. 공포·금리 충격 구간 베타 분해."
---

[← 리서치 목록](/portfolio/research/)

전체 페이퍼: [/research/bacbb/](/research/bacbb/)

## 이 글이 다루는 것

Asness의 Leverage Aversion 프레임을 가상자산에 적용해 BTC 베타를 충격 종류별로 분해. 공포(VIX 점프) vs 금리(2y 점프) 두 충격 채널에서 베타가 어떻게 다른지 보여주는 페이퍼.

## 핵심 가설

- 전통자산에서 "Bad Beta"는 공포 충격(현금흐름 베타)에서 더 비싸게 보상된다.
- BTC가 "디지털 골드"인지 "기술주 베타"인지에 대한 답은, 어떤 충격 채널에서 베타가 큰가에 달려 있다.

## 방법

- DCC-GARCH로 BTC와 SPY/금/BEI 간 시간변동 상관 추정.
- 충격 윈도우(VIX 95퍼센타일, 2y yield 95퍼센타일)에서 베타 분해.
- 롤링 회귀로 베타 시계열 시각화.

## 관련 자료

- 본문 — BACBB: Betting Against Cryptocurrency Bad Beta
- 코드 — `btc_pipeline.py`, `btc_analysis.py`
- 차트 — `btc_chart_dcc_btc_gold.png`, `btc_chart_rolling_correlations.png`, `btc_chart_spillover_full.png`
