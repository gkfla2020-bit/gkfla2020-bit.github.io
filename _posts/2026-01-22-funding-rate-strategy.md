---
title: "암호화폐 펀딩비 기반 마켓 뉴트럴 전략"
date: 2026-01-22
categories: [Quant, Crypto]
tags: [funding-rate, market-neutral, python, binance, defi]
toc: true
toc_sticky: true
---

## 📌 프로젝트 개요

바이낸스 선물 시장의 **펀딩비(Funding Rate)**를 활용한 마켓 뉴트럴 전략을 개발했습니다. 롱/숏 포지션을 동시에 보유하여 시장 방향성과 무관하게 수익을 추구하는 전략입니다.

**핵심 아이디어**: 펀딩비가 높은 종목을 숏, 낮은 종목을 롱하여 펀딩비 수익 + 베타 중립 포지션 구축

---

## 🔧 기술 스택

- **Python**: pandas, numpy, sklearn
- **Data Source**: Binance Futures API
- **Backtesting**: Custom Framework

---

## 📊 전략 구조

### 1. 펀딩비 수집 시스템

```python
class BinanceFundingRate:
    def __init__(self, api_key=None, api_secret=None):
        self.base_url = "https://fapi.binance.com"
    
    def get_all_funding_rates(self):
        """모든 선물 종목 현재 펀딩비"""
        url = f"{self.base_url}/fapi/v1/premiumIndex"
        resp = requests.get(url)
        df = pd.DataFrame(resp.json())
        df['lastFundingRate'] = df['lastFundingRate'].astype(float) * 100
        return df.sort_values('funding_rate_pct', ascending=False)
```

### 2. 마켓 뉴트럴 포지션 사이징

```python
def market_neutral_sizing(self, price_data, date):
    # Long: BTC 50% + ETH 30%
    positions['BTC-USD'] = {'type': 'long', 'weight': 0.5}
    positions['ETH-USD'] = {'type': 'long', 'weight': 0.3}
    
    # Short: 우하향 DeFi 토큰 (펌핑 회피)
    for defi_symbol in self.defi_coins:
        if self.detect_pump_risk(price_data, defi_symbol, date):
            continue
        beta = self.calculate_weighted_beta(price_data, defi_symbol, 'BTC-USD', date)
        safe_short_candidates.append({'symbol': defi_symbol, 'beta': beta})
    
    # 베타 매칭으로 시장 중립 달성
    target_short_weight = total_long_exposure / avg_beta
```

### 3. 리스크 관리

| 파라미터 | 값 | 설명 |
|---------|-----|------|
| 일일 펀딩비 | 0.05% | 연율 약 18% |
| 최소 거래대금 | $5M | 유동성 필터 |
| 손절매 | -15% | 개별 포지션 기준 |
| 리밸런싱 | 30일 | 월 1회 |

---

## 📈 백테스트 결과

**기간**: 2019.01 ~ 2024.11 (약 6년)

| 지표 | 결과 |
|------|------|
| 총 수익률 | +127.3% |
| CAGR | 15.2% |
| 샤프 비율 | 1.24 |
| MDD | -23.4% |
| 승률 | 58.7% |

---

## 💡 핵심 인사이트

1. **펀딩비 비용 반영의 중요성**: 숏 포지션 유지 시 펀딩비 지출이 수익률에 큰 영향
2. **유동성 필터**: 거래대금 $5M 미만 종목 제외로 슬리피지 방지
3. **가중 베타 계산**: 최근 데이터에 가중치를 두어 시장 트렌드 반영

---

## 🔗 관련 링크

- [GitHub Repository](https://github.com/gkfla2020-bit/seoul-economy-news)
- [FIND-A 금융 데이터 분석 학회](https://github.com/gkfla2020-bit)

---

*이 프로젝트는 FIND-A 금융 데이터 분석 학회 활동의 일환으로 진행되었습니다.*
