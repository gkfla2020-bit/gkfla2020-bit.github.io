---
layout: post
title: "MOVE-Vasicek Model: Bond Volatility-Based Interest Rate Forecasting"
date: 2026-02-05
categories: [Research]
tags: [vasicek, MOVE, interest-rate, backtest]
---

<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>

<style>
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-50px); }
    to { opacity: 1; transform: translateX(0); }
}
@keyframes gradientFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

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
.hero-title { font-size: 3rem; font-weight: 800; margin-bottom: 20px; animation: fadeInUp 1s ease; }
.hero-subtitle { font-size: 1.3rem; opacity: 0.9; animation: fadeInUp 1s ease 0.2s both; }
.hero-badge { display: inline-block; background: rgba(255,255,255,0.2); padding: 8px 20px; border-radius: 30px; margin-top: 25px; font-size: 0.9rem; animation: fadeInUp 1s ease 0.4s both; }

.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 40px 0; }
.stat-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px 20px; border-radius: 20px; text-align: center; animation: fadeInUp 0.8s ease both; transition: transform 0.3s ease; }
.stat-card:hover { transform: translateY(-10px); box-shadow: 0 20px 40px rgba(102, 126, 234, 0.4); }
.stat-card:nth-child(2) { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
.stat-card:nth-child(3) { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
.stat-card:nth-child(4) { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
.stat-number { font-size: 2.5rem; font-weight: 800; }
.stat-label { font-size: 0.85rem; opacity: 0.9; margin-top: 8px; text-transform: uppercase; letter-spacing: 1px; }
</style>

<style>
.content-section { background: white; padding: 40px; border-radius: 20px; margin: 30px 0; box-shadow: 0 10px 40px rgba(0,0,0,0.08); animation: slideInLeft 0.8s ease both; }
.section-title { font-size: 1.8rem; font-weight: 700; color: #1a1a2e; margin-bottom: 25px; padding-bottom: 15px; border-bottom: 3px solid #667eea; display: flex; align-items: center; gap: 12px; }
.section-icon { width: 40px; height: 40px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; }

.modern-table { width: 100%; border-collapse: separate; border-spacing: 0; margin: 25px 0; border-radius: 15px; overflow: hidden; box-shadow: 0 5px 20px rgba(0,0,0,0.1); }
.modern-table th { background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 18px 15px; text-align: left; font-weight: 600; font-size: 0.9rem; text-transform: uppercase; }
.modern-table td { padding: 16px 15px; border-bottom: 1px solid #eee; font-size: 0.95rem; }
.modern-table tr:hover td { background: #f8f9ff; }
.modern-table .num { text-align: right; font-family: 'SF Mono', monospace; font-weight: 600; }
.winner-badge { background: linear-gradient(135deg, #43e97b, #38f9d7); color: #1a1a2e; padding: 5px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; }

.formula-card { background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%); border-left: 5px solid #667eea; padding: 25px 30px; margin: 25px 0; border-radius: 0 15px 15px 0; }
.formula-title { color: #667eea; font-weight: 700; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 15px; }
.formula-content { font-family: 'Times New Roman', serif; font-size: 1.2rem; line-height: 2; color: #1a1a2e; }

.alert-box { padding: 25px 30px; border-radius: 15px; margin: 25px 0; display: flex; align-items: flex-start; gap: 15px; }
.alert-box.info { background: linear-gradient(135deg, #e0f7fa, #b2ebf2); border-left: 5px solid #00bcd4; }
.alert-box.warning { background: linear-gradient(135deg, #fff8e1, #ffecb3); border-left: 5px solid #ffc107; }
.alert-box.success { background: linear-gradient(135deg, #e8f5e9, #c8e6c9); border-left: 5px solid #4caf50; }
.alert-icon { font-size: 1.5rem; }
.alert-content { flex: 1; }
.alert-title { font-weight: 700; margin-bottom: 8px; }

.chart-wrapper { background: white; padding: 25px; border-radius: 15px; margin: 25px 0; box-shadow: 0 5px 20px rgba(0,0,0,0.08); }
.chart-header { margin-bottom: 20px; }
.chart-title-text { font-size: 1.1rem; font-weight: 700; color: #1a1a2e; }
.chart-subtitle-text { font-size: 0.85rem; color: #666; margin-top: 5px; }
.chart-area { height: 400px; }

.conclusion-section { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: white; padding: 50px 40px; border-radius: 25px; margin: 40px 0; }
.conclusion-section .section-title { color: white; border-bottom-color: rgba(255,255,255,0.3); }
.conclusion-text { font-size: 1.1rem; line-height: 1.9; color: rgba(255,255,255,0.85); margin-bottom: 15px; }

@media (max-width: 768px) { .hero-title { font-size: 2rem; } .stats-grid { grid-template-columns: repeat(2, 1fr); } .content-section { padding: 25px; } }
</style>


<div class="hero-section">
    <div class="hero-title">🎯 MOVE-Vasicek Model</div>
    <div class="hero-subtitle">Empirical Analysis of Interest Rate Forecasting Using Bond Market Volatility Index</div>
    <div class="hero-badge">📊 LR Statistic 17.52 | Sample 191 months | 2010-2025</div>
</div>

<div class="stats-grid">
    <div class="stat-card"><div class="stat-number">191</div><div class="stat-label">Sample Period (months)</div></div>
    <div class="stat-card"><div class="stat-number">17.52</div><div class="stat-label">LR Statistic</div></div>
    <div class="stat-card"><div class="stat-number">0.035</div><div class="stat-label">Granger p-value</div></div>
    <div class="stat-card"><div class="stat-number">2.2%</div><div class="stat-label">FEVD Contribution</div></div>
</div>

<div class="content-section">
    <div class="section-title"><div class="section-icon">📋</div>Research Overview</div>
    <p style="font-size: 1.05rem; line-height: 1.9; color: #444;">
        This study extends the Vasicek (1977) interest rate model by incorporating the bond market volatility index (MOVE) as a state indicator. 
        The analysis reveals that MOVE-related parameters provide statistically significant additional explanatory power, 
        with patterns of higher equilibrium rates and volatility observed in high-MOVE regimes.
    </p>
    <div class="alert-box info">
        <div class="alert-icon">💡</div>
        <div class="alert-content">
            <div class="alert-title">Key Finding</div>
            This study aims for descriptive characterization of interest rate dynamics conditional on market states, rather than causal claims.
        </div>
    </div>
</div>

<div class="content-section">
    <div class="section-title"><div class="section-icon">📐</div>Model Specification</div>
    
    <h3 style="color: #667eea; margin: 25px 0 15px;">Standard Vasicek Model</h3>
    <div class="formula-card">
        <div class="formula-title">Stochastic Differential Equation</div>
        <div class="formula-content">dr<sub>t</sub> = κ(θ − r<sub>t</sub>)dt + σdW<sub>t</sub></div>
    </div>
    
    <table class="modern-table">
        <tr><th>Symbol</th><th>Name</th><th>Meaning</th><th class="num">Estimate</th></tr>
        <tr><td><strong>κ</strong></td><td>Mean-reversion speed</td><td>Speed of reversion to equilibrium</td><td class="num">0.7208</td></tr>
        <tr><td><strong>θ</strong></td><td>Long-term equilibrium</td><td>Long-term rate level</td><td class="num">1.93%</td></tr>
        <tr><td><strong>σ</strong></td><td>Volatility</td><td>Diffusion coefficient</td><td class="num">0.0074</td></tr>
    </table>
    
    <h3 style="color: #667eea; margin: 35px 0 15px;">MOVE-Vasicek Extended Model</h3>
    <div class="formula-card">
        <div class="formula-title">State-Dependent SDE</div>
        <div class="formula-content">
            dr<sub>t</sub> = κ<sub>r</sub>(θ(M<sub>t</sub>) − r<sub>t</sub>)dt + σ(M<sub>t</sub>)dW<sub>t</sub><br><br>
            θ(M) = θ<sub>0</sub> + θ<sub>1</sub> · ln(M)<br>
            σ(M) = σ<sub>0</sub> + σ<sub>1</sub> · M
        </div>
    </div>
    
    <table class="modern-table">
        <tr><th>Symbol</th><th>Name</th><th class="num">Estimate</th></tr>
        <tr><td><strong>κ<sub>r</sub></strong></td><td>Mean-reversion speed</td><td class="num">0.7418</td></tr>
        <tr><td><strong>θ<sub>0</sub></strong></td><td>Base equilibrium rate</td><td class="num">1.47%</td></tr>
        <tr><td><strong>θ<sub>1</sub></strong></td><td>MOVE→θ sensitivity</td><td class="num">0.001204</td></tr>
        <tr><td><strong>σ<sub>0</sub></strong></td><td>Base volatility</td><td class="num">0.0051</td></tr>
        <tr><td><strong>σ<sub>1</sub></strong></td><td>MOVE→σ sensitivity</td><td class="num">0.000032</td></tr>
    </table>
</div>
