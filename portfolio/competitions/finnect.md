---
layout: page
title: "한국형 Credit Builder — FINNECT 배틀"
permalink: /portfolio/competitions/finnect/
description: "FINNECT 배틀. 다중 LLM 토론으로 한국형 Credit Builder 모델 3안을 비교한 분석 보고서."
---

[← 공모전 목록](/portfolio/competitions/)

**공모전**: FINNECT 배틀 · **결과**: 제출 · **기간**: 2026

## 한 줄 요약

Credit Builder Loan 모델 3개 안(전당포형, 통신·구독료 연계형, 임대료 연계형)을 다중 LLM 토론 파이프라인에 넣고, 각자 비즈니스 가능성과 규제 리스크를 공격·방어하게 만든 보고서.

## 왜 LLM 토론인가

같은 모델에게 같은 질문을 반복해 묻는 것은 의미가 없다. Credit Builder를 한국 환경에 맞춰 변형하려면 신용평가, 통신요금 데이터, 주택 임차, 규제(여신금융업법, 신용정보법)를 동시에 짚어야 하기 때문에, 각 페르소나를 가진 다중 에이전트가 *대치하며* 결과를 정리하게 했다.

## 파이프라인

- **claude_battle_v3.py** — 라운드별 발화 / 반박 / 종합 단계로 분리된 토론 루프. 각 라운드가 끝나면 메타 평가자가 점수 부여.
- **battle_log_*.txt** — 모든 발화 원문을 파일로 남겨 사후 검증 가능.
- **battle_report*.html** — 안별 상세 페이지와 상위 3안 비교 페이지.

## 결론

> 한국 시장은 통신요금·구독료 연계형이 단기 진입성에서 가장 우수하지만, 장기적으로는 임대료 연계형이 가계 신용 회복에 가장 큰 사회적 효과를 가진다.
