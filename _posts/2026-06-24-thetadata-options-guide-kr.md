---
layout: post
title: "옵션 데이터 가이드 — 처음 보는 사람도 분석 시작할 수 있게"
date: 2026-06-24 14:00:00
permalink: /research/thetadata-options-guide-kr/
categories: [research, options, derivatives]
tags: [options, theta, iv, greeks, beginner, finance]
toc: true
toc_sticky: true
---

<style>
    :root {
        --wsj-black: #111111;
        --wsj-gray: #666666;
        --wsj-light: #f5f5f5;
        --wsj-cream: #ffffff;
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
    .analogy-box { background: #e8f4fd; border-left: 4px solid var(--wsj-accent); padding: 20px 25px; margin: 25px 0; border-radius: 0 8px 8px 0; }
    .analogy-label { font-size: 12px; font-weight: 700; text-transform: uppercase; color: var(--wsj-accent); margin-bottom: 8px; }
    .analogy-text { font-family: var(--serif); font-size: 16px; line-height: 1.8; }
    .code-block { background: #1e1e1e; color: #d4d4d4; padding: 20px; border-radius: 6px; font-family: var(--mono); font-size: 13px; line-height: 1.7; overflow-x: auto; margin: 20px 0; white-space: pre; }
    .code-kw { color: #569cd6; }
    .code-str { color: #ce9178; }
    .code-cm { color: #6a9955; }
    .code-fn { color: #dcdcaa; }
    .code-num { color: #b5cea8; }
    .code-cls { color: #4ec9b0; }
    .formula-box { background: var(--wsj-light); border-left: 4px solid var(--wsj-accent); padding: 20px 25px; margin: 25px 0; }
    .formula-label { font-size: 11px; font-weight: 700; text-transform: uppercase; color: var(--wsj-accent); margin-bottom: 10px; }
    .formula-content { font-family: var(--mono); font-size: 14px; line-height: 2.0; }
    .formula-note { font-size: 13px; color: var(--wsj-gray); margin-top: 10px; font-style: italic; }
    .data-table { width: 100%; border-collapse: collapse; font-size: 14px; margin: 20px 0; }
    .data-table th { font-weight: 700; text-transform: uppercase; font-size: 11px; padding: 12px; text-align: left; border-bottom: 2px solid var(--wsj-black); background: var(--wsj-light); }
    .data-table td { padding: 12px; border-bottom: 1px solid #e0e0e0; }
    .data-table .mono { font-family: var(--mono); font-size: 12px; }
    .step-box { background: white; border: 2px solid var(--wsj-accent); padding: 20px; margin: 20px 0; border-radius: 8px; }
    .step-number { display: inline-block; background: var(--wsj-accent); color: white; width: 32px; height: 32px; border-radius: 50%; text-align: center; line-height: 32px; font-weight: 700; font-size: 16px; margin-right: 10px; }
    .step-title { font-family: var(--sans); font-size: 16px; font-weight: 700; display: inline; }
    .warning-box { background: #fff3e0; border-left: 4px solid var(--wsj-orange); padding: 20px 25px; margin: 25px 0; }
    .warning-label { font-size: 12px; font-weight: 700; text-transform: uppercase; color: var(--wsj-orange); margin-bottom: 8px; }
    .conclusion-box { background: var(--wsj-black); color: white; padding: 35px; margin: 50px 0; }
    .conclusion-box .section-header { color: white; border-bottom-color: #444; }
    .conclusion-box .body-text { color: #ccc; }
    @media (max-width: 768px) { .headline { font-size: 26px; } }
</style>

<div class="report-container">
    <div class="masthead">
        <span class="section-label">Options · Beginner Guide</span>
        <span class="date-line">June 24, 2026</span>
    </div>

    <h1 class="headline">옵션 데이터 가이드<br>처음 보는 사람도 분석 시작할 수 있게</h1>
    <p class="deck">"이 컬럼이 대체 뭔데?" 라는 질문에 대한 완전한 답변.<br>옵션을 한 번도 거래해본 적 없어도 데이터를 읽고 해석할 수 있도록 단계별로 설명합니다.</p>

    <div class="abstract">
        <div class="abstract-title">이 글의 목표</div>
        <p class="body-text" style="margin-bottom:0;">
        ThetaData에서 받은 옵션 데이터에는 한 행마다 46개의 컬럼이 있다. <code>delta</code>, <code>vega</code>, <code>vanna</code>, <code>charm</code>, <code>vomma</code>... 처음 보면 외계어다. 이 글은 옵션이 무엇인지부터 시작해서, 그 46개 컬럼이 각각 무엇을 의미하는지, 어떻게 분석에 쓰는지를 <strong>비유와 단계별 설명</strong>으로 풀어낸다. 옵션 거래 경험이 0이어도 끝까지 읽으면 옵션 데이터로 분석을 시작할 수 있다.
        </p>
    </div>

    <h2 class="section-header">먼저, 옵션이 뭔가요</h2>

    <p class="body-text">한 문장으로: <strong>"미래의 어느 날에, 정해진 가격으로, 어떤 자산을 사거나 팔 수 있는 권리"</strong>.</p>

    <p class="body-text">권리이지 의무가 아니다. 행사하기 싫으면 안 해도 된다. 이 점이 선물(futures)과 결정적으로 다르다.</p>

    <div class="analogy-box">
        <div class="analogy-label">🎫 비유: 콘서트 예매권</div>
        <div class="analogy-text">
            BTS 콘서트가 6개월 후에 열리는데, 지금 "6개월 후에 15만원으로 입장권을 살 수 있는 권리"를 5만원에 사두는 것이다.<br><br>
            • <strong>6개월 후 콘서트가 대박나서 암표가 50만원에 거래된다</strong> → 권리 행사: 15만원에 사서 암표로 50만원에 판매. 이익 30만원.<br>
            • <strong>BTS가 콘서트를 취소했다</strong> → 권리 포기: 5만원만 손해. 의무가 아니라 권리니까.<br><br>
            이게 "콜 옵션"이다. 그 권리를 사기 위해 낸 5만원이 "프리미엄(옵션 가격)"이다.
        </div>
    </div>

    <h2 class="section-header">옵션의 4가지 핵심 부품</h2>

    <table class="data-table">
        <tr><th>이름</th><th>영문</th><th>의미</th><th>예시</th></tr>
        <tr><td>기초자산</td><td>Underlying</td><td>옵션이 가리키는 실제 자산</td><td class="mono">SPY</td></tr>
        <tr><td>행사가</td><td>Strike</td><td>미리 정해둔 매매 가격</td><td class="mono">600 ($600)</td></tr>
        <tr><td>만기일</td><td>Expiration</td><td>권리가 사라지는 날</td><td class="mono">2025-12-19</td></tr>
        <tr><td>권리 종류</td><td>Right</td><td>살 권리(콜) / 팔 권리(풋)</td><td class="mono">CALL or PUT</td></tr>
    </table>

    <div class="formula-box">
        <div class="formula-label">한 옵션 = 4개 정보의 조합</div>
        <div class="formula-content">SPY · 2025-12-19 만기 · 600 · CALL</div>
        <div class="formula-note">→ "SPY를 2025년 12월 19일에 600달러로 살 수 있는 권리"</div>
    </div>

    <h2 class="section-header">콜 vs 풋, 직관적으로</h2>

    <div class="step-box">
        <span class="step-number">C</span>
        <span class="step-title">콜 옵션 (CALL) — 살 권리</span>
        <p class="body-text" style="margin-top:10px;">기초자산 가격이 행사가 위로 올라가면 이익. 위로 가는 것에 베팅.</p>
        <p class="body-text">예: SPY 600 콜을 5달러에 샀다. 만기일 SPY가 620까지 올라가면 → 600에 사서 620에 팔 수 있음 = 20달러 이익. 5달러 프리미엄 빼면 순이익 15달러.</p>
    </div>

    <div class="step-box">
        <span class="step-number">P</span>
        <span class="step-title">풋 옵션 (PUT) — 팔 권리</span>
        <p class="body-text" style="margin-top:10px;">기초자산 가격이 행사가 아래로 내려가면 이익. 아래로 가는 것에 베팅 = 보험.</p>
        <p class="body-text">예: SPY 600 풋을 5달러에 샀다. 만기일 SPY가 580까지 떨어지면 → 600에 팔 수 있음 = 20달러 이익. 순이익 15달러. <strong>주식 폭락 헷지의 정석</strong>.</p>
    </div>

    <h2 class="section-header">옵션 가격은 어떻게 정해지나 — 5가지 요소</h2>

    <p class="body-text">시장에서 옵션 가격이 결정되는 데에는 정확히 다섯 가지 요인이 작용한다. 1973년 Black-Scholes-Merton 공식이 이를 수학적으로 정리했다.</p>

    <table class="data-table">
        <tr><th>기호</th><th>이름</th><th>옵션 가격에 미치는 영향</th></tr>
        <tr><td class="mono">S</td><td>기초자산 가격</td><td>콜은 S↑일 때 비싸짐, 풋은 S↓일 때 비싸짐</td></tr>
        <tr><td class="mono">K</td><td>행사가</td><td>콜은 K↓일 때 비싸짐, 풋은 K↑일 때 비싸짐</td></tr>
        <tr><td class="mono">T</td><td>만기까지 시간</td><td>T↑이면 둘 다 비싸짐 (시간 = 가능성)</td></tr>
        <tr><td class="mono">σ</td><td>변동성</td><td>σ↑이면 둘 다 비싸짐 <strong>(가장 중요)</strong></td></tr>
        <tr><td class="mono">r</td><td>무위험금리</td><td>콜에 +, 풋에 - (영향 작음)</td></tr>
    </table>

    <div class="analogy-box">
        <div class="analogy-label">💡 핵심: 변동성이 가장 중요하다</div>
        <div class="analogy-text">
            S, K, T, r은 다 객관적으로 측정 가능하다. 그런데 σ(변동성)는 <strong>"미래에 자산 가격이 얼마나 출렁일지"</strong>다. 누구도 미래를 모른다.<br><br>
            → 옵션 가격에서 가장 모호하고, 가장 거래의 핵심이고, 가장 분석 가치가 높은 변수가 σ다.
        </div>
    </div>

    <h2 class="section-header">내재변동성 (IV) — 가장 중요한 컬럼</h2>

    <p class="body-text">실제 시장의 옵션 가격을 BSM 공식에 거꾸로 넣어서 σ를 역산할 수 있다. 이걸 <strong>내재변동성(Implied Volatility, IV)</strong>이라고 한다.</p>

    <div class="formula-box">
        <div class="formula-label">정의</div>
        <div class="formula-content">시장 옵션 가격 = BSM(S, K, T, r, IV)</div>
        <div class="formula-note">→ S, K, T, r, 가격은 다 알고 있으니, 거꾸로 IV를 풀어낼 수 있다.<br>→ "시장이 미래에 예상하는 변동성" = IV</div>
    </div>

    <p class="body-text">IV는 옵션 분석의 알파이자 오메가다. 다음을 IV로 측정한다.</p>

    <div class="step-box">
        <span class="step-number">1</span>
        <span class="step-title">변동성 위험 프리미엄 (Volatility Risk Premium, VRP)</span>
        <p class="body-text" style="margin-top:10px;">IV (시장이 예상한 변동성) − RV (실제 발생한 변동성). <strong>평균적으로 +1~2%p</strong>다. 즉 시장은 항상 약간 더 두려워한다. 이 차이가 옵션 매도자의 평균적 수익원이다.</p>
    </div>

    <div class="step-box">
        <span class="step-number">2</span>
        <span class="step-title">변동성 스마일/스큐 (Volatility Smile/Skew)</span>
        <p class="body-text" style="margin-top:10px;">같은 만기, 다른 행사가의 IV를 그래프로 그리면 <strong>OTM 풋이 OTM 콜보다 IV가 높다</strong>. 시장이 좌측 꼬리(폭락)를 더 두려워한다는 증거.</p>
    </div>

    <div class="step-box">
        <span class="step-number">3</span>
        <span class="step-title">변동성 기간구조 (Term Structure)</span>
        <p class="body-text" style="margin-top:10px;">같은 행사가, 다른 만기의 IV. 평시에는 장기 IV가 단기 IV보다 높다(<strong>contango</strong>). 위기 때는 단기가 폭증한다(<strong>backwardation</strong>). 이 형태 변화로 시장 스트레스를 측정한다.</p>
    </div>

    <h2 class="section-header">ATM, ITM, OTM — 옵션 위치 용어</h2>

    <table class="data-table">
        <tr><th>약어</th><th>풀네임</th><th>의미</th><th>특징</th></tr>
        <tr><td><strong>ATM</strong></td><td>At-The-Money</td><td>행사가 ≈ 기초자산 가격</td><td>가장 활발히 거래. IV 분석에 가장 깨끗</td></tr>
        <tr><td><strong>ITM</strong></td><td>In-The-Money</td><td>콜: K&lt;S, 풋: K&gt;S</td><td>이미 가치 있음. 시간가치 작음</td></tr>
        <tr><td><strong>OTM</strong></td><td>Out-of-The-Money</td><td>콜: K&gt;S, 풋: K&lt;S</td><td>가능성 베팅. 만기까지 가야 가치 발생</td></tr>
    </table>

    <h2 class="section-header">옵션 데이터의 모양 — "체인(chain)"</h2>

    <p class="body-text">한 종목, 하루치 옵션 데이터는 <strong>체인 표</strong> 형태로 저장된다. 같은 만기 안의 모든 행사가가 한 표에 들어간다.</p>

    <div class="code-block"><span class="code-cm">SPY · 2025-12-19 만기 · 2025-08-15 관측</span>

행사가     콜 close   콜 IV    풋 close   풋 IV    OI(콜)   OI(풋)
-----      ------     ------   ------     ------   ------   ------
580        25.40      0.18     0.85       0.32     12,345   8,901
590        16.20      0.16     1.50       0.28      8,765   5,432
600        8.50       0.15     3.80       0.24      4,321   3,210   <span class="code-cm"># ATM</span>
610        3.20       0.14     8.40       0.22      2,109   1,876
620        0.85       0.13     16.10      0.21        987     654</div>

    <p class="body-text">하루에 한 종목 × 만기 수십 개 × 행사가 수십 개 = 수천 행. 1년치면 수십~수백만 행이 된다.</p>

    <h2 class="section-header">그릭스 (Greeks) — 옵션 가격의 민감도</h2>

    <p class="body-text">옵션 가격이 다섯 요소(S, K, T, σ, r)에 따라 변하는 정도를 측정한 게 <strong>그릭스</strong>다. 그리스 알파벳에서 이름을 따왔다고 해서 그릭스다 (예외: vega는 그리스 글자가 아님).</p>

    <div class="subsection">1차 그릭스 (필수 5개)</div>

    <div class="step-box">
        <span class="step-number">Δ</span>
        <span class="step-title">delta — 방향성 노출</span>
        <p class="body-text" style="margin-top:10px;">기초자산 가격 1달러 변화 시 옵션 가격이 얼마나 변하는가. 콜은 0~1, 풋은 -1~0. ATM 콜의 delta는 약 0.5다 (= "절반의 주식을 들고 있는 셈").</p>
    </div>

    <div class="step-box">
        <span class="step-number">Γ</span>
        <span class="step-title">gamma — delta의 변화율</span>
        <p class="body-text" style="margin-top:10px;">기초자산이 1달러 움직일 때 delta가 얼마나 변하는가. <strong>ATM, 만기 임박 시 폭증.</strong> 0DTE 옵션은 gamma 폭주 → 위험.</p>
    </div>

    <div class="step-box">
        <span class="step-number">Θ</span>
        <span class="step-title">theta — 시간 가치 소멸</span>
        <p class="body-text" style="margin-top:10px;">하루 지날 때 옵션 가격이 얼마나 줄어드는가 (대개 음수). <strong>옵션 매도자의 수익원</strong>이 바로 이 theta다. 매도자는 매일 시간 가치를 가져간다.</p>
    </div>

    <div class="step-box">
        <span class="step-number">V</span>
        <span class="step-title">vega — 변동성 민감도</span>
        <p class="body-text" style="margin-top:10px;">IV가 1%p 변화할 때 옵션 가격이 얼마나 변하는가. 변동성을 매수/매도하는 전략의 핵심 지표.</p>
    </div>

    <div class="step-box">
        <span class="step-number">ρ</span>
        <span class="step-title">rho — 금리 민감도</span>
        <p class="body-text" style="margin-top:10px;">무위험금리 1%p 변화 시 옵션 가격 변화. 단기 옵션은 거의 무시 가능. 장기 LEAPS는 신경 써야 함.</p>
    </div>

    <div class="subsection">고차 그릭스 (전문 분석용)</div>

    <p class="body-text">시장 마켓메이커, 변동성 트레이더, 학술 연구자가 쓴다. 일반 매매에는 거의 필요 없지만 우리 데이터에는 있으니 정리해둔다.</p>

    <table class="data-table">
        <tr><th>이름</th><th>측정 대상</th><th>언제 쓰나</th></tr>
        <tr><td class="mono">vanna</td><td>delta의 변동성 민감도</td><td>변동성 ↔ 방향성 교차 헷지</td></tr>
        <tr><td class="mono">charm</td><td>delta의 시간 민감도</td><td>만기 임박 시 ITM/OTM 정해지는 효과</td></tr>
        <tr><td class="mono">vomma</td><td>vega의 변동성 민감도</td><td>변동성 스마일 곡률</td></tr>
        <tr><td class="mono">veta</td><td>vega의 시간 민감도</td><td>장기 옵션 변동성 노출 변화</td></tr>
        <tr><td class="mono">speed, zomma, color, ultima</td><td>3차 그릭스</td><td>마켓메이커 미세 헷지</td></tr>
        <tr><td class="mono">d1, d2</td><td>BSM 공식 중간항</td><td>IV 계산 검증</td></tr>
    </table>

    <h2 class="section-header">Open Interest (OI) — 시장 참여도</h2>

    <p class="body-text">미결제약정. 그 옵션이 현재 몇 계약이 시장에 살아있는지. <strong>거래량(volume)과 다르다.</strong></p>

    <div class="formula-box">
        <div class="formula-label">차이</div>
        <div class="formula-content">volume = 그 날 새로 거래된 양
OI = 그 시점 미청산 계약 총량</div>
        <div class="formula-note">→ A가 B에게 팔고, B가 다시 C에게 팔면 volume은 +2이지만 OI는 +1만 증가.</div>
    </div>

    <p class="body-text">OI가 큰 행사가 = 시장이 그 가격대를 중요하게 본다. 만기 직전에 OI 가 폭락하면 = 만기 청산. 옵션 시장 미시구조 분석에 핵심.</p>

    <h2 class="section-header">EOD (End-of-Day) 데이터의 의미와 한계</h2>

    <p class="body-text">우리 데이터는 <strong>EOD</strong> = 하루의 마감(보통 16:00 ET) 시점 스냅샷이다. 하루 한 줄.</p>

    <div class="warning-box">
        <div class="warning-label">⚠️ EOD로 할 수 있는 것 / 할 수 없는 것</div>
        <p class="body-text" style="margin-bottom:0;">
        <strong>할 수 있는 것:</strong><br>
        • 일별 IV 변화, 변동성 위험 프리미엄<br>
        • 만기 구조(term structure) 시계열<br>
        • OI 변화로 본 시장 참여 패턴<br>
        • 종목 간 횡단면 비교 (SPY vs QQQ 등)<br><br>
        <strong>할 수 없는 것:</strong><br>
        • 인트라데이 가격 마이크로구조<br>
        • 0DTE 옵션의 시간대별 행태<br>
        • 호가창 깊이(depth) 변화<br>
        • 1초/1분 단위 헷지 시뮬레이션<br><br>
        → 인트라데이 분석이 필요하면 ThetaData의 분봉/틱 데이터를 따로 받아야 한다.
        </p>
    </div>

    <h2 class="section-header">우리 데이터의 46개 컬럼 — 카테고리별</h2>

    <table class="data-table">
        <tr><th>카테고리</th><th>컬럼</th><th>의미</th></tr>
        <tr><td><strong>식별자</strong></td><td class="mono">symbol, expiration, strike, right, _date</td><td>이 행이 가리키는 옵션</td></tr>
        <tr><td><strong>OHLC</strong></td><td class="mono">open, high, low, close, volume, count</td><td>그 옵션의 그 날 가격 변동</td></tr>
        <tr><td><strong>호가</strong></td><td class="mono">bid, ask, bid_size, ask_size, bid_exchange, ask_exchange</td><td>종가 시점 매수/매도 호가</td></tr>
        <tr><td><strong>1차 그릭스</strong></td><td class="mono">delta, gamma, theta, vega, rho</td><td>가격 민감도 5종</td></tr>
        <tr><td><strong>고차 그릭스</strong></td><td class="mono">vanna, charm, vomma, veta, vera, speed, zomma, color, ultima, epsilon, lambda</td><td>2-3차 민감도</td></tr>
        <tr><td><strong>BSM 보조</strong></td><td class="mono">d1, d2, dual_delta, dual_gamma</td><td>BSM 공식 중간 결과</td></tr>
        <tr><td><strong>IV</strong></td><td class="mono">implied_vol, iv_error</td><td>내재변동성 + 수렴 오차</td></tr>
        <tr><td><strong>기초자산</strong></td><td class="mono">underlying_price, underlying_timestamp</td><td>옵션과 동시점 SPY 가격</td></tr>
        <tr><td><strong>OI</strong></td><td class="mono">open_interest, timestamp_open_interest</td><td>미결제약정 + 측정 시각</td></tr>
    </table>

    <h2 class="section-header">데이터로 할 수 있는 분석 12가지</h2>

    <p class="body-text">이 데이터로 어떤 연구가 가능한지 분야별 예시.</p>

    <div class="subsection">A. 변동성 연구</div>

    <table class="data-table">
        <tr><th>#</th><th>주제</th><th>핵심 변수</th></tr>
        <tr><td>1</td><td>변동성 위험 프리미엄 (VRP) 측정</td><td>30D ATM IV − 30D 후행 RV</td></tr>
        <tr><td>2</td><td>변동성 스마일/스큐</td><td>OTM Put IV − OTM Call IV</td></tr>
        <tr><td>3</td><td>기간구조 (Contango/Backwardation)</td><td>(장기 IV − 단기 IV) / 단기 IV</td></tr>
    </table>

    <div class="subsection">B. 옵션 롤(roll) 전략</div>

    <table class="data-table">
        <tr><th>#</th><th>주제</th><th>핵심 변수</th></tr>
        <tr><td>4</td><td>VXX 롤 손실 정량화</td><td>1M IV vs 2M IV 차이의 누적</td></tr>
        <tr><td>5</td><td>SPY 풋 롤다운 매도 전략</td><td>theta 누적, gamma 위험</td></tr>
        <tr><td>6</td><td>캘린더 스프레드</td><td>같은 행사가 단기/장기 IV gap</td></tr>
    </table>

    <div class="subsection">C. 횡단면 비교</div>

    <table class="data-table">
        <tr><th>#</th><th>주제</th><th>핵심 변수</th></tr>
        <tr><td>7</td><td>SPY vs QQQ IV 스프레드</td><td>QQQ_IV − SPY_IV (같은 manyness)</td></tr>
        <tr><td>8</td><td>베타 헷지 비용</td><td>IWM 헷지: SPY풋 vs IWM풋</td></tr>
    </table>

    <div class="subsection">D. 시장 효율성·이벤트</div>

    <table class="data-table">
        <tr><th>#</th><th>주제</th><th>핵심 변수</th></tr>
        <tr><td>9</td><td>0DTE 만기일 행태</td><td>만기일 종가 OI / volume 패턴</td></tr>
        <tr><td>10</td><td>Put-Call Parity 위반</td><td>C − P − (S − K·e^(−rT))</td></tr>
        <tr><td>11</td><td>FOMC 전후 IV 점프</td><td>발표일 ±5일 IV 변화</td></tr>
        <tr><td>12</td><td>어닝 시즌 변동성</td><td>발표 전 IV inflation</td></tr>
    </table>

    <h2 class="section-header">분석 시작하기 — 코드 한 묶음</h2>

    <p class="body-text">Parquet으로 저장된 통합본을 DuckDB나 pandas로 읽으면 된다.</p>

    <div class="subsection">1. 한 만기 한 날의 체인 보기</div>

    <div class="code-block"><span class="code-kw">import</span> duckdb

df = duckdb.sql(<span class="code-str">"""
  SELECT _date, expiration, strike, right,
         close, bid, ask, implied_vol, delta, gamma, open_interest, underlying_price
  FROM read_parquet('data/eod/SPY/_ALL_SPY.parquet')
  WHERE _date = '2025-08-15'
    AND expiration = '2025-12-19'
    AND bid &gt; 0 AND ask &gt; 0
  ORDER BY strike, right
"""</span>).df()</div>

    <div class="subsection">2. ATM IV 시계열 (VRP 분석 시작점)</div>

    <div class="code-block"><span class="code-kw">import</span> pandas <span class="code-kw">as</span> pd

spy = pd.read_parquet(<span class="code-str">'data/eod/SPY/_ALL_SPY.parquet'</span>)
spy[<span class="code-str">'_date'</span>] = pd.to_datetime(spy[<span class="code-str">'_date'</span>])
spy[<span class="code-str">'dte'</span>] = (pd.to_datetime(spy[<span class="code-str">'expiration'</span>]) - spy[<span class="code-str">'_date'</span>]).dt.days
spy[<span class="code-str">'moneyness'</span>] = spy[<span class="code-str">'strike'</span>] / spy[<span class="code-str">'underlying_price'</span>]

<span class="code-cm"># 30DTE 부근 ATM 콜만</span>
atm_30d = spy[(spy[<span class="code-str">'dte'</span>].between(<span class="code-num">25</span>, <span class="code-num">35</span>)) &amp;
              (spy[<span class="code-str">'moneyness'</span>].between(<span class="code-num">0.99</span>, <span class="code-num">1.01</span>)) &amp;
              (spy[<span class="code-str">'right'</span>] == <span class="code-str">'CALL'</span>)]

daily_iv = atm_30d.groupby(<span class="code-str">'_date'</span>)[<span class="code-str">'implied_vol'</span>].mean()
daily_iv.plot(title=<span class="code-str">'SPY 30D ATM Call IV'</span>)</div>

    <div class="subsection">3. VXX 변동성 기간구조 (롤 손실)</div>

    <div class="code-block">vxx = pd.read_parquet(<span class="code-str">'data/eod/VXX/_ALL_VXX.parquet'</span>)
vxx[<span class="code-str">'_date'</span>] = pd.to_datetime(vxx[<span class="code-str">'_date'</span>])
vxx[<span class="code-str">'dte'</span>] = (pd.to_datetime(vxx[<span class="code-str">'expiration'</span>]) - vxx[<span class="code-str">'_date'</span>]).dt.days

<span class="code-cm"># ATM 콜만 추출</span>
atm = vxx[(vxx[<span class="code-str">'right'</span>]==<span class="code-str">'CALL'</span>) &amp;
          (<span class="code-fn">abs</span>(vxx[<span class="code-str">'strike'</span>] - vxx[<span class="code-str">'underlying_price'</span>]) &lt; <span class="code-num">1</span>)]

<span class="code-cm"># 1개월 vs 2개월 IV 비교</span>
front = atm[atm[<span class="code-str">'dte'</span>].between(<span class="code-num">20</span>, <span class="code-num">35</span>)].groupby(<span class="code-str">'_date'</span>)[<span class="code-str">'implied_vol'</span>].mean()
back  = atm[atm[<span class="code-str">'dte'</span>].between(<span class="code-num">50</span>, <span class="code-num">70</span>)].groupby(<span class="code-str">'_date'</span>)[<span class="code-str">'implied_vol'</span>].mean()

contango = (back - front) / front
contango.plot(title=<span class="code-str">'VXX term structure: (back - front) / front'</span>)</div>

    <h2 class="section-header">학술 인용 — 데이터 신뢰도</h2>

    <div class="callout-orange" style="background: #fff3e0; border: 1px solid var(--wsj-orange); padding: 20px 25px; margin: 25px 0;">
        <p class="body-text" style="margin-bottom:0;">
        ThetaData는 <strong>OPRA(Options Price Reporting Authority)</strong>의 정식 라이센시다. OPRA는 미국 SEC가 옵션거래소들에 통합 호가 보고를 의무화하면서 만들어진 공식 데이터 채널이다.<br><br>
        즉, OptionMetrics(Wharton WRDS), Bloomberg, Refinitiv가 쓰는 <strong>같은 OPRA 원천</strong>을 우리도 쓴다. 학술 출판에 필요한 데이터 신뢰도는 충족한다.
        </p>
    </div>

    <div class="conclusion-box">
        <h2 class="section-header">정리</h2>
        <p class="body-text">
        옵션은 미래의 권리이고, 그 가격은 5가지 요소(S, K, T, σ, r)로 결정된다. 그중 σ가 가장 중요하고, 시장 가격에서 거꾸로 σ를 풀어낸 게 <strong>IV(내재변동성)</strong>다.
        </p>
        <p class="body-text">
        그릭스는 옵션 가격이 5요소 변화에 얼마나 민감한지를 측정한 도구다. 1차 그릭스 5개(Δ Γ Θ Vega ρ)만 알아도 대부분의 분석이 가능하다.
        </p>
        <p class="body-text">
        EOD 데이터는 인트라데이 마이크로구조를 못 본다는 한계가 있지만, <strong>VRP, 기간구조, 롤 손실, 횡단면 비교</strong> 같은 일반적 변동성 연구에는 충분하다.
        </p>
        <p class="body-text" style="color:white;">
        <strong>다음 글</strong>에서는 이 데이터를 실제로 받아서 저장하는 운영 가이드—Theta Terminal 설치, REST API 호출, Parquet 아카이빙, 이어받기 정책—를 다룬다.
        </p>
    </div>

</div>
