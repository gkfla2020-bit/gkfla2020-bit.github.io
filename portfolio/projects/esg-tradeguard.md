---
layout: page
title: "ESG TradeGuard — 시스템 단면"
permalink: /portfolio/projects/esg-tradeguard/
description: "ESG TradeGuard 프로젝트의 아키텍처와 데이터 임베딩 방식."
---

[← 프로젝트 목록](/portfolio/projects/)

데모: [/esg-tradeguard/](/esg-tradeguard/) · 공모전 페이지: [ESG TradeGuard 본선 통과작](/portfolio/competitions/esg-tradeguard/)

## 이 글이 다루는 것

공모전 페이지가 "왜 만들었나"라면, 이 글은 "어떻게 만들어졌나"다. 모듈 분할, 도메인 데이터 임베딩 방식, 단일 페이지 내 6단계 상태 전이를 정리한다.

## 아키텍처 한 줄

> 완전 정적. 모든 도메인 데이터(CBAM 배출계수, NGFS 가격경로, EU 기본값)는 코드에 임베드. LLM·서버 호출 없음. GitHub Pages 단일 호스팅.

## 6단계 상태 전이

1. **Step 1 · Upload.** 인보이스/B/L 파일 입력. 가짜 파일 풀(`fake-docs/`)로 시연 안정성 확보.
2. **Step 2 · OCR.** 클라이언트 사이드 OCR 시뮬레이션. HS코드·수량·원산지를 추출 모형으로 표시.
3. **Step 3 · Regulation Match.** 추출값을 CBAM/EUDR/탄소국경세 룰셋과 매칭.
4. **Step 4 · CarbonCast.**
   - 4a. 데이터 품질 스코어
   - 4b. 블록체인 스탬핑(증명 시각)
   - 4c. CBAM 비용 산출 — Phase-in 비율 곱
5. **Step 5 · NDVI.** 위성 NDVI(2022~2024)로 EUDR 산림 파괴 검증. 좌표 기반 Leaflet 표시.
6. **Step 6 · Report.** 누적 결과를 PDF 스타일 한 페이지로 통합.

## 도메인 데이터 임베딩

- CBAM 6개 업종(철강·시멘트·알루미늄·비료·전력·수소) — EU 기본 배출계수와 벤치마크 σ.
- NGFS 4개 시나리오(Net Zero 2050 / Below 2°C / Delayed / Current) ETS 가격경로.
- Phase-in 비율: 2026 2.5% → 2034 100% 단계.

## UI 디자인 토큰

- 포인트 컬러: 하나 그린 `#008C73` 단 하나.
- 토스×당근 톤: 카드 라운드, 충분한 여백, 모듈 간 강한 분리.
- Framer Motion으로 단계 전이를 수직 슬라이드로 통일.
