---
layout: post
title: "바이낸스 데이터 수집기 코드 딥다이브 — 모듈별 구현 해설"
date: 2026-02-27
permalink: /research/binance-collector-code-deepdive-kr/
categories: [research, data-engineering]
tags: [binance, websocket, orderbook, asyncio, python, parquet, code-review]
toc: true
toc_sticky: true
---

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
    .headline { font-family: var(--serif); font-size: 34px; font-weight: 700; line-height: 1.15; margin-bottom: 20px; text-align: center; }
    .deck { font-family: var(--serif); font-size: 18px; color: var(--wsj-gray); text-align: center; font-style: italic; margin-bottom: 40px; }
    .abstract { background: var(--wsj-light); padding: 25px; margin: 30px 0; border-left: 4px solid var(--wsj-accent); }
    .abstract-title { font-size: 12px; font-weight: 700; text-transform: uppercase; color: var(--wsj-accent); margin-bottom: 10px; }
    .section-header { font-family: var(--serif); font-size: 26px; font-weight: 700; margin: 50px 0 20px; padding-bottom: 10px; border-bottom: 2px solid var(--wsj-black); }
    .subsection { font-family: var(--serif); font-size: 18px; font-weight: 700; margin: 30px 0 15px; color: var(--wsj-gray); }
    .body-text { font-family: var(--serif); font-size: 17px; line-height: 1.9; margin-bottom: 18px; text-align: justify; }
    .code-block { background: #1e1e1e; color: #d4d4d4; padding: 20px; border-radius: 6px; font-family: var(--mono); font-size: 13px; line-height: 1.7; overflow-x: auto; margin: 20px 0; white-space: pre; }
    .code-kw { color: #569cd6; }
    .code-str { color: #ce9178; }
    .code-cm { color: #6a9955; }
    .code-fn { color: #dcdcaa; }
    .code-num { color: #b5cea8; }
    .code-cls { color: #4ec9b0; }
    .code-dec { color: #c586c0; }
    .formula-box { background: var(--wsj-light); border-left: 4px solid var(--wsj-accent); padding: 20px 25px; margin: 25px 0; }
    .formula-label { font-size: 11px; font-weight: 700; text-transform: uppercase; color: var(--wsj-accent); margin-bottom: 10px; }
    .formula-content { font-family: var(--mono); font-size: 14px; line-height: 2.0; }
    .formula-note { font-size: 13px; color: var(--wsj-gray); margin-top: 10px; font-style: italic; }
    .callout { border: 1px solid var(--wsj-black); padding: 20px; margin: 30px 0; }
    .callout-header { font-weight: 700; font-size: 12px; text-transform: uppercase; margin-bottom: 10px; }
    .data-table { width: 100%; border-collapse: collapse; font-size: 14px; margin: 20px 0; }
    .data-table th { font-weight: 700; text-transform: uppercase; font-size: 11px; padding: 12px; text-align: left; border-bottom: 2px solid var(--wsj-black); background: var(--wsj-light); }
    .data-table td { padding: 12px; border-bottom: 1px solid #e0e0e0; }
    .data-table .mono { font-family: var(--mono); font-size: 12px; }
    .key-stats { display: grid; grid-template-columns: repeat(4, 1fr); border: 1px solid var(--wsj-black); margin: 40px 0; }
    .stat-item { padding: 20px; text-align: center; border-right: 1px solid #ddd; }
    .stat-item:last-child { border-right: none; }
    .stat-label { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: var(--wsj-gray); }
    .stat-value { font-family: var(--serif); font-size: 28px; font-weight: 700; }
    .stat-value.accent { color: var(--wsj-accent); }
    .stat-value.positive { color: var(--wsj-green); }
    .badge { display: inline-block; font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 2px; margin-right: 4px; }
    .badge-blue { background: var(--wsj-accent); color: white; }
    .badge-green { background: var(--wsj-green); color: white; }
    .badge-orange { background: var(--wsj-orange); color: white; }
    .badge-red { background: var(--wsj-red); color: white; }
    .limitation-box { background: #fff8e1; border: 1px solid #ffcc02; padding: 20px; margin: 30px 0; }
    .limitation-header { color: #f57c00; font-weight: 700; font-size: 14px; margin-bottom: 10px; }
    .conclusion-box { background: var(--wsj-black); color: white; padding: 35px; margin: 50px 0; }
    .conclusion-box .section-header { color: white; border-bottom-color: #444; }
    .conclusion-box .body-text { color: #ccc; }
    @media (max-width: 768px) { .headline { font-size: 26px; } .key-stats { grid-template-columns: repeat(2, 1fr); } }
</style>

<div class="report-container">
    <div class="masthead">
        <span class="section-label">Code Deep Dive &amp; Engineering</span>
        <span class="date-line">February 27, 2026</span>
    </div>

    <h1 class="headline">바이낸스 데이터 수집기 코드 딥다이브</h1>
    <p class="deck">11개 모듈의 구현 원리를 코드 레벨에서 해부한다:<br>WebSocket 수신부터 Parquet 저장, 클라우드 동기화까지</p>

    <div class="abstract">
        <div class="abstract-title">이 글에서 다루는 것</div>
        <p class="body-text" style="margin-bottom:0;">
        <a href="/research/binance-hft-data-collector-kr/">이전 글</a>에서 시스템의 아키텍처와 설계 원리를 다루었다면,
        이 글에서는 실제 코드를 한 줄씩 뜯어보며 "왜 이렇게 짰는가"를 설명한다.
        main.py의 모듈 초기화 구조, WebSocket 메시지 라우팅, 오더북 diff 적용 알고리즘,
        asyncio.Lock 기반 버퍼링, 원자적 Parquet 저장, rclone 클라우드 동기화까지 —
        각 모듈의 핵심 코드와 설계 결정의 이유를 상세히 기술한다.
        </p>
    </div>

    <div class="key-stats">
        <div class="stat-item"><div class="stat-label">소스 파일</div><div class="stat-value accent">12</div></div>
        <div class="stat-item"><div class="stat-label">총 코드 라인</div><div class="stat-value">~1,200</div></div>
        <div class="stat-item"><div class="stat-label">테스트 파일</div><div class="stat-value positive">16</div></div>
        <div class="stat-item"><div class="stat-label">외부 의존성</div><div class="stat-value">5</div></div>
    </div>

    <h2 class="section-header">I. main.py — 엔트리포인트와 모듈 조립</h2>

    <p class="body-text">시스템의 시작점인 main.py를 보면 12개의 import가 나열되어 있다. 처음 보면 압도적이지만, 각 import는 시스템의 한 가지 책임을 담당하는 독립 모듈이다. 이 구조를 이해하면 전체 시스템이 보인다.</p>

    <div class="code-block"><span class="code-cm"># main.py — 모듈 임포트</span>
<span class="code-kw">from</span> src.config <span class="code-kw">import</span> <span class="code-cls">Config</span>                <span class="code-cm"># ① 설정 로드</span>
<span class="code-kw">from</span> src.models <span class="code-kw">import</span> *                       <span class="code-cm"># ② 데이터 모델 (dataclass)</span>
<span class="code-kw">from</span> src.orderbook_manager <span class="code-kw">import</span> <span class="code-cls">OrderBookManager</span>  <span class="code-cm"># ③ 오더북 재구성</span>
<span class="code-kw">from</span> src.buffer <span class="code-kw">import</span> <span class="code-cls">DataBuffer</span>              <span class="code-cm"># ④ 메모리 버퍼</span>
<span class="code-kw">from</span> src.flusher <span class="code-kw">import</span> <span class="code-cls">Flusher</span>               <span class="code-cm"># ⑤ Parquet 저장</span>
<span class="code-kw">from</span> src.collector <span class="code-kw">import</span> <span class="code-cls">Collector</span>            <span class="code-cm"># ⑥ WebSocket 수신</span>
<span class="code-kw">from</span> src.integrity_logger <span class="code-kw">import</span> <span class="code-cls">IntegrityLogger</span>  <span class="code-cm"># ⑦ 무결성 로깅</span>
<span class="code-kw">from</span> src.syncer <span class="code-kw">import</span> <span class="code-cls">Syncer</span>                 <span class="code-cm"># ⑧ 클라우드 동기화</span>
<span class="code-kw">from</span> src.telegram_reporter <span class="code-kw">import</span> <span class="code-cls">TelegramReporter</span> <span class="code-cm"># ⑨ 텔레그램 알림</span>
<span class="code-kw">from</span> src.funding_rate_collector <span class="code-kw">import</span> <span class="code-cls">FundingRateCollector</span> <span class="code-cm"># ⑩ 펀딩비 수집</span>
<span class="code-kw">from</span> src.time_sync_monitor <span class="code-kw">import</span> <span class="code-cls">TimeSyncMonitor</span>  <span class="code-cm"># ⑪ 시간 동기화</span>
<span class="code-kw">from</span> src.environment_recorder <span class="code-kw">import</span> <span class="code-cls">EnvironmentRecorder</span> <span class="code-cm"># ⑫ 환경 기록</span></div>

    <p class="body-text">이 12개 모듈은 크게 4개 레이어로 분류된다:</p>

    <table class="data-table">
        <tr><th>레이어</th><th>모듈</th><th>역할</th></tr>
        <tr><td><span class="badge badge-blue">수집</span></td><td class="mono">Collector, FundingRateCollector</td><td>바이낸스 API에서 데이터를 가져오는 입구</td></tr>
        <tr><td><span class="badge badge-green">처리</span></td><td class="mono">OrderBookManager, DataBuffer</td><td>수신 데이터를 검증하고 메모리에 적재</td></tr>
        <tr><td><span class="badge badge-orange">저장</span></td><td class="mono">Flusher, Syncer</td><td>디스크 저장 + 클라우드 업로드</td></tr>
        <tr><td><span class="badge badge-red">모니터링</span></td><td class="mono">IntegrityLogger, TimeSyncMonitor, TelegramReporter, EnvironmentRecorder</td><td>무결성 추적, 시간 동기화, 알림</td></tr>
    </table>

    <div class="subsection">1.1 의존성 주입 패턴</div>

    <p class="body-text">main.py에서 가장 중요한 부분은 모듈 간 연결 방식이다. 각 모듈은 생성자에서 필요한 의존성을 주입받는다. 이렇게 하면 테스트 시 mock 객체를 쉽게 주입할 수 있고, 모듈 간 결합도가 낮아진다.</p>

    <div class="code-block"><span class="code-cm"># main.py — 모듈 초기화 (의존성 주입)</span>
config = <span class="code-cls">Config</span>.<span class="code-fn">from_yaml</span>(<span class="code-str">"config.yaml"</span>)

<span class="code-cm"># 1단계: 독립 모듈 생성</span>
integrity_logger = <span class="code-cls">IntegrityLogger</span>(config.log_dir)
telegram = <span class="code-cls">TelegramReporter</span>(config)
buffer = <span class="code-cls">DataBuffer</span>(config.max_buffer_mb)

<span class="code-cm"># 2단계: 의존성 있는 모듈 생성</span>
ob_manager = <span class="code-cls">OrderBookManager</span>(config.symbols, integrity_logger)
syncer = <span class="code-cls">Syncer</span>(config, integrity_logger)

<span class="code-cm"># 3단계: 콜백 연결 — Flusher가 파일 생성하면 Syncer에 통보</span>
flusher = <span class="code-cls">Flusher</span>(config, buffer, integrity_logger,
                  on_file_created=syncer.enqueue_file)  <span class="code-cm"># ← 콜백!</span>

<span class="code-cm"># 4단계: 최상위 모듈 — 모든 의존성 주입</span>
collector = <span class="code-cls">Collector</span>(config, ob_manager, buffer, integrity_logger, telegram)</div>

    <p class="body-text">핵심은 <code>on_file_created=syncer.enqueue_file</code> 부분이다. Flusher가 Parquet 파일을 저장할 때마다 이 콜백이 호출되어 Syncer의 대기열에 파일 경로가 추가된다. 이렇게 하면 Flusher는 Syncer의 존재를 몰라도 되고, 콜백 하나로 느슨하게 연결된다.</p>

    <div class="subsection">1.2 asyncio.gather — 동시 실행</div>

    <p class="body-text">모든 모듈이 초기화되면, asyncio.gather로 동시에 실행한다. 각 모듈의 run() 메서드는 무한 루프로 동작하는 코루틴이다.</p>

    <div class="code-block"><span class="code-cm"># main.py — 7개 태스크 동시 실행</span>
tasks = [
    collector.<span class="code-fn">run</span>(),           <span class="code-cm"># WebSocket 수신 (무한 루프)</span>
    flusher.<span class="code-fn">run</span>(),             <span class="code-cm"># 1시간마다 Parquet 저장</span>
    syncer.<span class="code-fn">run</span>(),              <span class="code-cm"># 대기열 파일 클라우드 업로드</span>
    time_sync.<span class="code-fn">run</span>(),           <span class="code-cm"># 10분마다 NTP 측정</span>
    <span class="code-fn">periodic_log</span>(),            <span class="code-cm"># 1시간마다 통계 JSON 저장</span>
    <span class="code-fn">daily_summary</span>(),           <span class="code-cm"># 24시간마다 일별 요약</span>
    <span class="code-fn">force_flush_monitor</span>(),     <span class="code-cm"># 30초마다 메모리 체크</span>
]

<span class="code-kw">if</span> config.use_futures:
    tasks.append(funding_collector.<span class="code-fn">run</span>())  <span class="code-cm"># 8시간마다 펀딩비 조회</span>

<span class="code-kw">await</span> asyncio.<span class="code-fn">gather</span>(*tasks)</div>

    <p class="body-text">asyncio.gather는 여러 코루틴을 하나의 이벤트 루프에서 동시에 실행한다. 멀티스레딩이 아니라 협력적 멀티태스킹(cooperative multitasking)이다. 각 코루틴이 await를 만나면 제어권을 양보하고, 다른 코루틴이 실행된다. WebSocket 메시지를 기다리는 동안 Flusher의 sleep이 끝나면 플러시가 실행되는 식이다.</p>

    <div class="formula-box">
        <div class="formula-label">왜 asyncio인가?</div>
        <div class="formula-content">
            멀티프로세싱: 프로세스 간 데이터 공유 복잡 (IPC 필요)<br>
            멀티스레딩: GIL 제약 + 락 관리 복잡<br>
            asyncio: 단일 스레드, 단일 프로세스 → 공유 메모리 직접 접근<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ Buffer에 Lock 하나면 충분
        </div>
        <div class="formula-note">I/O 바운드 작업(WebSocket 수신, HTTP 요청, 파일 쓰기)에는 asyncio가 가장 효율적이다. CPU 바운드 작업이 없으므로 GIL도 문제되지 않는다.</div>
    </div>

    <h2 class="section-header">II. models.py — 데이터 모델</h2>

    <p class="body-text">시스템이 다루는 모든 데이터의 형태를 dataclass로 정의한다. 바이낸스 WebSocket이 보내는 JSON을 파이썬 객체로 변환할 때의 "계약서" 역할을 한다.</p>

    <div class="code-block"><span class="code-kw">from</span> dataclasses <span class="code-kw">import</span> dataclass, field

<span class="code-dec">@dataclass</span>
<span class="code-kw">class</span> <span class="code-cls">DepthDiffEvent</span>:
    <span class="code-str">"""바이낸스 depth_diff WebSocket 이벤트"""</span>
    symbol: <span class="code-cls">str</span>
    event_time: <span class="code-cls">int</span>              <span class="code-cm"># 거래소 이벤트 시각 (ms)</span>
    recv_time: <span class="code-cls">float</span>             <span class="code-cm"># 로컬 수신 시각 (unix timestamp)</span>
    first_update_id: <span class="code-cls">int</span>         <span class="code-cm"># U — diff 시작 ID</span>
    final_update_id: <span class="code-cls">int</span>         <span class="code-cm"># u — diff 끝 ID</span>
    bids: <span class="code-cls">list</span>[<span class="code-cls">list</span>[<span class="code-cls">str</span>]]        <span class="code-cm"># [[price, qty], ...]</span>
    asks: <span class="code-cls">list</span>[<span class="code-cls">list</span>[<span class="code-cls">str</span>]]        <span class="code-cm"># [[price, qty], ...]</span>

<span class="code-dec">@dataclass</span>
<span class="code-kw">class</span> <span class="code-cls">OrderBookState</span>:
    <span class="code-str">"""심볼별 오더북 내부 상태 — dict로 O(1) 가격 조회"""</span>
    bids: <span class="code-cls">dict</span>[<span class="code-cls">str</span>, <span class="code-cls">str</span>] = field(default_factory=<span class="code-cls">dict</span>)  <span class="code-cm"># {price: qty}</span>
    asks: <span class="code-cls">dict</span>[<span class="code-cls">str</span>, <span class="code-cls">str</span>] = field(default_factory=<span class="code-cls">dict</span>)
    last_update_id: <span class="code-cls">int</span> = <span class="code-num">0</span>
    initialized: <span class="code-cls">bool</span> = <span class="code-kw">False</span>
    init_time: <span class="code-cls">float</span> = <span class="code-num">0.0</span>       <span class="code-cm"># 초기화 시각 (grace period용)</span>

<span class="code-dec">@dataclass</span>
<span class="code-kw">class</span> <span class="code-cls">AggTradeEvent</span>:
    <span class="code-str">"""집계 체결 이벤트"""</span>
    symbol: <span class="code-cls">str</span>
    trade_id: <span class="code-cls">int</span>
    price: <span class="code-cls">str</span>                  <span class="code-cm"># 문자열 유지 → 부동소수점 오차 방지</span>
    quantity: <span class="code-cls">str</span>
    trade_time: <span class="code-cls">int</span>              <span class="code-cm"># T (ms)</span>
    recv_time: <span class="code-cls">float</span>
    is_buyer_maker: <span class="code-cls">bool</span>         <span class="code-cm"># True = 매도 체결 (maker가 buyer)</span></div>

    <div class="callout">
        <div class="callout-header">💡 왜 가격을 str로 저장하는가?</div>
        <p class="body-text" style="margin-bottom:0;">바이낸스 API는 가격과 수량을 문자열로 전송한다 (예: <code>"68347.87"</code>). 이를 float로 변환하면 부동소수점 오차가 발생한다 (<code>0.1 + 0.2 = 0.30000000000000004</code>). 금융 데이터에서 이런 오차는 치명적이므로, 원본 문자열을 그대로 보존하고 분석 시점에 Decimal로 변환하는 것이 정석이다.</p>
    </div>

    <p class="body-text">OrderBookState에서 bids/asks를 <code>dict[str, str]</code>로 저장하는 이유도 중요하다. 리스트로 저장하면 특정 가격의 수량을 갱신할 때 O(n) 탐색이 필요하지만, dict는 O(1)이다. 100ms마다 수십 개의 가격 업데이트가 들어오므로 이 차이는 크다.</p>

    <h2 class="section-header">III. collector.py — WebSocket 수신과 메시지 라우팅</h2>

    <p class="body-text">Collector는 시스템의 "귀"다. 바이낸스 WebSocket에 연결하여 초당 수백 건의 메시지를 수신하고, 메시지 유형에 따라 적절한 처리 모듈로 라우팅한다.</p>

    <div class="subsection">3.1 Combined Stream URL 생성</div>

    <p class="body-text">바이낸스는 하나의 WebSocket 연결로 여러 스트림을 동시에 수신할 수 있는 combined stream을 제공한다. 심볼 6개 × 스트림 3종 = 18개 스트림을 하나의 연결로 처리한다.</p>

    <div class="code-block"><span class="code-kw">class</span> <span class="code-cls">Collector</span>:
    SPOT_WS = <span class="code-str">"wss://stream.binance.com:9443/stream"</span>
    FUTURES_WS = <span class="code-str">"wss://fstream.binance.com/stream"</span>

    <span class="code-kw">def</span> <span class="code-fn">build_ws_url</span>(self) -> <span class="code-cls">str</span>:
        streams = []
        <span class="code-kw">for</span> s <span class="code-kw">in</span> self.config.symbols:
            streams.append(f<span class="code-str">"{s}@depth@100ms"</span>)    <span class="code-cm"># 오더북 diff (100ms)</span>
            streams.append(f<span class="code-str">"{s}@aggTrade"</span>)       <span class="code-cm"># 집계 체결</span>
            streams.append(f<span class="code-str">"{s}@kline_1m"</span>)       <span class="code-cm"># 1분봉 캔들</span>
        <span class="code-kw">return</span> f<span class="code-str">"{self.SPOT_WS}?streams={'<span class="code-fn">/</span>'.join(streams)}"</span>
        <span class="code-cm"># 결과: wss://stream.binance.com:9443/stream?streams=</span>
        <span class="code-cm">#   btcusdt@depth@100ms/btcusdt@aggTrade/btcusdt@kline_1m/...</span></div>

    <div class="subsection">3.2 메시지 라우팅 — _handle_message</div>

    <p class="body-text">수신된 JSON 메시지의 stream 필드를 보고 어떤 데이터인지 판별한다. 이 라우팅 로직이 시스템의 핵심 분기점이다.</p>

    <div class="code-block"><span class="code-kw">async def</span> <span class="code-fn">_handle_message</span>(self, raw_msg: <span class="code-cls">str</span>) -> <span class="code-kw">None</span>:
    recv_time = time.<span class="code-fn">time</span>()  <span class="code-cm"># ← 수신 즉시 로컬 시각 기록!</span>
    data = json.<span class="code-fn">loads</span>(raw_msg)
    stream = data.get(<span class="code-str">"stream"</span>, <span class="code-str">""</span>)   <span class="code-cm"># 예: "btcusdt@depth@100ms"</span>
    payload = data.get(<span class="code-str">"data"</span>, {})

    <span class="code-kw">if</span> <span class="code-str">"depth"</span> <span class="code-kw">in</span> stream:
        <span class="code-cm"># 오더북 diff → OrderBookManager로 전달</span>
        event = <span class="code-cls">DepthDiffEvent</span>(
            symbol=stream.split(<span class="code-str">"@"</span>)[<span class="code-num">0</span>].upper(),
            event_time=payload.get(<span class="code-str">"E"</span>, <span class="code-num">0</span>),
            recv_time=recv_time,
            first_update_id=payload.get(<span class="code-str">"U"</span>, <span class="code-num">0</span>),
            final_update_id=payload.get(<span class="code-str">"u"</span>, <span class="code-num">0</span>),
            bids=payload.get(<span class="code-str">"b"</span>, []),
            asks=payload.get(<span class="code-str">"a"</span>, []),
        )
        snapshot = self.ob_manager.<span class="code-fn">apply_diff</span>(event.symbol, event)
        <span class="code-kw">if</span> snapshot:
            <span class="code-kw">await</span> self.buffer.<span class="code-fn">add_orderbook</span>(event.symbol, <span class="code-fn">asdict</span>(snapshot))

    <span class="code-kw">elif</span> <span class="code-str">"aggTrade"</span> <span class="code-kw">in</span> stream:
        <span class="code-cm"># 체결 → 바로 버퍼에 적재</span>
        event = <span class="code-cls">AggTradeEvent</span>(...)
        <span class="code-kw">await</span> self.buffer.<span class="code-fn">add_trade</span>(event.symbol, <span class="code-fn">asdict</span>(event))

    <span class="code-kw">elif</span> <span class="code-str">"forceOrder"</span> <span class="code-kw">in</span> stream:
        <span class="code-cm"># 청산 (선물) → 버퍼에 적재</span>
        event = <span class="code-cls">LiquidationEvent</span>(...)
        <span class="code-kw">await</span> self.buffer.<span class="code-fn">add_liquidation</span>(event.symbol, <span class="code-fn">asdict</span>(event))

    <span class="code-kw">elif</span> <span class="code-str">"kline"</span> <span class="code-kw">in</span> stream:
        k = payload.get(<span class="code-str">"k"</span>, {})
        <span class="code-kw">if</span> k.get(<span class="code-str">"x"</span>, <span class="code-kw">False</span>):  <span class="code-cm"># x=True → 확정된 캔들만 저장</span>
            event = <span class="code-cls">KlineEvent</span>(...)
            <span class="code-kw">await</span> self.buffer.<span class="code-fn">add_kline</span>(event.symbol, <span class="code-fn">asdict</span>(event))</div>

    <div class="callout">
        <div class="callout-header">💡 recv_time을 왜 맨 처음에 기록하는가?</div>
        <p class="body-text" style="margin-bottom:0;"><code>recv_time = time.time()</code>을 JSON 파싱 전에 호출한다. 파싱, 객체 생성, 오더북 diff 적용 등의 처리 시간이 수신 시각에 포함되면 레이턴시 측정이 부정확해지기 때문이다. 학술 데이터에서 마이크로초 단위의 정확성이 중요할 때 이 차이가 의미를 가진다.</p>
    </div>

    <div class="subsection">3.3 지수 백오프 재연결</div>

    <p class="body-text">WebSocket 연결이 끊기면 즉시 재연결을 시도하되, 반복 실패 시 대기 시간을 지수적으로 늘린다. 이는 서버에 과부하를 주지 않으면서도 빠른 복구를 보장하는 표준 패턴이다.</p>

    <div class="code-block"><span class="code-kw">async def</span> <span class="code-fn">_run_spot</span>(self) -> <span class="code-kw">None</span>:
    <span class="code-kw">while</span> <span class="code-kw">True</span>:  <span class="code-cm"># ← 영원히 재시도</span>
        <span class="code-kw">try</span>:
            <span class="code-kw">await</span> self.<span class="code-fn">_connect_and_collect</span>()
        <span class="code-kw">except</span> <span class="code-cls">Exception</span> <span class="code-kw">as</span> e:
            self._disconnect_time = self._disconnect_time <span class="code-kw">or</span> time.<span class="code-fn">time</span>()
            <span class="code-kw">await</span> asyncio.<span class="code-fn">sleep</span>(self.reconnect_delay)
            self.reconnect_delay = <span class="code-fn">min</span>(self.reconnect_delay * <span class="code-num">2</span>, <span class="code-num">60.0</span>)
            <span class="code-cm"># 1초 → 2초 → 4초 → 8초 → 16초 → 32초 → 60초 (상한)</span>

<span class="code-kw">async def</span> <span class="code-fn">_connect_and_collect</span>(self) -> <span class="code-kw">None</span>:
    <span class="code-kw">async with</span> websockets.<span class="code-fn">connect</span>(url, ping_interval=<span class="code-num">20</span>) <span class="code-kw">as</span> ws:
        <span class="code-cm"># 재연결 성공 → 끊김 지속시간 계산 후 알림</span>
        <span class="code-kw">if</span> self._disconnect_time:
            downtime = time.<span class="code-fn">time</span>() - self._disconnect_time
            <span class="code-kw">await</span> self.telegram.<span class="code-fn">send_reconnect_alert</span>(downtime)
            self._disconnect_time = <span class="code-kw">None</span>

        self.reconnect_delay = <span class="code-num">1.0</span>  <span class="code-cm"># 백오프 리셋</span>

        <span class="code-cm"># 모든 심볼 오더북 스냅샷 재초기화</span>
        <span class="code-kw">for</span> sym <span class="code-kw">in</span> self.config.symbols:
            <span class="code-kw">await</span> self.ob_manager.<span class="code-fn">initialize</span>(sym, self.config.orderbook_depth)

        <span class="code-kw">async for</span> raw_msg <span class="code-kw">in</span> ws:  <span class="code-cm"># 무한 수신 루프</span>
            <span class="code-kw">await</span> self.<span class="code-fn">_handle_message</span>(raw_msg)</div>

    <p class="body-text">재연결 성공 시 두 가지 중요한 작업이 수행된다: (1) 백오프 딜레이를 1초로 리셋, (2) 모든 심볼의 오더북 스냅샷을 REST API로 다시 가져온다. 연결이 끊긴 동안 오더북 diff를 놓쳤으므로, 스냅샷부터 다시 시작해야 정확한 오더북을 유지할 수 있다.</p>

    <h2 class="section-header">IV. orderbook_manager.py — 오더북 재구성의 핵심</h2>

    <p class="body-text">이 모듈은 시스템에서 가장 까다로운 로직을 담당한다. 바이낸스 공식 가이드라인(<a href="https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams#how-to-manage-a-local-order-book-correctly" target="_blank">How to manage a local order book correctly</a>)을 코드로 구현한 것이다.</p>

    <div class="subsection">4.1 초기화 — REST 스냅샷</div>

    <div class="code-block"><span class="code-kw">async def</span> <span class="code-fn">initialize</span>(self, symbol: <span class="code-cls">str</span>, depth: <span class="code-cls">int</span> = <span class="code-num">1000</span>) -> <span class="code-kw">None</span>:
    sym = symbol.upper()
    url = f<span class="code-str">"{self.BASE_URL}/api/v3/depth?symbol={sym}&limit={depth}"</span>

    <span class="code-kw">async with</span> aiohttp.<span class="code-cls">ClientSession</span>() <span class="code-kw">as</span> session:
        <span class="code-kw">async with</span> session.<span class="code-fn">get</span>(url) <span class="code-kw">as</span> resp:
            data = <span class="code-kw">await</span> resp.<span class="code-fn">json</span>()

    state = <span class="code-cls">OrderBookState</span>(
        bids={p: q <span class="code-kw">for</span> p, q <span class="code-kw">in</span> data.get(<span class="code-str">"bids"</span>, [])},  <span class="code-cm"># list → dict 변환</span>
        asks={p: q <span class="code-kw">for</span> p, q <span class="code-kw">in</span> data.get(<span class="code-str">"asks"</span>, [])},
        last_update_id=data.get(<span class="code-str">"lastUpdateId"</span>, <span class="code-num">0</span>),
        initialized=<span class="code-kw">True</span>,
        init_time=time.<span class="code-fn">time</span>(),  <span class="code-cm"># grace period 시작 시각</span>
    )
    self.books[sym] = state</div>

    <p class="body-text">REST API에서 받은 스냅샷의 bids/asks를 리스트에서 dict로 변환한다. <code>{"68347.87": "1.234", "68347.86": "0.567", ...}</code> 형태가 되어, 이후 diff 적용 시 O(1)로 특정 가격의 수량을 갱신할 수 있다.</p>

    <div class="subsection">4.2 시퀀스 검증 — 갭 감지</div>

    <p class="body-text">오더북 재구성에서 가장 중요한 부분이다. 바이낸스의 규칙은 단순하다: 새로 도착한 diff의 first_update_id(F)와 final_update_id(L) 사이에 현재 lastUpdateId+1이 포함되어야 한다.</p>

    <div class="formula-box">
        <div class="formula-label">시퀀스 검증 규칙</div>
        <div class="formula-content">
            현재 상태: lastUpdateId = X<br>
            새 diff: first_update_id = F, final_update_id = L<br><br>
            유효 조건: F ≤ (X + 1) ≤ L<br><br>
            예시: X = 100, F = 99, L = 103 → 99 ≤ 101 ≤ 103 ✅<br>
            예시: X = 100, F = 105, L = 110 → 105 ≤ 101? ❌ → 갭!
        </div>
    </div>

    <div class="code-block"><span class="code-kw">def</span> <span class="code-fn">apply_diff</span>(self, symbol: <span class="code-cls">str</span>, event: <span class="code-cls">DepthDiffEvent</span>) -> <span class="code-cls">OrderBookSnapshot</span> | <span class="code-kw">None</span>:
    state = self.books[symbol]
    expected = state.last_update_id + <span class="code-num">1</span>

    <span class="code-cm"># 이미 처리된 오래된 diff → 무시 (갭 아님)</span>
    <span class="code-kw">if</span> event.final_update_id &lt; expected:
        <span class="code-kw">return None</span>

    <span class="code-cm"># 시퀀스 검증: F ≤ expected ≤ L</span>
    <span class="code-kw">if not</span> self.<span class="code-fn">validate_sequence</span>(symbol, event.first_update_id, event.final_update_id):
        <span class="code-cm"># 초기화 직후 3초 grace period — 스냅샷과 diff 사이 타이밍 이슈 허용</span>
        <span class="code-kw">if</span> time.<span class="code-fn">time</span>() - state.init_time &lt; <span class="code-num">3.0</span>:
            <span class="code-kw">return None</span>  <span class="code-cm"># 조용히 무시</span>

        <span class="code-cm"># 진짜 갭 → 무결성 로거에 기록 + 재초기화 트리거</span>
        self.integrity_logger.<span class="code-fn">record_gap</span>(symbol, expected, event.first_update_id)
        state.initialized = <span class="code-kw">False</span>  <span class="code-cm"># Collector가 이걸 보고 재초기화</span>
        <span class="code-kw">return None</span>

    <span class="code-cm"># diff 적용</span>
    self.<span class="code-fn">_apply_updates</span>(state.bids, event.bids)
    self.<span class="code-fn">_apply_updates</span>(state.asks, event.asks)
    state.last_update_id = event.final_update_id

    <span class="code-kw">return</span> self.<span class="code-fn">get_top_levels</span>(symbol, event_time=event.event_time, recv_time=event.recv_time)</div>

    <div class="callout">
        <div class="callout-header">💡 Grace Period가 필요한 이유</div>
        <p class="body-text" style="margin-bottom:0;">REST 스냅샷을 요청하는 동안에도 WebSocket diff는 계속 도착한다. 스냅샷의 lastUpdateId가 100인데, 스냅샷 응답이 도착하기 전에 이미 diff 101~105가 도착해서 버려진 상태일 수 있다. 이때 다음 diff가 106부터 시작하면 시퀀스 검증에 실패한다. 3초 grace period 동안은 이런 타이밍 이슈를 허용하고, 그 이후에도 검증 실패하면 진짜 갭으로 판단한다.</p>
    </div>

    <div class="subsection">4.3 diff 적용 — _apply_updates</div>

    <div class="code-block"><span class="code-dec">@staticmethod</span>
<span class="code-kw">def</span> <span class="code-fn">_apply_updates</span>(book_side: <span class="code-cls">dict</span>[<span class="code-cls">str</span>, <span class="code-cls">str</span>], updates: <span class="code-cls">list</span>) -> <span class="code-kw">None</span>:
    <span class="code-str">"""오더북 한쪽(bids 또는 asks)에 업데이트 적용"""</span>
    <span class="code-kw">for</span> price, qty <span class="code-kw">in</span> updates:
        <span class="code-kw">if</span> qty == <span class="code-str">"0"</span> <span class="code-kw">or</span> qty == <span class="code-str">"0.00000000"</span>:
            book_side.<span class="code-fn">pop</span>(price, <span class="code-kw">None</span>)  <span class="code-cm"># 수량 0 → 해당 가격 제거</span>
        <span class="code-kw">else</span>:
            book_side[price] = qty          <span class="code-cm"># 수량 갱신 (없으면 추가)</span></div>

    <p class="body-text">바이낸스의 규칙은 명확하다: 수량이 0이면 해당 가격대를 오더북에서 제거하고, 0이 아니면 갱신(또는 신규 추가)한다. dict의 pop과 대입 연산 모두 O(1)이므로, 수백 개의 업데이트도 빠르게 처리된다.</p>

    <div class="subsection">4.4 상위 N호가 추출 — get_top_levels</div>

    <div class="code-block"><span class="code-kw">def</span> <span class="code-fn">get_top_levels</span>(self, symbol, levels=<span class="code-num">20</span>, event_time=<span class="code-num">0</span>, recv_time=<span class="code-num">0.0</span>):
    state = self.books[symbol]

    <span class="code-cm"># bids: 높은 가격순 (내림차순) — 최우선 매수가가 첫 번째</span>
    sorted_bids = <span class="code-fn">sorted</span>(state.bids.items(),
                         key=<span class="code-kw">lambda</span> x: <span class="code-fn">float</span>(x[<span class="code-num">0</span>]), reverse=<span class="code-kw">True</span>)[:levels]

    <span class="code-cm"># asks: 낮은 가격순 (오름차순) — 최우선 매도가가 첫 번째</span>
    sorted_asks = <span class="code-fn">sorted</span>(state.asks.items(),
                         key=<span class="code-kw">lambda</span> x: <span class="code-fn">float</span>(x[<span class="code-num">0</span>]))[:levels]

    <span class="code-kw">return</span> <span class="code-cls">OrderBookSnapshot</span>(
        symbol=symbol, event_time=event_time, recv_time=recv_time,
        last_update_id=state.last_update_id,
        bids=[[p, q] <span class="code-kw">for</span> p, q <span class="code-kw">in</span> sorted_bids],
        asks=[[p, q] <span class="code-kw">for</span> p, q <span class="code-kw">in</span> sorted_asks],
    )</div>

    <p class="body-text">dict에 저장된 전체 오더북에서 상위 20호가만 추출하여 저장한다. 전체 1,000호가를 모두 저장하면 데이터 크기가 50배 이상 커지므로, 연구에 필요한 상위 호가만 선별한다. 필요하다면 config.yaml의 <code>orderbook_top_levels</code>를 조정할 수 있다.</p>

    <h2 class="section-header">V. buffer.py — 메모리 버퍼와 동시성 제어</h2>

    <p class="body-text">DataBuffer는 수집된 데이터가 디스크에 저장되기 전까지 머무는 "대기실"이다. 여러 코루틴이 동시에 데이터를 추가하므로, asyncio.Lock으로 동시성을 제어한다.</p>

    <div class="code-block"><span class="code-kw">class</span> <span class="code-cls">DataBuffer</span>:
    <span class="code-kw">def</span> <span class="code-fn">__init__</span>(self, max_memory_mb: <span class="code-cls">int</span> = <span class="code-num">500</span>):
        self.max_memory_bytes = max_memory_mb * <span class="code-num">1024</span> * <span class="code-num">1024</span>
        <span class="code-cm"># 심볼별 분리 저장 — defaultdict로 자동 초기화</span>
        self._orderbook_data: <span class="code-cls">dict</span>[<span class="code-cls">str</span>, <span class="code-cls">list</span>] = <span class="code-fn">defaultdict</span>(<span class="code-cls">list</span>)
        self._trade_data: <span class="code-cls">dict</span>[<span class="code-cls">str</span>, <span class="code-cls">list</span>] = <span class="code-fn">defaultdict</span>(<span class="code-cls">list</span>)
        self._liquidation_data: <span class="code-cls">dict</span>[<span class="code-cls">str</span>, <span class="code-cls">list</span>] = <span class="code-fn">defaultdict</span>(<span class="code-cls">list</span>)
        self._kline_data: <span class="code-cls">dict</span>[<span class="code-cls">str</span>, <span class="code-cls">list</span>] = <span class="code-fn">defaultdict</span>(<span class="code-cls">list</span>)
        self._funding_data: <span class="code-cls">list</span> = []
        self._lock = asyncio.<span class="code-cls">Lock</span>()  <span class="code-cm"># ← 동시성 제어의 핵심</span>

    <span class="code-kw">async def</span> <span class="code-fn">add_orderbook</span>(self, symbol: <span class="code-cls">str</span>, record: <span class="code-cls">dict</span>) -> <span class="code-kw">None</span>:
        <span class="code-kw">async with</span> self._lock:  <span class="code-cm"># 한 번에 하나의 코루틴만 접근</span>
            self._orderbook_data[symbol].append(record)

    <span class="code-kw">async def</span> <span class="code-fn">flush</span>(self) -> <span class="code-cls">dict</span>:
        <span class="code-str">"""모든 데이터를 반환하고 버퍼 초기화 — 원자적 연산"""</span>
        <span class="code-kw">async with</span> self._lock:
            result = {
                <span class="code-str">"orderbook"</span>: <span class="code-fn">dict</span>(self._orderbook_data),
                <span class="code-str">"trade"</span>: <span class="code-fn">dict</span>(self._trade_data),
                <span class="code-str">"liquidation"</span>: <span class="code-fn">dict</span>(self._liquidation_data),
                <span class="code-str">"kline"</span>: <span class="code-fn">dict</span>(self._kline_data),
                <span class="code-str">"funding"</span>: <span class="code-fn">list</span>(self._funding_data),
            }
            <span class="code-cm"># 새 defaultdict로 교체 — 기존 데이터는 result에 안전하게 보존</span>
            self._orderbook_data = <span class="code-fn">defaultdict</span>(<span class="code-cls">list</span>)
            self._trade_data = <span class="code-fn">defaultdict</span>(<span class="code-cls">list</span>)
            <span class="code-cm">... (나머지도 동일)</span>
            <span class="code-kw">return</span> result</div>

    <div class="callout">
        <div class="callout-header">💡 flush()가 원자적인 이유</div>
        <p class="body-text" style="margin-bottom:0;">flush()는 Lock 안에서 (1) 현재 데이터를 복사하고 (2) 버퍼를 비우는 두 작업을 한 번에 수행한다. Lock 밖에서 이 두 작업을 하면, 복사와 비우기 사이에 새 데이터가 들어와서 유실될 수 있다. <code>dict(self._orderbook_data)</code>는 얕은 복사(shallow copy)이므로, 새 defaultdict로 교체해도 기존 리스트 객체는 result에 안전하게 남아있다.</p>
    </div>

    <div class="subsection">5.1 메모리 감시 — 강제 플러시</div>

    <div class="code-block"><span class="code-kw">def</span> <span class="code-fn">estimate_memory_usage</span>(self) -> <span class="code-cls">int</span>:
    <span class="code-str">"""현재 메모리 사용량 추정 (바이트)"""</span>
    total = <span class="code-num">0</span>
    <span class="code-kw">for</span> store <span class="code-kw">in</span> [self._orderbook_data, self._trade_data,
                  self._liquidation_data, self._kline_data]:
        <span class="code-kw">for</span> records <span class="code-kw">in</span> store.values():
            total += sys.<span class="code-fn">getsizeof</span>(records)
            <span class="code-kw">for</span> r <span class="code-kw">in</span> records:
                total += sys.<span class="code-fn">getsizeof</span>(r)
    <span class="code-kw">return</span> total

<span class="code-cm"># main.py에서 30초마다 체크</span>
<span class="code-kw">async def</span> <span class="code-fn">force_flush_monitor</span>():
    <span class="code-kw">while</span> <span class="code-kw">True</span>:
        <span class="code-kw">await</span> asyncio.<span class="code-fn">sleep</span>(<span class="code-num">30</span>)
        <span class="code-kw">if</span> buffer.<span class="code-fn">needs_force_flush</span>():  <span class="code-cm"># 500MB 초과?</span>
            <span class="code-kw">await</span> flusher.<span class="code-fn">flush_now</span>()</div>

    <p class="body-text">1시간 플러시 주기 사이에 메모리가 500MB를 초과하면 즉시 강제 플러시를 실행한다. BTC 같은 활발한 심볼은 1시간에 수십만 건의 레코드가 쌓일 수 있으므로, 이 안전장치가 OOM(Out of Memory)을 방지한다.</p>

    <h2 class="section-header">VI. flusher.py — Parquet 저장과 무결성</h2>

    <p class="body-text">Flusher는 메모리의 데이터를 디스크에 영구 저장하는 모듈이다. 단순히 파일을 쓰는 것이 아니라, 원자적 쓰기, 체크섬 기록, 콜백 통보까지 수행한다.</p>

    <div class="subsection">6.1 원자적 파일 쓰기</div>

    <p class="body-text">Parquet 파일을 직접 쓰다가 중간에 프로세스가 죽으면 반쪽짜리 파일이 남는다. 이를 방지하기 위해 임시 파일에 먼저 쓰고, 완료 후 os.replace로 원자적으로 교체한다.</p>

    <div class="code-block"><span class="code-dec">@staticmethod</span>
<span class="code-kw">def</span> <span class="code-fn">_save_parquet</span>(data: <span class="code-cls">list</span>[<span class="code-cls">dict</span>], filepath: <span class="code-cls">Path</span>) -> <span class="code-cls">int</span>:
    df = pd.<span class="code-cls">DataFrame</span>(data)

    <span class="code-cm"># 1. 임시 파일 생성 (같은 디렉토리에)</span>
    tmp_fd, tmp_path = tempfile.<span class="code-fn">mkstemp</span>(
        suffix=<span class="code-str">".parquet.tmp"</span>, dir=filepath.parent
    )
    os.<span class="code-fn">close</span>(tmp_fd)

    <span class="code-kw">try</span>:
        <span class="code-cm"># 2. 임시 파일에 Parquet 쓰기 (snappy 압축)</span>
        df.<span class="code-fn">to_parquet</span>(tmp_path, index=<span class="code-kw">False</span>, compression=<span class="code-str">"snappy"</span>)

        <span class="code-cm"># 3. 원자적 교체 — 이 시점에서 파일이 "갑자기" 나타남</span>
        os.<span class="code-fn">replace</span>(tmp_path, filepath)
    <span class="code-kw">except</span> <span class="code-cls">Exception</span>:
        <span class="code-kw">if</span> os.path.<span class="code-fn">exists</span>(tmp_path):
            os.<span class="code-fn">unlink</span>(tmp_path)  <span class="code-cm"># 실패 시 임시 파일 정리</span>
        <span class="code-kw">raise</span>

    <span class="code-kw">return</span> <span class="code-fn">len</span>(df)</div>

    <div class="formula-box">
        <div class="formula-label">os.replace vs os.rename</div>
        <div class="formula-content">
            os.rename: 대상 파일이 이미 존재하면 Windows에서 실패<br>
            os.replace: 대상 파일이 존재해도 원자적으로 덮어씀 (POSIX + Windows)<br>
            → 크로스 플랫폼 안전성을 위해 os.replace 사용
        </div>
    </div>

    <div class="subsection">6.2 SHA-256 체크섬</div>

    <p class="body-text">저장된 모든 Parquet 파일의 SHA-256 해시를 checksums.json에 기록한다. 나중에 파일이 손상되었는지 검증할 수 있다.</p>

    <div class="code-block"><span class="code-dec">@staticmethod</span>
<span class="code-kw">def</span> <span class="code-fn">compute_checksum</span>(filepath: <span class="code-cls">Path</span>) -> <span class="code-cls">str</span>:
    h = hashlib.<span class="code-fn">sha256</span>()
    <span class="code-kw">with</span> <span class="code-fn">open</span>(filepath, <span class="code-str">"rb"</span>) <span class="code-kw">as</span> f:
        <span class="code-kw">for</span> chunk <span class="code-kw">in</span> <span class="code-fn">iter</span>(<span class="code-kw">lambda</span>: f.<span class="code-fn">read</span>(<span class="code-num">8192</span>), b<span class="code-str">""</span>):
            h.<span class="code-fn">update</span>(chunk)
    <span class="code-kw">return</span> h.<span class="code-fn">hexdigest</span>()

<span class="code-cm"># checksums.json 예시:</span>
<span class="code-cm"># [</span>
<span class="code-cm">#   {</span>
<span class="code-cm">#     "filename": "BTCUSDT_orderbook_20260226_1100.parquet",</span>
<span class="code-cm">#     "sha256": "a1b2c3d4e5f6...",</span>
<span class="code-cm">#     "record_count": 36000,</span>
<span class="code-cm">#     "file_size": 2457600,</span>
<span class="code-cm">#     "created_at": "2026-02-26T11:00:00+00:00"</span>
<span class="code-cm">#   }</span>
<span class="code-cm"># ]</span></div>

    <p class="body-text">8KB 청크 단위로 읽어서 해시를 계산하므로, 수 GB 파일도 메모리 부담 없이 처리할 수 있다. 학술 논문에서 데이터 무결성을 증명할 때 이 체크섬 파일을 함께 공개하면 된다.</p>

    <div class="subsection">6.3 파일명 규칙</div>

    <div class="code-block"><span class="code-cm"># 파일명 패턴: {SYMBOL}_{datatype}_{YYYYMMDD}_{HHMM}.parquet</span>
<span class="code-cm"># 예시:</span>
<span class="code-cm">#   BTCUSDT_orderbook_20260226_1100.parquet</span>
<span class="code-cm">#   ETHUSDT_trade_20260226_1100.parquet</span>
<span class="code-cm">#   XRPUSDT_liquidation_20260226_1100.parquet</span>
<span class="code-cm">#   funding_rate_20260226_1100.parquet  (펀딩비는 심볼 통합)</span>

<span class="code-dec">@staticmethod</span>
<span class="code-kw">def</span> <span class="code-fn">_generate_filename</span>(symbol, datatype, timestamp):
    <span class="code-kw">return</span> f<span class="code-str">"{symbol.upper()}_{datatype}_{timestamp.strftime('%Y%m%d_%H%M')}.parquet"</span></div>

    <h2 class="section-header">VII. syncer.py — 클라우드 동기화와 로컬 정리</h2>

    <p class="body-text">Syncer는 Flusher가 생성한 Parquet 파일을 rclone을 통해 클라우드(Google Drive, S3 등)에 업로드하고, 오래된 로컬 파일을 정리한다.</p>

    <div class="code-block"><span class="code-kw">async def</span> <span class="code-fn">sync_file</span>(self, filepath: <span class="code-cls">Path</span>) -> <span class="code-cls">bool</span>:
    cmd = [<span class="code-str">"rclone"</span>, <span class="code-str">"copy"</span>, <span class="code-fn">str</span>(filepath),
           f<span class="code-str">"{self.config.cloud_remote}:{self.config.cloud_path}"</span>]

    proc = <span class="code-kw">await</span> asyncio.<span class="code-fn">create_subprocess_exec</span>(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = <span class="code-kw">await</span> proc.<span class="code-fn">communicate</span>()

    <span class="code-kw">if</span> proc.returncode == <span class="code-num">0</span>:
        self._synced_files.<span class="code-fn">add</span>(<span class="code-fn">str</span>(filepath))  <span class="code-cm"># 동기화 완료 기록</span>
        <span class="code-kw">return True</span>
    <span class="code-kw">else</span>:
        self._pending_queue.<span class="code-fn">append</span>(filepath)  <span class="code-cm"># 실패 → 재시도 대기열</span>
        <span class="code-kw">return False</span></div>

    <p class="body-text">rclone을 asyncio.create_subprocess_exec로 실행하므로, 업로드 중에도 다른 코루틴(WebSocket 수신 등)이 정상 동작한다. 업로드 실패 시 파일을 대기열에 다시 넣어 다음 주기에 재시도한다.</p>

    <div class="subsection">7.1 안전한 파일 삭제</div>

    <p class="body-text">로컬 파일 삭제는 두 가지 조건을 모두 만족해야만 수행된다: (1) cleanup_days(기본 7일) 이상 경과, (2) 클라우드 동기화 완료. 하나라도 충족하지 않으면 삭제하지 않는다.</p>

    <div class="code-block"><span class="code-kw">async def</span> <span class="code-fn">cleanup_old_files</span>(self) -> <span class="code-kw">None</span>:
    <span class="code-kw">for</span> filepath <span class="code-kw">in</span> data_dir.<span class="code-fn">glob</span>(<span class="code-str">"*.parquet"</span>):
        file_age = now - filepath.<span class="code-fn">stat</span>().st_mtime
        is_old_enough = file_age >= cutoff_seconds     <span class="code-cm"># 조건 1: 7일 경과</span>
        is_synced = <span class="code-fn">str</span>(filepath) <span class="code-kw">in</span> self._synced_files  <span class="code-cm"># 조건 2: 동기화 완료</span>

        <span class="code-kw">if</span> is_old_enough <span class="code-kw">and</span> is_synced:  <span class="code-cm"># 둘 다 만족해야 삭제</span>
            filepath.<span class="code-fn">unlink</span>()</div>

    <div class="limitation-box">
        <div class="limitation-header">⚠️ 주의: cloud_remote 미설정 시</div>
        <p class="body-text" style="margin-bottom:0;">config.yaml에서 cloud_remote를 비워두면 동기화가 건너뛰어지고, 파일이 _synced_files에 추가되지 않으므로 로컬 파일도 영원히 삭제되지 않는다. 이는 의도된 동작이다 — 클라우드 백업 없이 로컬 파일을 삭제하면 데이터 유실이 발생하기 때문이다.</p>
    </div>

    <h2 class="section-header">VIII. 모니터링 모듈들</h2>

    <div class="subsection">8.1 integrity_logger.py — 무결성 추적</div>

    <p class="body-text">시스템에서 발생하는 모든 "이상 징후"를 기록한다: 시퀀스 갭, 재연결, 플러시 통계, 동기화 상태. 이 데이터는 수집된 시장 데이터의 품질을 평가하는 메타데이터가 된다.</p>

    <div class="code-block"><span class="code-kw">class</span> <span class="code-cls">IntegrityLogger</span>:
    <span class="code-kw">def</span> <span class="code-fn">record_gap</span>(self, symbol, expected_id, actual_id, timestamp):
        <span class="code-str">"""시퀀스 갭 기록 — 오더북 데이터 누락 추적"""</span>
        self._gaps.append({
            <span class="code-str">"timestamp"</span>: timestamp,
            <span class="code-str">"symbol"</span>: symbol,
            <span class="code-str">"expected_id"</span>: expected_id,
            <span class="code-str">"actual_id"</span>: actual_id,
        })

    <span class="code-dec">@staticmethod</span>
    <span class="code-kw">def</span> <span class="code-fn">compute_coverage</span>(total_seconds, gap_seconds) -> <span class="code-cls">float</span>:
        <span class="code-str">"""데이터 커버리지 비율: (전체 시간 − 갭 시간) / 전체 시간"""</span>
        <span class="code-kw">if</span> total_seconds &lt;= <span class="code-num">0</span>:
            <span class="code-kw">return</span> <span class="code-num">0.0</span>
        <span class="code-kw">return</span> (total_seconds - gap_seconds) / total_seconds
        <span class="code-cm"># 예: 3600초 중 갭 5초 → 커버리지 = 99.86%</span></div>

    <p class="body-text">커버리지 비율은 논문에서 데이터 품질을 보고할 때 핵심 지표다. "본 연구에서 사용한 데이터의 커버리지는 99.9%이며, 총 3건의 시퀀스 갭이 발생하였다"와 같이 기술할 수 있다.</p>

    <div class="subsection">8.2 time_sync_monitor.py — 시간 동기화</div>

    <p class="body-text">10분마다 두 가지를 측정한다: (1) NTP 서버와 로컬 시계의 오프셋, (2) 바이낸스 서버와의 RTT(Round-Trip Time).</p>

    <div class="code-block"><span class="code-kw">async def</span> <span class="code-fn">measure_binance_offset</span>(self) -> <span class="code-cls">tuple</span>[<span class="code-cls">float</span>, <span class="code-cls">float</span>]:
    <span class="code-str">"""바이낸스 서버 시간 차이 및 RTT 측정"""</span>
    t1 = time.<span class="code-fn">time</span>()                          <span class="code-cm"># 요청 전 시각</span>
    <span class="code-kw">async with</span> session.<span class="code-fn">get</span>(<span class="code-str">"/api/v3/time"</span>) <span class="code-kw">as</span> resp:
        t2 = time.<span class="code-fn">time</span>()                      <span class="code-cm"># 응답 후 시각</span>
        data = <span class="code-kw">await</span> resp.<span class="code-fn">json</span>()
        server_time = data[<span class="code-str">"serverTime"</span>] / <span class="code-num">1000.0</span>

    rtt = t2 - t1                              <span class="code-cm"># 왕복 시간</span>
    local_mid = (t1 + t2) / <span class="code-num">2.0</span>               <span class="code-cm"># 로컬 중간 시각</span>
    offset = server_time - local_mid           <span class="code-cm"># 시간 차이</span>
    <span class="code-kw">return</span> offset, rtt</div>

    <p class="body-text"><code>(t1 + t2) / 2</code>는 요청이 서버에 도달한 시점의 근사치다. 이 값과 서버 시간의 차이가 시계 오프셋이 된다. NTP 오프셋이 100ms를 초과하면 텔레그램으로 경고를 보낸다.</p>

    <div class="subsection">8.3 telegram_reporter.py — 알림</div>

    <p class="body-text">텔레그램 봇을 통해 시스템 상태를 실시간으로 모니터링한다. 가장 중요한 설계 원칙: 텔레그램 전송 실패가 데이터 수집에 영향을 주지 않는다.</p>

    <div class="code-block"><span class="code-kw">async def</span> <span class="code-fn">send_message</span>(self, text: <span class="code-cls">str</span>) -> <span class="code-kw">None</span>:
    <span class="code-kw">if not</span> self.enabled:  <span class="code-cm"># 토큰 미설정 시 조용히 무시</span>
        <span class="code-kw">return</span>
    <span class="code-kw">try</span>:
        <span class="code-kw">async with</span> aiohttp.<span class="code-cls">ClientSession</span>() <span class="code-kw">as</span> session:
            <span class="code-kw">async with</span> session.<span class="code-fn">post</span>(url, json=payload,
                                     timeout=aiohttp.<span class="code-cls">ClientTimeout</span>(total=<span class="code-num">10</span>)) <span class="code-kw">as</span> resp:
                <span class="code-kw">if</span> resp.status != <span class="code-num">200</span>:
                    logger.<span class="code-fn">warning</span>(f<span class="code-str">"텔레그램 전송 실패: {resp.status}"</span>)
    <span class="code-kw">except</span> <span class="code-cls">Exception</span>:
        logger.<span class="code-fn">warning</span>(<span class="code-str">"텔레그램 전송 중 예외"</span>, exc_info=<span class="code-kw">True</span>)
        <span class="code-cm"># ← 예외를 삼킴! 수집 루프에 전파하지 않음</span></div>

    <p class="body-text">모든 예외를 try-except로 잡아서 로깅만 하고 넘어간다. 텔레그램 서버가 다운되어도, 네트워크가 불안정해도, 데이터 수집은 계속된다. 모니터링은 "있으면 좋고, 없어도 되는" 부가 기능이어야 한다.</p>

    <div class="subsection">8.4 environment_recorder.py — 환경 메타데이터</div>

    <p class="body-text">시스템 시작 시 한 번 실행되어, 수집 환경의 모든 정보를 JSON으로 기록한다. 논문의 재현성(reproducibility)을 위한 모듈이다.</p>

    <div class="code-block"><span class="code-cm"># environment_20260226_110000.json 예시:</span>
{
    <span class="code-str">"timestamp"</span>: <span class="code-str">"2026-02-26T11:00:00+00:00"</span>,
    <span class="code-str">"system"</span>: {
        <span class="code-str">"os"</span>: <span class="code-str">"Darwin"</span>,
        <span class="code-str">"machine"</span>: <span class="code-str">"arm64"</span>,
        <span class="code-str">"cpu_count"</span>: <span class="code-num">10</span>,
        <span class="code-str">"ram_total_gb"</span>: <span class="code-num">16.0</span>
    },
    <span class="code-str">"python"</span>: {
        <span class="code-str">"version"</span>: <span class="code-str">"3.14.2"</span>,
        <span class="code-str">"packages"</span>: {
            <span class="code-str">"websockets"</span>: <span class="code-str">"14.2"</span>,
            <span class="code-str">"pandas"</span>: <span class="code-str">"2.2.3"</span>,
            <span class="code-str">"pyarrow"</span>: <span class="code-str">"18.1.0"</span>
        }
    },
    <span class="code-str">"config"</span>: {
        <span class="code-str">"symbols"</span>: [<span class="code-str">"btcusdt"</span>, <span class="code-str">"ethusdt"</span>, ...],
        <span class="code-str">"telegram_bot_token"</span>: <span class="code-str">"***"</span>  <span class="code-cm">← 민감 정보 마스킹</span>
    }
}</div>

    <p class="body-text">텔레그램 토큰 같은 민감 정보는 자동으로 <code>"***"</code>로 마스킹된다. 이 파일을 논문의 부록이나 데이터 저장소에 함께 공개하면, 다른 연구자가 동일한 환경을 재현할 수 있다.</p>

    <h2 class="section-header">IX. config.py — 설정 관리</h2>

    <p class="body-text">Config는 YAML 파일을 파이썬 dataclass로 변환하는 간단한 모듈이다. 하지만 몇 가지 세심한 설계가 들어있다.</p>

    <div class="code-block"><span class="code-dec">@dataclass</span>
<span class="code-kw">class</span> <span class="code-cls">Config</span>:
    symbols: <span class="code-cls">list</span>[<span class="code-cls">str</span>] = field(default_factory=<span class="code-kw">lambda</span>: [<span class="code-str">"btcusdt"</span>, <span class="code-str">"ethusdt"</span>, <span class="code-str">"xrpusdt"</span>])
    flush_interval: <span class="code-cls">int</span> = <span class="code-num">3600</span>          <span class="code-cm"># 1시간</span>
    data_dir: <span class="code-cls">str</span> = <span class="code-str">"./data"</span>
    max_buffer_mb: <span class="code-cls">int</span> = <span class="code-num">500</span>
    orderbook_depth: <span class="code-cls">int</span> = <span class="code-num">1000</span>        <span class="code-cm"># REST 스냅샷 깊이</span>
    orderbook_top_levels: <span class="code-cls">int</span> = <span class="code-num">20</span>     <span class="code-cm"># 저장할 호가 수</span>
    use_futures: <span class="code-cls">bool</span> = <span class="code-kw">True</span>            <span class="code-cm"># 선물 API 사용 여부</span>
    telegram_bot_token: <span class="code-cls">str</span> = <span class="code-str">""</span>        <span class="code-cm"># 비어있으면 알림 비활성화</span>
    cloud_remote: <span class="code-cls">str</span> = <span class="code-str">""</span>              <span class="code-cm"># 비어있으면 동기화 건너뜀</span>

    <span class="code-dec">@classmethod</span>
    <span class="code-kw">def</span> <span class="code-fn">from_yaml</span>(cls, path: <span class="code-cls">str</span>) -> <span class="code-str">"Config"</span>:
        <span class="code-kw">if not</span> Path(path).<span class="code-fn">exists</span>():
            <span class="code-kw">return</span> cls()  <span class="code-cm"># 파일 없으면 기본값 사용</span>
        <span class="code-kw">with</span> <span class="code-fn">open</span>(path) <span class="code-kw">as</span> f:
            data = yaml.<span class="code-fn">safe_load</span>(f) <span class="code-kw">or</span> {}
        <span class="code-cm"># dataclass 필드에 있는 키만 추출 → 오타/잘못된 키 무시</span>
        <span class="code-kw">return</span> cls(**{k: v <span class="code-kw">for</span> k, v <span class="code-kw">in</span> data.items()
                      <span class="code-kw">if</span> k <span class="code-kw">in</span> cls.__dataclass_fields__})</div>

    <p class="body-text"><code>cls.__dataclass_fields__</code>를 사용하여 YAML에 정의된 키 중 dataclass 필드에 존재하는 것만 추출한다. config.yaml에 오타가 있거나 미래에 제거된 필드가 남아있어도 에러 없이 무시된다.</p>

    <h2 class="section-header">X. Graceful Shutdown — 우아한 종료</h2>

    <p class="body-text">24/7 수집 시스템에서 종료도 중요하다. Ctrl+C를 누르거나 kill 시그널을 보내면, 버퍼에 남아있는 데이터를 디스크에 저장한 후 종료해야 한다.</p>

    <div class="code-block"><span class="code-cm"># main.py — graceful shutdown</span>
loop = asyncio.<span class="code-fn">get_running_loop</span>()
shutdown_event = asyncio.<span class="code-cls">Event</span>()

<span class="code-kw">def</span> <span class="code-fn">_signal_handler</span>():
    logger.<span class="code-fn">info</span>(<span class="code-str">"종료 신호 수신, 마지막 플러시 실행 중..."</span>)
    shutdown_event.<span class="code-fn">set</span>()  <span class="code-cm"># 이벤트 발생 → 메인 루프 탈출</span>

<span class="code-kw">for</span> sig <span class="code-kw">in</span> (signal.SIGINT, signal.SIGTERM):
    loop.<span class="code-fn">add_signal_handler</span>(sig, _signal_handler)

<span class="code-cm"># 태스크 실행 + shutdown 대기</span>
gathered = asyncio.<span class="code-fn">gather</span>(*tasks, return_exceptions=<span class="code-kw">True</span>)
done, _ = <span class="code-kw">await</span> asyncio.<span class="code-fn">wait</span>(
    [asyncio.<span class="code-fn">create_task</span>(shutdown_event.<span class="code-fn">wait</span>()), gathered],
    return_when=asyncio.FIRST_COMPLETED,
)

<span class="code-cm"># 종료 시 마지막 플러시 — 버퍼 데이터 유실 방지</span>
<span class="code-kw">await</span> flusher.<span class="code-fn">flush_now</span>()</div>

    <p class="body-text"><code>asyncio.wait</code>의 <code>FIRST_COMPLETED</code>를 사용하여, shutdown 이벤트가 발생하면 즉시 메인 루프를 탈출한다. 그 후 <code>flusher.flush_now()</code>로 버퍼에 남아있는 모든 데이터를 Parquet로 저장한다. 이렇게 하면 1시간 플러시 주기 사이에 종료해도 데이터가 유실되지 않는다.</p>

    <h2 class="section-header">XI. 전체 데이터 흐름 요약</h2>

    <p class="body-text">지금까지 설명한 모든 모듈의 상호작용을 하나의 흐름으로 정리한다.</p>

    <div class="formula-box">
        <div class="formula-label">End-to-End Data Flow</div>
        <div class="formula-content">
<span style="color:var(--wsj-accent);">① 시작</span>
  main.py → Config.from_yaml() → 11개 모듈 초기화
  → EnvironmentRecorder.record() → 환경 메타데이터 JSON 저장
  → TelegramReporter.send_startup_report() → 시작 알림
  → asyncio.gather() → 7~8개 코루틴 동시 실행

<span style="color:var(--wsj-accent);">② 수집 (Collector)</span>
  WebSocket 연결 → depth@100ms, aggTrade, kline_1m 수신
  → recv_time 기록 → JSON 파싱 → stream 필드로 라우팅

<span style="color:var(--wsj-accent);">③ 오더북 처리 (OrderBookManager)</span>
  depth diff 수신 → 시퀀스 검증 (F ≤ X+1 ≤ L)
  → 검증 성공: diff 적용 → 상위 20호가 스냅샷 생성
  → 검증 실패: 갭 기록 → initialized=False → 자동 재초기화

<span style="color:var(--wsj-accent);">④ 버퍼링 (DataBuffer)</span>
  asyncio.Lock 보호 하에 심볼별 리스트에 append
  → 30초마다 메모리 체크 → 500MB 초과 시 강제 플러시

<span style="color:var(--wsj-accent);">⑤ 저장 (Flusher)</span>
  1시간마다 buffer.flush() → DataFrame 변환
  → tmpfile에 Parquet(snappy) 쓰기 → os.replace 원자적 교체
  → SHA-256 체크섬 → checksums.json 기록
  → on_file_created 콜백 → Syncer에 통보

<span style="color:var(--wsj-accent);">⑥ 동기화 (Syncer)</span>
  대기열의 파일 → rclone copy → 클라우드 업로드
  → 실패 시 재시도 대기열에 복귀
  → 7일 경과 + 동기화 완료 파일만 로컬 삭제

<span style="color:var(--wsj-accent);">⑦ 종료</span>
  SIGINT/SIGTERM → shutdown_event.set()
  → flusher.flush_now() → 마지막 데이터 저장 → 종료
        </div>
    </div>

    <div class="conclusion-box">
        <h2 class="section-header">마치며</h2>
        <p class="body-text">이 시스템은 총 12개의 소스 파일, 약 1,200줄의 코드로 구성되어 있다. 각 모듈은 하나의 명확한 책임을 가지며, 의존성 주입과 콜백 패턴으로 느슨하게 결합된다. asyncio 기반 단일 프로세스 아키텍처는 구형 PC에서도 효율적으로 동작하며, 멀티스레딩의 복잡성 없이 동시성을 달성한다.</p>
        <p class="body-text">핵심 설계 결정을 요약하면:</p>
        <p class="body-text">
            • 가격을 str로 보존 → 부동소수점 오차 방지<br>
            • 오더북을 dict로 관리 → O(1) 가격 조회<br>
            • asyncio.Lock → 단일 스레드 동시성 제어<br>
            • tmpfile + os.replace → 원자적 파일 쓰기<br>
            • 콜백 패턴 → Flusher↔Syncer 느슨한 결합<br>
            • 예외 삼킴 → 모니터링 실패가 수집에 영향 없음<br>
            • Grace period → 스냅샷-diff 타이밍 이슈 허용
        </p>
        <p class="body-text">전체 소스 코드는 <a href="https://github.com/gkfla2020-bit/binance-hft-data-collector" style="color:var(--wsj-accent);">GitHub</a>에서 확인할 수 있다.</p>
    </div>

    <div style="margin-top:40px; padding-top:20px; border-top:1px solid #ddd; font-size:13px; color:var(--wsj-gray);">
        <p><strong>관련 글:</strong> <a href="/research/binance-hft-data-collector-kr/">바이낸스 고빈도 데이터 수집 시스템 아키텍처</a> — 설계 동기, 연구 활용 방안, 실측 데이터 분석</p>
    </div>
</div>
