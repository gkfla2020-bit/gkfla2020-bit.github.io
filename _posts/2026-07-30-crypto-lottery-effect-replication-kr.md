---
layout: post
title: "암호화폐 로또 효과 재현: 9,378개 코인으로 검증한 MAX5 이상현상"
date: 2026-07-30
permalink: /research/crypto-lottery-effect-replication-kr/
categories: [research, asset-pricing]
tags: [cryptocurrency, lottery-effect, MAX5, anomaly, replication, portfolio-sort, newey-west, binance-futures]
toc: true
toc_sticky: true
description: "Wu, Tuan-Mu & Yen (2025)의 암호화폐 로또 효과를 9,378개 코인·2018-2025 독립 표본으로 재현. 가치가중 효과는 논문보다 강하게 확인(월 -4.78%, t=-2.22), 주간 확장에서 t=-3.37. EW 효과와 12개월 지속성이 재현되지 않는 원인을 코호트 분해로 규명하고, 선물시장 실거래 가능성까지 검증했다."
---

<style>
    :root {
        --wsj-black: #111111;
        --wsj-gray: #666666;
        --wsj-light: #f5f5f5;
        --wsj-accent: #0080c6;
        --wsj-red: #c41200;
        --wsj-green: #00843d;
        --wsj-orange: #e67e22;
        --serif: 'Georgia', 'Times New Roman', serif;
        --sans: 'Helvetica Neue', Arial, sans-serif;
        --mono: 'SF Mono', 'Fira Code', 'Consolas', monospace;
    }
    .report-container { max-width: 900px; margin: 0 auto; padding: 20px 0; }
    .masthead { border-bottom: 3px solid var(--wsj-black); padding: 15px 0; margin-bottom: 40px; display: flex; justify-content: space-between; }
    .section-label { font-size: 11px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: var(--wsj-accent); }
    .date-line { font-size: 13px; color: var(--wsj-gray); }
    .headline { font-family: var(--serif); font-size: 34px; font-weight: 700; line-height: 1.15; margin-bottom: 20px; text-align: center; }
    .deck { font-family: var(--serif); font-size: 18px; color: var(--wsj-gray); text-align: center; font-style: italic; margin-bottom: 40px; }
    .abstract { background: var(--wsj-light); padding: 25px; margin: 30px 0; border-left: 4px solid var(--wsj-accent); }
    .abstract-title { font-size: 12px; font-weight: 700; text-transform: uppercase; color: var(--wsj-accent); margin-bottom: 10px; }
    .section-header { font-family: var(--serif); font-size: 26px; font-weight: 700; margin: 50px 0 20px; padding-bottom: 10px; border-bottom: 2px solid var(--wsj-black); }
    .subsection { font-family: var(--serif); font-size: 18px; font-weight: 700; margin: 30px 0 15px; color: var(--wsj-gray); }
    .body-text { font-family: var(--serif); font-size: 17px; line-height: 1.9; margin-bottom: 18px; text-align: justify; }
    .data-table { width: 100%; border-collapse: collapse; font-size: 14px; margin: 20px 0; }
    .data-table th { font-weight: 700; text-transform: uppercase; font-size: 11px; padding: 10px 12px; text-align: left; border-bottom: 2px solid var(--wsj-black); background: var(--wsj-light); }
    .data-table td { padding: 10px 12px; border-bottom: 1px solid #e0e0e0; font-variant-numeric: tabular-nums; }
    .data-table .neg { color: var(--wsj-red); font-weight: 600; }
    .data-table .pos { color: var(--wsj-green); }
    .tstat { color: var(--wsj-gray); font-size: 12px; }
    .fig { margin: 30px 0; text-align: center; }
    .fig img { max-width: 100%; border: 1px solid #e0e0e0; border-radius: 4px; }
    .fig-caption { font-size: 13px; color: var(--wsj-gray); margin-top: 10px; font-style: italic; text-align: left; }
    .key-box { background: #e8f4fd; border-left: 4px solid var(--wsj-accent); padding: 20px 25px; margin: 25px 0; border-radius: 0 8px 8px 0; }
    .key-label { font-size: 12px; font-weight: 700; text-transform: uppercase; color: var(--wsj-accent); margin-bottom: 8px; }
    .warning-box { background: #fff3e0; border-left: 4px solid var(--wsj-orange); padding: 20px 25px; margin: 25px 0; }
    .warning-label { font-size: 12px; font-weight: 700; text-transform: uppercase; color: var(--wsj-orange); margin-bottom: 8px; }
    .verdict-pill { display: inline-block; font-size: 11px; font-weight: 700; border-radius: 12px; padding: 2px 10px; color: #fff; vertical-align: 2px; }
    .vp-ok { background: var(--wsj-green); }
    .vp-no { background: var(--wsj-red); }
    .vp-part { background: var(--wsj-orange); }
    .code-block { background: #1e1e1e; color: #d4d4d4; padding: 20px; border-radius: 6px; font-family: var(--mono); font-size: 13px; line-height: 1.7; overflow-x: auto; margin: 20px 0; white-space: pre; }
    .conclusion-box { background: var(--wsj-black); color: white; padding: 35px; margin: 50px 0; }
    .conclusion-box .section-header { color: white; border-bottom-color: #444; margin-top: 0; }
    .conclusion-box .body-text { color: #ccc; }
    @media (max-width: 768px) { .headline { font-size: 26px; } }
</style>

<div class="report-container">
    <div class="masthead">
        <span class="section-label">Asset Pricing · Replication Study</span>
        <span class="date-line">July 30, 2026</span>
    </div>

    <h1 class="headline">암호화폐 로또 효과 재현<br>9,378개 코인으로 검증한 MAX5 이상현상</h1>
    <p class="deck">"복권처럼 급등했던 코인은 그 다음에 하락한다."<br>Wu, Tuan-Mu &amp; Yen (2025)의 결과는 독립 표본에서도 살아남을까?</p>

    <div class="abstract">
        <div class="abstract-title">요약</div>
        <p class="body-text" style="margin-bottom:0;">
        Wu, Tuan-Mu &amp; Yen (2025, <i>Applied Economics Letters</i>)은 직전 한 달 일별 수익률 상위 5개의 평균(MAX5)으로 코인을 소팅하면, 최상위 분위가 최하위 분위를 월 -6.4%(EW)~-3.0%(VW)씩 유의하게 하회한다고 보고했다. 이 글은 논문과 겹치지 않는 데이터(자체 수집 9,378개 코인, 2018–2025)로 이를 재현한 기록이다. 결론부터: <strong>가치가중 로또 효과는 논문보다 강하게 재현되고(월 -4.78%, t=-2.22), 논문 표본이 끝난 2022년 5월 이후에도 살아있다</strong>. 반면 동일가중 효과와 12개월 지속성은 재현되지 않았는데, 그 원인이 방법론 오류가 아니라 <strong>2020년 형성 코호트가 2021년 알트코인 불장을 타면서 생긴 국면 효과</strong>임을 코호트 분해로 규명했다. 마지막으로 이 이상현상이 바이낸스 무기한 선물로 실제 거래 가능한지까지 검증했다.
        </p>
    </div>

    <h2 class="section-header">1. 원논문과 재현 설계</h2>

    <p class="body-text">Bali, Cakici &amp; Whitelaw (2011)가 주식시장에서 발견한 MAX 효과의 논리는 단순하다. 투자자는 "한 방"의 가능성이 보이는 자산(최근 극단적 일일 급등을 보인 자산)에 복권을 사듯 웃돈을 지불하고, 고평가된 가격은 이후 수익률 하락으로 되돌아온다. 암호화폐는 이 논리가 가장 잘 작동할 법한 시장이다 — 하루 +50%가 드물지 않고, 개인 투자자 비중이 압도적이다.</p>

    <p class="body-text">원논문은 CoinMarketCap 상위 1,000개 코인(2016.1–2022.4, 시총 $5M 이상)을 매월 MAX5 기준 5분위로 나누고 익월 수익률을 비교했다. 재현은 방법론을 그대로 유지하되 데이터를 완전히 독립시켰다:</p>

    <table class="data-table">
        <tr><th>항목</th><th>원논문</th><th>본 재현</th></tr>
        <tr><td>데이터</td><td>CoinMarketCap 상위 1,000개 (스냅샷)</td><td>자체 수집 9,378개 전체에서 매월 상위 1,000개 재구성</td></tr>
        <tr><td>기간</td><td>2016.1 – 2022.4 (76개월)</td><td>2018.2 – 2025.12 (95개월) — 2022.5 이후는 표본외</td></tr>
        <tr><td>신호 / 소팅</td><td>MAX5, 5분위, EW·VW</td><td>동일 + 주간 확장 (MAX1/MAX5 × 산정 2주/4주 × 필터 $1M/$5M)</td></tr>
        <tr><td>검정</td><td>Newey-West t</td><td>동일 (4 lags)</td></tr>
        <tr><td>정제</td><td>미공개</td><td>명시적 규칙: 일수익률 &gt;1000% 및 스파이크-반전 제거 (전체의 0.17%)</td></tr>
    </table>

    <p class="body-text">한 가지 설계 개선이 있다. 시총 필터를 표본 구성 시점에 한 번 적용하는 대신 <strong>매 리밸런싱 시점마다 재적용</strong>해서, 문턱($1M/$5M)을 넘나드는 코인의 진입·이탈을 그대로 반영했다. 매 리밸런싱마다 유니버스 크기도 기록했다 — 주간 기준 413회, 평균 908~1,353개.</p>

    <div class="fig">
        <img src="/assets/lottery-effect/A1_figure1_coin_count.png" alt="유니버스 코인 수 추이">
        <div class="fig-caption">그림 1. 논문 Figure 1 재현 — 시총 $5M 이상·상위 1,000개 캡 기준 유니버스. 원논문과 동일한 S자 성장 후 2021년 말 1,000개 상한 도달.</div>
    </div>

    <h2 class="section-header">2. 메인 결과: VW는 재현, EW는 미재현</h2>

    <p class="body-text">월간 재현의 핵심 수치다. 원논문 Table 2와 나란히 놓으면:</p>

    <table class="data-table">
        <tr><th>High − Low</th><th>원논문 (2016–2022)</th><th>재현: 전체 (2018–2025)</th><th>재현: 겹침 구간 (2018.2–2022.4)</th></tr>
        <tr>
            <td>동일가중 (EW)</td>
            <td class="neg">-0.0638*** <span class="tstat">(-3.41)</span></td>
            <td>-0.0190 <span class="tstat">(-0.95)</span></td>
            <td>-0.0026 <span class="tstat">(-0.09)</span></td>
        </tr>
        <tr>
            <td>가치가중 (VW)</td>
            <td class="neg">-0.0296** <span class="tstat">(-2.02)</span></td>
            <td class="neg">-0.0478** <span class="tstat">(-2.22)</span></td>
            <td class="neg">-0.0528 <span class="tstat">(-1.52)</span></td>
        </tr>
    </table>

    <div class="fig">
        <img src="/assets/lottery-effect/A2_table2_comparison.png" alt="논문 vs 재현 분위별 수익률">
        <div class="fig-caption">그림 2. 분위별 월간 수익률, 논문(파랑) vs 재현(주황). 가치가중에서 High 분위만 뚜렷하게 음수인 구조가 동일하다 — 로또 효과는 "복권성 최상위 코인의 급락"이 주도한다.</div>
    </div>

    <p class="body-text"><span class="verdict-pill vp-ok">재현 성공</span>&nbsp; 가치가중 효과는 원논문보다 오히려 크다(-4.78% vs -2.96%). High 분위만 음수인 패턴, 분위 간 단조성 모두 일치. <span class="verdict-pill vp-no">미재현</span>&nbsp; 동일가중은 방향만 음수고 유의하지 않다. 다만 홀딩 수익률을 1%/99% 윈저화하면 t=-1.74까지 회복된다 — 마이크로캡 밈코인의 극단 수익(가끔 터지는 로또 당첨)이 EW 평균을 끌어올려 효과를 가리는 구조다. 남는 격차는 원논문의 2016–17 구간 부재와 스냅샷 유니버스의 생존편향 가능성으로 설명된다.</p>

    <h2 class="section-header">3. 왜 12개월 지속성은 재현되지 않았나</h2>

    <p class="body-text">원논문 Table 3은 High−Low 누적수익률 차이가 12개월까지 전 구간 유의하다고 보고한다(VW 기준 t+11에서 -26.8%, t=-3.69). 재현에서는 2~6개월까지만 유의하고(t+1: -8.75%, t=-2.69) 9~12개월에서 소멸했다. 처음에는 데이터 오염을 의심했지만, 검증 결과는 다른 이야기를 들려줬다.</p>

    <p class="body-text">12개월 VW High−Low를 형성월 코호트로 분해하면:</p>

    <table class="data-table">
        <tr><th>형성월 코호트</th><th>12개월 VW High−Low</th><th>NW t</th></tr>
        <tr><td>2018.2 – 2021.6</td><td class="pos">+0.69</td><td>+1.07</td></tr>
        <tr><td>2021.7 – 2022.4</td><td class="neg">-0.28</td><td>-4.24</td></tr>
        <tr><td>2022.5 – (논문 표본 이후)</td><td class="neg">-0.42</td><td>-2.58</td></tr>
    </table>

    <p class="body-text">범인은 2020년 형성 코호트다. 이 해의 12개월 HML은 +267% — 2020년에 MAX5가 높았던 코인들의 면면을 보면 yearn.finance, ethlend(현 Aave), havven(현 Synthetix), zilliqa 등 <strong>DeFi Summer의 주역들</strong>이다. 이들은 "복권성 고평가로 하락할 코인"이 아니라 2021년 알트코인 대세장을 그대로 탄 실제 승자였다. 개별 종목 추적으로 데이터 글리치가 아닌 실제 시장 수익임을 확인했고, 생존편향도 배제했다(분위별 12개월 사망률 Q1 1.4% vs Q5 1.8%, 사망을 -100% 처리해도 결론 불변).</p>

    <div class="key-box">
        <div class="key-label">이 재현의 핵심 발견</div>
        <p class="body-text" style="margin-bottom:0;">로또 효과의 장기 지속성은 <strong>국면 의존적</strong>이다. 강세장 초입에 형성된 고MAX 포트폴리오는 하락하지 않고 오히려 불장을 탄다. 원논문이 전 구간 유의했던 것은 2016–17 형성 코호트(2018년 대폭락기에 High 분위 궤멸 → 강한 음수)가 2020 코호트를 상쇄해준 표본 구성 덕분으로 보인다. 즉 원논문의 "12개월 지속" 주장은 표본 특정적일 가능성이 있다.</p>
    </div>

    <h2 class="section-header">4. 주간 확장: 논문 설계의 독립 검증</h2>

    <p class="body-text">월간 재현에 더해, 리밸런싱을 주간으로 촘촘히 하고 신호 산정기간(J)과 지표(MAX1/MAX5), 시총 필터($1M/$5M)를 격자 탐색했다. 홀딩은 1주로 고정. 8개 조합의 High−Low:</p>

    <table class="data-table">
        <tr><th>구성</th><th>EW</th><th>VW</th></tr>
        <tr><td>MAX5 · 산정 2주 · $5M</td><td>+0.0018 <span class="tstat">(0.41)</span></td><td>-0.0021 <span class="tstat">(-0.40)</span></td></tr>
        <tr><td>MAX1 · 산정 4주 · $1M</td><td>-0.0002 <span class="tstat">(-0.04)</span></td><td class="neg">-0.0106** <span class="tstat">(-2.01)</span></td></tr>
        <tr><td>MAX5 · 산정 4주 · $1M</td><td>+0.0016 <span class="tstat">(0.40)</span></td><td class="neg">-0.0144*** <span class="tstat">(-2.87)</span></td></tr>
        <tr><td><strong>MAX5 · 산정 4주 · $5M</strong></td><td>-0.0016 <span class="tstat">(-0.37)</span></td><td class="neg"><strong>-0.0152*** <span class="tstat">(-3.37)</span></strong></td></tr>
    </table>

    <div class="fig">
        <img src="/assets/lottery-effect/B2_highlow_8configs.png" alt="8개 조합 High-Low">
        <div class="fig-caption">그림 3. 8개 조합의 High−Low 주간 수익률. 가치가중(주황) × 산정 4주 조합만 유의하다.</div>
    </div>

    <p class="body-text">여기서 흥미로운 패턴이 나온다. <strong>산정기간 2주는 어떤 조합에서도 효과가 없고, 4주(≈원논문의 1개월)는 강하게 유의하다.</strong> 이유는 신호의 선택도에 있다 — 14일 중 상위 5개는 상위 36%라 "극단"이 아니라 일반적 상방 변동성을 재는 반면, 28일 중 5개는 상위 18%로 원논문(약 17%)과 같은 극단만 골라낸다. MAX5 &gt; MAX1, VW &gt; EW 순위도 원논문과 정합적이다. 원논문의 설계 선택(1개월 산정 + MAX5)이 우연이 아님을 독립적으로 검증한 셈이다.</p>

    <div class="fig">
        <img src="/assets/lottery-effect/B4_longshort_cumulative.png" alt="롱숏 전략 누적가치">
        <div class="fig-caption">그림 4. Low−High 롱숏 누적가치 (VW, $5M, 로그축). MAX5·4주 조합만 일관되게 우상향 — 8년 누적 약 72배, 연환산 119%, Sharpe 1.14, 승률 60%. 거래비용 미반영.</div>
    </div>

    <p class="body-text">하위기간 강건성도 확인했다. 최강 조합(MAX5·4주·$5M)의 VW 효과는 2018–2021에서 -1.37%/주(t=-1.97), <strong>원논문이 볼 수 없었던 2022–2025에서 -1.67%/주(t=-2.91)로 오히려 더 유의하다</strong>. 표본외 검증을 통과한 것이다.</p>

    <h2 class="section-header">5. 이거 실제로 거래 가능한가: 선물시장 검증</h2>

    <p class="body-text">이상현상이 재현됐다면 다음 질문은 자연스럽다 — 왜 차익거래로 사라지지 않았을까? 답을 찾기 위해 바이낸스 USDT 무기한 선물(529개 계약)과 우리 유니버스를 교차시켰다.</p>

    <table class="data-table">
        <tr><th>실행 방식</th><th>VW High−Low</th><th>판정</th></tr>
        <tr><td>원전략 그대로 (전체 유니버스 롱숏)</td><td class="neg">-0.0152 <span class="tstat">(-3.37)</span></td><td>거래 불가 — Q1/Q5 코인 중 선물 존재 비율 5~6%</td></tr>
        <tr><td>교집합 방식: 전체로 소팅 → 선물 있는 것만 거래</td><td class="neg">-0.0147 <span class="tstat">(-1.86)</span></td><td>거래 가능 — 효과 유지, 유의성은 10% 수준으로 약화</td></tr>
        <tr><td>선물 유니버스 안에서만 소팅</td><td>-0.0036 <span class="tstat">(-0.51)</span></td><td>거래 가능하나 효과 소멸</td></tr>
    </table>

    <p class="body-text">세 번째 행이 이 이상현상의 정체를 말해준다. <strong>선물이 상장될 정도로 크고 유동적인 코인만 남기면 로또 효과가 사라진다.</strong> 효과의 원천은 공매도가 불가능한 마이크로캡에 있고, 그래서 차익거래가 청산하지 못한 채 지속된다 — 전형적인 limits-to-arbitrage 스토리다. 교집합 방식은 절충안으로 작동하지만(2025년에도 -2.08%/주), 매주 거래 가능 종목이 롱·숏 각 3~10개로 집중 리스크가 크고, Q5 숏은 신규 상장 밈코인이라 숏 스퀴즈를 주기적으로 맞는다.</p>

    <div class="warning-box">
        <div class="warning-label">실전 관점의 정직한 산수</div>
        <p class="body-text" style="margin-bottom:0;">기대 총수익 +1.47%/주에서 수수료(주간 리밸런싱 회전율 감안 0.1~0.3%/주), 펀딩비(Q5 신규상장 코인은 극단값 빈발), 슬리피지를 빼면 순엣지는 남을 가능성이 높지만 두껍지 않다. t=-1.86짜리 엣지는 "확실한 알파"가 아니라 "페이퍼 트레이딩으로 검증할 가설"이다. 신호 생성 파이프라인(바이낸스 API 연동, 매주 월요일 MAX5 소팅 → 롱/숏 목록 + 펀딩비 경고)은 구현해 뒀지만, 주문 자동화는 의도적으로 만들지 않았다.</p>
    </div>

    <h2 class="section-header">6. 재현 연구에서 배운 것</h2>

    <p class="body-text">재현 판정 요약:</p>

    <table class="data-table">
        <tr><th>원논문의 주장</th><th>판정</th><th>근거</th></tr>
        <tr><td>로또 효과 존재 (VW)</td><td><span class="verdict-pill vp-ok">재현</span></td><td>-4.78%/월 (t=-2.22), 원논문보다 강함</td></tr>
        <tr><td>로또 효과 존재 (EW)</td><td><span class="verdict-pill vp-no">미재현</span></td><td>윈저화 시에만 10% 유의 — 꼬리 노이즈에 민감</td></tr>
        <tr><td>12개월 지속성</td><td><span class="verdict-pill vp-part">부분 재현</span></td><td>2~6개월만 유의. 소멸 원인은 2020 코호트 × 2021 불장</td></tr>
        <tr><td>하위기간 강건성</td><td><span class="verdict-pill vp-ok">재현</span></td><td>표본외(2022.5~)에서 더 유의 (t=-2.91)</td></tr>
    </table>

    <p class="body-text">과정에서 데이터 품질의 교훈도 컸다. 원시 데이터에는 일수익률 +9.4×10<sup>44</sup> 같은 글리치가 있었고, 정제 없이는 High−Low가 +825%로 나오는 완전히 무의미한 결과가 나왔다. 반대로 정제를 강화할수록(일 &gt;300% 컷, 윈저화) 효과는 <em>더 유의해졌다</em>(VW t: -2.22 → -2.83 → -2.93) — 이상치가 만든 가짜 효과가 아니라, 이상치가 가리고 있던 진짜 효과라는 뜻이다.</p>

    <div class="conclusion-box">
        <h2 class="section-header">결론</h2>
        <p class="body-text">암호화폐 로또 효과는 독립 표본에서 가치가중 기준으로 원논문보다 강하게 재현되며, 원논문 표본 이후 3년간도 살아있다. 동일가중 효과와 12개월 지속성은 재현되지 않았고, 그 원인은 각각 마이크로캡 꼬리 노이즈와 2020–21 강세장 국면으로 특정된다. 효과가 지속되는 이유는 실행 제약이다 — 효과의 본산인 마이크로캡은 공매도가 불가능하고, 선물이 존재하는 종목만 남기면 효과가 사라진다. 학술적 이상현상과 거래 가능한 알파 사이의 간극을 이만큼 구체적으로 보여주는 사례도 드물다.</p>
        <p class="body-text" style="margin-bottom:0;">다음 단계: 이중 소팅(size·momentum 통제), Fama-MacBeth 회귀, 그리고 교집합 전략의 페이퍼 트레이딩 검증.</p>
    </div>

    <p class="body-text" style="font-size:14px; color:var(--wsj-gray);">
    참고문헌 — Wu, S.-F., C. Tuan-Mu, and K.-C. Yen. 2025. "Lottery-like Effect and Cryptocurrency." <i>Applied Economics Letters</i>. · Bali, T. G., N. Cakici, and R. F. Whitelaw. 2011. "Maxing Out: Stocks as Lotteries and the Cross-Section of Expected Returns." <i>Journal of Financial Economics</i> 99(2): 427–446. · Zhang, W., Y. Li, X. Xiong, and P. Wang. 2021. "Downside Risk and the Cross-Section of Cryptocurrency Returns." <i>Journal of Banking and Finance</i> 133: 106246.
    </p>
</div>
