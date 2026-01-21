---
layout: default
title: "기자 정량평가 시스템 개발기"
date: 2026-01-21
---

# 기자 정량평가 시스템 개발기

서울경제신문 인턴 기간 동안 기자들의 KPI를 관리하는 웹 시스템을 개발했습니다.

## 프로젝트 개요

신문사에서는 기자들의 성과를 정량적으로 평가하기 위해 기사 수, 글자 수, 지면 배치 등을 집계합니다. 기존에는 수작업으로 진행되던 이 과정을 자동화하는 시스템을 구축했습니다.

## 기술 스택

- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5, Chart.js
- **Backend**: AWS Lambda (Python)
- **Storage**: AWS S3
- **Scheduling**: AWS EventBridge

## 주요 기능

### 1. 자동 데이터 수집
- XML 파일에서 기사 정보 자동 파싱
- 매일 오전 6시, 오후 6시 자동 동기화
- 공동 취재 기사 분리 처리
- URL 기준 중복 기사 제거

### 2. 기자별 통계
- 기사 수, 총 글자수, 평균 글자수
- 면별 분포 (1면, 2-3면, 4면 이상)
- 톱기사 자동 분류

### 3. 정성 평가
- 위치: 톱, 사이드, 하단
- 취재유형: 특종, 단독, 기획발굴 등
- 임팩트 등급: S, A, B, C, D

### 4. 기간별 조회
- 일별 / 주별 / 월별 / 분기별 / 반기별 / 전체
- 날짜 네비게이션으로 기간 이동

### 5. 데이터 내보내기
- 엑셀 파일 다운로드
- 기사 목록 + 요약 통계 시트

## 배운 점

- AWS 서버리스 아키텍처 설계
- S3 정적 웹 호스팅
- Lambda Function URL 활용
- EventBridge 스케줄링
- XML 파싱 및 데이터 정제

## 링크

- [GitHub Repository](https://github.com/gkfla2020-bit/journalist-evaluation)
- [Live Demo](https://kpi.sedaily.ai)
