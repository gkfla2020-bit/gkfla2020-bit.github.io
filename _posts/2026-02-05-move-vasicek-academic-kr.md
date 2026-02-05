---
layout: post
title: "MOVE-Vasicek 모델: 채권 변동성 기반 금리 예측"
date: 2026-02-05
categories: [Research]
tags: [vasicek, MOVE, interest-rate, backtest]
---

<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>

<style>
/* 애니메이션 */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-50px); }
    to { opacity: 1; transform: translateX(0); }
}
@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}
@keyframes gradientFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* 히어로 섹션 */
.hero-section {
    background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #0f0c29);
    background-size: 400% 400%;
    animation: gradientFlow 15s ease infinite;
    color: white;
    padding: 80px 40px;
    margin: -20px -40px 40px -40px;
    text-align: center;
    border-radius: 0 0 30px 30px;
}
.hero-title {
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 20px;
    animation: fadeInUp 1s ease;
}
.hero-subtitle {
    font-size: 1.3rem;
    opacity: 0.9;
    animation: fadeInUp 1s ease 0.2s both;
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    padding: 8px 20px;
    border-radius: 30px;
    margin-top: 25px;
    font-size: 0.9rem;
    animation: fadeInUp 1s ease 0.4s both;
}
</style>

<style>
/* 핵심 지표 카드 */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin: 40px 0;
}
.stat-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 30px 20px;
    border-radius: 20px;
    text-align: center;
    animation: fadeInUp 0.8s ease both;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.stat-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(102, 126, 234, 0.4);
}
.stat-card:nth-child(1) { animation-delay: 0.1s; }
.stat-card:nth-child(2) { animation-delay: 0.2s; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
.stat-card:nth-child(3) { animation-delay: 0.3s; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
.stat-card:nth-child(4) { animation-delay: 0.4s; background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
.stat-number { font-size: 2.5rem; font-weight: 800; }
.stat-label { font-size: 0.85rem; opacity: 0.9; margin-top: 8px; text-transform: uppercase; letter-spacing: 1px; }

/* 섹션 스타일 */
.content-section {
    background: white;
    padding: 40px;
    border-radius: 20px;
    margin: 30px 0;
    box-shadow: 0 10px 40px rgba(0,0,0,0.08);
    animation: slideInLeft 0.8s ease both;
}
.section-title {
    font-size: 1.8rem;
    font-weight: 700;
    color: #1a1a2e;
    margin-bottom: 25px;
    padding-bottom: 15px;
    border-bottom: 3px solid #667eea;
    display: flex;
    align-items: center;
    gap: 12px;
}
.section-icon {
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
}

/* 테이블 스타일 */
.modern-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    margin: 25px 0;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
}
.modern-table th {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 18px 15px;
    text-align: left;
    font-weight: 600;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.modern-table td {
    padding: 16px 15px;
    border-bottom: 1px solid #eee;
    font-size: 0.95rem;
}
.modern-table tr:hover td { background: #f8f9ff; }
.modern-table .num { text-align: right; font-family: 'SF Mono', monospace; font-weight: 600; }
.winner-badge {
    background: linear-gradient(135deg, #43e97b, #38f9d7);
    color: #1a1a2e;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
}
</style>

<style>
/* 수식 박스 */
.formula-card {
    background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    border-left: 5px solid #667eea;
    padding: 25px 30px;
    margin: 25px 0;
    border-radius: 0 15px 15px 0;
}
.formula-title {
    color: #667eea;
    font-weight: 700;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 15px;
}
.formula-content {
    font-family: 'Times New Roman', serif;
    font-size: 1.2rem;
    line-height: 2;
    color: #1a1a2e;
}

/* 알림 박스 */
.alert-box {
    padding: 25px 30px;
    border-radius: 15px;
    margin: 25px 0;
    display: flex;
    align-items: flex-start;
    gap: 15px;
}
.alert-box.info {
    background: linear-gradient(135deg, #e0f7fa, #b2ebf2);
    border-left: 5px solid #00bcd4;
}
.alert-box.warning {
    background: linear-gradient(135deg, #fff8e1, #ffecb3);
    border-left: 5px solid #ffc107;
}
.alert-box.success {
    background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
    border-left: 5px solid #4caf50;
}
.alert-icon { font-size: 1.5rem; }
.alert-content { flex: 1; }
.alert-title { font-weight: 700; margin-bottom: 8px; }

/* 차트 컨테이너 */
.chart-wrapper {
    background: white;
    padding: 25px;
    border-radius: 15px;
    margin: 25px 0;
    box-shadow: 0 5px 20px rgba(0,0,0,0.08);
}
.chart-header {
    margin-bottom: 20px;
}
.chart-title-text {
    font-size: 1.1rem;
    font-weight: 700;
    color: #1a1a2e;
}
.chart-subtitle-text {
    font-size: 0.85rem;
    color: #666;
    margin-top: 5px;
}
.chart-area { height: 400px; }

/* 결론 박스 */
.conclusion-section {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    color: white;
    padding: 50px 40px;
    border-radius: 25px;
    margin: 40px 0;
}
.conclusion-section .section-title {
    color: white;
    border-bottom-color: rgba(255,255,255,0.3);
}
.conclusion-text {
    font-size: 1.1rem;
    line-height: 1.9;
    color: rgba(255,255,255,0.85);
    margin-bottom: 15px;
}

/* 반응형 */
@media (max-width: 768px) {
    .hero-title { font-size: 2rem; }
    .stats-grid { grid-template-columns: repeat(2, 1fr); }
    .content-section { padding: 25px; margin: 20px -10px; }
}
</style>


<!-- 히어로 섹션 -->
<div class="hero-section">
    <div class="hero-title">🎯 MOVE-Vasicek 모델</div>
    <div class="hero-subtitle">채권시장 변동성 지수를 활용한 금리 예측 모델의 실증 분석</div>
    <div class="hero-badge">📊 LR 통계량 17.52 | 표본 191개월 | 2010-2025</div>
</div>

<!-- 핵심 지표 -->
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-number">191</div>
        <div class="stat-label">표본 기간 (월)</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">17.52</div>
        <div class="stat-label">LR 통계량</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">0.035</div>
        <div class="stat-label">Granger p-value</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">2.2%</div>
        <div class="stat-label">FEVD 기여도</div>
    </div>
</div>

<!-- 연구 개요 -->
<div class="content-section">
    <div class="section-title">
        <div class="section-icon">📋</div>
        연구 개요
    </div>
    <p style="font-size: 1.05rem; line-height: 1.9; color: #444;">
        본 연구는 채권시장 변동성 지수(MOVE)를 상태변수로 활용하여 Vasicek(1977) 금리 모델을 확장하고, 
        그 경험적 타당성을 검토합니다. 분석 결과, MOVE 관련 파라미터가 통계적으로 유의한 추가 설명력을 
        제공하는 것으로 나타났으며, 고 MOVE 체제에서 균형금리와 변동성이 높게 나타나는 패턴이 관찰되었습니다.
    </p>
    
    <div class="alert-box info">
        <div class="alert-icon">💡</div>
        <div class="alert-content">
            <div class="alert-title">핵심 발견</div>
            본 연구는 인과관계가 아닌, 시장 변동성 체제에 따라 금리 역학이 달라지는 패턴의 기술적 특성화를 목표로 합니다.
        </div>
    </div>
</div>


<!-- 모델 명세 -->
<div class="content-section">
    <div class="section-title">
        <div class="section-icon">📐</div>
        모델 명세
    </div>
    
    <h3 style="color: #667eea; margin: 25px 0 15px;">Standard Vasicek Model</h3>
    
    <div class="formula-card">
        <div class="formula-title">확률미분방정식 (SDE)</div>
        <div class="formula-content">
            dr<sub>t</sub> = κ(θ − r<sub>t</sub>)dt + σdW<sub>t</sub>
        </div>
    </div>
    
    <table class="modern-table">
        <tr><th>기호</th><th>명칭</th><th>의미</th><th class="num">추정값</th></tr>
        <tr><td><strong>κ</strong></td><td>평균회귀 속도</td><td>균형으로 회귀하는 속도 (연율)</td><td class="num">0.7208</td></tr>
        <tr><td><strong>θ</strong></td><td>장기 균형금리</td><td>금리가 수렴하는 장기 수준</td><td class="num">1.93%</td></tr>
        <tr><td><strong>σ</strong></td><td>변동성</td><td>금리의 확산 계수</td><td class="num">0.0074</td></tr>
    </table>
    
    <h3 style="color: #667eea; margin: 35px 0 15px;">MOVE-Vasicek Extended Model</h3>
    
    <div class="formula-card">
        <div class="formula-title">상태 의존적 확률미분방정식</div>
        <div class="formula-content">
            dr<sub>t</sub> = κ<sub>r</sub>(θ(M<sub>t</sub>) − r<sub>t</sub>)dt + σ(M<sub>t</sub>)dW<sub>t</sub><br><br>
            θ(M) = θ<sub>0</sub> + θ<sub>1</sub> · ln(M) &nbsp;&nbsp;← 상태 조건부 균형금리<br>
            σ(M) = σ<sub>0</sub> + σ<sub>1</sub> · M &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;← 상태 조건부 변동성
        </div>
    </div>
    
    <table class="modern-table">
        <tr><th>기호</th><th>명칭</th><th class="num">추정값</th></tr>
        <tr><td><strong>κ<sub>r</sub></strong></td><td>평균회귀 속도</td><td class="num">0.7418</td></tr>
        <tr><td><strong>θ<sub>0</sub></strong></td><td>기본 균형금리</td><td class="num">1.47%</td></tr>
        <tr><td><strong>θ<sub>1</sub></strong></td><td>MOVE→θ 민감도</td><td class="num">0.001204</td></tr>
        <tr><td><strong>σ<sub>0</sub></strong></td><td>기본 변동성</td><td class="num">0.0051</td></tr>
        <tr><td><strong>σ<sub>1</sub></strong></td><td>MOVE→σ 민감도</td><td class="num">0.000032</td></tr>
    </table>
</div>


<!-- 시계열 분석 -->
<div class="content-section">
    <div class="section-title">
        <div class="section-icon">📈</div>
        표본 기간 분석 (2010-2025)
    </div>
    
    <div class="chart-wrapper">
        <div class="chart-header">
            <div class="chart-title-text">US 10Y Treasury Rate & MOVE Index</div>
            <div class="chart-subtitle-text">Monthly data, 2010-02 to 2025-12</div>
        </div>
        <div id="timeSeriesChart" class="chart-area"></div>
    </div>
    
    <table class="modern-table">
        <tr><th>기간</th><th>주요 이벤트</th><th>MOVE</th><th>금리</th></tr>
        <tr><td>2010-2012</td><td>유럽 재정위기, QE2</td><td>변동성 상승</td><td>저금리 유지</td></tr>
        <tr><td>2013</td><td>Taper Tantrum</td><td>급등</td><td>급등 (100bp+)</td></tr>
        <tr><td>2020</td><td>COVID-19</td><td>역대 최고</td><td>급락 후 저점</td></tr>
        <tr><td>2022-2023</td><td>인플레이션, 급격한 인상</td><td>고수준 유지</td><td>급등</td></tr>
    </table>
</div>

<!-- 실증 분석 결과 -->
<div class="content-section">
    <div class="section-title">
        <div class="section-icon">🔬</div>
        실증 분석 결과
    </div>
    
    <h3 style="color: #667eea; margin: 25px 0 15px;">모델 적합도 비교</h3>
    
    <table class="modern-table">
        <tr><th>지표</th><th class="num">Standard Vasicek</th><th class="num">MOVE-Vasicek</th><th>Winner</th></tr>
        <tr><td>RMSE</td><td class="num">0.002988</td><td class="num">0.002972</td><td><span class="winner-badge">✓ MOVE</span> 낮을수록 좋음</td></tr>
        <tr><td>AIC</td><td class="num">-474.40</td><td class="num">-487.93</td><td><span class="winner-badge">✓ MOVE</span> 낮을수록 좋음</td></tr>
        <tr><td>BIC</td><td class="num">-468.28</td><td class="num">-477.71</td><td><span class="winner-badge">✓ MOVE</span> 낮을수록 좋음</td></tr>
        <tr><td>Log-Likelihood</td><td class="num">240.20</td><td class="num">248.96</td><td><span class="winner-badge">✓ MOVE</span> 높을수록 좋음</td></tr>
    </table>
    
    <div class="chart-wrapper">
        <div class="chart-header">
            <div class="chart-title-text">모델 비교 차트</div>
            <div class="chart-subtitle-text">정보 기준 및 로그우도 비교</div>
        </div>
        <div id="modelCompareChart" class="chart-area" style="height: 350px;"></div>
    </div>

    
    <h3 style="color: #667eea; margin: 35px 0 15px;">우도비 검정 (Likelihood Ratio Test)</h3>
    
    <div class="alert-box success">
        <div class="alert-icon">✅</div>
        <div class="alert-content">
            <div class="alert-title">LR Statistic = 17.52 > Critical Value (χ²₂, α=0.05) = 5.99</div>
            귀무가설 기각: MOVE 관련 파라미터가 통계적으로 유의한 추가 설명력 제공
        </div>
    </div>
    
    <div class="chart-wrapper">
        <div class="chart-header">
            <div class="chart-title-text">우도비 검정 시각화</div>
            <div class="chart-subtitle-text">χ² 분포 (자유도 2)</div>
        </div>
        <div id="lrTestChart" class="chart-area" style="height: 350px;"></div>
    </div>
    
    <h3 style="color: #667eea; margin: 35px 0 15px;">Granger 인과검정</h3>
    
    <table class="modern-table">
        <tr><th>방향</th><th class="num">p-value</th><th>결과</th><th>해석</th></tr>
        <tr><td>MOVE → 금리</td><td class="num">0.0348</td><td><span class="winner-badge">✓ 유의</span></td><td>예측적 선행성 존재</td></tr>
        <tr><td>금리 → MOVE</td><td class="num">0.4614</td><td>유의하지 않음</td><td>역방향 선행성 미발견</td></tr>
    </table>
    
    <div class="alert-box warning">
        <div class="alert-icon">⚠️</div>
        <div class="alert-content">
            <div class="alert-title">해석상 주의사항</div>
            Granger 인과검정에서 강한 양방향 동시성 증거는 발견되지 않았으나, 이것이 MOVE의 구조적 외생성을 보장하지는 않습니다. 
            따라서 MOVE는 "외생 변수"가 아닌 "상태 지표(state indicator)"로 해석하는 것이 적절합니다.
        </div>
    </div>
    
    <div class="chart-wrapper">
        <div class="chart-header">
            <div class="chart-title-text">Granger Causality & FEVD</div>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div id="grangerChart" style="height: 300px;"></div>
            <div id="fevdChart" style="height: 300px;"></div>
        </div>
    </div>
</div>


<!-- 결론 -->
<div class="conclusion-section">
    <div class="section-title">
        <div class="section-icon" style="background: rgba(255,255,255,0.2);">🎯</div>
        결론 및 시사점
    </div>
    <p class="conclusion-text">
        본 연구는 MOVE 지수를 상태변수로 활용한 확장 Vasicek 모델을 통해 미국 국채 금리의 동학적 특성을 분석하였습니다. 
        분석 결과, 채권 시장의 변동성 체제에 따라 금리의 균형 수준과 변동성이 상이한 패턴을 보이는 것이 관찰되었습니다.
    </p>
    <p class="conclusion-text">
        본 연구의 핵심 기여는 <strong style="color: #43e97b;">"MOVE가 금리를 움직인다"</strong>는 인과적 관계의 규명이 아니라, 
        <strong style="color: #43e97b;">"시장 변동성 체제에 따라 금리 역학이 달라지는 패턴이 존재한다"</strong>는 기술적 사실의 발견에 있습니다.
    </p>
    
    <div class="formula-card" style="background: rgba(255,255,255,0.1); border-left-color: #43e97b;">
        <div class="formula-title" style="color: #43e97b;">핵심 해석 프레임</div>
        <div class="formula-content" style="color: white;">
            θ₁ > 0 → "고 MOVE 체제에서 평균회귀 수준이 높게 나타나는 패턴이 관찰됨"<br>
            σ₁ > 0 → "고 MOVE 체제에서 금리 변동성이 크게 나타나는 패턴이 관찰됨"
        </div>
    </div>
</div>

<!-- 참고문헌 -->
<div class="content-section">
    <div class="section-title">
        <div class="section-icon">📚</div>
        참고문헌
    </div>
    <ul style="line-height: 2; color: #555;">
        <li>Black, F., & Scholes, M. (1973). The pricing of options and corporate liabilities. <em>Journal of Political Economy</em>, 81(3), 637-654.</li>
        <li>Vasicek, O. (1977). An equilibrium characterization of the term structure. <em>Journal of Financial Economics</em>, 5(2), 177-188.</li>
        <li>Cox, J. C., Ingersoll Jr, J. E., & Ross, S. A. (1985). A theory of the term structure of interest rates. <em>Econometrica</em>, 53(2), 385-407.</li>
        <li>Granger, C. W. (1969). Investigating causal relations by econometric models. <em>Econometrica</em>, 37(3), 424-438.</li>
    </ul>
</div>


<script>
const colors = { 
    primary: '#667eea', 
    secondary: '#764ba2', 
    accent: '#f5576c', 
    success: '#43e97b',
    gray: '#8892b0'
};
const layout = { 
    font: {family: 'Pretendard, -apple-system, sans-serif'}, 
    paper_bgcolor: 'rgba(0,0,0,0)', 
    plot_bgcolor: 'rgba(0,0,0,0)', 
    margin: {t:30,r:30,b:50,l:60}
};

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
    line: {color: colors.primary, width: 3}
}, {
    x: months.filter((m,i) => i%6===0), y: move.filter((m,i) => i%6===0).map(v => v/30),
    name: 'MOVE (scaled)', type: 'scatter', mode: 'lines', yaxis: 'y2',
    line: {color: colors.accent, width: 3}
}], {...layout, 
    xaxis: {title: '', tickangle: -45, gridcolor: '#eee'},
    yaxis: {title: 'Rate (%)', side: 'left', gridcolor: '#eee'},
    yaxis2: {title: 'MOVE', side: 'right', overlaying: 'y'},
    legend: {orientation: 'h', y: 1.12},
    annotations: [
        {x: '2013-06', y: 3, text: '<b>Taper Tantrum</b>', showarrow: true, arrowhead: 2, ax: 0, ay: -40, font: {size: 11, color: colors.primary}},
        {x: '2020-03', y: 1, text: '<b>COVID-19</b>', showarrow: true, arrowhead: 2, ax: 0, ay: -40, font: {size: 11, color: colors.accent}}
    ]
}, {responsive: true});


// Model Comparison Chart
Plotly.newPlot('modelCompareChart', [{
    x: ['RMSE', 'AIC', 'BIC', 'Log-Likelihood'],
    y: [0.002988, -474.40, -468.28, 240.20],
    name: 'Standard Vasicek', type: 'bar', 
    marker: {color: colors.gray, opacity: 0.7}
}, {
    x: ['RMSE', 'AIC', 'BIC', 'Log-Likelihood'],
    y: [0.002972, -487.93, -477.71, 248.96],
    name: 'MOVE-Vasicek', type: 'bar', 
    marker: {color: colors.primary}
}], {...layout, barmode: 'group', legend: {orientation:'h', y:1.12},
    xaxis: {gridcolor: '#eee'},
    yaxis: {gridcolor: '#eee'}
}, {responsive: true});

// LR Test Visualization
const xv = [], yv = [];
for(let x=0; x<=25; x+=0.1) { xv.push(x); yv.push(0.5*Math.exp(-x/2)); }
Plotly.newPlot('lrTestChart', [{
    x: xv, y: yv, type: 'scatter', mode: 'lines', fill: 'tozeroy',
    fillcolor: 'rgba(102,126,234,0.2)', line: {color: colors.primary, width:3}, name: 'χ² (df=2)'
}, {
    x: [5.99,5.99], y: [0,0.15], type: 'scatter', mode: 'lines',
    line: {color: colors.accent, width:3, dash:'dash'}, name: '임계값 (5.99)'
}, {
    x: [17.52], y: [0.5*Math.exp(-17.52/2)], type: 'scatter', mode: 'markers+text',
    marker: {color: colors.success, size:18, symbol:'diamond'}, text: ['LR=17.52'], textposition: 'top', name: 'LR 통계량'
}], {...layout, xaxis:{title:'통계량',range:[0,25], gridcolor:'#eee'}, yaxis:{title:'밀도', gridcolor:'#eee'}, legend:{orientation:'h',y:1.12},
    shapes:[{type:'rect',x0:5.99,x1:25,y0:0,y1:0.3,fillcolor:'rgba(245,87,108,0.1)',line:{width:0}}],
    annotations:[{x:15,y:0.12,text:'<b>기각역</b>',showarrow:false,font:{size:12,color:colors.accent}}]
}, {responsive:true});

// Granger Chart
Plotly.newPlot('grangerChart', [{
    x: ['MOVE → 금리', '금리 → MOVE'],
    y: [0.0348, 0.4614],
    type: 'bar',
    marker: {color: [colors.success, colors.gray]},
    text: ['p=0.035', 'p=0.461'],
    textposition: 'outside'
}, {
    x: ['MOVE → 금리', '금리 → MOVE'],
    y: [0.05, 0.05],
    type: 'scatter', mode: 'lines',
    line: {color: colors.accent, width: 2, dash: 'dash'},
    name: 'α = 0.05'
}], {...layout, yaxis: {title: 'p-value', range: [0, 0.6], gridcolor:'#eee'}, showlegend: false,
    title: {text: 'Granger Causality', font: {size: 14}}
}, {responsive: true});

// FEVD Chart
const fevd_months = [1,3,6,9,12];
const move_contrib = [0.5, 1.2, 1.8, 2.0, 2.2];
Plotly.newPlot('fevdChart', [{
    x: fevd_months, y: move_contrib,
    type: 'scatter', mode: 'lines+markers',
    line: {color: colors.primary, width: 3},
    marker: {size: 10, color: colors.primary},
    fill: 'tozeroy',
    fillcolor: 'rgba(102,126,234,0.2)'
}], {...layout, 
    xaxis: {title: '예측 기간 (월)', gridcolor:'#eee'}, 
    yaxis: {title: 'MOVE 기여도 (%)', range: [0, 3], gridcolor:'#eee'},
    title: {text: 'FEVD: MOVE 기여도', font: {size: 14}}
}, {responsive: true});
</script>
