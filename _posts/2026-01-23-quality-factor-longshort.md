---
title: "퀄리티 팩터 롱숏 전략: BTC/ETH Long + DeFi Short"
date: 2026-01-23
categories: [Quant, Crypto]
tags: [long-short, quality-factor, defi, bitcoin, ethereum]
toc: true
toc_sticky: true
---

## 📌 프로젝트 개요

전통 금융의 **퀄리티 팩터(Quality Factor)** 개념을 암호화폐 시장에 적용한 롱숏 전략입니다. 

**전략 컨셉**:
- **Long**: 시가총액 상위, 네트워크 효과가 검증된 BTC/ETH
- **Short**: 우하향 추세의 DeFi 토큰 (펌핑 회피 로직 적용)

---

## 🎯 전략 설계

### 롱 포지션 (Quality Assets)

| 자산 | 비중 | 선정 이유 |
|------|------|----------|
| BTC | 50% | 시장 지배력, 기관 수요 |
| ETH | 50% | DeFi 생태계 기반, 스테이킹 수익 |

### 숏 포지션 (Declining DeFi)

```python
short_assets = [
    'SUSHI-USD', 'UNI-USD', 'AAVE-USD', 'CRV-USD',
    'COMP-USD', 'SNX-USD', 'YFI-USD', '1INCH-USD',
]
```

**숏 후보 선정 기준**:
1. 60일 추세 기울기 < 0 (우하향)
2. 7일 급등률 < 25% (펌핑 회피)
3. 상위 4개 종목만 선정

---

## 🔧 리스크 관리 시스템

### 손절/익절 로직

```python
self.stop_loss = -0.15      # 15% 손절
self.take_profit = 0.25     # 25% 익절
self.max_short_loss = -0.30 # 숏 최대 손실 제한
```

### 펌핑 감지 알고리즘

```python
def detect_pump(self, df, idx, lookback=7):
    current = float(df['Close'].iloc[idx])
    past = float(df['Close'].iloc[idx - lookback])
    return (current / past - 1) > 0.25  # 7일 25% 이상 급등
```

### 비용 구조

| 항목 | 비율 | 연간 영향 |
|------|------|----------|
| 거래 수수료 | 0.05% | ~1.3% |
| 펀딩비 (숏) | 0.01% × 3회/일 | ~10.9% |

---

## 📈 백테스트 결과

**기간**: 2021.01 ~ 2024.12 (4년)

```
📊 결과
============================================================
최종자본: $142,847
총수익률: 42.8%
CAGR: 9.4%
MDD: -31.2%
샤프: 0.87
승률: 54.3%
------------------------------------------------------------
거래: 156회
손절: 23회 / 익절: 18회
수수료: $1,247
펀딩비: $8,934
============================================================
```

---

## 📊 성과 시각화

![Quality Factor Result](/assets/images/quality_factor_result.png)

상단: 포트폴리오 가치 추이  
하단: 드로다운 구간

---

## 💡 전략 개선 포인트

### 현재 한계점
1. 펀딩비 비용이 수익의 상당 부분 잠식
2. DeFi 섹터 전반 하락 시 숏 수익 제한적
3. 2021년 불장에서 숏 손실 발생

### 개선 방향
1. **동적 레버리지**: 변동성 기반 레버리지 조절
2. **섹터 로테이션**: DeFi 외 다른 섹터 숏 후보 추가
3. **펀딩비 최적화**: 펀딩비 낮은 거래소 활용

---

## 🔗 코드 저장소

전체 코드는 GitHub에서 확인할 수 있습니다:
- [quality_factor_longshort_strategy.py](https://github.com/gkfla2020-bit/seoul-economy-news)

---

*본 전략은 교육 및 연구 목적으로 작성되었으며, 실제 투자 권유가 아닙니다.*
