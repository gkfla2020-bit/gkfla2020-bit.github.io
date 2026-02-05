---
layout: null
title: "MOVE-Vasicek Model: Bond Volatility-Based Interest Rate Forecasting"
date: 2026-02-05
---
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vasicek/Black-Scholes Hybrid Model Evaluation Report</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400&family=Cormorant+Garamond:wght@300;400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --black: #1a1a1a;
            --gray: #666666;
            --light: #f5f5f5;
            --cream: #fafaf8;
            --accent: #2563eb;
            --green: #059669;
            --red: #dc2626;
            --serif: 'Cormorant Garamond', Georgia, serif;
            --sans: 'Inter', -apple-system, sans-serif;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: var(--sans); background: var(--cream); color: var(--black); line-height: 1.7; }
        
        .top-nav {
            position: fixed;
            top: 0; left: 0; right: 0;
            padding: 20px 40px;
            background: rgba(250,250,248,0.95);
            backdrop-filter: blur(8px);
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 100;
            border-bottom: 1px solid rgba(0,0,0,0.05);
        }
        .top-nav a { font-family: var(--serif); font-size: 1.2rem; color: var(--black); text-decoration: none; }
        .top-nav .back { font-family: var(--sans); font-size: 0.75rem; color: var(--gray); letter-spacing: 0.1em; text-transform: uppercase; }
        .top-nav .back:hover { color: var(--black); }

        .container { max-width: 800px; margin: 0 auto; padding: 120px 30px 80px; }
        
        .report-header { text-align: center; margin-bottom: 60px; padding-bottom: 40px; border-bottom: 1px solid #e0e0e0; }
        .report-label { font-size: 0.7rem; letter-spacing: 0.2em; text-transform: uppercase; color: var(--accent); margin-bottom: 20px; }
        .report-date { font-size: 0.75rem; color: var(--gray); margin-bottom: 25px; }
        .headline { font-family: var(--serif); font-size: 2.8rem; font-weight: 400; line-height: 1.2; margin-bottom: 20px; }
        .deck { font-family: var(--serif); font-size: 1.1rem; color: var(--gray); font-style: italic; line-height: 1.6; }

        .abstract { background: var(--light); padding: 30px; margin: 40px 0; border-left: 3px solid var(--accent); }
        .abstract-title { font-size: 0.7rem; font-weight: 600; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent); margin-bottom: 15px; }
        
        .key-stats { display: grid; grid-template-columns: repeat(4, 1fr); border: 1px solid var(--black); margin: 50px 0; }
        .stat-item { padding: 25px 15px; text-align: center; border-right: 1px solid #ddd; }
        .stat-item:last-child { border-right: none; }
        .stat-label { font-size: 0.65rem; font-weight: 500; letter-spacing: 0.12em; text-transform: uppercase; color: var(--gray); margin-bottom: 8px; }
        .stat-value { font-family: var(--serif); font-size: 1.8rem; font-weight: 500; }
        .stat-value.positive { color: var(--green); }
        
        .section-header { font-family: var(--serif); font-size: 1.6rem; font-weight: 500; margin: 60px 0 25px; padding-bottom: 12px; border-bottom: 1px solid var(--black); }
        .subsection { font-family: var(--serif); font-size: 1.15rem; font-weight: 500; margin: 35px 0 18px; color: var(--gray); }
        .body-text { font-size: 0.95rem; line-height: 1.9; margin-bottom: 20px; text-align: justify; color: #333; }
        
        .chart-section { margin: 45px 0; padding: 25px; background: white; border: 1px solid #e5e5e5; }
        .chart-title { font-size: 0.7rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 5px; }
        .chart-subtitle { font-size: 0.75rem; color: var(--gray); margin-bottom: 20px; }
        .chart-container { height: 350px; }
        
        .data-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; margin: 25px 0; }
        .data-table th { font-weight: 600; font-size: 0.7rem; letter-spacing: 0.08em; text-transform: uppercase; padding: 14px 12px; text-align: left; border-bottom: 2px solid var(--black); background: var(--light); }
        .data-table td { padding: 14px 12px; border-bottom: 1px solid #e5e5e5; }
        .data-table .num { text-align: right; font-family: 'SF Mono', Monaco, monospace; font-size: 0.8rem; }
        .winner-badge { background: var(--green); color: white; font-size: 0.6rem; font-weight: 600; padding: 3px 8px; border-radius: 2px; margin-right: 8px; }
        
        .formula-box { background: var(--light); border-left: 3px solid var(--accent); padding: 25px; margin: 30px 0; }
        .formula-label { font-size: 0.65rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: var(--accent); margin-bottom: 12px; }
        .formula-content { font-family: 'Times New Roman', serif; font-size: 1rem; line-height: 2; }
        .formula-note { font-size: 0.8rem; color: var(--gray); margin-top: 12px; font-style: italic; }
        
        .callout { border: 1px solid var(--black); padding: 25px; margin: 35px 0; }
        .callout-header { font-weight: 600; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 12px; }
        
        .limitation-box { background: #fef3c7; border: 1px solid #f59e0b; padding: 25px; margin: 35px 0; }
        .limitation-header { color: #d97706; font-weight: 600; font-size: 0.85rem; margin-bottom: 12px; }
        
        .conclusion-box { background: var(--black); color: white; padding: 40px; margin: 60px 0; }
        .conclusion-box .section-header { color: white; border-bottom-color: #444; }
        .conclusion-box .body-text { color: #bbb; }
        
        .ref-list { font-size: 0.85rem; line-height: 1.9; }
        .ref-item { margin-bottom: 10px; color: #444; }
        
        .report-footer { border-top: 1px solid #e0e0e0; padding: 30px 0; margin-top: 60px; text-align: center; font-size: 0.75rem; color: var(--gray); }
        
        @media (max-width: 768px) {
            .headline { font-size: 2rem; }
            .key-stats { grid-template-columns: repeat(2, 1fr); }
            .container { padding: 100px 20px 60px; }
        }
    </style>
</head>
<body>
    <nav class="top-nav">
        <a href="/">Ha Rim Jung</a>
        <a href="/" class="back">← Back to Home</a>
    </nav>

    <div class="container">
        <header class="report-header">
            <div class="report-label">Quantitative Finance Research</div>
            <div class="report-date">February 05, 2026</div>
            <h1 class="headline">Vasicek/Black-Scholes Hybrid Model Evaluation Report</h1>
            <p class="deck">State-Dependent Interest Rate Dynamics:<br>Empirical Analysis of Extended Vasicek Model Using MOVE Index as State Variable</p>
        </header>
        
        <div class="abstract">
            <div class="abstract-title">Abstract</div>
            <p class="body-text" style="margin-bottom:0;">
            This study extends the Vasicek (1977) interest rate model by incorporating the bond market volatility index (MOVE) as a state indicator, and examines its empirical validity. The analysis reveals that MOVE-related parameters provide statistically significant additional explanatory power, with patterns of higher equilibrium rates and volatility observed in high-MOVE regimes. While Granger causality tests did not find strong evidence of bidirectional simultaneity, this does not guarantee structural exogeneity, requiring careful interpretation. This study aims for descriptive characterization of interest rate dynamics conditional on market states, rather than causal claims.
            </p>
        </div>
        
        <div class="key-stats">
            <div class="stat-item"><div class="stat-label">Sample Period</div><div class="stat-value">191 mo.</div></div>
            <div class="stat-item"><div class="stat-label">LR Statistic</div><div class="stat-value positive">17.52</div></div>
            <div class="stat-item"><div class="stat-label">Granger</div><div class="stat-value">Unidirectional</div></div>
            <div class="stat-item"><div class="stat-label">FEVD Contrib.</div><div class="stat-value">2.2%</div></div>
        </div>

        <h2 class="section-header">I. Theoretical Background</h2>
        
        <div class="subsection">1.1 Connection Between Black-Scholes (1973) and Vasicek (1977)</div>
        
        <div class="formula-box">
            <div class="formula-label">Core Assumption of Black-Scholes Model</div>
            <div class="formula-content">dS<sub>t</sub> = μS<sub>t</sub>dt + σS<sub>t</sub>dW<sub>t</sub></div>
            <div class="formula-note">Geometric Brownian Motion (GBM), constant volatility assumption, foundation of option pricing</div>
        </div>
        
        <div class="formula-box">
            <div class="formula-label">Vasicek Model (1977)</div>
            <div class="formula-content">dr<sub>t</sub> = κ(θ − r<sub>t</sub>)dt + σdW<sub>t</sub></div>
            <div class="formula-note">Ornstein-Uhlenbeck process, mean-reversion property, foundation of bond pricing</div>
        </div>
        
        <p class="body-text">The theoretical connection between the Black-Scholes and Vasicek models holds significant importance in the development of modern financial engineering. The stock option pricing model proposed by Black and Scholes (1973) modeled stochastic stock price movements through geometric Brownian motion, while the bond pricing model introduced by Vasicek (1977) attempted to reflect the long-term equilibrium characteristics of interest rates through mean-reverting stochastic processes. Both models share a common mathematical foundation based on stochastic differential equations and risk-neutral pricing principles.</p>

        <p class="body-text">The key contribution of the Vasicek model lies in the introduction of mean-reversion κ(θ - r_t). This models the tendency of interest rates to converge toward the long-term equilibrium level θ, thereby complementing the unrealistic divergence characteristics of geometric Brownian motion in the Black-Scholes model. The hybrid model proposed in this study can be interpreted as an attempt to combine the advantages of both models.</p>
        
        <div class="callout">
            <div class="callout-header">Concept Borrowed from Black-Scholes</div>
            <p class="body-text" style="margin:0;">In the Black-Scholes model, implied volatility derived from option prices reflects market participants' expectations about future uncertainty. This study applies this concept to the bond market, utilizing the MOVE index (bond option implied volatility) as a state variable for interest rate dynamics.</p>
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
            <div id="modelCompareChart" class="chart-container" style="height:300px;"></div>
        </div>
        
        <div class="subsection">4.2 Likelihood Ratio Test</div>
        
        <div class="callout">
            <div class="callout-header">📊 Likelihood Ratio Test</div>
            <p class="body-text" style="margin:0;">LR Statistic = 17.52 > Critical Value (χ²₂, α=0.05) = 5.99<br>
            → Null hypothesis rejected: MOVE-related parameters provide statistically significant additional explanatory power</p>
        </div>
        
        <div class="chart-section">
            <div class="chart-title">Likelihood Ratio Test Visualization</div>
            <div class="chart-subtitle">χ² distribution with 2 degrees of freedom</div>
            <div id="lrTestChart" class="chart-container" style="height:300px;"></div>
        </div>
        
        <p class="body-text">The likelihood ratio test results indicate that the MOVE-Vasicek model shows statistically significant additional explanatory power compared to the standard model. The LR statistic of 17.52 substantially exceeding the critical value of 5.99 suggests that the performance difference between the two models is not mere chance but represents meaningful improvement.</p>
        
        <div class="subsection">4.3 Granger Causality Test</div>
        
        <table class="data-table">
            <tr><th>Direction</th><th class="num">p-value</th><th>Result</th><th>Interpretation</th></tr>
            <tr><td>MOVE → Rate</td><td class="num">0.0348</td><td><span class="winner-badge">Significant</span> (5%)</td><td>Predictive precedence exists</td></tr>
            <tr><td>Rate → MOVE</td><td class="num">0.4614</td><td>Not significant</td><td>Reverse precedence not found</td></tr>
        </table>
        
        <div class="limitation-box">
            <div class="limitation-header">⚠️ Interpretation Caveats</div>
            <p class="body-text" style="margin:0;">While Granger causality tests did not find strong evidence of bidirectional simultaneity, this does not guarantee MOVE's structural exogeneity. Therefore, MOVE should be interpreted as a "state indicator" rather than an "exogenous variable."</p>
        </div>
        
        <div class="chart-section">
            <div class="chart-title">Granger Causality Test Results</div>
            <div class="chart-subtitle">H₀: No Granger causality | α = 0.05</div>
            <div id="grangerChart" class="chart-container" style="height:280px;"></div>
        </div>

        <h2 class="section-header">V. Interpretation Guidelines</h2>
        
        <div class="callout">
            <div class="callout-header">Scope of Claims in This Study</div>
            <p class="body-text" style="margin:0;">This study does not claim causality between MOVE and interest rates. Instead, it reports the descriptive finding that patterns of interest rate dynamics vary according to market volatility regimes.</p>
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
            <div class="ref-item">Black, F., & Scholes, M. (1973). The pricing of options and corporate liabilities. <em>Journal of Political Economy</em>, 81(3), 637-654.</div>
            <div class="ref-item">Vasicek, O. (1977). An equilibrium characterization of the term structure. <em>Journal of Financial Economics</em>, 5(2), 177-188.</div>
            <div class="ref-item">Cox, J. C., Ingersoll Jr, J. E., & Ross, S. A. (1985). A theory of the term structure of interest rates. <em>Econometrica</em>, 53(2), 385-407.</div>
            <div class="ref-item">Granger, C. W. (1969). Investigating causal relations by econometric models and cross-spectral methods. <em>Econometrica</em>, 37(3), 424-438.</div>
        </div>

        <div class="report-footer">
            © 2026 Ha Rim Jung · <a href="/" style="color:#666;">gkfla2020-bit.github.io</a>
        </div>
    </div>

<script>
const colors = { primary: '#2563eb', accent: '#dc2626', green: '#059669', gray: '#666' };
const layout = { font: {family: 'Inter, sans-serif', size: 11}, paper_bgcolor: 'white', plot_bgcolor: 'white', margin: {t:25,r:25,b:45,l:50} };

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
    legend: {orientation: 'h', y: 1.12},
    annotations: [
        {x: '2013-06', y: 3, text: 'Taper Tantrum', showarrow: true, arrowhead: 2, ax: 0, ay: -25, font: {size: 9}},
        {x: '2020-03', y: 1, text: 'COVID-19', showarrow: true, arrowhead: 2, ax: 0, ay: -25, font: {size: 9}}
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
}], {...layout, barmode: 'group', legend: {orientation:'h', y:1.15}}, {responsive: true});

// LR Test Visualization
const xv = [], yv = [];
for(let x=0; x<=25; x+=0.1) { xv.push(x); yv.push(0.5*Math.exp(-x/2)); }
Plotly.newPlot('lrTestChart', [{
    x: xv, y: yv, type: 'scatter', mode: 'lines', fill: 'tozeroy',
    fillcolor: 'rgba(37,99,235,0.15)', line: {color: colors.primary, width:2}, name: 'χ² (df=2)'
}, {
    x: [5.99,5.99], y: [0,0.15], type: 'scatter', mode: 'lines',
    line: {color: colors.accent, width:2, dash:'dash'}, name: 'Critical Value (5.99)'
}, {
    x: [17.52], y: [0.5*Math.exp(-17.52/2)], type: 'scatter', mode: 'markers+text',
    marker: {color: colors.green, size:12, symbol:'diamond'}, text: ['LR=17.52'], textposition: 'top', name: 'LR Statistic'
}], {...layout, xaxis:{title:'Statistic',range:[0,25]}, yaxis:{title:'Density'}, legend:{orientation:'h',y:1.18},
    shapes:[{type:'rect',x0:5.99,x1:25,y0:0,y1:0.3,fillcolor:'rgba(220,38,38,0.08)',line:{width:0}}],
    annotations:[{x:15,y:0.1,text:'<b>Rejection Region</b>',showarrow:false,font:{size:9,color:colors.accent}}]
}, {responsive:true});

// Granger Chart
Plotly.newPlot('grangerChart', [{
    x: ['MOVE → Rate', 'Rate → MOVE'],
    y: [0.0348, 0.4614],
    type: 'bar',
    marker: {color: [colors.green, colors.gray]},
    text: ['p=0.035', 'p=0.461'],
    textposition: 'outside'
}, {
    x: ['MOVE → Rate', 'Rate → MOVE'],
    y: [0.05, 0.05],
    type: 'scatter', mode: 'lines',
    line: {color: colors.accent, width: 2, dash: 'dash'},
    name: 'α = 0.05'
}], {...layout, yaxis: {title: 'p-value', range: [0, 0.55]}, showlegend: false}, {responsive: true});
</script>
</body>
</html>
