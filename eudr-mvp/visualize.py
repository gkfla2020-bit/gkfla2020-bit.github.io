"""
EUDR 판정 결과 시각화
실제 MODIS 데이터 기반 대시보드 생성 → HTML로 로컬 오픈
"""
import sys
sys.path.insert(0, '.')

import json
import webbrowser
import os
from real_assessment import *


def run_and_visualize():
    print("데이터 수집 중... (약 30초)")

    results = []
    for plot in SUPPLY_CHAIN["plots"]:
        result = assess_plot(plot)
        results.append(result)

    # HTML 대시보드 생성
    html = generate_dashboard(results)
    output_path = os.path.abspath("eudr_dashboard.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n  대시보드 생성 완료: {output_path}")
    webbrowser.open(f"file://{output_path}")


def generate_dashboard(results: list) -> str:
    total = len(results)
    compliant = sum(1 for r in results if r.compliant)
    total_area = sum(r.area_ha for r in results)
    deforested_area = sum(r.area_ha for r in results if r.deforestation)

    # 플롯 데이터 JSON
    plot_data = json.dumps([
        {
            "id": r.plot_id,
            "name": r.name,
            "lat": r.lat,
            "lon": r.lon,
            "area_ha": r.area_ha,
            "supplier": r.supplier,
            "baseline_ndvi": round(r.baseline_ndvi, 4),
            "current_ndvi": round(r.current_ndvi, 4),
            "ndvi_change": round(r.ndvi_change, 4),
            "baseline_cover": round(r.baseline_cover * 100, 1),
            "current_cover": round(r.current_cover * 100, 1),
            "cover_change": round(r.cover_change * 100, 1),
            "height_m": round(r.canopy_height_m, 1),
            "was_forest": r.was_forest,
            "is_forest": r.is_forest,
            "deforestation": r.deforestation,
            "compliant": r.compliant,
            "risk": r.risk,
            "reason": r.reason,
        }
        for r in results
    ], ensure_ascii=False)

    risk_counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
    for r in results:
        risk_counts[r.risk] += 1

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EUDR Deforestation-Free Compliance Dashboard</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #0f1419;
    color: #e7e9ea;
    min-height: 100vh;
    padding: 24px;
}}
.header {{
    text-align: center;
    margin-bottom: 32px;
    padding: 32px;
    background: linear-gradient(135deg, #1a2332 0%, #0d4b3c 100%);
    border-radius: 16px;
    border: 1px solid #2d3d2d;
}}
.header h1 {{
    font-size: 28px;
    color: #4ade80;
    margin-bottom: 8px;
}}
.header p {{
    color: #9ca3af;
    font-size: 14px;
}}
.header .company {{
    font-size: 18px;
    color: #e7e9ea;
    margin-top: 12px;
}}
.summary-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-bottom: 32px;
}}
.summary-card {{
    background: #1a2332;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    border: 1px solid #2a3a4a;
}}
.summary-card .value {{
    font-size: 36px;
    font-weight: 700;
    margin: 8px 0;
}}
.summary-card .label {{
    font-size: 12px;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 1px;
}}
.green {{ color: #4ade80; }}
.yellow {{ color: #fbbf24; }}
.red {{ color: #f87171; }}
.blue {{ color: #60a5fa; }}

.charts-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    margin-bottom: 32px;
}}
@media (max-width: 900px) {{
    .charts-grid {{ grid-template-columns: 1fr; }}
}}
.chart-card {{
    background: #1a2332;
    border-radius: 12px;
    padding: 24px;
    border: 1px solid #2a3a4a;
}}
.chart-card h3 {{
    font-size: 16px;
    margin-bottom: 16px;
    color: #e7e9ea;
}}

.ndvi-bar-chart {{
    display: flex;
    flex-direction: column;
    gap: 12px;
}}
.ndvi-row {{
    display: flex;
    align-items: center;
    gap: 12px;
}}
.ndvi-row .label {{
    width: 80px;
    font-size: 12px;
    color: #9ca3af;
    flex-shrink: 0;
}}
.ndvi-row .bars {{
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 4px;
}}
.bar-container {{
    display: flex;
    align-items: center;
    gap: 8px;
}}
.bar {{
    height: 20px;
    border-radius: 4px;
    transition: width 0.5s ease;
    position: relative;
}}
.bar.baseline {{ background: #3b82f6; }}
.bar.current {{ background: #4ade80; }}
.bar-value {{
    font-size: 11px;
    color: #9ca3af;
    min-width: 50px;
}}

.risk-chart {{
    display: flex;
    align-items: flex-end;
    gap: 16px;
    height: 160px;
    padding: 16px 0;
    justify-content: center;
}}
.risk-bar-wrapper {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
}}
.risk-bar {{
    width: 48px;
    border-radius: 6px 6px 0 0;
    transition: height 0.5s ease;
}}
.risk-bar.low {{ background: #4ade80; }}
.risk-bar.medium {{ background: #fbbf24; }}
.risk-bar.high {{ background: #f97316; }}
.risk-bar.critical {{ background: #f87171; }}
.risk-label {{
    font-size: 11px;
    color: #9ca3af;
}}
.risk-count {{
    font-size: 14px;
    font-weight: 600;
}}

.map-section {{
    background: #1a2332;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 32px;
    border: 1px solid #2a3a4a;
}}
.map-section h3 {{
    margin-bottom: 16px;
}}
.map-container {{
    width: 100%;
    height: 400px;
    background: #0f1923;
    border-radius: 8px;
    position: relative;
    overflow: hidden;
}}
.map-dot {{
    position: absolute;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    border: 2px solid white;
    transform: translate(-50%, -50%);
    cursor: pointer;
    transition: transform 0.2s;
}}
.map-dot:hover {{
    transform: translate(-50%, -50%) scale(1.5);
}}
.map-dot.compliant {{ background: #4ade80; }}
.map-dot.non-compliant {{ background: #f87171; }}
.map-dot.medium-risk {{ background: #fbbf24; }}
.map-tooltip {{
    position: absolute;
    background: #1a2332;
    border: 1px solid #4ade80;
    border-radius: 8px;
    padding: 12px;
    font-size: 12px;
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.2s;
    z-index: 10;
    min-width: 200px;
}}

.plot-table {{
    background: #1a2332;
    border-radius: 12px;
    padding: 24px;
    border: 1px solid #2a3a4a;
    overflow-x: auto;
}}
.plot-table h3 {{
    margin-bottom: 16px;
}}
table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}}
th {{
    text-align: left;
    padding: 12px 8px;
    border-bottom: 2px solid #2a3a4a;
    color: #9ca3af;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}
td {{
    padding: 12px 8px;
    border-bottom: 1px solid #1f2937;
}}
tr:hover td {{
    background: #1f2937;
}}
.status-badge {{
    display: inline-block;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
}}
.status-badge.pass {{ background: #064e3b; color: #4ade80; }}
.status-badge.fail {{ background: #7f1d1d; color: #f87171; }}
.status-badge.warn {{ background: #78350f; color: #fbbf24; }}

.change-indicator {{
    display: inline-flex;
    align-items: center;
    gap: 4px;
}}
.change-indicator.positive {{ color: #4ade80; }}
.change-indicator.negative {{ color: #f87171; }}
.change-indicator.neutral {{ color: #9ca3af; }}

.footer {{
    text-align: center;
    padding: 24px;
    color: #6b7280;
    font-size: 12px;
}}
.legend {{
    display: flex;
    gap: 16px;
    margin-bottom: 12px;
    font-size: 12px;
}}
.legend-item {{
    display: flex;
    align-items: center;
    gap: 6px;
}}
.legend-dot {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
}}
</style>
</head>
<body>

<div class="header">
    <h1>EUDR Deforestation-Free Compliance</h1>
    <p>EU Regulation 2023/1115 | FAO Forest Definition | Cutoff: 2020-12-31</p>
    <div class="company">
        <strong>{SUPPLY_CHAIN['company']}</strong> → {SUPPLY_CHAIN['eu_importer']}
    </div>
    <p style="margin-top:8px;">Commodity: {SUPPLY_CHAIN['commodity']} | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
</div>

<div class="summary-grid">
    <div class="summary-card">
        <div class="label">Total Plots</div>
        <div class="value blue">{total}</div>
        <div class="label">{total_area:.0f} hectares</div>
    </div>
    <div class="summary-card">
        <div class="label">Compliant</div>
        <div class="value green">{compliant}</div>
        <div class="label">deforestation-free</div>
    </div>
    <div class="summary-card">
        <div class="label">Non-Compliant</div>
        <div class="value red">{total - compliant}</div>
        <div class="label">{deforested_area:.0f} ha affected</div>
    </div>
    <div class="summary-card">
        <div class="label">Compliance Rate</div>
        <div class="value {'green' if compliant == total else 'yellow'}">{compliant/total*100:.0f}%</div>
        <div class="label">pass rate</div>
    </div>
</div>

<div class="charts-grid">
    <div class="chart-card">
        <h3>NDVI Comparison (2020 Baseline vs 2025 Current)</h3>
        <div class="legend">
            <div class="legend-item"><div class="legend-dot" style="background:#3b82f6"></div>2020 Baseline</div>
            <div class="legend-item"><div class="legend-dot" style="background:#4ade80"></div>2025 Current</div>
        </div>
        <div class="ndvi-bar-chart" id="ndvi-chart"></div>
    </div>
    <div class="chart-card">
        <h3>Risk Distribution</h3>
        <div class="risk-chart">
            <div class="risk-bar-wrapper">
                <div class="risk-count">{risk_counts['LOW']}</div>
                <div class="risk-bar low" style="height:{risk_counts['LOW']/total*140}px"></div>
                <div class="risk-label">LOW</div>
            </div>
            <div class="risk-bar-wrapper">
                <div class="risk-count">{risk_counts['MEDIUM']}</div>
                <div class="risk-bar medium" style="height:{max(risk_counts['MEDIUM']/total*140, 4)}px"></div>
                <div class="risk-label">MEDIUM</div>
            </div>
            <div class="risk-bar-wrapper">
                <div class="risk-count">{risk_counts['HIGH']}</div>
                <div class="risk-bar high" style="height:{max(risk_counts['HIGH']/total*140, 4)}px"></div>
                <div class="risk-label">HIGH</div>
            </div>
            <div class="risk-bar-wrapper">
                <div class="risk-count">{risk_counts['CRITICAL']}</div>
                <div class="risk-bar critical" style="height:{max(risk_counts['CRITICAL']/total*140, 4)}px"></div>
                <div class="risk-label">CRITICAL</div>
            </div>
        </div>
    </div>
</div>

<div class="charts-grid">
    <div class="chart-card">
        <h3>Canopy Cover Change (%)</h3>
        <div id="cover-chart" style="height:200px;display:flex;align-items:flex-end;gap:12px;padding-top:20px;justify-content:center;"></div>
    </div>
    <div class="chart-card">
        <h3>Canopy Height (meters)</h3>
        <div id="height-chart" style="height:200px;display:flex;align-items:flex-end;gap:12px;padding-top:20px;justify-content:center;"></div>
    </div>
</div>

<div class="map-section">
    <h3>Supply Chain Map - Indonesia</h3>
    <div class="map-container" id="map">
        <div class="map-tooltip" id="tooltip"></div>
    </div>
</div>

<div class="plot-table">
    <h3>Detailed Plot Assessment</h3>
    <table>
        <thead>
            <tr>
                <th>Status</th>
                <th>Plot ID</th>
                <th>Location</th>
                <th>Supplier</th>
                <th>Area (ha)</th>
                <th>NDVI 2020</th>
                <th>NDVI 2025</th>
                <th>Change</th>
                <th>Cover %</th>
                <th>Height (m)</th>
                <th>Risk</th>
                <th>Verdict</th>
            </tr>
        </thead>
        <tbody id="table-body"></tbody>
    </table>
</div>

<div class="footer">
    <p>Data Sources: MODIS MOD13Q1 (ORNL DAAC) | Copernicus Sentinel-2 (OData) | NASA GEDI L2A | NDVI-Height Regression (Potapov et al. 2021)</p>
    <p style="margin-top:8px;">Standard: FAO Forest Definition (Crown Cover ≥10%, Height ≥5m, Area ≥0.5ha) | EUDR Cutoff: 2020-12-31</p>
</div>

<script>
const plots = {plot_data};

// NDVI Bar Chart
const ndviChart = document.getElementById('ndvi-chart');
plots.forEach(p => {{
    const maxNdvi = Math.max(...plots.map(x => Math.max(x.baseline_ndvi, x.current_ndvi)), 1);
    const bw = (p.baseline_ndvi / maxNdvi) * 100;
    const cw = (p.current_ndvi / maxNdvi) * 100;
    ndviChart.innerHTML += `
        <div class="ndvi-row">
            <div class="label">${{p.id}}</div>
            <div class="bars">
                <div class="bar-container">
                    <div class="bar baseline" style="width:${{bw}}%"></div>
                    <div class="bar-value">${{p.baseline_ndvi.toFixed(3)}}</div>
                </div>
                <div class="bar-container">
                    <div class="bar current" style="width:${{cw}}%"></div>
                    <div class="bar-value">${{p.current_ndvi.toFixed(3)}}</div>
                </div>
            </div>
        </div>`;
}});

// Cover Change Chart
const coverChart = document.getElementById('cover-chart');
plots.forEach(p => {{
    const change = p.cover_change;
    const height = Math.abs(change) * 2;
    const color = change >= 0 ? '#4ade80' : '#f87171';
    const direction = change >= 0 ? 'up' : 'down';
    coverChart.innerHTML += `
        <div style="display:flex;flex-direction:column;align-items:center;gap:4px;">
            <div style="font-size:11px;color:${{color}}">${{change >= 0 ? '+' : ''}}${{change.toFixed(1)}}%</div>
            <div style="width:36px;height:${{Math.max(height, 8)}}px;background:${{color}};border-radius:4px;"></div>
            <div style="font-size:10px;color:#9ca3af">${{p.id}}</div>
        </div>`;
}});

// Height Chart
const heightChart = document.getElementById('height-chart');
const maxHeight = Math.max(...plots.map(p => p.height_m));
plots.forEach(p => {{
    const h = (p.height_m / maxHeight) * 160;
    const color = p.height_m >= 5 ? '#4ade80' : '#f87171';
    heightChart.innerHTML += `
        <div style="display:flex;flex-direction:column;align-items:center;gap:4px;">
            <div style="font-size:11px;color:#e7e9ea">${{p.height_m.toFixed(0)}}m</div>
            <div style="width:36px;height:${{h}}px;background:${{color}};border-radius:4px 4px 0 0;"></div>
            <div style="font-size:10px;color:#9ca3af">${{p.id}}</div>
        </div>`;
}});

// Map
const map = document.getElementById('map');
const tooltip = document.getElementById('tooltip');
const lats = plots.map(p => p.lat);
const lons = plots.map(p => p.lon);
const minLat = Math.min(...lats) - 1;
const maxLat = Math.max(...lats) + 1;
const minLon = Math.min(...lons) - 1;
const maxLon = Math.max(...lons) + 1;

plots.forEach(p => {{
    const x = ((p.lon - minLon) / (maxLon - minLon)) * 90 + 5;
    const y = ((maxLat - p.lat) / (maxLat - minLat)) * 85 + 5;
    let cls = 'compliant';
    if (!p.compliant) cls = 'non-compliant';
    else if (p.risk === 'MEDIUM') cls = 'medium-risk';

    const dot = document.createElement('div');
    dot.className = `map-dot ${{cls}}`;
    dot.style.left = x + '%';
    dot.style.top = y + '%';
    dot.addEventListener('mouseenter', (e) => {{
        tooltip.style.opacity = 1;
        tooltip.style.left = (x + 2) + '%';
        tooltip.style.top = (y + 3) + '%';
        tooltip.innerHTML = `
            <strong>${{p.name}}</strong><br>
            ${{p.id}} | ${{p.area_ha}}ha<br>
            NDVI: ${{p.baseline_ndvi.toFixed(3)}} → ${{p.current_ndvi.toFixed(3)}}<br>
            Cover: ${{p.baseline_cover.toFixed(1)}}% → ${{p.current_cover.toFixed(1)}}%<br>
            Height: ${{p.height_m}}m<br>
            <strong style="color:${{p.compliant ? '#4ade80' : '#f87171'}}">${{p.compliant ? '✅ Compliant' : '❌ Non-Compliant'}}</strong>
        `;
    }});
    dot.addEventListener('mouseleave', () => {{ tooltip.style.opacity = 0; }});
    map.appendChild(dot);

    // Label
    const label = document.createElement('div');
    label.style.cssText = `position:absolute;left:${{x+2}}%;top:${{y+1}}%;font-size:10px;color:#9ca3af;`;
    label.textContent = p.id;
    map.appendChild(label);
}});

// Table
const tbody = document.getElementById('table-body');
plots.forEach(p => {{
    const statusClass = p.compliant ? (p.risk === 'MEDIUM' ? 'warn' : 'pass') : 'fail';
    const statusText = p.compliant ? '✅' : '❌';
    const changeClass = p.ndvi_change >= 0 ? 'positive' : (p.ndvi_change < -0.05 ? 'negative' : 'neutral');
    const changeArrow = p.ndvi_change >= 0 ? '↑' : '↓';

    tbody.innerHTML += `
        <tr>
            <td>${{statusText}}</td>
            <td><strong>${{p.id}}</strong></td>
            <td>${{p.name}}</td>
            <td>${{p.supplier}}</td>
            <td>${{p.area_ha}}</td>
            <td>${{p.baseline_ndvi.toFixed(4)}}</td>
            <td>${{p.current_ndvi.toFixed(4)}}</td>
            <td><span class="change-indicator ${{changeClass}}">${{changeArrow}} ${{(p.ndvi_change >= 0 ? '+' : '') + p.ndvi_change.toFixed(4)}}</span></td>
            <td>${{p.current_cover.toFixed(1)}}%</td>
            <td>${{p.height_m}}</td>
            <td><span class="status-badge ${{statusClass}}">${{p.risk}}</span></td>
            <td style="max-width:200px;font-size:11px;">${{p.reason}}</td>
        </tr>`;
}});
</script>
</body>
</html>"""


if __name__ == "__main__":
    run_and_visualize()
