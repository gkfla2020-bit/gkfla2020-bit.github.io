---
layout: post
title: "바이낸스 데이터 수집기 — 전체 코드 한 줄씩 리뷰"
date: 2026-02-27 20:00:00
permalink: /research/binance-collector-full-code-review-kr/
categories: [research, data-engineering]
tags: [binance, websocket, python, code-review, asyncio, parquet, line-by-line]
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
    .code-block { background: #1e1e1e; color: #d4d4d4; padding: 20px; border-radius: 6px; font-family: var(--mono); font-size: 12.5px; line-height: 1.7; overflow-x: auto; margin: 20px 0; white-space: pre; }
    .code-kw { color: #569cd6; }
    .code-str { color: #ce9178; }
    .code-cm { color: #6a9955; }
    .code-fn { color: #dcdcaa; }
    .code-num { color: #b5cea8; }
    .code-cls { color: #4ec9b0; }
    .code-dec { color: #c586c0; }
    .line-review { background: #f8f9fa; border-left: 3px solid var(--wsj-accent); padding: 15px 20px; margin: 15px 0; font-family: var(--serif); font-size: 15px; line-height: 1.8; }
    .line-review code { background: #e8e8e8; padding: 2px 6px; border-radius: 3px; font-family: var(--mono); font-size: 13px; }
    .line-review .line-num { color: var(--wsj-accent); font-weight: 700; font-family: var(--mono); }
    .formula-box { background: var(--wsj-light); border-left: 4px solid var(--wsj-accent); padding: 20px 25px; margin: 25px 0; }
    .formula-label { font-size: 11px; font-weight: 700; text-transform: uppercase; color: var(--wsj-accent); margin-bottom: 10px; }
    .formula-content { font-family: var(--mono); font-size: 14px; line-height: 2.0; }
    .formula-note { font-size: 13px; color: var(--wsj-gray); margin-top: 10px; font-style: italic; }
    .callout { border: 1px solid var(--wsj-black); padding: 20px; margin: 30px 0; }
    .callout-header { font-weight: 700; font-size: 12px; text-transform: uppercase; margin-bottom: 10px; }
    .analogy-box { background: #e8f4fd; border-left: 4px solid var(--wsj-accent); padding: 20px 25px; margin: 25px 0; border-radius: 0 8px 8px 0; }
    .analogy-label { font-size: 12px; font-weight: 700; text-transform: uppercase; color: var(--wsj-accent); margin-bottom: 8px; }
    .analogy-text { font-family: var(--serif); font-size: 16px; line-height: 1.8; }
    .warning-box { background: #fff3e0; border-left: 4px solid var(--wsj-orange); padding: 20px 25px; margin: 25px 0; }
    .warning-label { font-size: 12px; font-weight: 700; text-transform: uppercase; color: var(--wsj-orange); margin-bottom: 8px; }
    .file-header { background: #2d2d2d; color: #e0e0e0; padding: 12px 20px; border-radius: 6px 6px 0 0; font-family: var(--mono); font-size: 14px; font-weight: 700; margin-top: 30px; margin-bottom: 0; display: flex; justify-content: space-between; }
    .file-header .file-path { color: var(--wsj-accent); }
    .file-header .file-lines { color: #888; font-weight: 400; }
    .data-table { width: 100%; border-collapse: collapse; font-size: 14px; margin: 20px 0; }
    .data-table th { font-weight: 700; text-transform: uppercase; font-size: 11px; padding: 12px; text-align: left; border-bottom: 2px solid var(--wsj-black); background: var(--wsj-light); }
    .data-table td { padding: 12px; border-bottom: 1px solid #e0e0e0; }
    .data-table .mono { font-family: var(--mono); font-size: 12px; }
    .conclusion-box { background: var(--wsj-black); color: white; padding: 35px; margin: 50px 0; }
    .conclusion-box .section-header { color: white; border-bottom-color: #444; }
    .conclusion-box .body-text { color: #ccc; }
    @media (max-width: 768px) { .headline { font-size: 26px; } }
</style>

<div class="report-container">
    <div class="masthead">
        <span class="section-label">Full Code Review — Line by Line</span>
        <span class="date-line">February 27, 2026</span>
    </div>

    <h1 class="headline">바이낸스 데이터 수집기<br>전체 코드 한 줄씩 리뷰</h1>
    <p class="deck">12개 소스 파일, 약 1,200줄의 코드를 한 줄도 빠짐없이 해설한다.<br>각 줄이 왜 거기 있는지, 없으면 어떻게 되는지, 다른 방법은 없는지까지.</p>

    <div class="abstract">
        <div class="abstract-title">읽는 법</div>
        <p class="body-text" style="margin-bottom:0;">
        각 파일의 전체 코드를 먼저 보여주고, 그 아래에 줄 단위 또는 블록 단위로 해설한다.
        코드 블록의 <span style="color:#6a9955;">초록색 주석</span>은 원본 코드의 주석이고,
        아래 파란 박스의 해설이 이 글에서 추가한 설명이다.
        <br><br>
        관련 글: <a href="/research/binance-collector-beginner-guide-kr/">비전공자용 해설</a> |
        <a href="/research/binance-collector-code-deepdive-kr/">코드 딥다이브</a> |
        <a href="/research/binance-hft-data-collector-kr/">아키텍처</a>
        </p>
    </div>

    <!-- ============================================================ -->
    <!-- FILE 1: config.py -->
    <!-- ============================================================ -->
    <h2 class="section-header">파일 1/12 — config.py</h2>
    <p class="body-text">시스템의 모든 설정을 관리하는 모듈. YAML 파일을 읽어서 파이썬 객체로 변환한다. 가장 먼저 이해해야 할 파일이다.</p>

    <div class="file-header"><span class="file-path">src/config.py</span><span class="file-lines">38 lines</span></div>
    <div class="code-block"><span class="code-str">"""시스템 설정 모듈 - config.yaml 로드 및 Config 데이터클래스"""</span>

<span class="code-kw">from</span> dataclasses <span class="code-kw">import</span> dataclass, field, asdict
<span class="code-kw">from</span> pathlib <span class="code-kw">import</span> Path

<span class="code-kw">import</span> yaml


<span class="code-dec">@dataclass</span>
<span class="code-kw">class</span> <span class="code-cls">Config</span>:
    <span class="code-str">"""시스템 설정 (config.yaml에서 로드)"""</span>
    symbols: list[str] = field(default_factory=<span class="code-kw">lambda</span>: [<span class="code-str">"btcusdt"</span>, <span class="code-str">"ethusdt"</span>, <span class="code-str">"xrpusdt"</span>])
    flush_interval: int = <span class="code-num">3600</span>
    data_dir: str = <span class="code-str">"./data"</span>
    log_dir: str = <span class="code-str">"./logs"</span>
    max_buffer_mb: int = <span class="code-num">500</span>
    cleanup_days: int = <span class="code-num">7</span>
    cloud_remote: str = <span class="code-str">""</span>
    cloud_path: str = <span class="code-str">""</span>
    orderbook_depth: int = <span class="code-num">1000</span>
    orderbook_top_levels: int = <span class="code-num">20</span>
    telegram_bot_token: str = <span class="code-str">""</span>
    telegram_chat_id: str = <span class="code-str">""</span>
    use_futures: bool = <span class="code-kw">True</span>

    <span class="code-dec">@classmethod</span>
    <span class="code-kw">def</span> <span class="code-fn">from_yaml</span>(cls, path: str) -> <span class="code-str">"Config"</span>:
        <span class="code-str">"""YAML 파일에서 Config 객체 생성"""</span>
        p = Path(path)
        <span class="code-kw">if not</span> p.exists():
            <span class="code-kw">return</span> cls()
        <span class="code-kw">with</span> open(p, <span class="code-str">"r"</span>, encoding=<span class="code-str">"utf-8"</span>) <span class="code-kw">as</span> f:
            data = yaml.safe_load(f) <span class="code-kw">or</span> {}
        <span class="code-kw">return</span> cls(**{k: v <span class="code-kw">for</span> k, v <span class="code-kw">in</span> data.items() <span class="code-kw">if</span> k <span class="code-kw">in</span> cls.__dataclass_fields__})

    <span class="code-kw">def</span> <span class="code-fn">to_yaml</span>(self, path: str) -> <span class="code-kw">None</span>:
        <span class="code-kw">with</span> open(path, <span class="code-str">"w"</span>, encoding=<span class="code-str">"utf-8"</span>) <span class="code-kw">as</span> f:
            yaml.dump(asdict(self), f, default_flow_style=<span class="code-kw">False</span>, allow_unicode=<span class="code-kw">True</span>)

    <span class="code-kw">def</span> <span class="code-fn">to_dict</span>(self) -> dict:
        <span class="code-kw">return</span> asdict(self)</div>

    <div class="line-review">
        <span class="line-num">Line 1:</span> <code>from dataclasses import dataclass, field, asdict</code><br>
        파이썬 3.7+의 dataclass를 사용한다. 일반 클래스로 만들면 <code>__init__</code>, <code>__repr__</code>, <code>__eq__</code> 등을 직접 써야 하는데, <code>@dataclass</code>를 붙이면 자동 생성된다. <code>field</code>는 기본값이 리스트처럼 변경 가능한(mutable) 객체일 때 필요하고, <code>asdict</code>는 객체를 딕셔너리로 변환한다.
    </div>

    <div class="line-review">
        <span class="line-num">Line 2:</span> <code>from pathlib import Path</code><br>
        파일 경로를 다루는 현대적인 방법. <code>os.path.join("a", "b")</code> 대신 <code>Path("a") / "b"</code>로 쓸 수 있다. 운영체제(Windows/Mac/Linux)에 따라 경로 구분자(\ vs /)를 자동 처리한다.
    </div>

    <div class="line-review">
        <span class="line-num">Line 4:</span> <code>import yaml</code><br>
        PyYAML 라이브러리. YAML은 JSON보다 사람이 읽기 쉬운 설정 파일 형식이다. <code>pip install pyyaml</code>로 설치한다.
    </div>

    <div class="line-review">
        <span class="line-num">Line 7:</span> <code>@dataclass</code><br>
        이 데코레이터를 붙이면 아래 클래스의 필드들을 보고 자동으로 <code>__init__</code>을 만들어준다. 즉 <code>Config(symbols=["btcusdt"], flush_interval=3600)</code>처럼 객체를 생성할 수 있게 된다.
    </div>

    <div class="line-review">
        <span class="line-num">Line 10:</span> <code>symbols: list[str] = field(default_factory=lambda: ["btcusdt", "ethusdt", "xrpusdt"])</code><br>
        왜 <code>symbols = ["btcusdt"]</code>로 안 쓰고 <code>field(default_factory=...)</code>를 쓸까? 파이썬에서 기본값으로 리스트를 직접 넣으면, 모든 인스턴스가 같은 리스트 객체를 공유하는 버그가 생긴다. <code>default_factory</code>는 매번 새 리스트를 만들어서 이 문제를 방지한다.
    </div>

    <div class="line-review">
        <span class="line-num">Line 11-20:</span> 나머지 필드들<br>
        <code>flush_interval: int = 3600</code> → 1시간(3600초)마다 파일 저장<br>
        <code>max_buffer_mb: int = 500</code> → 메모리 500MB 초과 시 강제 저장<br>
        <code>cleanup_days: int = 7</code> → 7일 지난 파일 삭제<br>
        <code>orderbook_depth: int = 1000</code> → REST 스냅샷에서 가져올 호가 수<br>
        <code>orderbook_top_levels: int = 20</code> → 실제 저장할 상위 호가 수<br>
        <code>telegram_bot_token: str = ""</code> → 빈 문자열이면 텔레그램 비활성화<br>
        <code>use_futures: bool = True</code> → 선물 API(청산/펀딩비) 사용 여부
    </div>

    <div class="line-review">
        <span class="line-num">Line 22:</span> <code>@classmethod</code><br>
        클래스 메서드는 인스턴스 없이 <code>Config.from_yaml("config.yaml")</code>처럼 호출할 수 있다. "팩토리 메서드" 패턴이라고 한다 — 객체를 만드는 또 다른 방법을 제공하는 것.
    </div>

    <div class="line-review">
        <span class="line-num">Line 26:</span> <code>if not p.exists(): return cls()</code><br>
        설정 파일이 없으면 에러를 내지 않고 기본값으로 Config를 생성한다. 처음 실행할 때 config.yaml이 없어도 프로그램이 돌아간다.
    </div>

    <div class="line-review">
        <span class="line-num">Line 28:</span> <code>data = yaml.safe_load(f) or {}</code><br>
        <code>safe_load</code>는 YAML을 파이썬 딕셔너리로 변환한다. <code>or {}</code>는 파일이 비어있을 때 None 대신 빈 딕셔너리를 반환하기 위한 안전장치. <code>yaml.load</code>(unsafe)가 아닌 <code>safe_load</code>를 쓰는 이유는 보안 — unsafe 버전은 임의의 파이썬 코드를 실행할 수 있다.
    </div>

    <div class="line-review">
        <span class="line-num">Line 29:</span> <code>cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})</code><br>
        이 줄이 가장 영리한 부분이다. YAML에서 읽은 키-값 중에서 Config 클래스에 정의된 필드만 골라서 전달한다. config.yaml에 오타가 있거나 (<code>symols</code> 대신 <code>symbols</code>), 미래에 삭제된 필드가 남아있어도 에러 없이 무시된다. <code>__dataclass_fields__</code>는 dataclass가 자동으로 만들어주는 딕셔너리로, 정의된 필드 이름들이 들어있다.
    </div>

    <!-- ============================================================ -->
    <!-- FILE 2: models.py -->
    <!-- ============================================================ -->
    <h2 class="section-header">파일 2/12 — models.py</h2>
    <p class="body-text">시스템이 다루는 모든 데이터의 "설계도". 바이낸스 API가 보내는 JSON을 파이썬 객체로 변환할 때의 계약서 역할을 한다.</p>

    <div class="file-header"><span class="file-path">src/models.py</span><span class="file-lines">75 lines</span></div>
    <div class="code-block"><span class="code-str">"""데이터 모델 정의 - 바이낸스 WebSocket/REST 이벤트 및 내부 상태"""</span>

<span class="code-kw">from</span> dataclasses <span class="code-kw">import</span> dataclass, field


<span class="code-cm"># ── 오더북 관련 ──</span>

<span class="code-dec">@dataclass</span>
<span class="code-kw">class</span> <span class="code-cls">DepthDiffEvent</span>:
    <span class="code-str">"""바이낸스 depth_diff WebSocket 이벤트"""</span>
    symbol: str
    event_time: int              <span class="code-cm"># 거래소 이벤트 시각 (ms)</span>
    recv_time: float             <span class="code-cm"># 로컬 수신 시각 (unix timestamp)</span>
    first_update_id: int         <span class="code-cm"># U</span>
    final_update_id: int         <span class="code-cm"># u</span>
    bids: list[list[str]]        <span class="code-cm"># [[price, qty], ...]</span>
    asks: list[list[str]]        <span class="code-cm"># [[price, qty], ...]</span>

<span class="code-dec">@dataclass</span>
<span class="code-kw">class</span> <span class="code-cls">OrderBookState</span>:
    <span class="code-str">"""심볼별 오더북 내부 상태"""</span>
    bids: dict[str, str] = field(default_factory=dict)
    asks: dict[str, str] = field(default_factory=dict)
    last_update_id: int = <span class="code-num">0</span>
    initialized: bool = <span class="code-kw">False</span>
    init_time: float = <span class="code-num">0.0</span>

<span class="code-dec">@dataclass</span>
<span class="code-kw">class</span> <span class="code-cls">OrderBookSnapshot</span>:
    <span class="code-str">"""버퍼에 저장되는 오더북 스냅샷 레코드"""</span>
    symbol: str
    event_time: int
    recv_time: float
    last_update_id: int
    bids: list[list[str]]
    asks: list[list[str]]

<span class="code-cm"># ── 체결 관련 ──</span>

<span class="code-dec">@dataclass</span>
<span class="code-kw">class</span> <span class="code-cls">AggTradeEvent</span>:
    symbol: str
    trade_id: int
    price: str
    quantity: str
    first_trade_id: int
    last_trade_id: int
    trade_time: int
    recv_time: float
    is_buyer_maker: bool

<span class="code-cm"># ── 청산 관련 ──</span>

<span class="code-dec">@dataclass</span>
<span class="code-kw">class</span> <span class="code-cls">LiquidationEvent</span>:
    symbol: str
    side: str
    order_type: str
    price: str
    quantity: str
    trade_time: int
    recv_time: float

<span class="code-cm"># ── 펀딩비 관련 ──</span>

<span class="code-dec">@dataclass</span>
<span class="code-kw">class</span> <span class="code-cls">FundingRateRecord</span>:
    symbol: str
    funding_rate: str
    funding_time: int
    next_funding_time: int
    recv_time: float

<span class="code-cm"># ── 캔들 관련 ──</span>

<span class="code-dec">@dataclass</span>
<span class="code-kw">class</span> <span class="code-cls">KlineEvent</span>:
    symbol: str
    open_time: int
    close_time: int
    open: str
    high: str
    low: str
    close: str
    volume: str
    quote_volume: str
    trade_count: int
    recv_time: float</div>

    <div class="line-review">
        <span class="line-num">DepthDiffEvent</span> — 바이낸스가 WebSocket으로 보내는 오더북 변경 사항.<br>
        • <code>event_time: int</code> — 바이낸스 서버에서 이벤트가 발생한 시각. 밀리초(ms) 단위. 예: 1740567600000 = 2025-02-26 11:00:00 UTC<br>
        • <code>recv_time: float</code> — 우리 컴퓨터가 이 메시지를 받은 시각. <code>time.time()</code>의 반환값 (초 단위 Unix timestamp). 이 두 시각의 차이가 네트워크 레이턴시의 근사치가 된다.<br>
        • <code>first_update_id / final_update_id</code> — 바이낸스가 매 diff에 붙이는 일련번호. 이 번호가 연속인지 확인해서 데이터 누락을 감지한다.<br>
        • <code>bids / asks: list[list[str]]</code> — 변경된 호가 목록. <code>[["68347.87", "1.234"], ["68346.00", "0"]]</code> 형태. 수량이 "0"이면 해당 가격대 삭제.
    </div>

    <div class="line-review">
        <span class="line-num">OrderBookState</span> — 프로그램 내부에서 관리하는 오더북 상태.<br>
        • <code>bids: dict[str, str]</code> — DepthDiffEvent의 bids는 <code>list</code>인데 여기서는 <code>dict</code>다. 왜? 리스트에서 특정 가격을 찾으려면 처음부터 끝까지 훑어야 한다(O(n)). dict는 키로 바로 접근한다(O(1)). 0.1초마다 수십 개 가격이 업데이트되므로 이 차이가 크다.<br>
        • <code>initialized: bool</code> — REST 스냅샷을 받았는지 여부. False면 diff를 적용하지 않는다.<br>
        • <code>init_time: float</code> — 스냅샷을 받은 시각. 이후 3초간은 시퀀스 검증 실패를 허용한다(grace period).
    </div>

    <div class="line-review">
        <span class="line-num">OrderBookSnapshot</span> — 실제로 파일에 저장되는 오더북 데이터.<br>
        OrderBookState(전체 1000호가)에서 상위 20호가만 추출한 것. bids는 가격 내림차순, asks는 오름차순으로 정렬되어 있다.
    </div>

    <div class="line-review">
        <span class="line-num">AggTradeEvent</span> — 집계 체결 이벤트.<br>
        • <code>price: str</code> — 가격을 문자열로 저장하는 이유: <code>float(0.1) + float(0.2) = 0.30000000000000004</code>. 금융 데이터에서 이런 오차는 치명적이다. 원본 문자열을 보존하고, 분석 시 <code>Decimal</code>로 변환하는 것이 정석.<br>
        • <code>is_buyer_maker: bool</code> — True면 매수자가 maker(지정가 주문), 즉 매도 체결. False면 매수 체결. 시장의 공격적 매수/매도 비율을 분석할 때 핵심 필드.
    </div>

    <div class="line-review">
        <span class="line-num">LiquidationEvent</span> — 강제 청산 이벤트. 선물 시장에서 증거금이 부족해 포지션이 강제로 청산될 때 발생한다. <code>side: str</code>이 "SELL"이면 롱 포지션 청산(가격 하락으로), "BUY"면 숏 포지션 청산(가격 상승으로).
    </div>

    <div class="line-review">
        <span class="line-num">KlineEvent</span> — 1분봉 캔들. OHLCV(시가/고가/저가/종가/거래량) + 거래 횟수. WebSocket에서 <code>x: true</code>(확정된 캔들)일 때만 저장한다. 미확정 캔들은 계속 바뀌므로 저장하지 않는다.
    </div>

    <div class="callout">
        <div class="callout-header">💡 왜 6개나 되는 dataclass가 필요한가?</div>
        <p class="body-text" style="margin-bottom:0;">전부 dict로 처리해도 동작은 한다. 하지만 dataclass를 쓰면: (1) 어떤 필드가 있는지 코드만 보고 알 수 있다, (2) 오타를 IDE가 잡아준다 (<code>event["evnet_time"]</code> 같은 실수), (3) 타입 힌트로 int/str/bool을 구분할 수 있다. 코드가 길어질수록 이 장점이 커진다.</p>
    </div>

    <!-- ============================================================ -->
    <!-- FILE 3: collector.py -->
    <!-- ============================================================ -->
    <h2 class="section-header">파일 3/12 — collector.py</h2>
    <p class="body-text">시스템의 "귀". 바이낸스 WebSocket에 연결하여 초당 수백 건의 메시지를 수신하고, 유형별로 분류하여 적절한 모듈로 전달한다. 가장 긴 파일(~180줄)이자 가장 중요한 파일이다.</p>

    <div class="file-header"><span class="file-path">src/collector.py</span><span class="file-lines">~180 lines</span></div>
    <div class="code-block"><span class="code-str">"""WebSocket 데이터 수집 모듈"""</span>

<span class="code-kw">from</span> __future__ <span class="code-kw">import</span> annotations
<span class="code-kw">import</span> asyncio, json, logging, time
<span class="code-kw">from</span> dataclasses <span class="code-kw">import</span> asdict
<span class="code-kw">from</span> typing <span class="code-kw">import</span> TYPE_CHECKING
<span class="code-kw">import</span> websockets
<span class="code-kw">from</span> src.models <span class="code-kw">import</span> DepthDiffEvent, AggTradeEvent, LiquidationEvent, KlineEvent

<span class="code-kw">if</span> TYPE_CHECKING:
    <span class="code-kw">from</span> src.buffer <span class="code-kw">import</span> DataBuffer
    <span class="code-kw">from</span> src.config <span class="code-kw">import</span> Config
    <span class="code-cm">... (나머지 타입 임포트)</span></div>

    <div class="line-review">
        <span class="line-num">from __future__ import annotations</span><br>
        파이썬 3.10 미만에서도 <code>str | None</code> 같은 새로운 타입 힌트 문법을 쓸 수 있게 해준다. 이 줄이 없으면 <code>Optional[str]</code>로 써야 한다. 파이썬 3.14에서는 사실 필요 없지만, 하위 호환성을 위해 넣어둔 것.
    </div>

    <div class="line-review">
        <span class="line-num">if TYPE_CHECKING:</span><br>
        이 블록 안의 import는 실행 시에는 무시되고, IDE의 타입 체크 시에만 사용된다. 왜 이렇게 할까? 순환 참조(circular import) 방지. collector.py가 buffer.py를 import하고, buffer.py가 collector.py를 import하면 에러가 난다. <code>TYPE_CHECKING</code> 안에 넣으면 실행 시에는 import하지 않으므로 순환이 깨진다.
    </div>

    <div class="code-block"><span class="code-kw">class</span> <span class="code-cls">Collector</span>:
    SPOT_WS = <span class="code-str">"wss://stream.binance.com:9443/stream"</span>
    FUTURES_WS = <span class="code-str">"wss://fstream.binance.com/stream"</span>

    <span class="code-kw">def</span> <span class="code-fn">__init__</span>(self, config, orderbook_manager, buffer,
                 integrity_logger=<span class="code-kw">None</span>, telegram=<span class="code-kw">None</span>):
        self.config = config
        self.ob_manager = orderbook_manager
        self.buffer = buffer
        self.integrity_logger = integrity_logger
        self.telegram = telegram
        self.reconnect_delay = <span class="code-num">1.0</span>
        self._disconnect_time = <span class="code-kw">None</span></div>

    <div class="line-review">
        <span class="line-num">SPOT_WS / FUTURES_WS</span> — 클래스 변수로 WebSocket URL을 정의. 스팟(현물)과 선물(futures)은 서로 다른 서버를 사용한다. <code>wss://</code>는 WebSocket Secure(암호화된 WebSocket).<br><br>
        <span class="line-num">__init__</span> — 의존성 주입 패턴. Collector는 자기가 필요한 모듈(config, ob_manager, buffer 등)을 직접 만들지 않고, 외부에서 받는다. 이렇게 하면 테스트할 때 가짜(mock) 객체를 넣을 수 있다.<br><br>
        <span class="line-num">integrity_logger=None, telegram=None</span> — 선택적 의존성. 없어도 동작한다. 텔레그램을 설정하지 않아도 수집은 된다.<br><br>
        <span class="line-num">reconnect_delay = 1.0</span> — 지수 백오프의 현재 대기 시간. 1초에서 시작해서 실패할 때마다 2배씩 늘어난다.<br><br>
        <span class="line-num">_disconnect_time = None</span> — 연결이 끊긴 시각. 재연결 성공 시 끊김 지속 시간을 계산하는 데 사용.
    </div>

    <div class="subsection">WebSocket URL 생성</div>

    <div class="code-block">    <span class="code-kw">def</span> <span class="code-fn">build_ws_url</span>(self) -> str:
        streams = []
        <span class="code-kw">for</span> s <span class="code-kw">in</span> self.config.symbols:
            streams.append(f<span class="code-str">"{s}@depth@100ms"</span>)
            streams.append(f<span class="code-str">"{s}@aggTrade"</span>)
            streams.append(f<span class="code-str">"{s}@kline_1m"</span>)
        <span class="code-kw">return</span> f<span class="code-str">"{self.SPOT_WS}?streams={'<span class="code-fn">/</span>'.join(streams)}"</span></div>

    <div class="line-review">
        바이낸스의 "combined stream" 기능을 사용한다. 하나의 WebSocket 연결로 여러 스트림을 동시에 수신할 수 있다. 6개 심볼 × 3개 스트림 = 18개 스트림이 하나의 URL에 들어간다.<br><br>
        결과 URL 예시:<br>
        <code>wss://stream.binance.com:9443/stream?streams=btcusdt@depth@100ms/btcusdt@aggTrade/btcusdt@kline_1m/ethusdt@depth@100ms/...</code><br><br>
        <code>@depth@100ms</code>는 "오더북 diff를 100밀리초마다 보내줘"라는 뜻. <code>@aggTrade</code>는 "집계 체결을 실시간으로", <code>@kline_1m</code>은 "1분봉 캔들을".
    </div>

    <div class="subsection">메인 수집 루프</div>

    <div class="code-block">    <span class="code-kw">async def</span> <span class="code-fn">run</span>(self) -> <span class="code-kw">None</span>:
        tasks = [self._run_spot()]
        <span class="code-kw">if</span> self.config.use_futures:
            tasks.append(self._run_futures())
        <span class="code-kw">await</span> asyncio.gather(*tasks)

    <span class="code-kw">async def</span> <span class="code-fn">_run_spot</span>(self) -> <span class="code-kw">None</span>:
        <span class="code-kw">while</span> <span class="code-kw">True</span>:
            <span class="code-kw">try</span>:
                <span class="code-kw">await</span> self._connect_and_collect()
            <span class="code-kw">except</span> Exception <span class="code-kw">as</span> e:
                self._disconnect_time = self._disconnect_time <span class="code-kw">or</span> time.time()
                <span class="code-kw">if</span> self.telegram:
                    <span class="code-kw">await</span> self.telegram.send_disconnect_alert(str(e))
                <span class="code-kw">if</span> self.integrity_logger:
                    self.integrity_logger.record_reconnect(time.time(), str(e))
                <span class="code-kw">await</span> asyncio.sleep(self.reconnect_delay)
                self.reconnect_delay = min(self.reconnect_delay * <span class="code-num">2</span>, <span class="code-num">60.0</span>)</div>

    <div class="line-review">
        <span class="line-num">run()</span> — 스팟과 선물 WebSocket을 동시에 실행. <code>use_futures</code>가 False면 스팟만.<br><br>
        <span class="line-num">_run_spot()</span> — <code>while True</code>로 영원히 반복. 연결이 끊기면 except로 잡아서 재연결한다. 프로그램이 종료될 때까지 이 루프는 절대 끝나지 않는다.<br><br>
        <span class="line-num">self._disconnect_time = self._disconnect_time or time.time()</span> — 이미 끊김 시각이 기록되어 있으면 덮어쓰지 않는다. 첫 번째 끊김 시각만 기록하고, 이후 재시도 실패에서는 유지. 재연결 성공 시 이 값으로 총 끊김 시간을 계산한다.<br><br>
        <span class="line-num">self.reconnect_delay = min(self.reconnect_delay * 2, 60.0)</span> — 지수 백오프. 1→2→4→8→16→32→60(상한). 서버가 과부하일 때 수천 클라이언트가 동시에 재연결하면 서버가 더 죽는다. 대기 시간을 늘려서 부하를 분산한다.
    </div>

    <div class="subsection">연결 및 수신</div>

    <div class="code-block">    <span class="code-kw">async def</span> <span class="code-fn">_connect_and_collect</span>(self) -> <span class="code-kw">None</span>:
        url = self.build_ws_url()
        <span class="code-kw">async with</span> websockets.connect(url, ping_interval=<span class="code-num">20</span>) <span class="code-kw">as</span> ws:
            <span class="code-cm"># 재연결 성공 처리</span>
            <span class="code-kw">if</span> self._disconnect_time:
                downtime = time.time() - self._disconnect_time
                <span class="code-kw">if</span> self.telegram:
                    <span class="code-kw">await</span> self.telegram.send_reconnect_alert(downtime)
                self._disconnect_time = <span class="code-kw">None</span>

            self._reset_reconnect_delay()

            <span class="code-cm"># 오더북 스냅샷 재초기화</span>
            <span class="code-kw">for</span> sym <span class="code-kw">in</span> self.config.symbols:
                <span class="code-kw">await</span> self.ob_manager.initialize(sym, self.config.orderbook_depth)

            <span class="code-kw">async for</span> raw_msg <span class="code-kw">in</span> ws:
                <span class="code-kw">await</span> self._handle_message(raw_msg)</div>

    <div class="line-review">
        <span class="line-num">websockets.connect(url, ping_interval=20)</span> — WebSocket 연결. <code>ping_interval=20</code>은 20초마다 ping 프레임을 보내서 연결이 살아있는지 확인한다. 바이낸스는 응답이 없으면 연결을 끊으므로 이 설정이 필수.<br><br>
        <span class="line-num">async with ... as ws</span> — 컨텍스트 매니저. 블록을 벗어나면 자동으로 연결을 닫는다. 예외가 발생해도 연결이 깔끔하게 정리된다.<br><br>
        <span class="line-num">재연결 성공 처리</span> — <code>_disconnect_time</code>이 있으면 이전에 끊긴 적이 있다는 뜻. 끊김 지속 시간을 계산해서 텔레그램으로 알린다. 그리고 None으로 리셋.<br><br>
        <span class="line-num">오더북 스냅샷 재초기화</span> — 연결이 끊긴 동안 놓친 diff가 있으므로, 모든 심볼의 오더북을 REST API로 다시 받아온다. 깨끗한 상태에서 다시 시작.<br><br>
        <span class="line-num">async for raw_msg in ws</span> — WebSocket에서 메시지가 올 때마다 반복. 메시지가 없으면 여기서 대기(await)하고, 그동안 다른 코루틴이 실행된다. 연결이 끊기면 이 루프가 예외를 발생시키고, <code>_run_spot</code>의 except로 잡힌다.
    </div>

    <div class="subsection">메시지 라우팅 — _handle_message</div>

    <div class="code-block">    <span class="code-kw">async def</span> <span class="code-fn">_handle_message</span>(self, raw_msg: str) -> <span class="code-kw">None</span>:
        recv_time = time.time()  <span class="code-cm"># ← 가장 먼저!</span>
        data = json.loads(raw_msg)
        stream = data.get(<span class="code-str">"stream"</span>, <span class="code-str">""</span>)
        payload = data.get(<span class="code-str">"data"</span>, {})

        <span class="code-kw">if</span> <span class="code-str">"depth"</span> <span class="code-kw">in</span> stream:
            event = DepthDiffEvent(
                symbol=stream.split(<span class="code-str">"@"</span>)[<span class="code-num">0</span>].upper(),
                event_time=payload.get(<span class="code-str">"E"</span>, <span class="code-num">0</span>),
                recv_time=recv_time,
                first_update_id=payload.get(<span class="code-str">"U"</span>, <span class="code-num">0</span>),
                final_update_id=payload.get(<span class="code-str">"u"</span>, <span class="code-num">0</span>),
                bids=payload.get(<span class="code-str">"b"</span>, []),
                asks=payload.get(<span class="code-str">"a"</span>, []),
            )
            snapshot = self.ob_manager.apply_diff(event.symbol, event)
            <span class="code-kw">if</span> snapshot:
                <span class="code-kw">await</span> self.buffer.add_orderbook(event.symbol, asdict(snapshot))
            <span class="code-kw">else</span>:
                <span class="code-cm"># 갭 감지 → 자동 재초기화</span>
                state = self.ob_manager.books.get(event.symbol)
                <span class="code-kw">if</span> state <span class="code-kw">and not</span> state.initialized:
                    <span class="code-kw">try</span>:
                        <span class="code-kw">await</span> self.ob_manager.initialize(event.symbol, self.config.orderbook_depth)
                    <span class="code-kw">except</span> Exception <span class="code-kw">as</span> e:
                        logger.error(f<span class="code-str">"[재초기화 실패] {event.symbol}: {e}"</span>)

        <span class="code-kw">elif</span> <span class="code-str">"aggTrade"</span> <span class="code-kw">in</span> stream:
            event = AggTradeEvent(...)
            <span class="code-kw">await</span> self.buffer.add_trade(event.symbol, asdict(event))

        <span class="code-kw">elif</span> <span class="code-str">"forceOrder"</span> <span class="code-kw">in</span> stream:
            event = LiquidationEvent(...)
            <span class="code-kw">await</span> self.buffer.add_liquidation(event.symbol, asdict(event))

        <span class="code-kw">elif</span> <span class="code-str">"kline"</span> <span class="code-kw">in</span> stream:
            k = payload.get(<span class="code-str">"k"</span>, {})
            <span class="code-kw">if</span> k.get(<span class="code-str">"x"</span>, <span class="code-kw">False</span>):  <span class="code-cm"># 확정된 캔들만</span>
                event = KlineEvent(...)
                <span class="code-kw">await</span> self.buffer.add_kline(event.symbol, asdict(event))</div>

    <div class="line-review">
        <span class="line-num">recv_time = time.time()</span> — 이 줄이 함수의 맨 첫 줄인 이유: JSON 파싱, 객체 생성, 오더북 diff 적용 등의 처리 시간이 수신 시각에 포함되면 레이턴시 측정이 부정확해진다. 마이크로초 단위의 정확성이 중요한 학술 데이터에서 이 차이가 의미를 가진다.<br><br>
        <span class="line-num">stream.split("@")[0].upper()</span> — <code>"btcusdt@depth@100ms"</code>에서 <code>"btcusdt"</code>를 추출하고 대문자로 변환. 바이낸스는 스트림 이름을 소문자로 보내지만, 심볼은 대문자가 표준이다.<br><br>
        <span class="line-num">payload.get("E", 0)</span> — 바이낸스 API의 필드명은 한 글자 약어다. E=Event time, U=First update ID, u=final update ID, b=bids, a=asks. <code>.get(key, default)</code>를 써서 필드가 없을 때 에러 대신 기본값을 반환한다.<br><br>
        <span class="line-num">asdict(snapshot)</span> — dataclass 객체를 딕셔너리로 변환. Buffer는 dict를 받으므로 변환이 필요하다.<br><br>
        <span class="line-num">갭 감지 → 자동 재초기화</span> — <code>apply_diff</code>가 None을 반환하면 두 가지 경우다: (1) 이미 처리된 오래된 diff, (2) 시퀀스 갭. <code>state.initialized</code>가 False면 갭이 발생한 것이므로 REST 스냅샷을 다시 요청한다.<br><br>
        <span class="line-num">k.get("x", False)</span> — kline 메시지의 <code>x</code> 필드는 "이 캔들이 확정되었는가?"를 나타낸다. 1분봉이 아직 진행 중이면 x=False이고, 1분이 지나서 확정되면 x=True. 확정된 캔들만 저장해야 데이터가 중복되지 않는다.
    </div>

    <!-- ============================================================ -->
    <!-- FILE 4: orderbook_manager.py -->
    <!-- ============================================================ -->
    <h2 class="section-header">파일 4/12 — orderbook_manager.py</h2>
    <p class="body-text">시스템에서 가장 까다로운 로직. 바이낸스 공식 가이드라인을 코드로 구현한 것이다. 오더북의 정확성이 이 파일에 달려있다.</p>

    <div class="file-header"><span class="file-path">src/orderbook_manager.py</span><span class="file-lines">~130 lines</span></div>
    <div class="code-block"><span class="code-kw">class</span> <span class="code-cls">OrderBookManager</span>:
    BASE_URL = <span class="code-str">"https://api.binance.com"</span>

    <span class="code-kw">def</span> <span class="code-fn">__init__</span>(self, symbols, integrity_logger=<span class="code-kw">None</span>):
        self.symbols = symbols
        self.integrity_logger = integrity_logger
        self.books = {s.upper(): OrderBookState() <span class="code-kw">for</span> s <span class="code-kw">in</span> symbols}</div>

    <div class="line-review">
        <span class="line-num">self.books</span> — 심볼별 오더북 상태를 딕셔너리로 관리. <code>{"BTCUSDT": OrderBookState(), "ETHUSDT": OrderBookState(), ...}</code>. 각 심볼이 독립적인 오더북을 가진다.
    </div>

    <div class="code-block">    <span class="code-kw">async def</span> <span class="code-fn">initialize</span>(self, symbol, depth=<span class="code-num">1000</span>):
        sym = symbol.upper()
        url = f<span class="code-str">"{self.BASE_URL}/api/v3/depth?symbol={sym}&limit={depth}"</span>

        <span class="code-kw">async with</span> aiohttp.ClientSession() <span class="code-kw">as</span> session:
            <span class="code-kw">async with</span> session.get(url) <span class="code-kw">as</span> resp:
                data = <span class="code-kw">await</span> resp.json()

        state = OrderBookState(
            bids={p: q <span class="code-kw">for</span> p, q <span class="code-kw">in</span> data.get(<span class="code-str">"bids"</span>, [])},
            asks={p: q <span class="code-kw">for</span> p, q <span class="code-kw">in</span> data.get(<span class="code-str">"asks"</span>, [])},
            last_update_id=data.get(<span class="code-str">"lastUpdateId"</span>, <span class="code-num">0</span>),
            initialized=<span class="code-kw">True</span>,
            init_time=time.time(),
        )
        self.books[sym] = state</div>

    <div class="line-review">
        <span class="line-num">/api/v3/depth?limit=1000</span> — 바이낸스 REST API로 현재 오더북 스냅샷을 요청. limit=1000은 매수/매도 각 1000호가를 가져온다는 뜻. 이게 오더북 재구성의 "시작점"이다.<br><br>
        <span class="line-num">bids={p: q for p, q in ...}</span> — REST API는 <code>[["68347.87", "1.234"], ["68346.00", "0.567"]]</code> 형태의 리스트를 반환한다. 이걸 <code>{"68347.87": "1.234", "68346.00": "0.567"}</code> 형태의 딕셔너리로 변환한다. 이유: 나중에 diff를 적용할 때 특정 가격을 O(1)로 찾기 위해.<br><br>
        <span class="line-num">init_time=time.time()</span> — 초기화 시각 기록. 이후 3초간은 시퀀스 검증 실패를 허용한다(grace period). REST 요청과 WebSocket diff 사이의 타이밍 이슈를 흡수하기 위함.
    </div>

    <div class="code-block">    <span class="code-kw">def</span> <span class="code-fn">validate_sequence</span>(self, symbol, first_update_id, final_update_id):
        state = self.books.get(symbol.upper())
        <span class="code-kw">if not</span> state <span class="code-kw">or not</span> state.initialized:
            <span class="code-kw">return False</span>
        expected = state.last_update_id + <span class="code-num">1</span>
        <span class="code-kw">return</span> first_update_id &lt;= expected &lt;= final_update_id</div>

    <div class="line-review">
        <span class="line-num">바이낸스 공식 규칙</span>: 새 diff의 <code>first_update_id(F)</code>와 <code>final_update_id(L)</code> 사이에 <code>lastUpdateId + 1</code>이 포함되어야 한다.<br><br>
        예시: lastUpdateId=100, 새 diff F=99, L=103 → expected=101 → 99 ≤ 101 ≤ 103 ✅<br>
        예시: lastUpdateId=100, 새 diff F=105, L=110 → expected=101 → 105 ≤ 101? ❌ → 갭!<br><br>
        이 검증이 실패하면 중간에 diff를 놓친 것이므로, 오더북이 더 이상 정확하지 않다.
    </div>

    <div class="code-block">    <span class="code-kw">def</span> <span class="code-fn">apply_diff</span>(self, symbol, event):
        state = self.books.get(symbol.upper())
        <span class="code-kw">if not</span> state <span class="code-kw">or not</span> state.initialized:
            <span class="code-kw">return None</span>

        expected = state.last_update_id + <span class="code-num">1</span>

        <span class="code-cm"># 이미 처리된 오래된 diff → 무시</span>
        <span class="code-kw">if</span> event.final_update_id &lt; expected:
            <span class="code-kw">return None</span>

        <span class="code-cm"># 시퀀스 검증</span>
        <span class="code-kw">if not</span> self.validate_sequence(symbol, event.first_update_id, event.final_update_id):
            <span class="code-cm"># 3초 grace period</span>
            <span class="code-kw">if</span> time.time() - state.init_time &lt; <span class="code-num">3.0</span>:
                <span class="code-kw">return None</span>
            <span class="code-cm"># 진짜 갭</span>
            <span class="code-kw">if</span> self.integrity_logger:
                self.integrity_logger.record_gap(symbol, expected, event.first_update_id)
            state.initialized = <span class="code-kw">False</span>
            <span class="code-kw">return None</span>

        <span class="code-cm"># diff 적용</span>
        self._apply_updates(state.bids, event.bids)
        self._apply_updates(state.asks, event.asks)
        state.last_update_id = event.final_update_id

        <span class="code-kw">return</span> self.get_top_levels(symbol, event_time=event.event_time, recv_time=event.recv_time)</div>

    <div class="line-review">
        <span class="line-num">event.final_update_id &lt; expected</span> — 이미 처리된 오래된 diff. 스냅샷 이전에 도착한 diff가 아직 WebSocket 버퍼에 남아있을 수 있다. 이건 갭이 아니라 그냥 무시하면 된다.<br><br>
        <span class="line-num">3초 grace period</span> — REST 스냅샷을 요청하는 동안에도 WebSocket diff는 계속 도착한다. 스냅샷 응답이 오기 전에 이미 몇 개의 diff가 도착해서 버려진 상태일 수 있다. 이때 다음 diff가 시퀀스 검증에 실패할 수 있는데, 3초 안이면 이런 타이밍 이슈로 간주하고 조용히 무시한다.<br><br>
        <span class="line-num">state.initialized = False</span> — 이 한 줄이 "자동 재초기화 트리거"다. Collector의 <code>_handle_message</code>에서 이 값을 확인하고, False면 REST 스냅샷을 다시 요청한다.<br><br>
        <span class="line-num">return self.get_top_levels(...)</span> — diff 적용 성공 시 상위 20호가 스냅샷을 반환. 이 스냅샷이 Buffer에 저장된다.
    </div>

    <div class="code-block">    <span class="code-dec">@staticmethod</span>
    <span class="code-kw">def</span> <span class="code-fn">_apply_updates</span>(book_side, updates):
        <span class="code-kw">for</span> price, qty <span class="code-kw">in</span> updates:
            <span class="code-kw">if</span> qty == <span class="code-str">"0"</span> <span class="code-kw">or</span> qty == <span class="code-str">"0.00000000"</span>:
                book_side.pop(price, <span class="code-kw">None</span>)
            <span class="code-kw">else</span>:
                book_side[price] = qty

    <span class="code-kw">def</span> <span class="code-fn">get_top_levels</span>(self, symbol, levels=<span class="code-num">20</span>, event_time=<span class="code-num">0</span>, recv_time=<span class="code-num">0.0</span>):
        state = self.books[symbol.upper()]
        sorted_bids = sorted(state.bids.items(), key=<span class="code-kw">lambda</span> x: float(x[<span class="code-num">0</span>]), reverse=<span class="code-kw">True</span>)[:<span class="code-num">levels</span>]
        sorted_asks = sorted(state.asks.items(), key=<span class="code-kw">lambda</span> x: float(x[<span class="code-num">0</span>]))[:<span class="code-num">levels</span>]
        <span class="code-kw">return</span> OrderBookSnapshot(
            symbol=symbol.upper(), event_time=event_time, recv_time=recv_time,
            last_update_id=state.last_update_id,
            bids=[[p, q] <span class="code-kw">for</span> p, q <span class="code-kw">in</span> sorted_bids],
            asks=[[p, q] <span class="code-kw">for</span> p, q <span class="code-kw">in</span> sorted_asks],
        )</div>

    <div class="line-review">
        <span class="line-num">_apply_updates</span> — 바이낸스의 규칙: 수량이 "0"이면 해당 가격대를 삭제, 아니면 갱신(또는 신규 추가). <code>book_side.pop(price, None)</code>은 해당 키가 없어도 에러를 내지 않는다. <code>@staticmethod</code>인 이유: self를 사용하지 않으므로 인스턴스 없이도 호출 가능. 테스트하기도 쉽다.<br><br>
        <span class="line-num">qty == "0" or qty == "0.00000000"</span> — 바이낸스가 "0"을 보내는 형식이 두 가지다. 둘 다 처리해야 한다.<br><br>
        <span class="line-num">get_top_levels</span> — dict에 저장된 전체 오더북(최대 1000호가)에서 상위 20호가만 추출. bids는 가격 내림차순(비싼 것부터), asks는 오름차순(싼 것부터). <code>float(x[0])</code>으로 문자열 가격을 숫자로 변환해서 정렬한다. <code>[:levels]</code>로 상위 N개만 자른다.
    </div>

    <!-- ============================================================ -->
    <!-- FILE 5: buffer.py -->
    <!-- ============================================================ -->
    <h2 class="section-header">파일 5/12 — buffer.py</h2>
    <p class="body-text">수집된 데이터가 디스크에 저장되기 전까지 머무는 "대기실". 여러 코루틴이 동시에 접근하므로 Lock으로 보호한다.</p>

    <div class="file-header"><span class="file-path">src/buffer.py</span><span class="file-lines">~75 lines</span></div>
    <div class="code-block"><span class="code-kw">from</span> collections <span class="code-kw">import</span> defaultdict

<span class="code-kw">class</span> <span class="code-cls">DataBuffer</span>:
    <span class="code-kw">def</span> <span class="code-fn">__init__</span>(self, max_memory_mb=<span class="code-num">500</span>):
        self.max_memory_bytes = max_memory_mb * <span class="code-num">1024</span> * <span class="code-num">1024</span>
        self._orderbook_data = defaultdict(list)  <span class="code-cm"># {"BTCUSDT": [...], "ETHUSDT": [...]}</span>
        self._trade_data = defaultdict(list)
        self._liquidation_data = defaultdict(list)
        self._kline_data = defaultdict(list)
        self._funding_data = []                   <span class="code-cm"># 펀딩비는 심볼 통합</span>
        self._lock = asyncio.Lock()</div>

    <div class="line-review">
        <span class="line-num">defaultdict(list)</span> — 일반 dict에서 없는 키에 접근하면 KeyError가 난다. defaultdict(list)는 없는 키에 접근하면 자동으로 빈 리스트를 만들어준다. <code>self._orderbook_data["BTCUSDT"].append(record)</code>를 할 때, "BTCUSDT" 키가 없어도 에러 없이 동작한다.<br><br>
        <span class="line-num">max_memory_mb * 1024 * 1024</span> — MB를 바이트로 변환. 500MB = 500 × 1024 × 1024 = 524,288,000 바이트.<br><br>
        <span class="line-num">asyncio.Lock()</span> — 여러 코루틴이 동시에 리스트에 append하면 데이터가 꼬일 수 있다. Lock은 "한 번에 하나의 코루틴만 접근 가능"하게 한다. 멀티스레딩의 threading.Lock과 비슷하지만, asyncio 전용이라 await와 함께 쓴다.<br><br>
        <span class="line-num">_funding_data = []</span> — 펀딩비는 심볼별이 아닌 통합 리스트. 8시간마다 한 번 들어오므로 양이 적어서 분리할 필요가 없다.
    </div>

    <div class="code-block">    <span class="code-kw">async def</span> <span class="code-fn">add_orderbook</span>(self, symbol, record):
        <span class="code-kw">async with</span> self._lock:
            self._orderbook_data[symbol].append(record)

    <span class="code-kw">async def</span> <span class="code-fn">flush</span>(self):
        <span class="code-kw">async with</span> self._lock:
            result = {
                <span class="code-str">"orderbook"</span>: dict(self._orderbook_data),
                <span class="code-str">"trade"</span>: dict(self._trade_data),
                <span class="code-str">"liquidation"</span>: dict(self._liquidation_data),
                <span class="code-str">"kline"</span>: dict(self._kline_data),
                <span class="code-str">"funding"</span>: list(self._funding_data),
            }
            self._orderbook_data = defaultdict(list)
            self._trade_data = defaultdict(list)
            self._liquidation_data = defaultdict(list)
            self._kline_data = defaultdict(list)
            self._funding_data = []
            <span class="code-kw">return</span> result</div>

    <div class="line-review">
        <span class="line-num">async with self._lock</span> — Lock을 획득한다. 다른 코루틴이 이미 Lock을 잡고 있으면 여기서 대기(await)한다. 블록이 끝나면 자동으로 Lock을 해제한다.<br><br>
        <span class="line-num">flush()의 원자성</span> — Lock 안에서 (1) 현재 데이터를 복사하고 (2) 버퍼를 비우는 두 작업을 한 번에 수행한다. 이 두 작업 사이에 새 데이터가 들어오면 유실될 수 있으므로, Lock으로 묶어서 원자적으로 만든다.<br><br>
        <span class="line-num">dict(self._orderbook_data)</span> — defaultdict를 일반 dict로 변환. 이건 "얕은 복사(shallow copy)"다. 새 defaultdict로 교체해도 기존 리스트 객체는 result에 안전하게 남아있다. 깊은 복사(deep copy)를 하면 안전하지만 느리다. 여기서는 교체 후 기존 객체를 더 이상 수정하지 않으므로 얕은 복사로 충분하다.
    </div>

    <div class="code-block">    <span class="code-kw">def</span> <span class="code-fn">estimate_memory_usage</span>(self):
        total = <span class="code-num">0</span>
        <span class="code-kw">for</span> store <span class="code-kw">in</span> [self._orderbook_data, self._trade_data,
                      self._liquidation_data, self._kline_data]:
            <span class="code-kw">for</span> records <span class="code-kw">in</span> store.values():
                total += sys.getsizeof(records)
                <span class="code-kw">for</span> r <span class="code-kw">in</span> records:
                    total += sys.getsizeof(r)
        <span class="code-kw">return</span> total

    <span class="code-kw">def</span> <span class="code-fn">needs_force_flush</span>(self):
        <span class="code-kw">return</span> self.estimate_memory_usage() >= self.max_memory_bytes</div>

    <div class="line-review">
        <span class="line-num">sys.getsizeof</span> — 파이썬 객체의 메모리 크기를 바이트로 반환한다. 정확한 값은 아니고 추정치다 — 중첩된 객체의 크기는 포함하지 않으므로 실제보다 작게 나온다. 하지만 "500MB를 넘었는지" 판단하는 용도로는 충분하다.<br><br>
        <span class="line-num">needs_force_flush</span> — 이 메서드를 main.py에서 30초마다 호출한다. True를 반환하면 즉시 flush를 실행한다. 이게 OOM(Out of Memory) 방지 안전장치다.
    </div>

    <!-- ============================================================ -->
    <!-- FILE 6: flusher.py -->
    <!-- ============================================================ -->
    <h2 class="section-header">파일 6/12 — flusher.py</h2>
    <p class="body-text">메모리의 데이터를 디스크에 영구 저장하는 모듈. 원자적 쓰기, 체크섬 기록, Syncer 콜백까지 수행한다.</p>

    <div class="file-header"><span class="file-path">src/flusher.py</span><span class="file-lines">~150 lines</span></div>
    <div class="code-block"><span class="code-kw">class</span> <span class="code-cls">Flusher</span>:
    <span class="code-kw">def</span> <span class="code-fn">__init__</span>(self, config, buffer, integrity_logger=<span class="code-kw">None</span>,
                 on_file_created=<span class="code-kw">None</span>):
        self.config = config
        self.buffer = buffer
        self.integrity_logger = integrity_logger
        self.on_file_created = on_file_created  <span class="code-cm"># Syncer 연결용 콜백</span>
        self.data_dir = Path(config.data_dir)
        self.data_dir.mkdir(parents=<span class="code-kw">True</span>, exist_ok=<span class="code-kw">True</span>)</div>

    <div class="line-review">
        <span class="line-num">on_file_created</span> — 콜백 함수. main.py에서 <code>on_file_created=syncer.enqueue_file</code>로 전달된다. Flusher가 파일을 저장할 때마다 이 함수를 호출해서 Syncer에게 "새 파일 생겼어"라고 알린다. Flusher는 Syncer의 존재를 모른다 — 콜백 하나로 느슨하게 연결된 것.<br><br>
        <span class="line-num">mkdir(parents=True, exist_ok=True)</span> — 디렉토리가 없으면 생성. <code>parents=True</code>는 중간 디렉토리도 함께 생성 (<code>./data/sub/dir</code>에서 sub가 없어도 OK). <code>exist_ok=True</code>는 이미 존재해도 에러 안 냄.
    </div>

    <div class="code-block">    <span class="code-kw">async def</span> <span class="code-fn">run</span>(self):
        <span class="code-kw">while</span> <span class="code-kw">True</span>:
            <span class="code-kw">await</span> asyncio.sleep(self.config.flush_interval)  <span class="code-cm"># 3600초 대기</span>
            <span class="code-kw">try</span>:
                <span class="code-kw">await</span> self.flush_now()
            <span class="code-kw">except</span> Exception <span class="code-kw">as</span> e:
                logger.error(f<span class="code-str">"[플러시 에러] {e}"</span>)</div>

    <div class="line-review">
        <span class="line-num">await asyncio.sleep(3600)</span> — 1시간 동안 이 코루틴은 "잠든다". 그동안 다른 코루틴(Collector, TimeSyncMonitor 등)이 실행된다. 이게 asyncio의 핵심 — 기다리는 시간을 낭비하지 않는다.<br><br>
        <span class="line-num">try/except</span> — 플러시 중 에러가 나도 프로그램이 죽지 않는다. 로그만 남기고 다음 주기에 다시 시도한다. 데이터는 Buffer에 그대로 남아있으므로 다음 플러시에서 저장된다.
    </div>

    <div class="code-block">    <span class="code-kw">async def</span> <span class="code-fn">flush_now</span>(self):
        data = <span class="code-kw">await</span> self.buffer.flush()
        now = datetime.now(timezone.utc)
        created_files = []

        <span class="code-kw">for</span> datatype <span class="code-kw">in</span> [<span class="code-str">"orderbook"</span>, <span class="code-str">"trade"</span>, <span class="code-str">"liquidation"</span>, <span class="code-str">"kline"</span>]:
            symbol_data = data.get(datatype, {})
            <span class="code-kw">for</span> symbol, records <span class="code-kw">in</span> symbol_data.items():
                <span class="code-kw">if not</span> records:
                    <span class="code-kw">continue</span>
                fname = self._generate_filename(symbol, datatype, now)
                fpath = self.data_dir / fname
                count = self._save_parquet(records, fpath)
                file_size = fpath.stat().st_size

                <span class="code-cm"># 체크섬 기록</span>
                sha256 = self.compute_checksum(fpath)
                self.record_checksum(fpath, sha256, count, file_size)

                <span class="code-cm"># IntegrityLogger 통보</span>
                <span class="code-kw">if</span> self.integrity_logger:
                    <span class="code-cm">... (시간 범위 계산 + record_flush 호출)</span>

                <span class="code-cm"># Syncer 콜백</span>
                <span class="code-kw">if</span> self.on_file_created:
                    self.on_file_created(fpath)

        <span class="code-kw">return</span> created_files</div>

    <div class="line-review">
        <span class="line-num">data = await self.buffer.flush()</span> — Buffer에서 모든 데이터를 가져오고 Buffer를 비운다. 이 시점부터 Buffer는 새 데이터를 받을 준비가 된다.<br><br>
        <span class="line-num">이중 for 루프</span> — 외부 루프는 데이터 유형(orderbook, trade, ...), 내부 루프는 심볼(BTCUSDT, ETHUSDT, ...). 각 조합마다 별도의 Parquet 파일을 생성한다. 예: BTCUSDT_orderbook_20260226_1100.parquet<br><br>
        <span class="line-num">if not records: continue</span> — 해당 심볼/유형에 데이터가 없으면 빈 파일을 만들지 않고 건너뛴다.<br><br>
        <span class="line-num">저장 후 3단계</span>: (1) SHA-256 체크섬 기록, (2) IntegrityLogger에 통계 전달, (3) Syncer에 새 파일 알림. 이 순서가 중요하다 — 파일이 완전히 저장된 후에만 체크섬을 계산하고 동기화를 시작한다.
    </div>

    <div class="code-block">    <span class="code-dec">@staticmethod</span>
    <span class="code-kw">def</span> <span class="code-fn">_save_parquet</span>(data, filepath):
        df = pd.DataFrame(data)
        tmp_fd, tmp_path = tempfile.mkstemp(suffix=<span class="code-str">".parquet.tmp"</span>, dir=filepath.parent)
        os.close(tmp_fd)
        <span class="code-kw">try</span>:
            df.to_parquet(tmp_path, index=<span class="code-kw">False</span>, compression=<span class="code-str">"snappy"</span>)
            os.replace(tmp_path, filepath)
        <span class="code-kw">except</span> Exception:
            <span class="code-kw">if</span> os.path.exists(tmp_path):
                os.unlink(tmp_path)
            <span class="code-kw">raise</span>
        <span class="code-kw">return</span> len(df)</div>

    <div class="line-review">
        <span class="line-num">tempfile.mkstemp</span> — 같은 디렉토리에 임시 파일을 생성한다. 같은 디렉토리여야 <code>os.replace</code>가 원자적으로 동작한다 (같은 파일시스템 내에서만 원자적 rename이 보장됨).<br><br>
        <span class="line-num">os.close(tmp_fd)</span> — mkstemp는 파일 디스크립터(fd)를 반환한다. pandas의 to_parquet는 파일 경로를 받으므로, fd는 닫아야 한다. 안 닫으면 파일 디스크립터 누수(leak)가 발생한다.<br><br>
        <span class="line-num">df.to_parquet(tmp_path, compression="snappy")</span> — 임시 파일에 Parquet 형식으로 저장. snappy 압축은 gzip보다 압축률은 낮지만 속도가 훨씬 빠르다. 실시간 시스템에서는 속도가 우선.<br><br>
        <span class="line-num">os.replace(tmp_path, filepath)</span> — 핵심! 임시 파일의 이름을 진짜 이름으로 바꾼다. 이 연산은 운영체제 수준에서 원자적이다 — 중간에 전원이 꺼져도 파일이 "없거나" "완전하거나" 둘 중 하나다. 반쪽짜리 파일은 절대 생기지 않는다.<br><br>
        <span class="line-num">except → os.unlink(tmp_path)</span> — 저장 실패 시 임시 파일을 삭제한다. 안 하면 .tmp 파일이 쌓인다. <code>raise</code>로 예외를 다시 던져서 상위에서 처리하게 한다.
    </div>

    <div class="code-block">    <span class="code-dec">@staticmethod</span>
    <span class="code-kw">def</span> <span class="code-fn">compute_checksum</span>(filepath):
        h = hashlib.sha256()
        <span class="code-kw">with</span> open(filepath, <span class="code-str">"rb"</span>) <span class="code-kw">as</span> f:
            <span class="code-kw">for</span> chunk <span class="code-kw">in</span> iter(<span class="code-kw">lambda</span>: f.read(<span class="code-num">8192</span>), b<span class="code-str">""</span>):
                h.update(chunk)
        <span class="code-kw">return</span> h.hexdigest()</div>

    <div class="line-review">
        <span class="line-num">iter(lambda: f.read(8192), b"")</span> — 파이썬의 2-인자 iter 패턴. "8192바이트씩 읽어서, 빈 바이트열(b"")이 나올 때까지 반복"이라는 뜻. 파일 전체를 메모리에 올리지 않고 8KB 청크 단위로 처리하므로, 수 GB 파일도 메모리 부담 없이 해시를 계산할 수 있다.<br><br>
        <span class="line-num">h.hexdigest()</span> — 64자리 16진수 문자열 반환. 예: <code>"a1b2c3d4e5f6..."</code>. 파일이 1비트라도 바뀌면 완전히 다른 문자열이 나온다.
    </div>

    <!-- ============================================================ -->
    <!-- FILE 7: syncer.py -->
    <!-- ============================================================ -->
    <h2 class="section-header">파일 7/12 — syncer.py</h2>
    <p class="body-text">클라우드 동기화와 로컬 파일 정리. rclone을 사용하여 Parquet 파일을 클라우드에 업로드하고, 오래된 파일을 안전하게 삭제한다.</p>

    <div class="file-header"><span class="file-path">src/syncer.py</span><span class="file-lines">~110 lines</span></div>
    <div class="code-block"><span class="code-kw">class</span> <span class="code-cls">Syncer</span>:
    <span class="code-kw">def</span> <span class="code-fn">__init__</span>(self, config, integrity_logger):
        self.config = config
        self.logger = integrity_logger
        self._pending_queue = []     <span class="code-cm"># 업로드 대기 파일 목록</span>
        self._synced_files = set()   <span class="code-cm"># 업로드 완료된 파일 경로</span>

    <span class="code-kw">def</span> <span class="code-fn">enqueue_file</span>(self, filepath):
        self._pending_queue.append(filepath)</div>

    <div class="line-review">
        <span class="line-num">_pending_queue = []</span> — 업로드할 파일들의 대기열. Flusher의 콜백(<code>on_file_created</code>)이 여기에 파일을 추가한다.<br><br>
        <span class="line-num">_synced_files = set()</span> — 업로드 완료된 파일 경로의 집합. set을 쓰는 이유: <code>"파일이 동기화됐는지"</code> 확인할 때 O(1)로 검색 가능. 리스트면 O(n).<br><br>
        <span class="line-num">enqueue_file</span> — Flusher가 호출하는 콜백. 단순히 리스트에 추가만 한다. 실제 업로드는 <code>run()</code>에서 수행.
    </div>

    <div class="code-block">    <span class="code-kw">async def</span> <span class="code-fn">sync_file</span>(self, filepath):
        cmd = [<span class="code-str">"rclone"</span>, <span class="code-str">"copy"</span>, str(filepath),
               f<span class="code-str">"{self.config.cloud_remote}:{self.config.cloud_path}"</span>]

        proc = <span class="code-kw">await</span> asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        stdout, stderr = <span class="code-kw">await</span> proc.communicate()

        <span class="code-kw">if</span> proc.returncode == <span class="code-num">0</span>:
            self._synced_files.add(str(filepath))
            self.logger.record_sync(str(filepath), <span class="code-str">"success"</span>)
            <span class="code-kw">return True</span>
        <span class="code-kw">else</span>:
            self._pending_queue.append(filepath)  <span class="code-cm"># 실패 → 재시도 대기열</span>
            self.logger.record_sync(str(filepath), <span class="code-str">"failed"</span>)
            <span class="code-kw">return False</span></div>

    <div class="line-review">
        <span class="line-num">asyncio.create_subprocess_exec</span> — rclone을 비동기 서브프로세스로 실행한다. <code>subprocess.run</code>과 달리 업로드 중에도 다른 코루틴이 실행된다. WebSocket 수신이 멈추지 않는다.<br><br>
        <span class="line-num">실패 시 재시도</span> — 업로드 실패한 파일을 다시 대기열에 넣는다. 다음 주기에 자동으로 재시도된다. 네트워크가 일시적으로 불안정해도 결국 업로드된다.
    </div>

    <div class="code-block">    <span class="code-kw">async def</span> <span class="code-fn">cleanup_old_files</span>(self):
        <span class="code-kw">for</span> filepath <span class="code-kw">in</span> data_dir.glob(<span class="code-str">"*.parquet"</span>):
            file_age = now - filepath.stat().st_mtime
            is_old_enough = file_age >= cutoff_seconds     <span class="code-cm"># 7일 경과?</span>
            is_synced = str(filepath) <span class="code-kw">in</span> self._synced_files  <span class="code-cm"># 백업 완료?</span>

            <span class="code-kw">if</span> is_old_enough <span class="code-kw">and</span> is_synced:
                filepath.unlink()</div>

    <div class="line-review">
        <span class="line-num">두 가지 조건 AND</span> — 파일 삭제는 (1) 7일 이상 경과 AND (2) 클라우드 백업 완료, 두 조건을 모두 만족해야만 수행된다. 하나라도 안 되면 삭제하지 않는다. 클라우드 백업 없이 로컬 파일을 삭제하면 데이터가 영원히 사라지므로, 이 안전장치가 핵심이다.<br><br>
        <span class="line-num">cloud_remote가 비어있으면?</span> — sync_file이 호출되지 않으므로 _synced_files에 아무것도 추가되지 않는다. 따라서 is_synced가 항상 False → 파일이 영원히 삭제되지 않는다. 의도된 동작이다.
    </div>

    <!-- ============================================================ -->
    <!-- FILE 8: integrity_logger.py -->
    <!-- ============================================================ -->
    <h2 class="section-header">파일 8/12 — integrity_logger.py</h2>
    <p class="body-text">데이터 품질의 "블랙박스". 갭, 재연결, 플러시 통계, 커버리지를 기록한다.</p>

    <div class="file-header"><span class="file-path">src/integrity_logger.py</span><span class="file-lines">~140 lines</span></div>
    <div class="code-block"><span class="code-kw">class</span> <span class="code-cls">IntegrityLogger</span>:
    MAX_GAP_BUFFER = <span class="code-num">10000</span>

    <span class="code-kw">def</span> <span class="code-fn">__init__</span>(self, log_dir):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=<span class="code-kw">True</span>, exist_ok=<span class="code-kw">True</span>)
        self._gaps = []
        self._reconnects = []
        self._flush_stats = []
        self._sync_events = []
        self._message_counts = defaultdict(int)

    <span class="code-kw">def</span> <span class="code-fn">record_gap</span>(self, symbol, expected_id, actual_id, timestamp):
        <span class="code-kw">if</span> len(self._gaps) >= self.MAX_GAP_BUFFER:
            self._gaps = self._gaps[-self.MAX_GAP_BUFFER // <span class="code-num">2</span>:]
        self._gaps.append({...})</div>

    <div class="line-review">
        <span class="line-num">MAX_GAP_BUFFER = 10000</span> — 갭 기록을 최대 10,000개까지만 보관한다. 네트워크가 심하게 불안정하면 갭이 수만 개 쌓일 수 있는데, 메모리를 무한히 쓰면 안 되므로 상한을 둔다.<br><br>
        <span class="line-num">self._gaps[-MAX_GAP_BUFFER // 2:]</span> — 상한에 도달하면 오래된 절반을 버린다. 전부 버리지 않고 절반만 버리는 이유: 최근 갭 정보는 유지하면서 메모리를 확보하기 위해.<br><br>
        <span class="line-num">defaultdict(int)</span> — 없는 키에 접근하면 0을 반환. <code>self._message_counts["BTCUSDT"] += 1</code>을 할 때 키가 없어도 에러 없이 0+1=1이 된다.
    </div>

    <div class="code-block">    <span class="code-dec">@staticmethod</span>
    <span class="code-kw">def</span> <span class="code-fn">compute_coverage</span>(total_seconds, gap_seconds):
        <span class="code-kw">if</span> total_seconds &lt;= <span class="code-num">0</span>:
            <span class="code-kw">return</span> <span class="code-num">0.0</span>
        gap_seconds = max(<span class="code-num">0.0</span>, min(gap_seconds, total_seconds))
        <span class="code-kw">return</span> (total_seconds - gap_seconds) / total_seconds</div>

    <div class="line-review">
        <span class="line-num">compute_coverage</span> — 데이터 커버리지 비율 계산. 24시간(86400초) 중 갭이 5초면 (86400-5)/86400 = 99.994%.<br><br>
        <span class="line-num">gap_seconds = max(0.0, min(gap_seconds, total_seconds))</span> — 방어적 프로그래밍. gap_seconds가 음수이거나 total_seconds보다 크면 결과가 이상해지므로, 0~total_seconds 범위로 클램핑한다. 이런 "있을 수 없는 입력"에 대한 방어가 프로덕션 코드의 특징이다.
    </div>

    <!-- ============================================================ -->
    <!-- FILE 9: telegram_reporter.py -->
    <!-- ============================================================ -->
    <h2 class="section-header">파일 9/12 — telegram_reporter.py</h2>
    <p class="body-text">텔레그램 봇을 통한 실시간 알림. 가장 중요한 설계 원칙: 알림 실패가 데이터 수집에 영향을 주지 않는다.</p>

    <div class="file-header"><span class="file-path">src/telegram_reporter.py</span><span class="file-lines">~120 lines</span></div>
    <div class="code-block"><span class="code-kw">class</span> <span class="code-cls">TelegramReporter</span>:
    <span class="code-kw">def</span> <span class="code-fn">__init__</span>(self, config):
        self.bot_token = config.telegram_bot_token
        self.chat_id = config.telegram_chat_id
        self.enabled = bool(self.bot_token <span class="code-kw">and</span> self.chat_id)

    <span class="code-kw">async def</span> <span class="code-fn">send_message</span>(self, text):
        <span class="code-kw">if not</span> self.enabled:
            <span class="code-kw">return</span>
        <span class="code-kw">try</span>:
            url = f<span class="code-str">"https://api.telegram.org/bot{self.bot_token}/sendMessage"</span>
            payload = {<span class="code-str">"chat_id"</span>: self.chat_id, <span class="code-str">"text"</span>: text, <span class="code-str">"parse_mode"</span>: <span class="code-str">"HTML"</span>}
            <span class="code-kw">async with</span> aiohttp.ClientSession() <span class="code-kw">as</span> session:
                <span class="code-kw">async with</span> session.post(url, json=payload,
                                         timeout=aiohttp.ClientTimeout(total=<span class="code-num">10</span>)) <span class="code-kw">as</span> resp:
                    <span class="code-kw">if</span> resp.status != <span class="code-num">200</span>:
                        logger.warning(f<span class="code-str">"텔레그램 전송 실패: {resp.status}"</span>)
        <span class="code-kw">except</span> Exception:
            logger.warning(<span class="code-str">"텔레그램 전송 중 예외"</span>, exc_info=<span class="code-kw">True</span>)
            <span class="code-cm"># ← 예외를 삼킨다! raise하지 않음</span></div>

    <div class="line-review">
        <span class="line-num">self.enabled = bool(self.bot_token and self.chat_id)</span> — 토큰과 채팅 ID가 둘 다 있어야 활성화. 하나라도 비어있으면 모든 메서드가 조용히 아무것도 안 한다.<br><br>
        <span class="line-num">if not self.enabled: return</span> — 비활성화 상태면 즉시 반환. HTTP 요청도 하지 않는다. 이 패턴이 모든 send_* 메서드에 반복된다.<br><br>
        <span class="line-num">timeout=aiohttp.ClientTimeout(total=10)</span> — 텔레그램 서버가 10초 안에 응답하지 않으면 포기한다. 텔레그램 서버가 느려서 수집이 멈추면 안 되니까.<br><br>
        <span class="line-num">except Exception: ... (raise 없음)</span> — 이게 핵심 설계. 모든 예외를 잡아서 로깅만 하고 넘어간다. 텔레그램 서버가 다운되어도, 네트워크가 끊겨도, 데이터 수집은 계속된다. 모니터링은 "있으면 좋고, 없어도 되는" 부가 기능이어야 한다.
    </div>

    <div class="code-block">    <span class="code-kw">async def</span> <span class="code-fn">send_startup_report</span>(self, config):
        symbols = <span class="code-str">", "</span>.join(s.upper() <span class="code-kw">for</span> s <span class="code-kw">in</span> config.symbols)
        text = (
            <span class="code-str">"🚀 &lt;b&gt;수집 시스템 시작&lt;/b&gt;\n"</span>
            f<span class="code-str">"심볼: {symbols}\n"</span>
            f<span class="code-str">"플러시 주기: {config.flush_interval}초\n"</span>
            f<span class="code-str">"시작 시각: {datetime.now(timezone.utc)...}"</span>
        )
        <span class="code-kw">await</span> self.send_message(text)</div>

    <div class="line-review">
        <span class="line-num">parse_mode="HTML"</span> — 텔레그램은 HTML 태그로 메시지를 꾸밀 수 있다. <code>&lt;b&gt;굵게&lt;/b&gt;</code> 같은 태그를 사용. Markdown도 지원하지만 HTML이 더 안정적이다.<br><br>
        나머지 send_* 메서드들(disconnect_alert, reconnect_alert, gap_alert, daily_report)도 같은 패턴이다: 메시지 텍스트를 만들고 send_message를 호출.
    </div>

    <!-- ============================================================ -->
    <!-- FILE 10: funding_rate_collector.py -->
    <!-- ============================================================ -->
    <h2 class="section-header">파일 10/13 — funding_rate_collector.py</h2>
    <p class="body-text">바이낸스 선물 시장의 펀딩비(Funding Rate)를 8시간 주기로 수집하는 모듈이다. 다른 모듈들이 WebSocket 실시간 스트림을 쓰는 것과 달리, 이 모듈은 REST API를 사용한다. 펀딩비는 8시간에 한 번만 바뀌므로 실시간 스트림이 필요 없기 때문이다.</p>

    <div class="file-header"><span class="file-path">src/funding_rate_collector.py</span><span class="file-lines">~70 lines</span></div>
    <div class="code-block"><span class="code-str">"""펀딩비 수집 모듈 - 8시간 주기 REST API 조회"""</span>

<span class="code-kw">from</span> __future__ <span class="code-kw">import</span> annotations

<span class="code-kw">import</span> asyncio
<span class="code-kw">import</span> logging
<span class="code-kw">import</span> time
<span class="code-kw">from</span> typing <span class="code-kw">import</span> TYPE_CHECKING

<span class="code-kw">import</span> aiohttp

<span class="code-kw">from</span> src.models <span class="code-kw">import</span> FundingRateRecord

<span class="code-kw">if</span> TYPE_CHECKING:
    <span class="code-kw">from</span> src.buffer <span class="code-kw">import</span> DataBuffer
    <span class="code-kw">from</span> src.config <span class="code-kw">import</span> Config
    <span class="code-kw">from</span> src.integrity_logger <span class="code-kw">import</span> IntegrityLogger

logger = logging.getLogger(__name__)

FUNDING_INTERVAL = <span class="code-num">8</span> * <span class="code-num">3600</span>  <span class="code-cm"># 8시간</span></div>

    <div class="line-review">
        <span class="line-num">from __future__ import annotations</span> — 타입 힌트를 문자열로 처리. 순환 임포트 방지의 핵심 패턴이다.<br><br>
        <span class="line-num">TYPE_CHECKING</span> — 이 블록 안의 import는 실행 시에는 무시되고, mypy 같은 타입 체커만 읽는다. DataBuffer, Config, IntegrityLogger를 런타임에 import하면 순환 참조가 발생할 수 있으므로 이렇게 분리한다.<br><br>
        <span class="line-num">FUNDING_INTERVAL = 8 * 3600</span> — 8시간 = 28,800초. 바이낸스 선물 시장은 00:00, 08:00, 16:00 UTC에 펀딩비를 정산한다. 이 상수가 sleep 주기를 결정한다.<br><br>
        <span class="line-num">FundingRateRecord</span> — models.py에서 정의한 데이터클래스. symbol, funding_rate, funding_time, next_funding_time, recv_time 필드를 가진다.
    </div>

    <div class="code-block"><span class="code-kw">class</span> <span class="code-cls">FundingRateCollector</span>:
    <span class="code-str">"""8시간 주기 펀딩비 수집 (REST API)"""</span>

    FUTURES_URL = <span class="code-str">"https://fapi.binance.com/fapi/v1/premiumIndex"</span>

    <span class="code-kw">def</span> <span class="code-fn">__init__</span>(self, config, buffer, integrity_logger=<span class="code-kw">None</span>):
        self.config = config
        self.buffer = buffer
        self.integrity_logger = integrity_logger
        self.max_retries = <span class="code-num">3</span></div>

    <div class="line-review">
        <span class="line-num">FUTURES_URL</span> — 바이낸스 선물(Futures) API 엔드포인트. <code>fapi</code>는 "futures API"의 약자다. 현물(Spot)은 <code>api.binance.com</code>을 쓰지만, 선물은 <code>fapi.binance.com</code>을 쓴다.<br><br>
        <span class="line-num">premiumIndex</span> — 이 엔드포인트는 펀딩비뿐 아니라 마크 가격, 인덱스 가격도 함께 반환한다. 하나의 API 호출로 여러 정보를 얻을 수 있어 효율적이다.<br><br>
        <span class="line-num">max_retries = 3</span> — REST API 호출은 WebSocket과 달리 일시적 실패가 흔하다. 서버 과부하, 네트워크 지연 등으로 한 번에 성공하지 못할 수 있으므로 3회까지 재시도한다.
    </div>

    <div class="code-block">    <span class="code-kw">async def</span> <span class="code-fn">run</span>(self):
        <span class="code-str">"""8시간 주기 펀딩비 조회 루프"""</span>
        <span class="code-kw">while True</span>:
            <span class="code-kw">for</span> symbol <span class="code-kw">in</span> self.config.symbols:
                record = <span class="code-kw">await</span> self.fetch_funding_rate(symbol)
                <span class="code-kw">if</span> record:
                    <span class="code-kw">from</span> dataclasses <span class="code-kw">import</span> asdict
                    <span class="code-kw">await</span> self.buffer.add_funding_rate(asdict(record))
            <span class="code-kw">await</span> asyncio.sleep(FUNDING_INTERVAL)</div>

    <div class="line-review">
        <span class="line-num">while True</span> — 무한 루프. 8시간마다 깨어나서 모든 심볼의 펀딩비를 조회한다. main.py의 asyncio.gather에 의해 다른 태스크와 동시에 실행된다.<br><br>
        <span class="line-num">for symbol in self.config.symbols</span> — 설정된 모든 심볼(BTCUSDT, ETHUSDT 등)을 순회하며 하나씩 조회한다. 한 번에 모든 심볼을 조회하는 API도 있지만, 개별 조회가 에러 처리에 유리하다. BTCUSDT 조회가 실패해도 ETHUSDT는 정상 수집된다.<br><br>
        <span class="line-num">from dataclasses import asdict</span> — 함수 안에서 import하는 "지연 임포트" 패턴. 모듈 로드 시점이 아니라 실제 사용 시점에 import한다. 여기서는 큰 의미는 없지만, 코드 구조상 dataclasses를 상단에 import하지 않은 것이다.<br><br>
        <span class="line-num">asdict(record)</span> — FundingRateRecord 데이터클래스를 딕셔너리로 변환. buffer.add_funding_rate()는 딕셔너리를 받으므로 변환이 필요하다.<br><br>
        <span class="line-num">asyncio.sleep(FUNDING_INTERVAL)</span> — 28,800초(8시간) 동안 잠든다. 이 동안 이벤트 루프는 다른 태스크(WebSocket 수신, 플러시 등)를 실행한다. sleep이 CPU를 소모하지 않는 이유: 이벤트 루프의 타이머에 등록만 해두고 제어권을 반환하기 때문이다.
    </div>

    <div class="code-block">    <span class="code-kw">async def</span> <span class="code-fn">fetch_funding_rate</span>(self, symbol):
        <span class="code-str">"""단일 심볼 펀딩비 조회 (최대 3회 재시도)"""</span>
        sym = symbol.upper()
        <span class="code-kw">for</span> attempt <span class="code-kw">in</span> range(self.max_retries):
            <span class="code-kw">try</span>:
                <span class="code-kw">async with</span> aiohttp.ClientSession() <span class="code-kw">as</span> session:
                    <span class="code-kw">async with</span> session.get(
                        self.FUTURES_URL,
                        params={<span class="code-str">"symbol"</span>: sym},
                        timeout=aiohttp.ClientTimeout(total=<span class="code-num">10</span>),
                    ) <span class="code-kw">as</span> resp:
                        <span class="code-kw">if</span> resp.status != <span class="code-num">200</span>:
                            logger.warning(f<span class="code-str">"[펀딩비] {sym} HTTP {resp.status}"</span>)
                            <span class="code-kw">continue</span>
                        data = <span class="code-kw">await</span> resp.json()
                        <span class="code-kw">return</span> FundingRateRecord(
                            symbol=sym,
                            funding_rate=str(data.get(<span class="code-str">"lastFundingRate"</span>, <span class="code-str">"0"</span>)),
                            funding_time=int(data.get(<span class="code-str">"time"</span>, <span class="code-num">0</span>)),
                            next_funding_time=int(data.get(<span class="code-str">"nextFundingTime"</span>, <span class="code-num">0</span>)),
                            recv_time=time.time(),
                        )
            <span class="code-kw">except</span> Exception <span class="code-kw">as</span> e:
                logger.warning(f<span class="code-str">"[펀딩비] {sym} 조회 실패 (시도 {attempt+1}): {e}"</span>)
                <span class="code-kw">if</span> attempt &lt; self.max_retries - <span class="code-num">1</span>:
                    <span class="code-kw">await</span> asyncio.sleep(<span class="code-num">2</span> ** attempt)
        <span class="code-kw">return None</span></div>

    <div class="line-review">
        <span class="line-num">sym = symbol.upper()</span> — 바이낸스 API는 심볼을 대문자로 요구한다. config에서 소문자로 저장되어 있을 수 있으므로 항상 변환한다.<br><br>
        <span class="line-num">for attempt in range(self.max_retries)</span> — 0, 1, 2 세 번 시도. 성공하면 return으로 즉시 빠져나오고, 실패하면 continue로 다음 시도로 넘어간다.<br><br>
        <span class="line-num">aiohttp.ClientSession()</span> — 매 요청마다 새 세션을 만든다. 8시간에 한 번 호출되므로 세션을 재사용할 필요가 없다. 오히려 8시간 동안 세션을 유지하면 커넥션이 끊어질 수 있다.<br><br>
        <span class="line-num">params={"symbol": sym}</span> — URL 쿼리 파라미터. <code>?symbol=BTCUSDT</code>가 URL에 추가된다. aiohttp가 자동으로 URL 인코딩을 처리한다.<br><br>
        <span class="line-num">timeout=aiohttp.ClientTimeout(total=10)</span> — 10초 타임아웃. 바이낸스 API가 보통 100ms 이내에 응답하므로 10초는 매우 넉넉하다. 하지만 서버 점검이나 네트워크 문제 시 무한 대기를 방지한다.<br><br>
        <span class="line-num">resp.status != 200 → continue</span> — HTTP 200이 아니면 재시도. 429(Rate Limit), 500(서버 에러) 등이 올 수 있다. continue는 for 루프의 다음 반복으로 넘어간다.<br><br>
        <span class="line-num">data.get("lastFundingRate", "0")</span> — 방어적 접근. API 응답에 해당 키가 없으면 기본값 "0"을 사용한다. API 스펙이 바뀌어도 크래시하지 않는다.<br><br>
        <span class="line-num">funding_rate=str(...)</span> — 펀딩비를 문자열로 저장한다. 왜? 부동소수점 정밀도 문제 때문이다. 0.0001 같은 작은 값이 float로 변환되면 0.00010000000000000000208... 같이 될 수 있다. 문자열로 보관하면 원본 정밀도가 유지된다.<br><br>
        <span class="line-num">asyncio.sleep(2 ** attempt)</span> — 지수 백오프(Exponential Backoff). 첫 번째 실패 후 1초, 두 번째 실패 후 2초 대기. 서버가 과부하 상태일 때 즉시 재시도하면 상황이 악화되므로, 점점 더 오래 기다린다.<br><br>
        <span class="line-num">return None</span> — 3번 모두 실패하면 None 반환. run() 메서드에서 <code>if record:</code>로 None을 걸러내므로 버퍼에 잘못된 데이터가 들어가지 않는다.
    </div>

    <!-- ============================================================ -->
    <!-- FILE 11: time_sync_monitor.py -->
    <!-- ============================================================ -->
    <h2 class="section-header">파일 11/13 — time_sync_monitor.py</h2>
    <p class="body-text">고빈도 데이터 수집에서 시간은 생명이다. 로컬 시계가 1초만 어긋나도 오더북 이벤트의 순서가 뒤바뀔 수 있다. 이 모듈은 10분마다 NTP 서버와 바이낸스 서버의 시간을 비교하여 로컬 시계의 정확도를 감시한다.</p>

    <div class="file-header"><span class="file-path">src/time_sync_monitor.py</span><span class="file-lines">~110 lines</span></div>
    <div class="code-block"><span class="code-str">"""시간 동기화 및 레이턴시 측정 모듈 - NTP 오프셋, 바이낸스 RTT"""</span>

<span class="code-kw">from</span> __future__ <span class="code-kw">import</span> annotations

<span class="code-kw">import</span> asyncio
<span class="code-kw">import</span> json
<span class="code-kw">import</span> logging
<span class="code-kw">import</span> time
<span class="code-kw">from</span> datetime <span class="code-kw">import</span> datetime, timezone
<span class="code-kw">from</span> pathlib <span class="code-kw">import</span> Path

<span class="code-kw">import</span> aiohttp

logger = logging.getLogger(__name__)

MEASURE_INTERVAL = <span class="code-num">600</span>   <span class="code-cm"># 10분</span>
NTP_ALERT_THRESHOLD = <span class="code-num">0.1</span>  <span class="code-cm"># 100ms</span></div>

    <div class="line-review">
        <span class="line-num">MEASURE_INTERVAL = 600</span> — 10분마다 측정. 너무 자주 측정하면 NTP 서버에 부담을 주고, 너무 드물면 시계 드리프트를 놓칠 수 있다. 10분은 적절한 균형점이다.<br><br>
        <span class="line-num">NTP_ALERT_THRESHOLD = 0.1</span> — 100밀리초. 로컬 시계가 NTP 서버와 100ms 이상 차이나면 경고를 보낸다. 왜 100ms인가? 오더북 이벤트는 보통 100ms 간격으로 오므로, 100ms 이상 어긋나면 이벤트 순서가 뒤바뀔 위험이 있다.<br><br>
        <span class="line-num">import aiohttp</span> — 바이낸스 서버 시간 조회에 사용. NTP는 별도의 ntplib 라이브러리를 쓰지만, 바이낸스 시간은 HTTP API로 조회한다.
    </div>

    <div class="code-block"><span class="code-kw">class</span> <span class="code-cls">TimeSyncMonitor</span>:
    <span class="code-str">"""NTP 시간 동기화 및 네트워크 레이턴시 측정"""</span>

    BINANCE_TIME_URL = <span class="code-str">"https://api.binance.com/api/v3/time"</span>

    <span class="code-kw">def</span> <span class="code-fn">__init__</span>(self, config, integrity_logger=<span class="code-kw">None</span>, telegram=<span class="code-kw">None</span>):
        self.config = config
        self.integrity_logger = integrity_logger
        self.telegram = telegram
        self.log_dir = Path(config.log_dir)
        self.log_dir.mkdir(parents=<span class="code-kw">True</span>, exist_ok=<span class="code-kw">True</span>)</div>

    <div class="line-review">
        <span class="line-num">BINANCE_TIME_URL</span> — 바이낸스의 서버 시간 API. 인증 없이 호출 가능하며, 서버의 현재 Unix 타임스탬프를 밀리초 단위로 반환한다.<br><br>
        <span class="line-num">telegram=None</span> — 텔레그램 리포터는 선택적 의존성. 없으면 경고 알림을 보내지 않을 뿐, 측정 자체는 정상 동작한다. 이것이 "느슨한 결합(Loose Coupling)"이다.<br><br>
        <span class="line-num">self.log_dir.mkdir(parents=True, exist_ok=True)</span> — 로그 디렉토리가 없으면 생성. parents=True는 중간 디렉토리도 함께 만든다. exist_ok=True는 이미 있어도 에러를 내지 않는다.
    </div>

    <div class="code-block">    <span class="code-kw">async def</span> <span class="code-fn">run</span>(self):
        <span class="code-str">"""10분 주기 측정 루프"""</span>
        <span class="code-kw">while True</span>:
            <span class="code-kw">try</span>:
                ntp_offset = <span class="code-kw">await</span> self.measure_ntp_offset()
                binance_offset, rtt = <span class="code-kw">await</span> self.measure_binance_offset()
                <span class="code-kw">await</span> self.save_measurement(ntp_offset, binance_offset, rtt)

                <span class="code-kw">if</span> abs(ntp_offset) > NTP_ALERT_THRESHOLD:
                    logger.warning(f<span class="code-str">"[시간동기화] NTP 오프셋 경고: {ntp_offset:.3f}초"</span>)
                    <span class="code-kw">if</span> self.telegram:
                        <span class="code-kw">await</span> self.telegram.send_message(
                            f<span class="code-str">"⏰ NTP 오프셋 경고: {ntp_offset*1000:.1f}ms"</span>
                        )
            <span class="code-kw">except</span> Exception <span class="code-kw">as</span> e:
                logger.error(f<span class="code-str">"[시간동기화] 측정 실패: {e}"</span>)
            <span class="code-kw">await</span> asyncio.sleep(MEASURE_INTERVAL)</div>

    <div class="line-review">
        <span class="line-num">run() 메서드</span> — 다른 모듈의 run()과 같은 패턴: while True + try/except + asyncio.sleep. 이 일관성이 main.py에서 모든 모듈을 asyncio.gather로 묶을 수 있게 한다.<br><br>
        <span class="line-num">measure_ntp_offset()</span> — NTP 서버와 로컬 시계의 차이를 초 단위로 반환. 양수면 로컬이 느리고, 음수면 로컬이 빠르다.<br><br>
        <span class="line-num">measure_binance_offset()</span> — 바이낸스 서버와의 시간 차이 + 왕복 시간(RTT)을 반환. 두 값을 튜플로 반환하는 것이 파이썬의 관용적 패턴이다.<br><br>
        <span class="line-num">abs(ntp_offset) > NTP_ALERT_THRESHOLD</span> — 절대값으로 비교. 시계가 빠르든 느리든 100ms 이상 차이나면 경고. abs()를 쓰지 않으면 시계가 빠른 경우(음수)를 놓친다.<br><br>
        <span class="line-num">ntp_offset*1000:.1f</span> — 초를 밀리초로 변환하여 표시. 0.153초 → "153.0ms". 사람이 읽기 쉬운 단위로 변환하는 것이 좋은 UX다.<br><br>
        <span class="line-num">except Exception → sleep</span> — 측정이 실패해도 루프는 계속된다. sleep이 except 바깥에 있으므로 성공/실패 모두 10분 후 다시 시도한다.
    </div>

    <div class="code-block">    <span class="code-kw">async def</span> <span class="code-fn">measure_ntp_offset</span>(self):
        <span class="code-str">"""NTP 서버와 로컬 시계 오프셋 측정 (초). ntplib 없으면 0.0 반환."""</span>
        <span class="code-kw">try</span>:
            <span class="code-kw">import</span> ntplib
            client = ntplib.NTPClient()
            loop = asyncio.get_running_loop()
            response = <span class="code-kw">await</span> loop.run_in_executor(
                <span class="code-kw">None</span>, <span class="code-kw">lambda</span>: client.request(<span class="code-str">"pool.ntp.org"</span>, version=<span class="code-num">3</span>)
            )
            <span class="code-kw">return</span> response.offset
        <span class="code-kw">except</span> ImportError:
            logger.warning(<span class="code-str">"[시간동기화] ntplib 미설치, NTP 오프셋 측정 건너뜀"</span>)
            <span class="code-kw">return</span> <span class="code-num">0.0</span>
        <span class="code-kw">except</span> Exception <span class="code-kw">as</span> e:
            logger.warning(f<span class="code-str">"[시간동기화] NTP 측정 실패: {e}"</span>)
            <span class="code-kw">return</span> <span class="code-num">0.0</span></div>

    <div class="line-review">
        <span class="line-num">import ntplib (함수 내부)</span> — 지연 임포트의 정석적 사용. ntplib는 선택적 의존성이다. 설치되어 있으면 사용하고, 없으면 ImportError를 잡아서 0.0을 반환한다. 이렇게 하면 ntplib 없이도 프로그램이 실행된다.<br><br>
        <span class="line-num">loop.run_in_executor(None, lambda: ...)</span> — 이것이 이 메서드의 핵심이다. ntplib.NTPClient.request()는 동기(blocking) 함수다. asyncio 이벤트 루프에서 blocking 함수를 직접 호출하면 전체 시스템이 멈춘다. run_in_executor는 이 함수를 별도의 스레드 풀에서 실행하고, 완료될 때까지 이벤트 루프는 다른 일을 한다.<br><br>
        <span class="line-num">None (첫 번째 인자)</span> — 기본 스레드 풀 사용. 커스텀 ThreadPoolExecutor를 만들 수도 있지만, 10분에 한 번 호출이므로 기본 풀로 충분하다.<br><br>
        <span class="line-num">pool.ntp.org</span> — 전 세계 NTP 서버 풀. DNS 라운드 로빈으로 가장 가까운 서버에 연결된다. 특정 서버(time.google.com 등)를 지정할 수도 있지만, 풀을 쓰면 하나가 다운되어도 다른 서버로 자동 전환된다.<br><br>
        <span class="line-num">version=3</span> — NTP 프로토콜 버전 3. 현재 최신은 v4이지만, v3이 호환성이 더 넓다.<br><br>
        <span class="line-num">response.offset</span> — NTP 서버와 로컬 시계의 차이(초). 이 값이 양수면 로컬 시계가 NTP보다 느리고, 음수면 빠르다.<br><br>
        <span class="line-num">except ImportError → 0.0</span> — ntplib가 없으면 오프셋을 0으로 간주. "측정할 수 없으면 문제없다고 가정"하는 것이 아니라, "측정 불가"를 로그로 남기고 시스템은 계속 돌린다.
    </div>

    <div class="code-block">    <span class="code-kw">async def</span> <span class="code-fn">measure_binance_offset</span>(self):
        <span class="code-str">"""바이낸스 서버 시간 차이 및 ping RTT 측정. (offset_sec, rtt_sec)"""</span>
        <span class="code-kw">try</span>:
            <span class="code-kw">async with</span> aiohttp.ClientSession() <span class="code-kw">as</span> session:
                t1 = time.time()
                <span class="code-kw">async with</span> session.get(
                    self.BINANCE_TIME_URL,
                    timeout=aiohttp.ClientTimeout(total=<span class="code-num">5</span>),
                ) <span class="code-kw">as</span> resp:
                    t2 = time.time()
                    data = <span class="code-kw">await</span> resp.json()
                    server_time = data.get(<span class="code-str">"serverTime"</span>, <span class="code-num">0</span>) / <span class="code-num">1000.0</span>
                    rtt = t2 - t1
                    local_mid = (t1 + t2) / <span class="code-num">2.0</span>
                    offset = server_time - local_mid
                    <span class="code-kw">return</span> offset, rtt
        <span class="code-kw">except</span> Exception <span class="code-kw">as</span> e:
            logger.warning(f<span class="code-str">"[시간동기화] 바이낸스 측정 실패: {e}"</span>)
            <span class="code-kw">return</span> <span class="code-num">0.0</span>, <span class="code-num">0.0</span></div>

    <div class="line-review">
        <span class="line-num">t1 = time.time()</span> — 요청 직전의 로컬 시간을 기록한다.<br><br>
        <span class="line-num">t2 = time.time()</span> — 응답 수신 직후의 로컬 시간을 기록한다.<br><br>
        <span class="line-num">rtt = t2 - t1</span> — 왕복 시간(Round-Trip Time). 요청을 보내고 응답을 받기까지 걸린 시간. 보통 50~200ms. 이 값이 크면 네트워크가 느린 것이다.<br><br>
        <span class="line-num">local_mid = (t1 + t2) / 2.0</span> — 요청과 응답의 중간 시점. 서버가 응답을 생성한 시점은 정확히 알 수 없지만, 요청-응답의 중간쯤이라고 가정한다. 이것이 NTP에서도 사용하는 표준적인 시간 추정 방법이다.<br><br>
        <span class="line-num">server_time = data["serverTime"] / 1000.0</span> — 바이낸스는 밀리초 단위 타임스탬프를 반환한다. 1000으로 나누어 초 단위로 변환한다.<br><br>
        <span class="line-num">offset = server_time - local_mid</span> — 바이낸스 서버와 로컬 시계의 차이. 양수면 로컬이 느리고, 음수면 로컬이 빠르다. 이 값이 0에 가까울수록 시간 동기화가 잘 되어 있다.<br><br>
        <span class="line-num">return offset, rtt</span> — 파이썬의 다중 반환. 호출 측에서 <code>offset, rtt = await self.measure_binance_offset()</code>로 언패킹한다.<br><br>
        <span class="line-num">return 0.0, 0.0</span> — 실패 시 기본값. 측정 불가를 나타내지만, 시스템은 계속 동작한다.
    </div>

    <div class="code-block">    <span class="code-kw">async def</span> <span class="code-fn">save_measurement</span>(self, ntp_offset, binance_offset, rtt):
        <span class="code-str">"""측정 결과를 time_sync_{YYYYMMDD}.json에 저장"""</span>
        now = datetime.now(timezone.utc)
        filename = f<span class="code-str">"time_sync_{now.strftime('%Y%m%d')}.json"</span>
        filepath = self.log_dir / filename

        entry = {
            <span class="code-str">"timestamp"</span>: now.isoformat(),
            <span class="code-str">"ntp_offset_sec"</span>: ntp_offset,
            <span class="code-str">"binance_offset_sec"</span>: binance_offset,
            <span class="code-str">"rtt_sec"</span>: rtt,
        }

        entries = []
        <span class="code-kw">if</span> filepath.exists():
            <span class="code-kw">with</span> open(filepath, <span class="code-str">"r"</span>) <span class="code-kw">as</span> f:
                entries = json.load(f)
        entries.append(entry)
        <span class="code-kw">with</span> open(filepath, <span class="code-str">"w"</span>) <span class="code-kw">as</span> f:
            json.dump(entries, f, indent=<span class="code-num">2</span>)</div>

    <div class="line-review">
        <span class="line-num">time_sync_{YYYYMMDD}.json</span> — 날짜별 파일. 하루에 144개의 측정값(10분 × 24시간 × 6)이 하나의 파일에 저장된다. 날짜별로 분리하면 오래된 데이터를 쉽게 삭제할 수 있다.<br><br>
        <span class="line-num">filepath.exists() → json.load</span> — 기존 파일이 있으면 읽어서 리스트에 추가한다. 없으면 빈 리스트에서 시작한다. 이 패턴은 "append to JSON array" 문제의 표준 해법이다. JSON은 파일 끝에 추가(append)할 수 없으므로, 전체를 읽고 → 추가하고 → 전체를 다시 쓴다.<br><br>
        <span class="line-num">json.dump(entries, f, indent=2)</span> — 사람이 읽기 쉽게 들여쓰기 2칸으로 저장. 디버깅할 때 파일을 직접 열어볼 수 있다. 프로덕션에서는 indent=None으로 하면 파일 크기가 줄어든다.<br><br>
        <span class="line-num">주의: 동시성 문제</span> — 이 코드는 파일 읽기와 쓰기 사이에 다른 프로세스가 파일을 수정하면 데이터가 손실될 수 있다. 하지만 이 모듈만 이 파일을 쓰고, 10분 간격이므로 실질적 위험은 없다.
    </div>

    <!-- ============================================================ -->
    <!-- FILE 12: environment_recorder.py -->
    <!-- ============================================================ -->
    <h2 class="section-header">파일 12/13 — environment_recorder.py</h2>
    <p class="body-text">수집 환경의 "스냅샷"을 찍는 모듈이다. OS, Python 버전, 설치된 패키지, CPU/RAM 정보, 설정값을 JSON으로 기록한다. 왜 필요한가? 3개월 후 "그때 어떤 환경에서 수집했지?"라는 질문에 답하기 위해서다. 데이터의 재현성(Reproducibility)을 보장하는 핵심 모듈이다.</p>

    <div class="file-header"><span class="file-path">src/environment_recorder.py</span><span class="file-lines">~80 lines</span></div>
    <div class="code-block"><span class="code-str">"""수집 환경 메타데이터 기록 모듈 - OS, Python, 패키지, CPU/RAM, 설정 정보"""</span>

<span class="code-kw">from</span> __future__ <span class="code-kw">import</span> annotations

<span class="code-kw">import</span> json
<span class="code-kw">import</span> logging
<span class="code-kw">import</span> os
<span class="code-kw">import</span> platform
<span class="code-kw">import</span> sys
<span class="code-kw">from</span> datetime <span class="code-kw">import</span> datetime, timezone
<span class="code-kw">from</span> pathlib <span class="code-kw">import</span> Path

logger = logging.getLogger(__name__)</div>

    <div class="line-review">
        <span class="line-num">import platform</span> — OS 이름, 버전, 아키텍처 등 시스템 정보를 가져오는 표준 라이브러리. <code>platform.system()</code>은 "Darwin"(macOS), "Linux", "Windows"를 반환한다.<br><br>
        <span class="line-num">import os</span> — <code>os.cpu_count()</code>로 CPU 코어 수를 가져온다. 환경 변수 접근에도 사용된다.<br><br>
        <span class="line-num">import sys</span> — <code>sys.version</code>으로 Python 버전, <code>sys.executable</code>로 Python 실행 파일 경로를 가져온다. 가상환경(venv)을 쓰는지 시스템 Python을 쓰는지 구분할 수 있다.
    </div>

    <div class="code-block"><span class="code-kw">class</span> <span class="code-cls">EnvironmentRecorder</span>:
    <span class="code-str">"""수집 환경 메타데이터 기록"""</span>

    SENSITIVE_FIELDS = {<span class="code-str">"telegram_bot_token"</span>, <span class="code-str">"telegram_chat_id"</span>}

    <span class="code-kw">def</span> <span class="code-fn">__init__</span>(self, config, log_dir):
        self.config = config
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=<span class="code-kw">True</span>, exist_ok=<span class="code-kw">True</span>)</div>

    <div class="line-review">
        <span class="line-num">SENSITIVE_FIELDS</span> — 민감 정보 필드 목록. 환경 메타데이터에 설정값을 기록할 때, 텔레그램 토큰과 채팅 ID는 마스킹한다. 이 파일이 실수로 공개되어도 토큰이 노출되지 않는다.<br><br>
        <span class="line-num">set 자료형 {...}</span> — 리스트가 아닌 집합(set)을 사용한다. <code>"telegram_bot_token" in SENSITIVE_FIELDS</code> 검사가 O(1)이다. 리스트는 O(n). 필드가 2개뿐이라 성능 차이는 없지만, "멤버십 검사에는 set"이라는 파이썬 관용구를 따른 것이다.
    </div>

    <div class="code-block">    <span class="code-kw">def</span> <span class="code-fn">record</span>(self):
        <span class="code-str">"""환경 메타데이터를 JSON으로 저장, 파일 경로 반환"""</span>
        now = datetime.now(timezone.utc)
        filename = f<span class="code-str">"environment_{now.strftime('%Y%m%d_%H%M%S')}.json"</span>
        filepath = self.log_dir / filename

        metadata = {
            <span class="code-str">"timestamp"</span>: now.isoformat(),
            <span class="code-str">"system"</span>: self._get_system_info(),
            <span class="code-str">"python"</span>: self._get_python_info(),
            <span class="code-str">"config"</span>: self._mask_sensitive_config(self.config),
        }

        <span class="code-kw">with</span> open(filepath, <span class="code-str">"w"</span>, encoding=<span class="code-str">"utf-8"</span>) <span class="code-kw">as</span> f:
            json.dump(metadata, f, indent=<span class="code-num">2</span>, ensure_ascii=<span class="code-kw">False</span>)

        logger.info(f<span class="code-str">"[환경] 메타데이터 저장: {filepath}"</span>)
        <span class="code-kw">return</span> filepath</div>

    <div class="line-review">
        <span class="line-num">record() — 동기 메서드</span> — 다른 모듈의 run()과 달리 async가 아니다. 시스템 시작 시 한 번만 호출되므로 비동기일 필요가 없다. main.py에서 <code>env_recorder.record()</code>로 호출한다 (await 없이).<br><br>
        <span class="line-num">environment_{YYYYMMDD_HHMMSS}.json</span> — 시작 시각을 파일명에 포함. 하루에 여러 번 재시작해도 파일이 덮어쓰이지 않는다. 각 실행의 환경이 독립적으로 기록된다.<br><br>
        <span class="line-num">self._get_system_info()</span> — OS, CPU, RAM 정보를 딕셔너리로 반환하는 private 메서드.<br><br>
        <span class="line-num">self._get_python_info()</span> — Python 버전, 설치된 패키지 목록을 반환.<br><br>
        <span class="line-num">self._mask_sensitive_config()</span> — 설정값에서 민감 정보를 "***"로 마스킹.<br><br>
        <span class="line-num">ensure_ascii=False</span> — 한글이 \uXXXX로 이스케이프되지 않고 그대로 저장된다. "심볼"이 "\uc2ec\ubcfc"이 아니라 "심볼"로 저장된다. 파일을 직접 열어볼 때 읽기 쉽다.
    </div>

    <div class="code-block">    <span class="code-dec">@staticmethod</span>
    <span class="code-kw">def</span> <span class="code-fn">_get_system_info</span>():
        <span class="code-str">"""OS, CPU, RAM 정보 수집"""</span>
        info = {
            <span class="code-str">"os"</span>: platform.system(),
            <span class="code-str">"os_version"</span>: platform.version(),
            <span class="code-str">"os_release"</span>: platform.release(),
            <span class="code-str">"machine"</span>: platform.machine(),
            <span class="code-str">"processor"</span>: platform.processor(),
            <span class="code-str">"cpu_count"</span>: os.cpu_count(),
        }
        <span class="code-kw">try</span>:
            <span class="code-kw">import</span> psutil
            mem = psutil.virtual_memory()
            info[<span class="code-str">"ram_total_gb"</span>] = round(mem.total / (<span class="code-num">1024</span>**<span class="code-num">3</span>), <span class="code-num">2</span>)
            info[<span class="code-str">"ram_available_gb"</span>] = round(mem.available / (<span class="code-num">1024</span>**<span class="code-num">3</span>), <span class="code-num">2</span>)
        <span class="code-kw">except</span> ImportError:
            info[<span class="code-str">"ram_total_gb"</span>] = <span class="code-str">"psutil 미설치"</span>
        <span class="code-kw">return</span> info</div>

    <div class="line-review">
        <span class="line-num">@staticmethod</span> — self를 사용하지 않는 메서드. 인스턴스 상태에 의존하지 않고 순수하게 시스템 정보만 수집한다. 클래스 밖에 함수로 둘 수도 있지만, 논리적으로 EnvironmentRecorder에 속하므로 staticmethod로 둔다.<br><br>
        <span class="line-num">platform.system()</span> — "Darwin"(macOS), "Linux", "Windows" 중 하나를 반환.<br><br>
        <span class="line-num">platform.machine()</span> — CPU 아키텍처. "arm64"(Apple Silicon), "x86_64"(Intel), "aarch64"(ARM 서버) 등. 같은 코드라도 아키텍처에 따라 성능이 다를 수 있으므로 기록한다.<br><br>
        <span class="line-num">os.cpu_count()</span> — 논리적 CPU 코어 수. 하이퍼스레딩이 있으면 물리 코어의 2배. asyncio는 단일 스레드이므로 코어 수가 직접적 영향은 없지만, run_in_executor의 스레드 풀 크기에 영향을 준다.<br><br>
        <span class="line-num">psutil.virtual_memory()</span> — 선택적 의존성. psutil이 설치되어 있으면 RAM 정보를 수집하고, 없으면 "psutil 미설치"라는 문자열을 저장한다. 이 패턴이 funding_rate_collector의 ntplib와 동일하다: 있으면 쓰고, 없으면 넘어간다.<br><br>
        <span class="line-num">mem.total / (1024**3)</span> — 바이트를 기가바이트로 변환. 1024³ = 1,073,741,824. round(..., 2)로 소수점 2자리까지. 16384000000 바이트 → 15.26 GB.
    </div>

    <div class="code-block">    <span class="code-dec">@staticmethod</span>
    <span class="code-kw">def</span> <span class="code-fn">_get_python_info</span>():
        <span class="code-str">"""Python 버전, 패키지 목록 수집"""</span>
        info = {
            <span class="code-str">"version"</span>: sys.version,
            <span class="code-str">"executable"</span>: sys.executable,
        }
        <span class="code-kw">try</span>:
            <span class="code-kw">import</span> importlib.metadata
            packages = {
                d.metadata[<span class="code-str">"Name"</span>]: d.metadata[<span class="code-str">"Version"</span>]
                <span class="code-kw">for</span> d <span class="code-kw">in</span> importlib.metadata.distributions()
            }
            info[<span class="code-str">"packages"</span>] = packages
        <span class="code-kw">except</span> Exception:
            info[<span class="code-str">"packages"</span>] = {}
        <span class="code-kw">return</span> info</div>

    <div class="line-review">
        <span class="line-num">sys.version</span> — "3.14.2 (main, Feb 10 2026, ...)" 같은 전체 버전 문자열. 마이너 버전까지 기록하면 "그때 3.12였는데 3.14로 올리니까 동작이 달라졌다" 같은 디버깅에 도움이 된다.<br><br>
        <span class="line-num">sys.executable</span> — Python 실행 파일의 절대 경로. "/Users/user/.venv/bin/python" 같은 값. 가상환경을 쓰는지, 시스템 Python을 쓰는지 알 수 있다.<br><br>
        <span class="line-num">importlib.metadata.distributions()</span> — 설치된 모든 패키지를 순회한다. pip freeze와 비슷하지만 프로그래밍 방식으로 접근한다. 딕셔너리 컴프리헨션으로 {패키지명: 버전} 형태로 변환한다.<br><br>
        <span class="line-num">except Exception → {}</span> — 패키지 목록 수집이 실패해도 빈 딕셔너리를 반환. 핵심 기능이 아니므로 실패를 허용한다.
    </div>

    <div class="code-block">    <span class="code-dec">@staticmethod</span>
    <span class="code-kw">def</span> <span class="code-fn">_mask_sensitive_config</span>(config):
        <span class="code-str">"""텔레그램 토큰 등 민감 정보 마스킹"""</span>
        d = config.to_dict()
        <span class="code-kw">for</span> field <span class="code-kw">in</span> EnvironmentRecorder.SENSITIVE_FIELDS:
            <span class="code-kw">if</span> field <span class="code-kw">in</span> d <span class="code-kw">and</span> d[field]:
                d[field] = <span class="code-str">"***"</span>
        <span class="code-kw">return</span> d</div>

    <div class="line-review">
        <span class="line-num">config.to_dict()</span> — Config 객체를 딕셔너리로 변환. 원본 config를 수정하지 않고 복사본을 만들어 마스킹한다. 이것이 "불변성(Immutability)" 원칙이다.<br><br>
        <span class="line-num">if field in d and d[field]</span> — 두 가지를 확인한다: (1) 해당 필드가 존재하는지, (2) 값이 비어있지 않은지. 빈 문자열이나 None이면 마스킹할 필요가 없다.<br><br>
        <span class="line-num">d[field] = "***"</span> — 실제 토큰 대신 별표 3개로 대체. 로그 파일에 "bot_token: 123456:ABC-DEF..." 같은 값이 남으면 보안 사고다. 이 한 줄이 그것을 방지한다.<br><br>
        이 패턴은 보안의 기본 원칙인 "최소 권한(Least Privilege)"과 "기본 거부(Default Deny)"를 따른다. 민감 정보는 명시적으로 허용하지 않는 한 노출하지 않는다.
    </div>

    <!-- ============================================================ -->
    <!-- FILE 13: main.py -->
    <!-- ============================================================ -->
    <h2 class="section-header">파일 13/13 — main.py (오케스트레이터)</h2>
    <p class="body-text">드디어 마지막 파일이다. main.py는 지금까지 리뷰한 12개 모듈을 모두 초기화하고, 의존성을 주입하고, asyncio.gather로 동시에 실행하는 "지휘자(Orchestrator)"다. 코드 자체는 짧지만, 전체 시스템의 생명주기를 관리하는 가장 중요한 파일이다.</p>

    <div class="file-header"><span class="file-path">src/main.py</span><span class="file-lines">~120 lines</span></div>
    <div class="code-block"><span class="code-str">"""메인 애플리케이션 - 모든 모듈 초기화 및 동시 실행"""</span>

<span class="code-kw">from</span> __future__ <span class="code-kw">import</span> annotations

<span class="code-kw">import</span> asyncio
<span class="code-kw">import</span> logging
<span class="code-kw">import</span> signal
<span class="code-kw">import</span> sys
<span class="code-kw">from</span> pathlib <span class="code-kw">import</span> Path

<span class="code-kw">from</span> src.config <span class="code-kw">import</span> Config
<span class="code-kw">from</span> src.models <span class="code-kw">import</span> *
<span class="code-kw">from</span> src.orderbook_manager <span class="code-kw">import</span> OrderBookManager
<span class="code-kw">from</span> src.buffer <span class="code-kw">import</span> DataBuffer
<span class="code-kw">from</span> src.flusher <span class="code-kw">import</span> Flusher
<span class="code-kw">from</span> src.collector <span class="code-kw">import</span> Collector
<span class="code-kw">from</span> src.integrity_logger <span class="code-kw">import</span> IntegrityLogger
<span class="code-kw">from</span> src.syncer <span class="code-kw">import</span> Syncer
<span class="code-kw">from</span> src.telegram_reporter <span class="code-kw">import</span> TelegramReporter
<span class="code-kw">from</span> src.funding_rate_collector <span class="code-kw">import</span> FundingRateCollector
<span class="code-kw">from</span> src.time_sync_monitor <span class="code-kw">import</span> TimeSyncMonitor
<span class="code-kw">from</span> src.environment_recorder <span class="code-kw">import</span> EnvironmentRecorder</div>

    <div class="line-review">
        <span class="line-num">12개의 import</span> — 이 프로젝트의 모든 모듈을 import한다. 각 모듈이 하나의 책임만 가지므로 12개가 되었다. "많다"고 느낄 수 있지만, 하나의 거대한 파일보다 12개의 작은 파일이 유지보수에 훨씬 유리하다.<br><br>
        <span class="line-num">from src.models import *</span> — 와일드카드 import. 보통은 권장하지 않지만, models.py는 데이터클래스만 정의하므로 이름 충돌 위험이 낮다. OrderBookRecord, TradeRecord 등을 일일이 나열하지 않아도 된다.<br><br>
        <span class="line-num">import signal</span> — Unix 시그널 처리. Ctrl+C(SIGINT)나 kill 명령(SIGTERM)을 받았을 때 깔끔하게 종료하기 위해 사용한다.<br><br>
        <span class="line-num">import 순서</span> — PEP 8 스타일: (1) 표준 라이브러리 (asyncio, logging, signal, sys, pathlib), (2) 서드파티 (없음), (3) 로컬 모듈 (src.*). 각 그룹 사이에 빈 줄을 둔다.
    </div>

    <div class="code-block">logging.basicConfig(
    level=logging.INFO,
    format=<span class="code-str">"%(asctime)s [%(levelname)s] %(name)s: %(message)s"</span>,
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)</div>

    <div class="line-review">
        <span class="line-num">logging.basicConfig</span> — 전역 로깅 설정. 모듈 레벨에서 실행되므로 import 시점에 설정된다. 모든 모듈의 logger가 이 설정을 상속받는다.<br><br>
        <span class="line-num">level=logging.INFO</span> — DEBUG 메시지는 숨기고 INFO 이상만 출력. 프로덕션에서는 WARNING으로 올릴 수 있다.<br><br>
        <span class="line-num">format 문자열</span> — <code>2026-02-27 14:30:00,123 [INFO] src.collector: WebSocket 연결 성공</code> 형태로 출력된다. %(name)s는 각 모듈의 logger 이름(src.collector, src.flusher 등)이 들어간다. 어떤 모듈에서 로그가 나왔는지 즉시 알 수 있다.<br><br>
        <span class="line-num">StreamHandler(sys.stdout)</span> — 콘솔에 출력. sys.stderr가 아닌 sys.stdout을 사용한다. Docker 환경에서 stdout과 stderr를 분리하여 수집할 때 유용하다.
    </div>

    <div class="code-block"><span class="code-kw">async def</span> <span class="code-fn">main</span>(config_path: str = <span class="code-str">"config.yaml"</span>) -> <span class="code-kw">None</span>:
    <span class="code-str">"""모든 모듈 초기화 및 asyncio.gather로 동시 실행"""</span>
    config = Config.from_yaml(config_path)

    <span class="code-cm"># 디렉토리 생성 (로깅 FileHandler보다 먼저)</span>
    Path(config.data_dir).mkdir(parents=<span class="code-kw">True</span>, exist_ok=<span class="code-kw">True</span>)
    Path(config.log_dir).mkdir(parents=<span class="code-kw">True</span>, exist_ok=<span class="code-kw">True</span>)

    <span class="code-cm"># 파일 핸들러 추가 (디렉토리 생성 후)</span>
    file_handler = logging.FileHandler(
        Path(config.log_dir) / <span class="code-str">"collector.log"</span>, encoding=<span class="code-str">"utf-8"</span>
    )
    file_handler.setFormatter(
        logging.Formatter(<span class="code-str">"%(asctime)s [%(levelname)s] %(name)s: %(message)s"</span>)
    )
    logging.getLogger().addHandler(file_handler)</div>

    <div class="line-review">
        <span class="line-num">Config.from_yaml(config_path)</span> — YAML 파일에서 설정을 로드한다. 팩토리 메서드 패턴. 생성자(__init__)가 아닌 클래스 메서드로 객체를 만든다. 이렇게 하면 다양한 소스(YAML, JSON, 환경변수)에서 Config를 만들 수 있다.<br><br>
        <span class="line-num">디렉토리 생성 순서</span> — 주석이 핵심을 설명한다: "로깅 FileHandler보다 먼저". FileHandler가 존재하지 않는 디렉토리에 파일을 만들려고 하면 에러가 난다. 그래서 디렉토리를 먼저 만든다. 이런 초기화 순서가 중요하다.<br><br>
        <span class="line-num">logging.getLogger().addHandler(file_handler)</span> — 루트 로거에 파일 핸들러를 추가한다. getLogger()에 이름을 주지 않으면 루트 로거를 반환한다. 루트 로거에 추가하면 모든 모듈의 로그가 이 파일에도 기록된다. 콘솔(StreamHandler) + 파일(FileHandler) 두 곳에 동시에 로그가 남는다.
    </div>

    <div class="code-block">    <span class="code-cm"># 모듈 초기화</span>
    integrity_logger = IntegrityLogger(config.log_dir)
    telegram = TelegramReporter(config)
    buffer = DataBuffer(config.max_buffer_mb)
    ob_manager = OrderBookManager(config.symbols, integrity_logger)
    syncer = Syncer(config, integrity_logger)
    flusher = Flusher(config, buffer, integrity_logger,
                      on_file_created=syncer.enqueue_file)
    collector = Collector(config, ob_manager, buffer, integrity_logger, telegram)
    funding_collector = FundingRateCollector(config, buffer, integrity_logger)
    time_sync = TimeSyncMonitor(config, integrity_logger, telegram)</div>

    <div class="line-review">
        <span class="line-num">의존성 주입(Dependency Injection)</span> — 이 블록이 전체 시스템의 "배선도"다. 각 모듈이 필요한 의존성을 생성자 인자로 받는다. 모듈 스스로가 의존성을 만들지 않는다.<br><br>
        <span class="line-num">초기화 순서가 중요하다</span> — integrity_logger와 telegram이 먼저 만들어져야 다른 모듈에 주입할 수 있다. buffer가 flusher보다 먼저, ob_manager가 collector보다 먼저 만들어져야 한다. 이 순서를 바꾸면 NameError가 발생한다.<br><br>
        <span class="line-num">on_file_created=syncer.enqueue_file</span> — 콜백 패턴. Flusher가 파일을 생성하면 Syncer의 enqueue_file 메서드를 호출한다. Flusher는 Syncer를 직접 알지 못하고, "파일이 생기면 이 함수를 호출해"라는 계약만 안다. 이것이 모듈 간 느슨한 결합을 만든다.<br><br>
        <span class="line-num">의존성 그래프</span>:<br>
        <code>Config → (모든 모듈)</code><br>
        <code>IntegrityLogger → Collector, Flusher, Syncer, FundingRateCollector, TimeSyncMonitor</code><br>
        <code>TelegramReporter → Collector, TimeSyncMonitor</code><br>
        <code>DataBuffer → Flusher, Collector, FundingRateCollector</code><br>
        <code>OrderBookManager → Collector</code><br>
        <code>Syncer.enqueue_file → Flusher (콜백)</code><br><br>
        Config가 모든 모듈에 주입되고, IntegrityLogger가 5개 모듈에 주입된다. 이 두 객체가 시스템의 "허브"다.
    </div>

    <div class="code-block">    <span class="code-cm"># 환경 메타데이터 기록</span>
    env_recorder = EnvironmentRecorder(config, config.log_dir)
    env_recorder.record()

    <span class="code-cm"># 시작 알림</span>
    <span class="code-kw">await</span> telegram.send_startup_report(config)
    logger.info(<span class="code-str">"=== 바이낸스 데이터 수집 시스템 시작 ==="</span>)
    logger.info(f<span class="code-str">"심볼: {[s.upper() for s in config.symbols]}"</span>)
    logger.info(f<span class="code-str">"플러시 주기: {config.flush_interval}초"</span>)</div>

    <div class="line-review">
        <span class="line-num">env_recorder.record()</span> — await 없이 호출. 동기 메서드이므로 이벤트 루프를 블로킹하지만, 시작 시 한 번만 실행되고 매우 빠르므로 문제없다.<br><br>
        <span class="line-num">await telegram.send_startup_report(config)</span> — 텔레그램으로 시작 알림을 보낸다. 이것이 await인 이유: HTTP 요청이 비동기이기 때문. 하지만 아직 다른 태스크가 실행 중이 아니므로 여기서는 순차 실행과 같다.<br><br>
        <span class="line-num">"=== 바이낸스 데이터 수집 시스템 시작 ==="</span> — 로그에서 시작 지점을 쉽게 찾기 위한 구분선. 로그 파일이 수만 줄이 되면 이런 마커가 유용하다.
    </div>

    <div class="code-block">    <span class="code-cm"># 주기적 로그/리포트 태스크</span>
    <span class="code-kw">async def</span> <span class="code-fn">periodic_log</span>():
        <span class="code-kw">while True</span>:
            <span class="code-kw">await</span> asyncio.sleep(config.flush_interval)
            <span class="code-kw">await</span> integrity_logger.write_periodic_log()

    <span class="code-kw">async def</span> <span class="code-fn">daily_summary</span>():
        <span class="code-kw">while True</span>:
            <span class="code-kw">await</span> asyncio.sleep(<span class="code-num">86400</span>)
            <span class="code-kw">await</span> integrity_logger.write_daily_summary()
            stats = integrity_logger.get_periodic_stats()
            <span class="code-kw">await</span> telegram.send_daily_report(stats)

    <span class="code-cm"># 강제 플러시 감시</span>
    <span class="code-kw">async def</span> <span class="code-fn">force_flush_monitor</span>():
        <span class="code-kw">while True</span>:
            <span class="code-kw">await</span> asyncio.sleep(<span class="code-num">30</span>)
            <span class="code-kw">if</span> buffer.needs_force_flush():
                logger.warning(<span class="code-str">"[강제 플러시] 메모리 임계값 초과"</span>)
                <span class="code-kw">await</span> flusher.flush_now()</div>

    <div class="line-review">
        <span class="line-num">함수 안의 함수 (클로저)</span> — periodic_log, daily_summary, force_flush_monitor는 main() 함수 안에 정의된 내부 함수다. 바깥 함수의 변수(config, integrity_logger, telegram, buffer, flusher)를 캡처한다. 이것이 "클로저(Closure)"다.<br><br>
        <span class="line-num">periodic_log()</span> — 플러시 주기(기본 60초)마다 무결성 로그를 기록한다. 수집 건수, 갭 발생 횟수 등의 통계를 파일에 남긴다.<br><br>
        <span class="line-num">daily_summary()</span> — 24시간(86400초)마다 일일 요약을 작성하고 텔레그램으로 보낸다. 매일 아침 "어제 수집 결과"를 확인할 수 있다.<br><br>
        <span class="line-num">force_flush_monitor()</span> — 30초마다 메모리 사용량을 확인한다. buffer.needs_force_flush()가 True를 반환하면(설정된 MB 초과) 즉시 플러시한다. 이것이 "메모리 안전장치"다. 정상적으로는 flush_interval마다 플러시하지만, 데이터가 폭주하면 메모리가 먼저 차므로 강제 플러시가 필요하다.<br><br>
        <span class="line-num">왜 30초인가?</span> — 메모리 체크는 가벼운 연산이므로 자주 해도 된다. 하지만 너무 자주(1초)하면 불필요한 CPU 사용이고, 너무 드물면(5분) 메모리 초과를 늦게 감지한다. 30초는 적절한 균형점이다.
    </div>

    <div class="code-block">    <span class="code-cm"># 모든 태스크 동시 실행</span>
    tasks = [
        collector.run(),          <span class="code-cm"># WebSocket 데이터 수신</span>
        flusher.run(),            <span class="code-cm"># 주기적 디스크 플러시</span>
        syncer.run(),             <span class="code-cm"># 클라우드 동기화</span>
        time_sync.run(),          <span class="code-cm"># 시간 동기화 감시</span>
        periodic_log(),           <span class="code-cm"># 주기적 로그</span>
        daily_summary(),          <span class="code-cm"># 일일 요약</span>
        force_flush_monitor(),    <span class="code-cm"># 메모리 감시</span>
    ]

    <span class="code-cm"># 선물 API 사용 시 펀딩비 수집 추가</span>
    <span class="code-kw">if</span> config.use_futures:
        tasks.append(funding_collector.run())</div>

    <div class="line-review">
        <span class="line-num">tasks 리스트</span> — 7~8개의 코루틴이 동시에 실행된다. 이것이 asyncio의 핵심이다. 하나의 스레드에서 7개의 "작업"이 협력적으로 실행된다. 각 코루틴이 await에서 멈추면 다른 코루틴이 실행된다.<br><br>
        <span class="line-num">실행 흐름 시각화</span>:<br>
        <code>시간 →→→→→→→→→→→→→→→→→→→→→→→→→→→→→→</code><br>
        <code>collector:  [수신][수신][수신][수신][수신][수신]...</code><br>
        <code>flusher:    [대기........][플러시][대기........]</code><br>
        <code>syncer:     [대기..............][동기화][대기..]</code><br>
        <code>time_sync:  [대기..................][측정][대기]</code><br>
        <code>flush_mon:  [체크][대기..][체크][대기..][체크]</code><br><br>
        모든 태스크가 하나의 이벤트 루프에서 번갈아 실행된다. CPU 코어 하나만 사용하지만, I/O 대기 시간을 겹치므로 효율적이다.<br><br>
        <span class="line-num">config.use_futures</span> — 선물 API를 사용하는 경우에만 펀딩비 수집을 추가한다. 현물만 수집하는 경우 불필요한 API 호출을 하지 않는다. 이것이 "조건부 태스크 등록" 패턴이다.
    </div>

    <div class="code-block">    <span class="code-cm"># graceful shutdown</span>
    loop = asyncio.get_running_loop()
    shutdown_event = asyncio.Event()

    <span class="code-kw">def</span> <span class="code-fn">_signal_handler</span>():
        logger.info(<span class="code-str">"종료 신호 수신, 마지막 플러시 실행 중..."</span>)
        shutdown_event.set()

    <span class="code-kw">for</span> sig <span class="code-kw">in</span> (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, _signal_handler)

    <span class="code-cm"># 태스크 실행</span>
    gathered = asyncio.gather(*tasks, return_exceptions=<span class="code-kw">True</span>)

    <span class="code-cm"># shutdown 대기</span>
    done, _ = <span class="code-kw">await</span> asyncio.wait(
        [asyncio.create_task(shutdown_event.wait()), gathered],
        return_when=asyncio.FIRST_COMPLETED,
    )</div>

    <div class="line-review">
        <span class="line-num">Graceful Shutdown</span> — "우아한 종료". Ctrl+C를 누르면 즉시 프로세스를 죽이는 대신, 마지막 플러시를 실행하고 깔끔하게 종료한다. 이것이 없으면 메모리에 있는 데이터가 손실된다.<br><br>
        <span class="line-num">asyncio.Event()</span> — 스레드 간 통신을 위한 이벤트 객체. set()을 호출하면 wait()에서 대기 중인 코루틴이 깨어난다. 시그널 핸들러(동기)와 코루틴(비동기) 사이의 다리 역할을 한다.<br><br>
        <span class="line-num">signal.SIGINT, signal.SIGTERM</span> — SIGINT는 Ctrl+C, SIGTERM은 kill 명령. 두 시그널 모두 같은 핸들러로 처리한다. Docker에서 컨테이너를 중지할 때 SIGTERM이 먼저 오고, 10초 후 SIGKILL이 온다. 그 10초 안에 마지막 플러시를 완료해야 한다.<br><br>
        <span class="line-num">loop.add_signal_handler(sig, _signal_handler)</span> — asyncio 이벤트 루프에 시그널 핸들러를 등록한다. 일반 signal.signal()과 달리, 이벤트 루프와 안전하게 상호작용할 수 있다.<br><br>
        <span class="line-num">asyncio.gather(*tasks, return_exceptions=True)</span> — 모든 태스크를 동시에 실행한다. return_exceptions=True는 하나의 태스크가 에러를 내도 다른 태스크를 중단하지 않는다. 이것이 없으면 collector가 에러를 내면 flusher, syncer 등도 모두 중단된다.<br><br>
        <span class="line-num">asyncio.wait([shutdown_event.wait(), gathered], return_when=FIRST_COMPLETED)</span> — 두 가지 중 하나가 먼저 완료되면 진행한다: (1) 종료 신호를 받거나, (2) 모든 태스크가 완료되거나. 정상적으로는 종료 신호가 먼저 온다 (while True 루프는 스스로 끝나지 않으므로).
    </div>

    <div class="code-block">    <span class="code-cm"># 종료 시 마지막 플러시</span>
    logger.info(<span class="code-str">"마지막 플러시 실행..."</span>)
    <span class="code-kw">try</span>:
        <span class="code-kw">await</span> flusher.flush_now()
    <span class="code-kw">except</span> Exception <span class="code-kw">as</span> e:
        logger.error(f<span class="code-str">"마지막 플러시 실패: {e}"</span>)

    logger.info(<span class="code-str">"=== 시스템 종료 ==="</span>)


<span class="code-kw">if</span> __name__ == <span class="code-str">"__main__"</span>:
    config_file = sys.argv[<span class="code-num">1</span>] <span class="code-kw">if</span> len(sys.argv) > <span class="code-num">1</span> <span class="code-kw">else</span> <span class="code-str">"config.yaml"</span>
    asyncio.run(main(config_file))</div>

    <div class="line-review">
        <span class="line-num">await flusher.flush_now()</span> — 종료 직전 마지막 플러시. 메모리에 남아있는 모든 데이터를 디스크에 쓴다. 이것이 없으면 마지막 flush_interval(60초) 동안 수집된 데이터가 손실된다.<br><br>
        <span class="line-num">try/except</span> — 마지막 플러시도 실패할 수 있다 (디스크 가득 참, 권한 문제 등). 실패해도 로그만 남기고 종료한다. 여기서 raise하면 에러 메시지가 지저분해진다.<br><br>
        <span class="line-num">if __name__ == "__main__"</span> — 파이썬의 표준 진입점 패턴. 이 파일을 직접 실행할 때만 main()을 호출한다. import할 때는 실행하지 않는다.<br><br>
        <span class="line-num">sys.argv[1] if len(sys.argv) > 1 else "config.yaml"</span> — 커맨드라인 인자로 설정 파일 경로를 받는다. 인자가 없으면 기본값 "config.yaml"을 사용한다. <code>python -m src.main production.yaml</code>처럼 다른 설정으로 실행할 수 있다.<br><br>
        <span class="line-num">asyncio.run(main(config_file))</span> — 이벤트 루프를 생성하고 main() 코루틴을 실행한다. main()이 완료되면 이벤트 루프를 정리하고 프로세스가 종료된다. 이 한 줄이 전체 시스템의 시작점이자 끝점이다.
    </div>

    <!-- ============================================================ -->
    <!-- CONCLUSION -->
    <!-- ============================================================ -->
    <h2 class="section-header">결론: 13개 파일이 하나의 시스템이 되기까지</h2>

    <p class="body-text">지금까지 13개 파일, 약 1,500줄의 코드를 한 줄 한 줄 살펴보았다. 마지막으로 전체를 관통하는 설계 원칙들을 정리한다.</p>

    <div class="line-review" style="background: var(--wsj-warm-bg); border-left: 4px solid var(--wsj-accent);">
        <p><strong>1. 단일 책임 원칙 (Single Responsibility)</strong><br>
        각 모듈이 정확히 하나의 일만 한다. collector는 수신만, buffer는 저장만, flusher는 디스크 쓰기만. 이 원칙 덕분에 하나의 모듈을 수정해도 다른 모듈에 영향이 없다.</p>

        <p><strong>2. 방어적 프로그래밍 (Defensive Programming)</strong><br>
        모든 외부 호출(API, 파일 I/O, 네트워크)에 try/except가 있다. 타임아웃이 설정되어 있다. 입력값을 검증한다. "이런 일은 일어나지 않겠지"라고 가정하지 않는다.</p>

        <p><strong>3. 실패 격리 (Failure Isolation)</strong><br>
        텔레그램이 다운되어도 수집은 계속된다. 클라우드 동기화가 실패해도 로컬 데이터는 안전하다. NTP 서버에 연결할 수 없어도 시스템은 돌아간다. 부가 기능의 실패가 핵심 기능을 멈추지 않는다.</p>

        <p><strong>4. 데이터 무결성 (Data Integrity)</strong><br>
        SHA-256 체크섬, 원자적 파일 쓰기(임시 파일 → rename), 오더북 시퀀스 검증, 갭 감지. 데이터가 "있다"만으로는 부족하고, "정확하다"를 증명할 수 있어야 한다.</p>

        <p><strong>5. 관찰 가능성 (Observability)</strong><br>
        모든 모듈이 로그를 남긴다. 텔레그램으로 실시간 알림을 보낸다. 환경 메타데이터를 기록한다. 시간 동기화를 감시한다. 문제가 생겼을 때 "무엇이, 언제, 왜" 발생했는지 추적할 수 있다.</p>

        <p><strong>6. 비동기 아키텍처 (Async Architecture)</strong><br>
        asyncio.gather로 7~8개의 태스크가 하나의 스레드에서 동시에 실행된다. I/O 바운드 작업(네트워크, 디스크)에 최적화된 구조다. CPU 코어 하나로 초당 수천 건의 메시지를 처리할 수 있다.</p>
    </div>

    <p class="body-text" style="margin-top: 2rem; padding: 1.5rem; background: var(--wsj-warm-bg); border-radius: 4px; text-align: center; font-size: 1.1rem;">
        이 글이 코드를 읽고 이해하는 데 도움이 되었기를 바랍니다.<br>
        전체 소스 코드는 <a href="https://github.com/gkfla2020-bit/binance-hft-data-collector" style="color: var(--wsj-link);">GitHub 저장소</a>에서 확인할 수 있습니다.
    </p>

</div>
