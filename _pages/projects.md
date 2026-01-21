---
layout: default
title: "Projects"
permalink: /projects/
---

## Quantitative Finance

### 1. Funding Rate Arbitrage Strategy

A market-neutral strategy exploiting funding rate differentials in cryptocurrency perpetual futures.

| Metric | Value |
|:-------|:------|
| Backtest Period | 2019.01 - 2024.11 |
| CAGR | 15.2% |
| Sharpe Ratio | 1.24 |
| Max Drawdown | -23.4% |

**Key Features**:
- Real-time funding rate collection via Binance API
- Beta-matched position sizing for market neutrality
- Liquidity filter ($5M minimum daily volume)
- Pump detection algorithm

**Tech Stack**: Python, Binance API, pandas, NumPy, scikit-learn

[GitHub Repository](https://github.com/gkfla2020-bit/seoul-economy-news)

---

### 2. Quality Factor Long-Short Portfolio

Systematic long-short strategy applying quality factor principles to cryptocurrency markets.

| Metric | Value |
|:-------|:------|
| Backtest Period | 2021.01 - 2024.12 |
| Total Return | 42.8% |
| Sharpe Ratio | 0.87 |
| Win Rate | 54.3% |

**Strategy Logic**:
- Long: BTC (50%), ETH (50%)
- Short: Top 4 declining DeFi tokens
- Rebalancing: Bi-weekly
- Risk controls: 15% stop-loss, 25% take-profit

**Tech Stack**: Python, yfinance, matplotlib

---

### 3. Leveraged BTC Strategy

Simple leveraged strategy designed to outperform BTC buy-and-hold.

| Metric | Strategy | BTC B&H |
|:-------|:---------|:--------|
| Total Return | 312.4% | 153.9% |
| CAGR | 28.7% | 17.4% |
| Max Drawdown | -67.2% | -77.3% |

**Design Philosophy**: Minimal complexity, maximum efficiency
- Fixed allocation: BTC 70% + ETH 30%
- 3x leverage
- Annual rebalancing only
- Relaxed stop-loss (-30%)

---

## Software Development

### 4. News Data Collection System

Automated news collection system for Seoul Economic Daily.

**Features**:
- BigKinds API integration
- Web scraping with fallback mechanisms
- JSON data storage with deduplication
- Command-line interface

**Tech Stack**: Python, requests, BeautifulSoup, argparse

---

### 5. KPI Dashboard System

Real-time KPI monitoring dashboard for business analytics.

**Features**:
- Interactive data visualization
- Excel data import/export (SheetJS)
- Chart.js integration
- AWS serverless backend

**Tech Stack**: JavaScript, Chart.js, SheetJS, AWS Lambda, API Gateway

---

## Data Analysis

### 6. Funding Rate Analysis Report

Comprehensive analysis of cryptocurrency funding rates across 70+ coins.

**Deliverables**:
- Monthly/annual funding rate statistics
- Interactive HTML reports
- Pivot table analysis
- Top performers identification

**Output**: [funding_analysis_report.html](https://github.com/gkfla2020-bit/seoul-economy-news)

---

## Contact

For collaboration inquiries or questions about these projects:

**Email**: gkfla2020@gmail.com  
**GitHub**: [github.com/gkfla2020-bit](https://github.com/gkfla2020-bit)
