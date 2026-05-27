---
layout: page
title: "MOVE-Vasicek — 옵션 IV로 단기금리 모형 보정"
permalink: /portfolio/research/move-vasicek/
description: "MOVE 지수에서 추출한 옵션 IV 정보를 활용해 Vasicek 단기금리 모델을 보정하는 절차."
---

[← 리서치 목록](/portfolio/research/)

전체 페이퍼 페이지: [한국어](/research/move-vasicek-kr/) · [English](/posts/move-vasicek-academic-en/)

## 이 글이 다루는 것

과거 시계열만 가지고 추정하는 Vasicek 모형은 종종 옵션 시장이 보내는 신호를 놓친다. MOVE 지수의 임플라이드 변동성을 정보로 사용해 κ·σ를 재추정하는 절차를 정리한 듀얼 언어 페이퍼.

## 요지

- 역사 시계열 기반 Vasicek은 σ가 평균회귀의 평형 변동성을 측정하지만, 옵션 시장의 변동성과는 자주 어긋난다.
- MOVE 지수가 시사하는 단기 변동성을 σ에 반영하고, κ는 짧은 기간 평균회귀 강도를 보정.
- 결과적으로 옵션 가격 적합도를 향상시키면서 시계열 적합도 손실은 작게 유지.

## 구조

1. 이론 — Vasicek 모형, 그 한계, 옵션 IV가 담는 정보.
2. 데이터 — 미국 단기금리·MOVE 지수·국채 옵션 시리즈.
3. 방법 — 시계열 + IV 동시 적합 손실 함수 정의, 가중치 조정.
4. 결과 — 캘리브레이션 전·후 옵션 가격 잔차 비교.
5. 시사점 — 한국 통안채/국채 옵션 데이터에 적용 시 고려할 차이.
