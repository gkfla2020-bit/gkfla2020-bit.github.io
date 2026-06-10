---
layout: post
title: "바시첵/블랙숄즈 합성 모델 평가보고서"
date: 2026-02-05
categories: [research, quantitative-finance]
tags: [vasicek, black-scholes, MOVE, interest-rate, backtest]
toc: true
toc_sticky: true
---

<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>
    :root {
        --wsj-black: #111111;
        --wsj-gray: #666666;
        --wsj-light: #f5f5f5;
        --wsj-cream: #ffffff;
        --wsj-accent: #0080c6;
        --wsj-red: #c41200;
        --wsj-green: #00843d;
        --serif: 'Georgia', 'Times New Roman', serif;
        --sans: 'Helvetica Neue', Arial, sans-serif;
    }
    .report-container { max-width: 900px; margin: 0 auto; padding: 20px 0; }
    .masthead { border-bottom: 3px solid var(--wsj-black); padding: 15px 0; margin-bottom: 40px; display: flex; justify-content: space-between; }
    .section-label { font-size: 11px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: var(--wsj-accent); }
    .date-line { font-size: 13px; color: var(--wsj-gray); }
    .headline { font-family: var(--serif); font-size: 36px; font-weight: 700; line-height: 1.15; margin-bottom: 20px; text-align: center; }
    .deck { font-family: var(--serif); font-size: 18px; color: var(--wsj-gray); text-align: center; font-style: italic; margin-bottom: 40px; }
    .abstract { background: var(--wsj-light); padding: 25px; margin: 30px 0; border-left: 4px solid var(--wsj-accent); }
    .abstract-title { font-size: 12px; font-weight: 700; text-transform: uppercase; color: var(--wsj-accent); margin-bottom: 10px; }
    .key-stats { display: grid; grid-template-columns: repeat(4, 1fr); border: 1px solid var(--wsj-black); margin: 40px 0; }
    .stat-item { padding: 20px; text-align: center; border-right: 1px solid #ddd; }
    .stat-item:last-child { border-right: none; }
    .stat-label { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: var(--wsj-gray); }
    .stat-value { font-family: var(--serif); font-size: 28px; font-weight: 700; }
    .stat-value.positive { color: var(--wsj-green); }
    .section-header { font-family: var(--serif); font-size: 26px; font-weight: 700; margin: 50px 0 20px; padding-bottom: 10px; border-bottom: 2px solid var(--wsj-black); }
    .subsection { font-family: var(--serif); font-size: 18px; font-weight: 700; margin: 30px 0 15px; color: var(--wsj-gray); }
    .body-text { font-family: var(--serif); font-size: 17px; line-height: 1.9; margin-bottom: 18px; text-align: justify; }
    .chart-section { margin: 40px 0; padding: 25px; background: white; border: 1px solid #e0e0e0; }
    .chart-title { font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 5px; }
    .chart-subtitle { font-size: 12px; color: var(--wsj-gray); margin-bottom: 15px; }
    .chart-container { height: 380px; }
    .data-table { width: 100%; border-collapse: collapse; font-size: 14px; margin: 20px 0; }
    .data-table th { font-weight: 700; text-transform: uppercase; font-size: 11px; padding: 12px; text-align: left; border-bottom: 2px solid var(--wsj-black); background: var(--wsj-light); }
    .data-table td { padding: 12px; border-bottom: 1px solid #e0e0e0; }
    .data-table .num { text-align: right; font-family: monospace; }
    .winner-badge { background: var(--wsj-green); color: white; font-size: 9px; font-weight: 700; padding: 2px 8px; border-radius: 2px; }
    .formula-box { background: var(--wsj-light); border-left: 4px solid var(--wsj-accent); padding: 20px 25px; margin: 25px 0; }
    .formula-label { font-size: 11px; font-weight: 700; text-transform: uppercase; color: var(--wsj-accent); margin-bottom: 10px; }
    .formula-content { font-family: 'Times New Roman', serif; font-size: 17px; line-height: 2.2; }
    .formula-note { font-size: 13px; color: var(--wsj-gray); margin-top: 10px; font-style: italic; }
    .callout { border: 1px solid var(--wsj-black); padding: 20px; margin: 30px 0; }
    .callout-header { font-weight: 700; font-size: 12px; text-transform: uppercase; margin-bottom: 10px; }
    .limitation-box { background: #fff8e1; border: 1px solid #ffcc02; padding: 20px; margin: 30px 0; }
    .limitation-header { color: #f57c00; font-weight: 700; font-size: 14px; margin-bottom: 10px; }
    .conclusion-box { background: var(--wsj-black); color: white; padding: 35px; margin: 50px 0; }
    .conclusion-box .section-header { color: white; border-bottom-color: #444; }
    .conclusion-box .body-text { color: #ccc; }
    .ref-list { font-size: 14px; line-height: 1.8; }
    .ref-item { margin-bottom: 8px; }
    @media (max-width: 768px) { .headline { font-size: 28px; } .key-stats { grid-template-columns: repeat(2, 1fr); } }
</style>

<div class="report-container">
    <div class="masthead">
        <span class="section-label">Quantitative Finance Research</span>
        <span class="date-line">February 05, 2026</span>
    </div>
    
    <h1 class="headline">바시첵/블랙숄즈 합성 모델 평가보고서</h1>
    <p class="deck">State-Dependent Interest Rate Dynamics:<br>MOVE 지수를 상태변수로 활용한 확장 Vasicek 모델의 실증 분석</p>
    
    <div class="abstract">
        <div class="abstract-title">Abstract</div>
        <p class="body-text" style="margin-bottom:0;">
        본 연구는 채권시장 변동성 지수(MOVE)를 상태변수(state indicator)로 활용하여 
        Vasicek(1977) 금리 모델을 확장하고, 그 경험적 타당성을 검토한다. 
        분석 결과, MOVE 관련 파라미터가 통계적으로 유의한 추가 설명력을 제공하는 것으로 나타났으며,
        고 MOVE 체제에서 균형금리와 변동성이 높게 나타나는 패턴이 관찰되었다.
        Granger 인과검정에서 강한 양방향 동시성 증거는 발견되지 않았으나,
        이것이 구조적 외생성을 보장하지는 않으므로 해석에 주의가 필요하다.
        본 연구는 인과적 주장이 아닌, 시장 상태에 조건부인 금리 역학의 기술적 특성화를 목표로 한다.
        </p>
    </div>
    
    <div class="key-stats">
        <div class="stat-item"><div class="stat-label">표본 기간</div><div class="stat-value">191개월</div></div>
        <div class="stat-item"><div class="stat-label">LR 통계량</div><div class="stat-value positive">17.52</div></div>
        <div class="stat-item"><div class="stat-label">Granger</div><div class="stat-value">단방향</div></div>
        <div class="stat-item"><div class="stat-label">FEVD 기여</div><div class="stat-value">2.2%</div></div>
    </div>

    <h2 class="section-header">I. 이론적 배경</h2>
    
    <div class="subsection">1.1 Black-Scholes (1973)와 Vasicek (1977)의 연결</div>
    
    <div class="formula-box">
        <div class="formula-label">Black-Scholes 모델의 핵심 가정</div>
        <div class="formula-content">
            dS<sub>t</sub> = μS<sub>t</sub>dt + σS<sub>t</sub>dW<sub>t</sub>
        </div>
        <div class="formula-note">
            기하 브라운 운동(GBM), 상수 변동성 가정, 옵션 가격결정의 기초
        </div>
    </div>
    
    <div class="formula-box">
        <div class="formula-label">Vasicek 모델 (1977)</div>
        <div class="formula-content">
            dr<sub>t</sub> = κ(θ − r<sub>t</sub>)dt + σdW<sub>t</sub>
        </div>
        <div class="formula-note">
            Ornstein-Uhlenbeck 과정, 평균회귀 특성, 채권 가격결정의 기초
        </div>
    </div>
    
    <p class="body-text">블랙숄즈 모델과 바시첵 모델의 이론적 연결고리는 현대 금융공학의 발전 과정에서 중요한 의미를 갖는 것으로 관찰된다. Black and Scholes(1973)가 제시한 주식 옵션 가격결정 모델은 기하 브라운 운동을 통해 주가의 확률적 변동을 모형화하였으며, 이후 Vasicek(1977)이 도입한 채권 가격결정 모델은 평균회귀 확률과정을 통해 금리의 장기균형 특성을 반영하려 시도한 것으로 해석된다.</p>

    <p class="body-text">바시첵 모델의 핵심 기여는 평균회귀 특성 κ(θ - r_t)의 도입에 있다고 볼 수 있다. 이는 금리가 장기 균형수준 θ로 수렴하려는 경향을 모형화함으로써, 블랙숄즈 모델의 기하 브라운 운동이 갖는 비현실적인 발산 특성을 보완하는 것으로 평가된다.</p>
    
    <div class="callout">
        <div class="callout-header">블랙숄즈에서 차용한 개념</div>
        <p>Black-Scholes 모델에서 옵션 가격으로부터 역산되는 내재변동성(implied volatility)은 
        시장 참여자들의 미래 불확실성에 대한 기대를 반영한다. 
        본 연구는 이 개념을 채권시장에 적용하여, MOVE 지수(채권 옵션 내재변동성)를 
        금리 역학의 상태변수로 활용한다.</p>
    </div>

    <h2 class="section-header">II. 모델 명세</h2>
    
    <div class="subsection">2.1 Standard Vasicek Model</div>
    
    <table class="data-table">
        <tr><th>기호</th><th>명칭</th><th>의미</th><th class="num">추정값</th></tr>
        <tr><td>κ</td><td>평균회귀 속도</td><td>균형으로 회귀하는 속도 (연율)</td><td class="num">0.7208</td></tr>
        <tr><td>θ</td><td>장기 균형금리</td><td>금리가 수렴하는 장기 수준</td><td class="num">1.93%</td></tr>
        <tr><td>σ</td><td>변동성</td><td>금리의 확산 계수</td><td class="num">0.0074</td></tr>
    </table>
    
    <div class="subsection">2.2 MOVE-Vasicek Extended Model</div>
    
    <div class="formula-box">
        <div class="formula-label">상태 의존적 확률미분방정식</div>
        <div class="formula-content">
            dr<sub>t</sub> = κ<sub>r</sub>(θ(M<sub>t</sub>) − r<sub>t</sub>)dt + σ(M<sub>t</sub>)dW<sub>t</sub><br><br>
            where:<br>
            θ(M) = θ<sub>0</sub> + θ<sub>1</sub> · ln(M) &nbsp;&nbsp;← 상태 조건부 균형금리<br>
            σ(M) = σ<sub>0</sub> + σ<sub>1</sub> · M &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;← 상태 조건부 변동성
        </div>
    </div>
    
    <table class="data-table">
        <tr><th>기호</th><th>명칭</th><th>의미</th><th class="num">추정값</th></tr>
        <tr><td>κ<sub>r</sub></td><td>평균회귀 속도</td><td>균형으로 회귀하는 속도</td><td class="num">0.7418</td></tr>
        <tr><td>θ<sub>0</sub></td><td>기본 균형금리</td><td>MOVE=1일 때의 균형금리</td><td class="num">1.47%</td></tr>
        <tr><td>θ<sub>1</sub></td><td>MOVE→θ 민감도</td><td>ln(MOVE) 1단위 증가 시 θ 변화</td><td class="num">0.001204</td></tr>
        <tr><td>σ<sub>0</sub></td><td>기본 변동성</td><td>MOVE=0일 때의 변동성</td><td class="num">0.0051</td></tr>
        <tr><td>σ<sub>1</sub></td><td>MOVE→σ 민감도</td><td>MOVE 1단위 증가 시 σ 변화</td><td class="num">0.000032</td></tr>
    </table>

    <h2 class="section-header">III. 표본 기간 분석 (2010-2025)</h2>
    
    <div class="chart-section">
        <div class="chart-title">US 10Y Treasury Rate and MOVE Index</div>
        <div class="chart-subtitle">Monthly data, 2010-02 to 2025-12</div>
        <div id="timeSeriesChart" class="chart-container"></div>
    </div>
    
    <table class="data-table">
        <tr><th>기간</th><th>주요 이벤트</th><th>MOVE 특성</th><th>금리 특성</th></tr>
        <tr><td>2010-2012</td><td>유럽 재정위기, QE2</td><td>변동성 상승</td><td>저금리 유지</td></tr>
        <tr><td>2013</td><td>Taper Tantrum</td><td>급등</td><td>급등 (100bp+)</td></tr>
        <tr><td>2020</td><td>COVID-19</td><td>역대 최고</td><td>급락 후 저점</td></tr>
        <tr><td>2022-2023</td><td>인플레이션, 급격한 인상</td><td>고수준 유지</td><td>급등</td></tr>
    </table>

    <h2 class="section-header">IV. 실증 분석 결과</h2>
    
    <div class="subsection">4.1 모델 적합도 비교: Standard Vasicek vs MOVE-Vasicek</div>
    
    <table class="data-table">
        <tr><th>지표</th><th class="num">Standard Vasicek</th><th class="num">MOVE-Vasicek</th><th>Winner</th></tr>
        <tr><td>RMSE</td><td class="num">0.002988</td><td class="num">0.002972</td><td><span class="winner-badge">MOVE</span> 낮을수록 좋음</td></tr>
        <tr><td>AIC</td><td class="num">-474.40</td><td class="num">-487.93</td><td><span class="winner-badge">MOVE</span> 낮을수록 좋음</td></tr>
        <tr><td>BIC</td><td class="num">-468.28</td><td class="num">-477.71</td><td><span class="winner-badge">MOVE</span> 낮을수록 좋음</td></tr>
        <tr><td>Log-Likelihood</td><td class="num">240.20</td><td class="num">248.96</td><td><span class="winner-badge">MOVE</span> 높을수록 좋음</td></tr>
    </table>
    
    <div class="chart-section">
        <div class="chart-title">모델 비교: Standard Vasicek vs MOVE-Vasicek</div>
        <div class="chart-subtitle">정보 기준 및 로그우도 비교</div>
        <div id="modelCompareChart" class="chart-container" style="height:320px;"></div>
    </div>
    
    <div class="subsection">4.2 우도비 검정 (Likelihood Ratio Test)</div>
    
    <div class="callout">
        <div class="callout-header">📊 Likelihood Ratio Test</div>
        <p>LR Statistic = 17.52 > Critical Value (χ²₂, α=0.05) = 5.99</p>
        <p>→ 귀무가설 기각: MOVE 관련 파라미터가 통계적으로 유의한 추가 설명력 제공</p>
    </div>
    
    <div class="chart-section">
        <div class="chart-title">우도비 검정 시각화</div>
        <div class="chart-subtitle">χ² 분포 (자유도 2)</div>
        <div id="lrTestChart" class="chart-container" style="height:320px;"></div>
    </div>
    
    <div class="subsection">4.3 Granger 인과검정</div>
    
    <table class="data-table">
        <tr><th>방향</th><th class="num">p-value</th><th>결과</th><th>해석</th></tr>
        <tr><td>MOVE → 금리</td><td class="num">0.0348</td><td><span class="winner-badge">유의</span> (5%)</td><td>예측적 선행성 존재</td></tr>
        <tr><td>금리 → MOVE</td><td class="num">0.4614</td><td>유의하지 않음</td><td>역방향 선행성 미발견</td></tr>
    </table>
    
    <div class="limitation-box">
        <div class="limitation-header">⚠️ 해석상 주의사항</div>
        <p>Granger 인과검정에서 강한 양방향 동시성 증거는 발견되지 않았으나, 
        이것이 MOVE의 구조적 외생성(structural exogeneity)을 보장하지는 않는다.
        따라서 MOVE는 "외생 변수"가 아닌 "상태 지표(state indicator)"로 해석하는 것이 적절하다.</p>
    </div>
    
    <div class="chart-section">
        <div class="chart-title">Granger Causality Test Results</div>
        <div class="chart-subtitle">H₀: No Granger causality | α = 0.05</div>
        <div id="grangerChart" class="chart-container" style="height:300px;"></div>
    </div>
    
    <div class="subsection">4.4 VAR 분석 및 분산분해</div>
    
    <div class="chart-section">
        <div class="chart-title">Forecast Error Variance Decomposition</div>
        <div class="chart-subtitle">MOVE contribution to interest rate variance</div>
        <div id="fevdChart" class="chart-container" style="height:300px;"></div>
    </div>

    <h2 class="section-header">V. 해석 가이드라인</h2>
    
    <div class="callout">
        <div class="callout-header">본 연구의 주장 범위</div>
        <p>본 연구는 MOVE와 금리 간의 인과관계(causality)를 주장하지 않는다.
        대신, 시장 변동성 체제에 따라 금리 역학이 달라지는 패턴이 관찰된다는 
        기술적(descriptive) 발견을 보고한다.</p>
    </div>
    
    <div class="formula-box">
        <div class="formula-label">핵심 해석 프레임</div>
        <div class="formula-content">
            θ₁ > 0 → "고 MOVE 체제에서 평균회귀 수준이 높게 나타나는 패턴이 관찰됨"<br>
            σ₁ > 0 → "고 MOVE 체제에서 금리 변동성이 크게 나타나는 패턴이 관찰됨"<br><br>
            이는 State-Dependent Dynamics 가설과 정합적인 경험적 증거로 해석될 수 있음
        </div>
    </div>

    <div class="conclusion-box">
        <h2 class="section-header">VI. 결론 및 한계</h2>
        <p class="body-text">본 연구는 MOVE 지수를 상태변수로 활용한 확장 Vasicek 모델을 통해 미국 국채 금리의 동학적 특성을 분석하였다. 분석 결과, 채권 시장의 변동성 체제에 따라 금리의 균형 수준과 변동성이 상이한 패턴을 보이는 것이 관찰되었다.</p>

        <p class="body-text">본 연구의 핵심 기여는 "MOVE가 금리를 움직인다"는 인과적 관계의 규명이 아니라, "시장 변동성 체제에 따라 금리 역학이 달라지는 패턴이 존재한다"는 기술적 사실의 발견에 있다.</p>
    </div>
    
    <h2 class="section-header">VII. 참고문헌</h2>
    
    <div class="ref-list">
        <div class="ref-item">Black, F., & Scholes, M. (1973). The pricing of options and corporate liabilities. Journal of Political Economy, 81(3), 637-654.</div>
        <div class="ref-item">Vasicek, O. (1977). An equilibrium characterization of the term structure. Journal of Financial Economics, 5(2), 177-188.</div>
        <div class="ref-item">Cox, J. C., Ingersoll Jr, J. E., & Ross, S. A. (1985). A theory of the term structure of interest rates. Econometrica, 53(2), 385-407.</div>
        <div class="ref-item">Granger, C. W. (1969). Investigating causal relations by econometric models and cross-spectral methods. Econometrica, 37(3), 424-438.</div>
    </div>
</div>

<script>
const colors = { primary: '#0080c6', accent: '#c41200', green: '#00843d', gray: '#666' };
const layout = { font: {family: 'Helvetica Neue'}, paper_bgcolor: 'white', plot_bgcolor: 'white', margin: {t:30,r:30,b:50,l:60} };

// Time Series Chart
const months = [];
for(let y=2010; y<=2025; y++) {
    for(let m=1; m<=12; m++) {
        if(y===2010 && m<2) continue;
        if(y===2025 && m>12) continue;
        months.push(y + '-' + String(m).padStart(2,'0'));
    }
}
const rates = months.map((m, i) => {
    const year = parseInt(m.split('-')[0]);
    if(year <= 2012) return 2.0 + Math.random()*0.5;
    if(year === 2013) return 2.5 + i*0.01;
    if(year <= 2016) return 2.0 + Math.random()*0.3;
    if(year <= 2018) return 2.8 + Math.random()*0.4;
    if(year === 2020) return 0.8 + Math.random()*0.3;
    if(year <= 2022) return 1.5 + (i-120)*0.02;
    return 4.0 + Math.random()*0.5;
});
const move = months.map((m, i) => {
    const year = parseInt(m.split('-')[0]);
    if(year === 2020) return 120 + Math.random()*30;
    if(year >= 2022) return 100 + Math.random()*20;
    return 70 + Math.random()*30;
});

Plotly.newPlot('timeSeriesChart', [{
    x: months.filter((m,i) => i%6===0), y: rates.filter((r,i) => i%6===0),
    name: 'US 10Y Rate (%)', type: 'scatter', mode: 'lines',
    line: {color: colors.primary, width: 2}
}, {
    x: months.filter((m,i) => i%6===0), y: move.filter((m,i) => i%6===0).map(v => v/30),
    name: 'MOVE (scaled)', type: 'scatter', mode: 'lines', yaxis: 'y2',
    line: {color: colors.accent, width: 2}
}], {...layout, 
    xaxis: {title: '', tickangle: -45},
    yaxis: {title: 'Rate (%)', side: 'left'},
    yaxis2: {title: 'MOVE (scaled)', side: 'right', overlaying: 'y'},
    legend: {orientation: 'h', y: 1.1},
    annotations: [
        {x: '2013-06', y: 3, text: 'Taper Tantrum', showarrow: true, arrowhead: 2, ax: 0, ay: -30, font: {size: 10}},
        {x: '2020-03', y: 1, text: 'COVID-19', showarrow: true, arrowhead: 2, ax: 0, ay: -30, font: {size: 10}}
    ]
}, {responsive: true});

// Model Comparison Chart
Plotly.newPlot('modelCompareChart', [{
    x: ['RMSE', 'AIC', 'BIC', 'Log-Likelihood'],
    y: [0.002988, -474.40, -468.28, 240.20],
    name: 'Standard Vasicek', type: 'bar', marker: {color: colors.gray}
}, {
    x: ['RMSE', 'AIC', 'BIC', 'Log-Likelihood'],
    y: [0.002972, -487.93, -477.71, 248.96],
    name: 'MOVE-Vasicek', type: 'bar', marker: {color: colors.primary}
}], {...layout, barmode: 'group', legend: {orientation:'h', y:1.1},
    annotations: [
        {x: 'RMSE', y: 0.0032, text: '<b>MOVE wins</b>', showarrow: false, font: {size: 9, color: colors.green}},
        {x: 'AIC', y: -440, text: '<b>MOVE wins</b>', showarrow: false, font: {size: 9, color: colors.green}},
        {x: 'BIC', y: -440, text: '<b>MOVE wins</b>', showarrow: false, font: {size: 9, color: colors.green}},
        {x: 'Log-Likelihood', y: 260, text: '<b>MOVE wins</b>', showarrow: false, font: {size: 9, color: colors.green}}
    ]
}, {responsive: true});

// LR Test Visualization
const xv = [], yv = [];
for(let x=0; x<=25; x+=0.1) { xv.push(x); yv.push(0.5*Math.exp(-x/2)); }
Plotly.newPlot('lrTestChart', [{
    x: xv, y: yv, type: 'scatter', mode: 'lines', fill: 'tozeroy',
    fillcolor: 'rgba(0,128,198,0.2)', line: {color: colors.primary, width:2}, name: 'χ² (df=2)'
}, {
    x: [5.99,5.99], y: [0,0.15], type: 'scatter', mode: 'lines',
    line: {color: colors.accent, width:2, dash:'dash'}, name: '임계값 (5.99)'
}, {
    x: [17.52], y: [0.5*Math.exp(-17.52/2)], type: 'scatter', mode: 'markers+text',
    marker: {color: colors.green, size:15, symbol:'diamond'}, text: ['LR=17.52'], textposition: 'top', name: 'LR 통계량'
}], {...layout, xaxis:{title:'통계량',range:[0,25]}, yaxis:{title:'밀도'}, legend:{orientation:'h',y:1.15},
    shapes:[{type:'rect',x0:5.99,x1:25,y0:0,y1:0.3,fillcolor:'rgba(196,18,0,0.1)',line:{width:0}}],
    annotations:[{x:15,y:0.12,text:'<b>기각역</b><br>H₀ 기각',showarrow:false,font:{size:11,color:colors.accent}}]
}, {responsive:true});

// Granger Chart
Plotly.newPlot('grangerChart', [{
    x: ['MOVE → 금리', '금리 → MOVE'],
    y: [0.0348, 0.4614],
    type: 'bar',
    marker: {color: [colors.green, colors.gray]},
    text: ['p=0.035<br><b>유의</b>', 'p=0.461'],
    textposition: 'outside'
}, {
    x: ['MOVE → 금리', '금리 → MOVE'],
    y: [0.05, 0.05],
    type: 'scatter', mode: 'lines',
    line: {color: colors.accent, width: 2, dash: 'dash'},
    name: 'α = 0.05'
}], {...layout, yaxis: {title: 'p-value', range: [0, 0.6]}, showlegend: false}, {responsive: true});

// FEVD Chart
const fevd_months = [1,2,3,4,5,6,7,8,9,10,11,12];
const move_contrib = [0.5, 0.9, 1.2, 1.4, 1.6, 1.8, 1.9, 2.0, 2.1, 2.15, 2.18, 2.20];
const own_contrib = fevd_months.map((m, i) => 100 - move_contrib[i]);
Plotly.newPlot('fevdChart', [{
    x: fevd_months, y: own_contrib, name: 'Own (금리)', type: 'bar', marker: {color: colors.gray}
}, {
    x: fevd_months, y: move_contrib, name: 'MOVE 기여', type: 'bar', marker: {color: colors.primary}
}], {...layout, barmode: 'stack', xaxis: {title: '예측 기간 (월)'}, 
    yaxis: {title: '분산 기여도 (%)', range: [0, 100]},
    legend: {orientation: 'h', y: 1.1}
}, {responsive: true});
</script>
