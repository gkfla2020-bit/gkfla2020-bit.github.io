---
layout: post
title: "바이낸스 고빈도 데이터 수집 시스템 아키텍처"
date: 2026-02-26
categories: [research, data-engineering]
tags: [binance, websocket, orderbook, high-frequency, parquet, asyncio, python]
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
        --wsj-orange: #e67e22;
        --serif: 'Georgia', 'Times New Roman', serif;
        --sans: 'Helvetica Neue', Arial, sans-serif;
        --mono: 'SF Mono', 'Fira Code', 'Consolas', monospace;
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
    .stat-value.accent { color: var(--wsj-accent); }
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
    .data-table .mono { font-family: var(--mono); font-size: 12px; }
    .formula-box { background: var(--wsj-light); border-left: 4px solid var(--wsj-accent); padding: 20px 25px; margin: 25px 0; }
    .formula-label { font-size: 11px; font-weight: 700; text-transform: uppercase; color: var(--wsj-accent); margin-bottom: 10px; }
    .formula-content { font-family: var(--mono); font-size: 14px; line-height: 2.0; }
    .formula-note { font-size: 13px; color: var(--wsj-gray); margin-top: 10px; font-style: italic; }
    .callout { border: 1px solid var(--wsj-black); padding: 20px; margin: 30px 0; }
    .callout-header { font-weight: 700; font-size: 12px; text-transform: uppercase; margin-bottom: 10px; }
    .limitation-box { background: #fff8e1; border: 1px solid #ffcc02; padding: 20px; margin: 30px 0; }
    .limitation-header { color: #f57c00; font-weight: 700; font-size: 14px; margin-bottom: 10px; }
    .code-block { background: #1e1e1e; color: #d4d4d4; padding: 20px; border-radius: 6px; font-family: var(--mono); font-size: 13px; line-height: 1.7; overflow-x: auto; margin: 20px 0; white-space: pre; }
    .code-kw { color: #569cd6; }
    .code-str { color: #ce9178; }
    .code-cm { color: #6a9955; }
    .code-fn { color: #dcdcaa; }
    .code-num { color: #b5cea8; }
    .code-cls { color: #4ec9b0; }
    .module-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 25px 0; }
    .module-card { background: white; border: 1px solid #e0e0e0; padding: 18px; border-radius: 4px; }
    .module-card.ingestion { border-top: 3px solid var(--wsj-accent); }
    .module-card.processing { border-top: 3px solid var(--wsj-green); }
    .module-card.storage { border-top: 3px solid var(--wsj-orange); }
    .module-card.monitoring { border-top: 3px solid var(--wsj-red); }
    .module-name { font-family: var(--mono); font-size: 13px; font-weight: 700; margin-bottom: 6px; }
    .module-desc { font-size: 12px; color: var(--wsj-gray); line-height: 1.5; }
    .badge { display: inline-block; font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 2px; margin-right: 4px; }
    .badge-blue { background: var(--wsj-accent); color: white; }
    .badge-green { background: var(--wsj-green); color: white; }
    .badge-orange { background: var(--wsj-orange); color: white; }
    .badge-red { background: var(--wsj-red); color: white; }
    .conclusion-box { background: var(--wsj-black); color: white; padding: 35px; margin: 50px 0; }
    .conclusion-box .section-header { color: white; border-bottom-color: #444; }
    .conclusion-box .body-text { color: #ccc; }
    .ref-list { font-size: 14px; line-height: 1.8; }
    .ref-item { margin-bottom: 8px; }
    .arch-flow { display: flex; align-items: center; justify-content: center; flex-wrap: wrap; gap: 8px; margin: 20px 0; font-family: var(--mono); font-size: 13px; }
    .arch-node { background: var(--wsj-light); border: 1px solid #ccc; padding: 8px 14px; border-radius: 4px; }
    .arch-node.highlight { background: var(--wsj-accent); color: white; border-color: var(--wsj-accent); }
    .arch-arrow { color: var(--wsj-gray); font-size: 18px; }
    @media (max-width: 768px) { .headline { font-size: 28px; } .key-stats { grid-template-columns: repeat(2, 1fr); } .module-grid { grid-template-columns: 1fr; } }
</style>

<div class="report-container">
    <div class="masthead">
        <span class="section-label">Data Engineering &amp; Crypto Research</span>
        <span class="date-line">February 26, 2026</span>
    </div>
    
    <h1 class="headline">바이낸스 고빈도 데이터 수집 시스템 아키텍처</h1>
    <p class="deck">Research-Grade Cryptocurrency Market Microstructure Data Pipeline:<br>Python asyncio 기반 24/7 오더북·체결·청산·펀딩비 수집 시스템의 설계와 구현</p>
    
    <div class="abstract">
        <div class="abstract-title">Abstract</div>
        <p class="body-text" style="margin-bottom:0;">
        본 글은 학술 논문 수준의 암호화폐 시장 미시구조(market microstructure) 데이터를 수집하기 위해 설계된 
        실시간 데이터 파이프라인의 아키텍처를 기술한다. 
        바이낸스 WebSocket API를 통해 100ms 단위 오더북 diff, 집계 체결(aggTrade), 청산(forceOrder), 
        1분봉 캔들(kline), 펀딩비(funding rate)를 24시간 무중단으로 수집하며, 
        바이낸스 공식 오더북 관리 가이드라인에 따른 lastUpdateId 시퀀스 검증을 통해 
        오더북 상태의 정확한 재구성을 보장한다. 
        이중 타임스탬프(거래소 서버 시각 + 로컬 수신 시각), SHA-256 체크섬, NTP 동기화 모니터링 등 
        학술 데이터 무결성 요건을 충족하도록 설계되었다.
        </p>
    </div>
    
    <div class="key-stats">
        <div class="stat-item"><div class="stat-label">모듈 수</div><div class="stat-value accent">11</div></div>
        <div class="stat-item"><div class="stat-label">테스트 수</div><div class="stat-value positive">107</div></div>
        <div class="stat-item"><div class="stat-label">데이터 유형</div><div class="stat-value">6종</div></div>
        <div class="stat-item"><div class="stat-label">수집 주기</div><div class="stat-value">100ms</div></div>
    </div>

    <h2 class="section-header">I. 설계 동기</h2>
    
    <p class="body-text">암호화폐 시장 미시구조 연구에서 가장 근본적인 과제는 데이터의 확보이다. 기존 학술 데이터 제공업체(Refinitiv, Bloomberg)는 전통 금융시장에 특화되어 있으며, 암호화폐 거래소의 틱 단위 오더북 데이터를 제공하지 않는다. Binance Vision(data.binance.vision)이 과거 데이터를 제공하지만, 실시간 오더북 재구성 데이터나 수신 레이턴시 정보는 포함되지 않는다.</p>

    <p class="body-text">본 시스템은 이러한 한계를 해결하기 위해 설계되었다. 핵심 설계 원칙은 세 가지이다: (1) 바이낸스 공식 오더북 관리 가이드라인의 엄격한 준수, (2) 구형 PC 환경을 고려한 최소 자원 사용(단일 프로세스, asyncio 기반), (3) SCI 논문 수준의 데이터 무결성 보장.</p>

    <div class="callout">
        <div class="callout-header">📊 수집 데이터 유형</div>
        <table class="data-table">
            <tr><th>데이터</th><th>소스</th><th>주기</th><th>용도</th></tr>
            <tr><td>오더북 Diff</td><td>Spot WebSocket</td><td>100ms</td><td>LOB 재구성, 유동성 분석</td></tr>
            <tr><td>집계 체결</td><td>Spot WebSocket</td><td>실시간</td><td>거래량, 가격 충격 분석</td></tr>
            <tr><td>청산</td><td>Futures WebSocket</td><td>실시간</td><td>레버리지 포지션 청산 추적</td></tr>
            <tr><td>1분봉 캔들</td><td>Spot WebSocket</td><td>1분</td><td>OHLCV 시계열</td></tr>
            <tr><td>펀딩비</td><td>Futures REST API</td><td>8시간</td><td>선물-현물 괴리 분석</td></tr>
            <tr><td>시간 동기화</td><td>NTP + Binance REST</td><td>10분</td><td>레이턴시 보정</td></tr>
        </table>
    </div>

    <h2 class="section-header">II. 시스템 아키텍처</h2>
    
    <div class="subsection">2.1 전체 구조</div>
    
    <p class="body-text">시스템은 Python asyncio 기반의 단일 프로세스 애플리케이션으로, 11개의 독립 모듈이 asyncio.gather를 통해 동시 실행된다. 각 모듈은 명확한 책임 경계를 가지며, 의존성 주입(dependency injection) 패턴으로 결합된다.</p>

    <div class="chart-section">
        <div class="chart-title">System Architecture — Data Flow</div>
        <div class="chart-subtitle">바이낸스 API → 수집 → 처리 → 버퍼링 → 저장 → 동기화</div>
        <div id="archChart" class="chart-container" style="height:450px;"></div>
    </div>

    <div class="module-grid">
        <div class="module-card ingestion">
            <div class="module-name"><span class="badge badge-blue">INGESTION</span></div>
            <div class="module-name">Collector</div>
            <div class="module-desc">Spot + Futures WebSocket 동시 연결. depth@100ms, aggTrade, kline_1m, forceOrder 수신. 지수 백오프 재연결.</div>
        </div>
        <div class="module-card ingestion">
            <div class="module-name"><span class="badge badge-blue">INGESTION</span></div>
            <div class="module-name">FundingRateCollector</div>
            <div class="module-desc">8시간 주기 Futures REST API 조회. 3회 재시도 + 지수 백오프.</div>
        </div>
        <div class="module-card processing">
            <div class="module-name"><span class="badge badge-green">PROCESSING</span></div>
            <div class="module-name">OrderBookManager</div>
            <div class="module-desc">REST 스냅샷 + diff 병합. lastUpdateId 시퀀스 검증. 갭 감지 시 자동 재초기화.</div>
        </div>
        <div class="module-card processing">
            <div class="module-name"><span class="badge badge-green">PROCESSING</span></div>
            <div class="module-name">DataBuffer</div>
            <div class="module-desc">심볼별 메모리 리스트. asyncio.Lock 동시성 제어. 500MB 임계값 강제 플러시.</div>
        </div>
        <div class="module-card storage">
            <div class="module-name"><span class="badge badge-orange">STORAGE</span></div>
            <div class="module-name">Flusher</div>
            <div class="module-desc">1시간 주기 Parquet 저장 (snappy 압축). 원자적 쓰기. SHA-256 체크섬 자동 기록.</div>
        </div>
        <div class="module-card storage">
            <div class="module-name"><span class="badge badge-orange">STORAGE</span></div>
            <div class="module-name">Syncer</div>
            <div class="module-desc">rclone 클라우드 업로드. 실패 대기열 재시도. 7일 경과 + 동기화 완료 파일만 삭제.</div>
        </div>
        <div class="module-card monitoring">
            <div class="module-name"><span class="badge badge-red">MONITORING</span></div>
            <div class="module-name">IntegrityLogger</div>
            <div class="module-desc">갭 추적, 플러시 통계, 재연결 이벤트, 커버리지 비율 계산.</div>
        </div>
        <div class="module-card monitoring">
            <div class="module-name"><span class="badge badge-red">MONITORING</span></div>
            <div class="module-name">TimeSyncMonitor</div>
            <div class="module-desc">10분 주기 NTP 오프셋 + 바이낸스 서버 RTT 측정. 100ms 초과 시 알림.</div>
        </div>
        <div class="module-card monitoring">
            <div class="module-name"><span class="badge badge-red">MONITORING</span></div>
            <div class="module-name">TelegramReporter</div>
            <div class="module-desc">시작/종료, 연결 끊김, 갭 감지, 일별 리포트 알림. 실패 시 수집에 영향 없음.</div>
        </div>
    </div>

    <div class="subsection">2.2 데이터 흐름</div>
    
    <div class="formula-box">
        <div class="formula-label">Pipeline Flow</div>
        <div class="formula-content">
            Binance WebSocket (depth@100ms, aggTrade, kline_1m, forceOrder)<br>
            &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
            Collector → OrderBookManager (시퀀스 검증 + diff 적용)<br>
            &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
            DataBuffer (심볼별 메모리 리스트, asyncio.Lock)<br>
            &nbsp;&nbsp;&nbsp;&nbsp;↓ &nbsp;flush_interval (3600s) 또는 강제 플러시 (500MB)<br>
            Flusher → Parquet (snappy) + SHA-256 checksums.json<br>
            &nbsp;&nbsp;&nbsp;&nbsp;↓ &nbsp;on_file_created 콜백<br>
            Syncer → rclone → Cloud Storage<br>
            &nbsp;&nbsp;&nbsp;&nbsp;↓ &nbsp;cleanup_days (7일) 경과 + 동기화 완료<br>
            로컬 파일 삭제
        </div>
    </div>

    <p class="body-text">Collector는 바이낸스 Spot WebSocket과 Futures WebSocket에 동시 연결하여 메시지를 수신한다. depth_diff 메시지는 OrderBookManager로 전달되어 lastUpdateId 시퀀스 검증 후 오더북 상태가 갱신된다. 갱신된 상위 20호가 스냅샷과 aggTrade, kline, forceOrder 데이터가 DataBuffer에 적재된다. Flusher가 1시간 주기로 Buffer에서 데이터를 가져와 Parquet 파일로 저장하고, SHA-256 체크섬을 자동 기록한다. Syncer가 새 파일을 클라우드에 업로드하고, 7일 경과 + 동기화 완료된 로컬 파일을 삭제한다.</p>

    <h2 class="section-header">III. 핵심 알고리즘</h2>
    
    <div class="subsection">3.1 오더북 재구성 (LOB Reconstruction)</div>
    
    <p class="body-text">바이낸스 오더북 재구성은 공식 가이드라인에 따라 REST 스냅샷과 WebSocket diff를 결합하는 방식으로 이루어진다. 이 과정에서 가장 중요한 것은 lastUpdateId 시퀀스의 연속성 검증이다.</p>

    <div class="formula-box">
        <div class="formula-label">시퀀스 검증 규칙</div>
        <div class="formula-content">
            스냅샷: lastUpdateId = X<br>
            새 diff: first_update_id = F, final_update_id = L<br><br>
            유효 조건: F ≤ X+1 ≤ L<br>
            → 조건 충족: diff 적용, X ← L<br>
            → 조건 불충족: 갭 감지 → 스냅샷 재요청
        </div>
        <div class="formula-note">바이낸스 공식 문서: "How to manage a local order book correctly"</div>
    </div>

    <div class="code-block"><span class="code-cm"># OrderBookManager.apply_diff — 핵심 로직</span>
<span class="code-kw">def</span> <span class="code-fn">apply_diff</span>(self, symbol, event):
    state = self.books[symbol]
    expected = state.last_update_id + <span class="code-num">1</span>
    
    <span class="code-cm"># 시퀀스 검증: F ≤ expected ≤ L</span>
    <span class="code-kw">if not</span> (event.first_update_id &lt;= expected &lt;= event.final_update_id):
        self.integrity_logger.<span class="code-fn">record_gap</span>(symbol, expected, event.first_update_id)
        state.initialized = <span class="code-kw">False</span>  <span class="code-cm"># → 자동 재초기화 트리거</span>
        <span class="code-kw">return None</span>
    
    <span class="code-cm"># diff 적용: qty=0이면 제거, 아니면 갱신</span>
    <span class="code-kw">for</span> price, qty <span class="code-kw">in</span> event.bids:
        <span class="code-kw">if</span> qty == <span class="code-str">"0"</span>: state.bids.pop(price, <span class="code-kw">None</span>)
        <span class="code-kw">else</span>: state.bids[price] = qty
    
    state.last_update_id = event.final_update_id
    <span class="code-kw">return</span> self.<span class="code-fn">get_top_levels</span>(symbol, levels=<span class="code-num">20</span>)</div>

    <p class="body-text">갭이 감지되면 해당 심볼의 initialized 플래그가 False로 설정되고, Collector의 메시지 핸들러에서 이를 감지하여 즉시 REST 스냅샷을 재요청한다. 이 자동 재초기화 메커니즘은 네트워크 불안정 상황에서도 오더북 정확성을 유지하는 핵심 장치이다.</p>

    <div class="subsection">3.2 이중 타임스탬프 (Dual Timestamp)</div>
    
    <p class="body-text">모든 수신 데이터에는 두 개의 시각 정보가 기록된다: 바이낸스 서버의 이벤트 발생 시각(event_time, 밀리초)과 로컬 머신의 수신 시각(recv_time, Unix timestamp). 이 차이값(recv_time - event_time/1000)이 네트워크 레이턴시의 근사치가 되며, 논문에서 시장 미시구조 분석 시 레이턴시 보정에 활용할 수 있다.</p>

    <div class="formula-box">
        <div class="formula-label">레이턴시 추정</div>
        <div class="formula-content">
            latency ≈ recv_time − (event_time / 1000)<br>
            NTP offset 보정: latency_corrected = latency − ntp_offset
        </div>
        <div class="formula-note">TimeSyncMonitor가 10분 주기로 NTP 오프셋과 바이낸스 서버 RTT를 측정하여 보정 데이터를 제공한다.</div>
    </div>

    <div class="subsection">3.3 재연결 및 장애 복구</div>
    
    <p class="body-text">24/7 무중단 수집에서 WebSocket 연결 끊김은 불가피하다. 시스템은 지수 백오프(exponential backoff) 전략으로 자동 재연결을 수행하며, 재연결 성공 시 모든 심볼의 오더북 스냅샷을 재초기화한다.</p>

    <div class="chart-section">
        <div class="chart-title">Exponential Backoff — Reconnection Delay</div>
        <div class="chart-subtitle">재연결 시도 횟수에 따른 대기 시간 (최대 60초)</div>
        <div id="backoffChart" class="chart-container" style="height:300px;"></div>
    </div>

    <table class="data-table">
        <tr><th>이벤트</th><th>시스템 대응</th><th>알림</th></tr>
        <tr><td>WebSocket 연결 끊김</td><td>지수 백오프 재연결 (1s → 2s → 4s → ... → 60s)</td><td>텔레그램 disconnect 알림</td></tr>
        <tr><td>재연결 성공</td><td>오더북 스냅샷 재초기화, 백오프 리셋</td><td>텔레그램 reconnect 알림 (끊김 지속시간 포함)</td></tr>
        <tr><td>오더북 시퀀스 갭</td><td>해당 심볼 REST 스냅샷 재요청</td><td>IntegrityLogger 갭 기록</td></tr>
        <tr><td>메모리 500MB 초과</td><td>즉시 강제 플러시</td><td>로그 경고</td></tr>
        <tr><td>Parquet 저장 실패</td><td>원자적 쓰기(tmpfile → rename)로 데이터 손상 방지</td><td>에러 로그</td></tr>
        <tr><td>클라우드 동기화 실패</td><td>실패 대기열에 추가, 다음 주기 재시도</td><td>IntegrityLogger sync 기록</td></tr>
    </table>

    <h2 class="section-header">IV. 저장 구조</h2>
    
    <div class="subsection">4.1 Parquet 스키마</div>
    
    <p class="body-text">모든 데이터는 Apache Parquet 형식으로 저장된다. Parquet는 열 지향(columnar) 포맷으로, 대량의 시계열 데이터에 대해 높은 압축률과 빠른 분석 쿼리 성능을 제공한다. snappy 압축을 적용하여 저장 공간을 절약하면서도 읽기 속도를 유지한다.</p>

    <table class="data-table">
        <tr><th>파일명 패턴</th><th>내용</th><th>주요 컬럼</th></tr>
        <tr><td class="mono">BTCUSDT_orderbook_20260226_1100.parquet</td><td>오더북 스냅샷</td><td>event_time, recv_time, last_update_id, bids, asks</td></tr>
        <tr><td class="mono">BTCUSDT_trade_20260226_1100.parquet</td><td>집계 체결</td><td>trade_time, price, quantity, is_buyer_maker</td></tr>
        <tr><td class="mono">BTCUSDT_liquidation_20260226_1100.parquet</td><td>청산</td><td>side, price, quantity, trade_time</td></tr>
        <tr><td class="mono">BTCUSDT_kline_20260226_1100.parquet</td><td>1분봉 캔들</td><td>open_time, OHLCV, trade_count</td></tr>
        <tr><td class="mono">funding_rate_20260226_1100.parquet</td><td>펀딩비</td><td>symbol, funding_rate, funding_time</td></tr>
    </table>

    <div class="subsection">4.2 무결성 보장</div>
    
    <p class="body-text">학술 데이터의 신뢰성을 보장하기 위해 세 가지 무결성 메커니즘을 적용한다.</p>

    <div class="formula-box">
        <div class="formula-label">무결성 3중 보장</div>
        <div class="formula-content">
            1. 원자적 쓰기: tmpfile → os.replace() (중간 상태 파일 방지)<br>
            2. SHA-256 체크섬: 모든 Parquet 파일의 해시를 checksums.json에 기록<br>
            3. 커버리지 비율: (전체 시간 − 갭 시간) / 전체 시간 → 0.0~1.0
        </div>
        <div class="formula-note">checksums.json은 파일명, SHA-256, 레코드 수, 파일 크기, 생성 시각을 포함한다.</div>
    </div>

    <h2 class="section-header">V. 실측 데이터</h2>
    
    <p class="body-text">시스템의 실제 동작을 검증하기 위해 3분간 수집 테스트를 수행하였다. 대상 심볼은 BTCUSDT, ETHUSDT, XRPUSDT이며, 바이낸스 Spot WebSocket에 연결하여 depth@100ms, aggTrade, kline_1m 스트림을 수신하였다.</p>

    <div class="chart-section">
        <div class="chart-title">3-Minute Collection Test — Records by Symbol</div>
        <div class="chart-subtitle">2026-02-26 10:59~11:02 UTC, Binance Spot WebSocket</div>
        <div id="collectChart" class="chart-container" style="height:350px;"></div>
    </div>

    <table class="data-table">
        <tr><th>심볼</th><th class="num">오더북</th><th class="num">체결</th><th class="num">캔들</th><th class="num">합계</th></tr>
        <tr><td>BTCUSDT</td><td class="num">1,796</td><td class="num">2,922</td><td class="num">3</td><td class="num">4,721</td></tr>
        <tr><td>ETHUSDT</td><td class="num">1,785</td><td class="num">1,348</td><td class="num">3</td><td class="num">3,136</td></tr>
        <tr><td>XRPUSDT</td><td class="num">1,396</td><td class="num">365</td><td class="num">3</td><td class="num">1,764</td></tr>
        <tr style="font-weight:700; border-top:2px solid #111;"><td>합계</td><td class="num">4,977</td><td class="num">4,635</td><td class="num">9</td><td class="num">9,621</td></tr>
    </table>

    <p class="body-text">3분간 총 9,621건의 레코드가 수집되었다. BTC의 체결 건수(2,922건)가 가장 많으며, 이는 BTC의 높은 거래 활성도를 반영한다. 오더북 스냅샷은 100ms 주기로 수신되므로 3분간 이론적 최대치는 1,800건이며, 실측값(1,796건)은 99.8%의 수신율을 보인다. 캔들은 확정된 1분봉만 기록하므로 3분간 심볼당 3건이 정확히 수집되었다.</p>

    <div class="chart-section">
        <div class="chart-title">BTC/USDT Orderbook Spread — Last 3 Snapshots</div>
        <div class="chart-subtitle">최우선 매수/매도 호가 및 스프레드</div>
        <div id="spreadChart" class="chart-container" style="height:300px;"></div>
    </div>

    <div class="callout">
        <div class="callout-header">📋 BTC/USDT 오더북 스냅샷 예시</div>
        <table class="data-table">
            <tr><th>update_id</th><th class="num">최우선 매수</th><th class="num">최우선 매도</th><th class="num">스프레드</th></tr>
            <tr><td class="mono">88801360882</td><td class="num">68,347.87</td><td class="num">68,347.88</td><td class="num">$0.01</td></tr>
            <tr><td class="mono">88801360895</td><td class="num">68,347.87</td><td class="num">68,347.88</td><td class="num">$0.01</td></tr>
            <tr><td class="mono">88801360897</td><td class="num">68,347.87</td><td class="num">68,347.88</td><td class="num">$0.01</td></tr>
        </table>
        <p style="font-size:13px; color:var(--wsj-gray); margin-top:10px;">BTC/USDT 스프레드 $0.01 — 바이낸스 최소 틱 사이즈와 일치하며, 오더북 재구성의 정확성을 확인할 수 있다.</p>
    </div>

    <h2 class="section-header">VI. 테스트 전략</h2>
    
    <p class="body-text">시스템의 정확성은 107개의 자동화된 테스트로 검증된다. 테스트는 크게 두 가지 방법론으로 구성된다: 속성 기반 테스트(Property-Based Testing, PBT)와 단위 테스트(Unit Testing).</p>

    <div class="subsection">6.1 속성 기반 테스트 (Hypothesis)</div>
    
    <p class="body-text">PBT는 임의의 입력을 대량 생성하여 시스템의 보편적 속성(invariant)이 항상 성립하는지 검증한다. 특정 예시가 아닌 "모든 유효한 입력에 대해 참이어야 하는 조건"을 테스트하므로, 개발자가 예상하지 못한 엣지 케이스를 발견할 수 있다.</p>

    <div class="chart-section">
        <div class="chart-title">Test Coverage — 16 Correctness Properties</div>
        <div class="chart-subtitle">각 속성은 최소 100~200회 반복 실행</div>
        <div id="testChart" class="chart-container" style="height:400px;"></div>
    </div>

    <table class="data-table">
        <tr><th>#</th><th>속성</th><th>검증 대상</th><th>테스트 파일</th></tr>
        <tr><td>P1</td><td>이중 타임스탬프 기록</td><td>모든 레코드에 event_time + recv_time 존재</td><td class="mono">test_collector.py</td></tr>
        <tr><td>P2</td><td>지수 백오프 범위</td><td>1초 ≤ delay ≤ 60초</td><td class="mono">test_collector.py</td></tr>
        <tr><td>P3</td><td>시퀀스 연속성 검증</td><td>F ≤ X+1 ≤ L 규칙 준수</td><td class="mono">test_orderbook.py</td></tr>
        <tr><td>P4</td><td>diff 적용 정확성</td><td>qty=0 제거, 비0 갱신, 미포함 불변</td><td class="mono">test_orderbook.py</td></tr>
        <tr><td>P5</td><td>상위 N호가 정렬</td><td>bids 내림차순, asks 오름차순</td><td class="mono">test_orderbook.py</td></tr>
        <tr><td>P6</td><td>버퍼 데이터 격리</td><td>심볼/타입 간 교차 오염 없음</td><td class="mono">test_buffer.py</td></tr>
        <tr><td>P7</td><td>플러시 후 버퍼 비움</td><td>flush 후 빈 버퍼 + 전체 데이터 반환</td><td class="mono">test_buffer.py</td></tr>
        <tr><td>P8</td><td>파일명 형식 준수</td><td>정규식 패턴 매칭</td><td class="mono">test_flusher.py</td></tr>
        <tr><td>P9</td><td>파일 삭제 조건</td><td>7일 경과 + 동기화 완료만 삭제</td><td class="mono">test_syncer.py</td></tr>
        <tr><td>P10</td><td>통계 JSON 라운드트립</td><td>직렬화 → 역직렬화 동일성</td><td class="mono">test_integrity.py</td></tr>
        <tr><td>P11</td><td>갭 정보 완전성</td><td>timestamp, symbol, expected_id, actual_id 필수</td><td class="mono">test_integrity.py</td></tr>
        <tr><td>P12</td><td>설정 YAML 라운드트립</td><td>Config → YAML → Config 동일성</td><td class="mono">test_config.py</td></tr>
        <tr><td>P13</td><td>텔레그램 전송 실패 격리</td><td>예외 발생해도 호출자에 전파 안 됨</td><td class="mono">test_telegram.py</td></tr>
        <tr><td>P14</td><td>체크섬 일관성</td><td>SHA-256 재계산 = 기록값</td><td class="mono">test_checksum.py</td></tr>
        <tr><td>P15</td><td>민감정보 마스킹</td><td>telegram_bot_token → "***"</td><td class="mono">test_environment.py</td></tr>
        <tr><td>P16</td><td>커버리지 비율 범위</td><td>0.0 ≤ coverage ≤ 1.0</td><td class="mono">test_coverage.py</td></tr>
    </table>

    <h2 class="section-header">VII. 용량 추정</h2>
    
    <p class="body-text">24/7 운영 시 저장 용량을 추정하기 위해 3분 실측 데이터를 기반으로 외삽(extrapolation)하였다. snappy 압축 적용 시 Parquet 파일의 압축률은 원본 대비 약 3~5배이다.</p>

    <div class="chart-section">
        <div class="chart-title">Storage Estimation — Daily / Monthly / Quarterly</div>
        <div class="chart-subtitle">3심볼 기준, snappy 압축 Parquet</div>
        <div id="storageChart" class="chart-container" style="height:320px;"></div>
    </div>

    <table class="data-table">
        <tr><th>기간</th><th class="num">오더북</th><th class="num">체결</th><th class="num">기타</th><th class="num">합계 (추정)</th></tr>
        <tr><td>1일</td><td class="num">~800MB</td><td class="num">~400MB</td><td class="num">~50MB</td><td class="num">~1.2GB</td></tr>
        <tr><td>1개월</td><td class="num">~24GB</td><td class="num">~12GB</td><td class="num">~1.5GB</td><td class="num">~37GB</td></tr>
        <tr><td>3개월</td><td class="num">~72GB</td><td class="num">~36GB</td><td class="num">~4.5GB</td><td class="num">~112GB</td></tr>
    </table>

    <div class="limitation-box">
        <div class="limitation-header">⚠️ 용량 관리 전략</div>
        <p>rclone을 통해 Google Drive, S3 등 클라우드에 자동 동기화하고, 로컬에는 7일치만 유지한다. 
        3개월 수집 시 약 112GB가 필요하므로, 클라우드 스토리지 용량을 사전에 확보해야 한다. 
        오더북 깊이(현재 상위 20호가)를 줄이면 용량을 크게 절감할 수 있다.</p>
    </div>

    <h2 class="section-header">VIII. 운영 설정</h2>
    
    <div class="code-block"><span class="code-cm"># config.yaml — 시스템 설정</span>
<span class="code-kw">symbols</span>:
  - btcusdt
  - ethusdt
  - xrpusdt

<span class="code-kw">flush_interval</span>: <span class="code-num">3600</span>        <span class="code-cm"># 1시간 (초)</span>
<span class="code-kw">data_dir</span>: <span class="code-str">"./data"</span>
<span class="code-kw">log_dir</span>: <span class="code-str">"./logs"</span>
<span class="code-kw">max_buffer_mb</span>: <span class="code-num">500</span>

<span class="code-kw">orderbook_depth</span>: <span class="code-num">1000</span>       <span class="code-cm"># REST 스냅샷 깊이</span>
<span class="code-kw">orderbook_top_levels</span>: <span class="code-num">20</span>    <span class="code-cm"># 저장할 호가 수</span>

<span class="code-kw">cloud_remote</span>: <span class="code-str">"gdrive"</span>      <span class="code-cm"># rclone 리모트 이름</span>
<span class="code-kw">cloud_path</span>: <span class="code-str">"crypto_data"</span>  <span class="code-cm"># 클라우드 저장 경로</span>
<span class="code-kw">cleanup_days</span>: <span class="code-num">7</span>             <span class="code-cm"># 로컬 파일 보관 일수</span>

<span class="code-kw">use_futures</span>: <span class="code-kw">true</span>           <span class="code-cm"># 선물 API (청산/펀딩비)</span>

<span class="code-kw">telegram_bot_token</span>: <span class="code-str">""</span>     <span class="code-cm"># @BotFather에서 발급</span>
<span class="code-kw">telegram_chat_id</span>: <span class="code-str">""</span>       <span class="code-cm"># 채팅 ID</span></div>

    <div class="conclusion-box">
        <h2 class="section-header">IX. 결론</h2>
        <p class="body-text">본 시스템은 학술 연구 목적의 암호화폐 시장 미시구조 데이터 수집을 위해 설계되었다. Python asyncio 기반의 단일 프로세스 아키텍처로 구형 PC에서도 24/7 무중단 운영이 가능하며, 바이낸스 공식 오더북 관리 가이드라인을 엄격히 준수하여 데이터의 정확성을 보장한다.</p>

        <p class="body-text">이중 타임스탬프, SHA-256 체크섬, NTP 동기화 모니터링, 환경 메타데이터 기록 등 SCI 논문 수준의 데이터 무결성 요건을 충족하도록 설계되었으며, 16개의 정확성 속성(correctness property)과 107개의 자동화된 테스트로 시스템의 신뢰성을 검증하였다.</p>

        <p class="body-text">rclone 기반 클라우드 동기화와 7일 로컬 보관 정책을 통해 장기 수집(3개월+)에도 로컬 디스크 부담 없이 운영할 수 있다. 텔레그램 알림을 통해 원격에서도 시스템 상태를 실시간으로 모니터링할 수 있다.</p>
    </div>
    
    <h2 class="section-header">X. 기술 스택</h2>
    
    <table class="data-table">
        <tr><th>구분</th><th>기술</th><th>용도</th></tr>
        <tr><td>언어</td><td>Python 3.14</td><td>asyncio 기반 비동기 프로그래밍</td></tr>
        <tr><td>WebSocket</td><td>websockets</td><td>바이낸스 실시간 스트림 수신</td></tr>
        <tr><td>HTTP</td><td>aiohttp</td><td>REST API 호출, 텔레그램 봇</td></tr>
        <tr><td>저장</td><td>Apache Parquet (pyarrow)</td><td>열 지향 압축 저장</td></tr>
        <tr><td>데이터</td><td>pandas</td><td>DataFrame 변환 및 Parquet 쓰기</td></tr>
        <tr><td>동기화</td><td>rclone</td><td>클라우드 스토리지 업로드</td></tr>
        <tr><td>시간</td><td>ntplib</td><td>NTP 서버 오프셋 측정</td></tr>
        <tr><td>설정</td><td>PyYAML</td><td>config.yaml 파싱</td></tr>
        <tr><td>테스트</td><td>pytest + hypothesis</td><td>단위 테스트 + 속성 기반 테스트</td></tr>
    </table>

    <h2 class="section-header">XI. 참고문헌</h2>
    
    <div class="ref-list">
        <div class="ref-item">Binance. (2024). How to manage a local order book correctly. Binance API Documentation.</div>
        <div class="ref-item">Gould, M. D., Porter, M. A., Williams, S., McDonald, M., Fenn, D. J., & Howison, S. D. (2013). Limit order books. Quantitative Finance, 13(11), 1709-1748.</div>
        <div class="ref-item">Cont, R., Stoikov, S., & Talreja, R. (2010). A stochastic model for order book dynamics. Operations Research, 58(3), 549-563.</div>
        <div class="ref-item">Cartea, Á., Jaimungal, S., & Penalva, J. (2015). Algorithmic and High-Frequency Trading. Cambridge University Press.</div>
        <div class="ref-item">Apache Software Foundation. (2024). Apache Parquet Format Specification.</div>
    </div>
</div>

<script>
const colors = { primary: '#0080c6', accent: '#c41200', green: '#00843d', orange: '#e67e22', gray: '#666' };
const baseLayout = { font: {family: 'Helvetica Neue'}, paper_bgcolor: 'white', plot_bgcolor: 'white', margin: {t:30,r:30,b:50,l:60} };

// ── Architecture Sankey Diagram ──
Plotly.newPlot('archChart', [{
    type: 'sankey',
    orientation: 'h',
    node: {
        pad: 20, thickness: 20,
        label: [
            'Spot WebSocket',       // 0
            'Futures WebSocket',    // 1
            'Futures REST',         // 2
            'Collector',            // 3
            'FundingRateCollector', // 4
            'OrderBookManager',    // 5
            'DataBuffer',          // 6
            'Flusher',             // 7
            'Parquet Files',       // 8
            'Syncer',              // 9
            'Cloud Storage',       // 10
            'IntegrityLogger',     // 11
            'TelegramReporter',    // 12
            'TimeSyncMonitor',     // 13
        ],
        color: [
            '#0080c6','#0080c6','#0080c6',
            '#2196F3','#2196F3',
            '#00843d','#00843d',
            '#e67e22','#e67e22',
            '#e67e22','#e67e22',
            '#c41200','#c41200','#c41200'
        ]
    },
    link: {
        source: [0,0,0,1,2, 3,3,3,3, 4, 5, 6, 7,7, 8, 3,5,7,9, 11,3,13],
        target: [3,3,3,3,4, 5,6,6,6, 6, 6, 7, 8,11, 9, 12,11,11,11, 12,11,12],
        value:  [3,2,1,1,1, 3,2,1,1, 1, 3, 5, 5,2,  4, 1,2,1,1,   1,1,1],
        color: [
            'rgba(0,128,198,0.15)','rgba(0,128,198,0.15)','rgba(0,128,198,0.15)',
            'rgba(0,128,198,0.15)','rgba(0,128,198,0.15)',
            'rgba(0,132,61,0.15)','rgba(0,132,61,0.15)','rgba(0,132,61,0.15)','rgba(0,132,61,0.15)',
            'rgba(0,132,61,0.15)','rgba(0,132,61,0.15)',
            'rgba(230,126,34,0.15)',
            'rgba(230,126,34,0.15)','rgba(196,18,0,0.15)',
            'rgba(230,126,34,0.15)',
            'rgba(196,18,0,0.15)','rgba(196,18,0,0.15)','rgba(196,18,0,0.15)','rgba(196,18,0,0.15)',
            'rgba(196,18,0,0.15)','rgba(196,18,0,0.15)','rgba(196,18,0,0.15)'
        ]
    }
}], {
    ...baseLayout,
    margin: {t:20,r:20,b:20,l:20},
}, {responsive: true});

// ── Backoff Chart ──
const attempts = Array.from({length:10}, (_,i) => i);
const delays = attempts.map(n => Math.min(Math.pow(2, n), 60));
Plotly.newPlot('backoffChart', [{
    x: attempts, y: delays,
    type: 'scatter', mode: 'lines+markers',
    line: {color: colors.primary, width: 3},
    marker: {size: 8, color: colors.primary},
    name: 'delay = min(2^N, 60)',
    fill: 'tozeroy', fillcolor: 'rgba(0,128,198,0.1)'
}, {
    x: [0,9], y: [60,60],
    type: 'scatter', mode: 'lines',
    line: {color: colors.accent, width: 2, dash: 'dash'},
    name: '최대 60초'
}], {
    ...baseLayout,
    xaxis: {title: '재연결 시도 횟수', dtick: 1},
    yaxis: {title: '대기 시간 (초)', range: [0, 70]},
    legend: {orientation: 'h', y: 1.12},
    showlegend: true
}, {responsive: true});

// ── Collection Test Chart ──
Plotly.newPlot('collectChart', [{
    x: ['BTCUSDT', 'ETHUSDT', 'XRPUSDT'],
    y: [1796, 1785, 1396],
    name: '오더북', type: 'bar',
    marker: {color: colors.primary}
}, {
    x: ['BTCUSDT', 'ETHUSDT', 'XRPUSDT'],
    y: [2922, 1348, 365],
    name: '체결', type: 'bar',
    marker: {color: colors.green}
}, {
    x: ['BTCUSDT', 'ETHUSDT', 'XRPUSDT'],
    y: [3, 3, 3],
    name: '캔들', type: 'bar',
    marker: {color: colors.orange}
}], {
    ...baseLayout,
    barmode: 'group',
    yaxis: {title: '레코드 수'},
    legend: {orientation: 'h', y: 1.12},
    annotations: [
        {x:'BTCUSDT', y:3100, text:'<b>4,721건</b>', showarrow:false, font:{size:11,color:'#111'}},
        {x:'ETHUSDT', y:2000, text:'<b>3,136건</b>', showarrow:false, font:{size:11,color:'#111'}},
        {x:'XRPUSDT', y:1600, text:'<b>1,764건</b>', showarrow:false, font:{size:11,color:'#111'}}
    ]
}, {responsive: true});

// ── Spread Chart ──
Plotly.newPlot('spreadChart', [{
    x: ['88801360882', '88801360895', '88801360897'],
    y: [68347.87, 68347.87, 68347.87],
    name: '최우선 매수 (Bid)', type: 'scatter', mode: 'lines+markers',
    line: {color: colors.green, width: 3},
    marker: {size: 10}
}, {
    x: ['88801360882', '88801360895', '88801360897'],
    y: [68347.88, 68347.88, 68347.88],
    name: '최우선 매도 (Ask)', type: 'scatter', mode: 'lines+markers',
    line: {color: colors.accent, width: 3},
    marker: {size: 10}
}], {
    ...baseLayout,
    xaxis: {title: 'update_id', type: 'category'},
    yaxis: {title: 'Price (USDT)', range: [68347.85, 68347.90], tickformat: ',.2f'},
    legend: {orientation: 'h', y: 1.12},
    annotations: [{
        x: '88801360895', y: 68347.875,
        text: 'Spread = $0.01', showarrow: true,
        arrowhead: 2, ax: 60, ay: 0,
        font: {size: 11, color: colors.primary}
    }]
}, {responsive: true});

// ── Test Properties Chart ──
const props = ['P1','P2','P3','P4','P5','P6','P7','P8','P9','P10','P11','P12','P13','P14','P15','P16'];
const propNames = [
    '이중 타임스탬프','지수 백오프','시퀀스 검증','diff 정확성',
    'N호가 정렬','버퍼 격리','플러시 비움','파일명 형식',
    '삭제 조건','JSON 라운드트립','갭 완전성','YAML 라운드트립',
    '텔레그램 격리','체크섬 일관성','민감정보 마스킹','커버리지 범위'
];
const propColors = props.map((p,i) => {
    if(i < 2) return colors.primary;
    if(i < 5) return colors.green;
    if(i < 7) return '#9c27b0';
    if(i < 9) return colors.orange;
    if(i < 12) return colors.accent;
    return '#607d8b';
});
Plotly.newPlot('testChart', [{
    type: 'bar', orientation: 'h',
    y: propNames.slice().reverse(),
    x: [200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200].reverse(),
    marker: {color: propColors.slice().reverse()},
    text: props.slice().reverse(),
    textposition: 'inside',
    hovertemplate: '%{y}: %{x}회 반복<extra></extra>'
}], {
    ...baseLayout,
    margin: {t:20,r:30,b:50,l:160},
    xaxis: {title: 'Hypothesis 반복 횟수'},
    yaxis: {automargin: true},
    showlegend: false,
    annotations: [{
        x: 210, y: '이중 타임스탬프',
        text: '✅ ALL PASS', showarrow: false,
        font: {size: 12, color: colors.green}
    }]
}, {responsive: true});

// ── Storage Estimation Chart ──
Plotly.newPlot('storageChart', [{
    x: ['1일', '1주', '1개월', '3개월'],
    y: [0.8, 5.6, 24, 72],
    name: '오더북', type: 'bar',
    marker: {color: colors.primary}
}, {
    x: ['1일', '1주', '1개월', '3개월'],
    y: [0.4, 2.8, 12, 36],
    name: '체결', type: 'bar',
    marker: {color: colors.green}
}, {
    x: ['1일', '1주', '1개월', '3개월'],
    y: [0.05, 0.35, 1.5, 4.5],
    name: '기타 (캔들/청산/펀딩비)', type: 'bar',
    marker: {color: colors.orange}
}], {
    ...baseLayout,
    barmode: 'stack',
    yaxis: {title: '용량 (GB)'},
    legend: {orientation: 'h', y: 1.12},
    annotations: [
        {x:'1일', y:1.4, text:'<b>~1.2GB</b>', showarrow:false, font:{size:10}},
        {x:'1개월', y:40, text:'<b>~37GB</b>', showarrow:false, font:{size:10}},
        {x:'3개월', y:118, text:'<b>~112GB</b>', showarrow:false, font:{size:10}}
    ]
}, {responsive: true});
</script>