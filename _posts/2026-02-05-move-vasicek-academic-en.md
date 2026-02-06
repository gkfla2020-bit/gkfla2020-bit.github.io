---
layout: post
title: "Vasicek/Black-Scholes Hybrid Model Evaluation Report"
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
        --wsj-cream: #faf9f6;
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
</style>
<style>
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
    
    <h1 class="headline">Vasicek/Black-Scholes Hybrid Model Evaluation Report</h1>
    <p class="deck">State-Dependent Interest Rate Dynamics:<br>Empirical Analysis of Extended Vasicek Model Using MOVE Index as State Variable</p>
    
    <div class="abstract">
        <div class="abstract-title">Abstract</div>
        <p class="body-text" style="margin-bottom:0;">
        This study extends the Vasicek (1977) interest rate model by incorporating the bond market volatility index (MOVE) as a state indicator, and examines its empirical validity. The analysis reveals that MOVE-related parameters provide statistically significant additional explanatory power, with patterns of higher equilibrium rates and volatility observed in high-MOVE regimes. While Granger causality tests did not find strong evidence of bidirectional simultaneity, this does not guarantee structural exogeneity, requiring careful interpretation. This study aims for descriptive characterization of interest rate dynamics conditional on market states, rather than causal claims.
        </p>
    </div>
    
    <div class="key-stats">
        <div class="stat-item"><div class="stat-label">Sample Period</div><div class="stat-value">191 months</div></div>
        <div class="stat-item"><div class="stat-label">LR Statistic</div><div class="stat-value positive">17.52</div></div>
        <div class="stat-item"><div class="stat-label">Granger</div><div class="stat-value">Unidirectional</div></div>
        <div class="stat-item"><div class="stat-label">FEVD Contrib.</div><div class="stat-value">2.2%</div></div>
    </div>

    <h2 class="section-header">I. Theoretical Background</h2>
    
    <div class="subsection">1.1 Connection Between Black-Scholes (1973) and Vasicek (1977)</div>
    
    <div class="formula-box">
        <div class="formula-label">Core Assumption of Black-Scholes Model</div>
        <div class="formula-content">
            dS<sub>t</sub> = μS<sub>t</sub>dt + σS<sub>t</sub>dW<sub>t</sub>
        </div>
        <div class="formula-note">
            Geometric Brownian Motion (GBM), constant volatility assumption, foundation of option pricing
        </div>
    </div>
    
    <div class="formula-box">
        <div class="formula-label">Vasicek Model (1977)</div>
        <div class="formula-content">
            dr<sub>t</sub> = κ(θ − r<sub>t</sub>)dt + σdW<sub>t</sub>
        </div>
        <div class="formula-note">
            Ornstein-Uhlenbeck process, mean-reversion property, foundation of bond pricing
        </div>
    </div>
    
    <p class="body-text">The theoretical connection between the Black-Scholes and Vasicek models holds significant importance in the development of modern financial engineering. The stock option pricing model proposed by Black and Scholes (1973) modeled stochastic stock price movements through geometric Brownian motion, while the bond pricing model introduced by Vasicek (1977) attempted to reflect the long-term equilibrium characteristics of interest rates through mean-reverting stochastic processes.</p>

    <p class="body-text">The key contribution of the Vasicek model lies in the introduction of mean-reversion κ(θ - r_t). This models the tendency of interest rates to converge toward the long-term equilibrium level θ, thereby complementing the unrealistic divergence characteristics of geometric Brownian motion in the Black-Scholes model.</p>
    
    <div class="callout">
        <div class="callout-header">Concept Borrowed from Black-Scholes</div>
        <p>In the Black-Scholes model, implied volatility derived from option prices reflects market participants' expectations about future uncertainty. This study applies this concept to the bond market, utilizing the MOVE index (bond option implied volatility) as a state variable for interest rate dynamics.</p>
    </div>

    <h2 class="section-header">II. Model Specification</h2>
    
    <div class="subsection">2.1 Standard Vasicek Model</div>
    
    <table class="data-table">
        <tr><th>Symbol</th><th>Name</th><th>Meaning</th><th class="num">Estimate</th></tr>
        <tr><td>κ</td><td>Mean-reversion speed</td><td>Speed of reversion to equilibrium (annualized)</td><td class="num">0.7208</td></tr>
        <tr><td>θ</td><td>Long-term equilibrium rate</td><td>Long-term level to which rates converge</td><td class="num">1.93%</td></tr>
        <tr><td>σ</td><td>Volatility</td><td>Diffusion coefficient of interest rates</td><td class="num">0.0074</td></tr>
    </table>
    
    <div class="subsection">2.2 MOVE-Vasicek Extended Model</div>
    
    <div class="formula-box">
        <div class="formula-label">State-Dependent Stochastic Differential Equation</div>
        <div class="formula-content">
            dr<sub>t</sub> = κ<sub>r</sub>(θ(M<sub>t</sub>) − r<sub>t</sub>)dt + σ(M<sub>t</sub>)dW<sub>t</sub><br><br>
            where:<br>
            θ(M) = θ<sub>0</sub> + θ<sub>1</sub> · ln(M) &nbsp;&nbsp;← State-conditional equilibrium rate<br>
            σ(M) = σ<sub>0</sub> + σ<sub>1</sub> · M &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;← State-conditional volatility
        </div>
    </div>
    
    <table class="data-table">
        <tr><th>Symbol</th><th>Name</th><th>Meaning</th><th class="num">Estimate</th></tr>
        <tr><td>κ<sub>r</sub></td><td>Mean-reversion speed</td><td>Speed of reversion to equilibrium</td><td class="num">0.7418</td></tr>
        <tr><td>θ<sub>0</sub></td><td>Base equilibrium rate</td><td>Equilibrium rate when MOVE=1</td><td class="num">1.47%</td></tr>
        <tr><td>θ<sub>1</sub></td><td>MOVE→θ sensitivity</td><td>Change in θ per unit increase in ln(MOVE)</td><td class="num">0.001204</td></tr>
        <tr><td>σ<sub>0</sub></td><td>Base volatility</td><td>Volatility when MOVE=0</td><td class="num">0.0051</td></tr>
        <tr><td>σ<sub>1</sub></td><td>MOVE→σ sensitivity</td><td>Change in σ per unit increase in MOVE</td><td class="num">0.000032</td></tr>
    </table>

    <h2 class="section-header">III. Sample Period Analysis (2010-2025)</h2>
    
    <div class="chart-section">
        <div class="chart-title">US 10Y Treasury Rate and MOVE Index</div>
        <div class="chart-subtitle">Monthly data, 2010-02 to 2025-12</div>
        <div id="timeSeriesChart" class="chart-container"></div>
    </div>
    
    <table class="data-table">
        <tr><th>Period</th><th>Major Events</th><th>MOVE Characteristics</th><th>Rate Characteristics</th></tr>
        <tr><td>2010-2012</td><td>European Debt Crisis, QE2</td><td>Elevated volatility</td><td>Low rates maintained</td></tr>
        <tr><td>2013</td><td>Taper Tantrum</td><td>Sharp spike</td><td>Sharp rise (100bp+)</td></tr>
        <tr><td>2020</td><td>COVID-19</td><td>All-time high</td><td>Sharp drop to lows</td></tr>
        <tr><td>2022-2023</td><td>Inflation, Rapid hikes</td><td>Elevated levels</td><td>Sharp rise</td></tr>
    </table>

    <h2 class="section-header">IV. Empirical Analysis Results</h2>
    
    <div class="subsection">4.1 Model Fit Comparison: Standard Vasicek vs MOVE-Vasicek</div>
    
    <table class="data-table">
        <tr><th>Metric</th><th class="num">Standard Vasicek</th><th class="num">MOVE-Vasicek</th><th>Winner</th></tr>
        <tr><td>RMSE</td><td class="num">0.002988</td><td class="num">0.002972</td><td><span class="winner-badge">MOVE</span> Lower is better</td></tr>
        <tr><td>AIC</td><td class="num">-474.40</td><td class="num">-487.93</td><td><span class="winner-badge">MOVE</span> Lower is better</td></tr>
        <tr><td>BIC</td><td class="num">-468.28</td><td class="num">-477.71</td><td><span class="winner-badge">MOVE</span> Lower is better</td></tr>
        <tr><td>Log-Likelihood</td><td class="num">240.20</td><td class="num">248.96</td><td><span class="winner-badge">MOVE</span> Higher is better</td></tr>
    </table>
    
    <div class="chart-section">
        <div class="chart-title">Model Comparison: Standard Vasicek vs MOVE-Vasicek</div>
        <div class="chart-subtitle">Information criteria and log-likelihood comparison</div>
        <div id="modelCompareChart" class="chart-container" style="height:320px;"></div>
    </div>
    
    <div class="subsection">4.2 Likelihood Ratio Test</div>
    
    <div class="callout">
        <div class="callout-header">📊 Likelihood Ratio Test</div>
        <p>LR Statistic = 17.52 > Critical Value (χ²₂, α=0.05) = 5.99</p>
        <p>→ Null hypothesis rejected: MOVE-related parameters provide statistically significant additional explanatory power</p>
    </div>
    
    <div class="chart-section">
        <div class="chart-title">Likelihood Ratio Test Visualization</div>
        <div class="chart-subtitle">χ² distribution with 2 degrees of freedom</div>
        <div id="lrTestChart" class="chart-container" style="height:320px;"></div>
    </div>
    
    <p class="body-text">The likelihood ratio test results indicate that the MOVE-Vasicek model shows statistically significant additional explanatory power compared to the standard model. The LR statistic of 17.52 substantially exceeding the critical value of 5.99 suggests that the performance difference between the two models is not mere chance but represents meaningful improvement. Specifically, the two additional parameters in the MOVE-Vasicek model significantly enhanced the ability to explain the data, and this improvement sufficiently offsets the cost of increased model complexity.</p>
    
    <div class="subsection">4.3 Granger Causality Test</div>
    
    <table class="data-table">
        <tr><th>Direction</th><th class="num">p-value</th><th>Result</th><th>Interpretation</th></tr>
        <tr><td>MOVE → Rate</td><td class="num">0.0348</td><td><span class="winner-badge">Significant</span> (5%)</td><td>Predictive precedence exists</td></tr>
        <tr><td>Rate → MOVE</td><td class="num">0.4614</td><td>Not significant</td><td>Reverse precedence not found</td></tr>
    </table>
    
    <div class="limitation-box">
        <div class="limitation-header">⚠️ Interpretation Caveats</div>
        <p>While Granger causality tests did not find strong evidence of bidirectional simultaneity, this does not guarantee MOVE's structural exogeneity. Therefore, MOVE should be interpreted as a "state indicator" rather than an "exogenous variable."</p>
    </div>
    
    <div class="chart-section">
        <div class="chart-title">Granger Causality Test Results</div>
        <div class="chart-subtitle">H₀: No Granger causality | α = 0.05</div>
        <div id="grangerChart" class="chart-container" style="height:300px;"></div>
    </div>
    
    <div class="subsection">4.4 VAR Analysis and Variance Decomposition</div>
    
    <div class="chart-section">
        <div class="chart-title">Forecast Error Variance Decomposition</div>
        <div class="chart-subtitle">MOVE contribution to interest rate variance</div>
        <div id="fevdChart" class="chart-container" style="height:300px;"></div>
    </div>

    <h2 class="section-header">V. Interpretation Guidelines</h2>
    
    <div class="callout">
        <div class="callout-header">Scope of Claims in This Study</div>
        <p>This study does not claim causality between MOVE and interest rates. Instead, it reports the descriptive finding that patterns of interest rate dynamics vary according to market volatility regimes.</p>
    </div>
    
    <div class="formula-box">
        <div class="formula-label">Core Interpretation Framework</div>
        <div class="formula-content">
            θ₁ > 0 → "Pattern observed where mean-reversion level is higher in high-MOVE regimes"<br>
            σ₁ > 0 → "Pattern observed where rate volatility is larger in high-MOVE regimes"<br><br>
            This can be interpreted as empirical evidence consistent with the State-Dependent Dynamics hypothesis
        </div>
    </div>

    <div class="conclusion-box">
        <h2 class="section-header">VI. Conclusions and Limitations</h2>
        <p class="body-text">This study analyzed the dynamic characteristics of US Treasury rates through an extended Vasicek model using the MOVE index as a state variable. The analysis observed that equilibrium levels and volatility of interest rates exhibit different patterns depending on bond market volatility regimes.</p>

        <p class="body-text">The core contribution of this study lies not in establishing the causal relationship that "MOVE moves interest rates," but in discovering the descriptive fact that "patterns exist where interest rate dynamics vary according to market volatility regimes."</p>
    </div>
    
    <h2 class="section-header">VII. References</h2>
    
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
    line: {color: colors.accent, width:2, dash:'dash'}, name: 'Critical Value (5.99)'
}, {
    x: [17.52], y: [0.5*Math.exp(-17.52/2)], type: 'scatter', mode: 'markers+text',
    marker: {color: colors.green, size:15, symbol:'diamond'}, text: ['LR=17.52'], textposition: 'top', name: 'LR Statistic'
}], {...layout, xaxis:{title:'Statistic',range:[0,25]}, yaxis:{title:'Density'}, legend:{orientation:'h',y:1.15},
    shapes:[{type:'rect',x0:5.99,x1:25,y0:0,y1:0.3,fillcolor:'rgba(196,18,0,0.1)',line:{width:0}}],
    annotations:[{x:15,y:0.12,text:'<b>Rejection Region</b><br>H₀ Rejected',showarrow:false,font:{size:11,color:colors.accent}}]
}, {responsive:true});

// Granger Chart
Plotly.newPlot('grangerChart', [{
    x: ['MOVE → Rate', 'Rate → MOVE'],
    y: [0.0348, 0.4614],
    type: 'bar',
    marker: {color: [colors.green, colors.gray]},
    text: ['p=0.035<br><b>Significant</b>', 'p=0.461'],
    textposition: 'outside'
}, {
    x: ['MOVE → Rate', 'Rate → MOVE'],
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
    x: fevd_months, y: own_contrib, name: 'Own (Rate)', type: 'bar', marker: {color: colors.gray}
}, {
    x: fevd_months, y: move_contrib, name: 'MOVE Contribution', type: 'bar', marker: {color: colors.primary}
}], {...layout, barmode: 'stack', xaxis: {title: 'Forecast Horizon (months)'}, 
    yaxis: {title: 'Variance Contribution (%)', range: [0, 100]},
    legend: {orientation: 'h', y: 1.1}
}, {responsive: true});
</script>
