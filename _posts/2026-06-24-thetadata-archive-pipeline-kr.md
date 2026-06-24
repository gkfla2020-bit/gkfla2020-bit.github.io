---
layout: post
title: "ThetaData 옵션 아카이빙 파이프라인 — 운영 가이드"
date: 2026-06-24 16:00:00
permalink: /research/thetadata-archive-pipeline-kr/
categories: [research, data-engineering]
tags: [thetadata, options, parquet, python, rest-api, archiving]
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
        <span class="section-label">Data Engineering · Operations</span>
        <span class="date-line">June 24, 2026</span>
    </div>

    <h1 class="headline">ThetaData 옵션 아카이빙 파이프라인<br>운영 가이드</h1>
    <p class="deck">결제하고 키 받았는데 어디서부터 시작해야 할지 모르는 사람을 위한 글.<br>로컬 Terminal 셋업부터 Parquet 영구 보관까지 한 번에 완성합니다.</p>

    <div class="abstract">
        <div class="abstract-title">이 글의 목표</div>
        <p class="body-text" style="margin-bottom:0;">
        ThetaData (https://www.thetadata.net) 는 OPRA-licensed 옵션 데이터 vendor다. 결제하면 API 키가 나오는데, 그걸로 끝이 아니다. <strong>로컬에 Java 기반 프록시(Theta Terminal)를 띄워야 REST API가 동작</strong>한다. 게다가 v3 API는 v2와 엔드포인트, 응답 형식, 쿼리 파라미터가 다 다르다. 이 글은 그 함정들을 다 피한 운영 가이드를 정리한다. 옵션이 뭔지 모르는 분은 <a href="/research/thetadata-options-guide-kr/">옵션 데이터 가이드</a>를 먼저 보길 권한다.
        </p>
    </div>

    <h2 class="section-header">전체 그림 — 30초 요약</h2>

    <div class="analogy-box">
        <div class="analogy-label">🔌 비유: 케이블 회사 셋업박스</div>
        <div class="analogy-text">
            ThetaData는 케이블 방송 회사다. 결제하면 채널 시청권을 주지만, 시청하려면 집에 셋톱박스를 설치해야 한다.<br><br>
            • <strong>케이블 회사</strong> = ThetaData (OPRA 데이터 보유)<br>
            • <strong>시청권</strong> = 구독 (STANDARD 등)<br>
            • <strong>셋톱박스</strong> = ThetaTerminal.jar (로컬에 띄움)<br>
            • <strong>TV</strong> = 우리 Python 코드 (REST API 호출)<br>
            • <strong>녹화기</strong> = Parquet 아카이브<br><br>
            셋톱박스가 꺼지면 TV는 검은 화면. 마찬가지로 Terminal이 죽으면 모든 API 호출이 실패한다.
        </div>
    </div>

    <h2 class="section-header">아키텍처 한 장</h2>

    <div class="code-block">┌─────────────────┐
│  ThetaData      │  ← OPRA 라이센스 데이터 클라우드
│  Cloud          │
└────────┬────────┘
         │ HTTPS 인증 (계정 ID/PW)
         ↓
┌─────────────────┐
│ ThetaTerminal   │  ← 로컬에서 java -jar 로 띄움
│ (Java 11+)      │     인증 처리, 데이터 캐싱, 로컬 프록시
│ :25503          │
└────────┬────────┘
         │ HTTP localhost (인증 헤더 X)
         ↓
┌─────────────────┐
│ theta_archive   │  ← 우리 Python 코드
│ .py             │     /v3/option/* 엔드포인트 호출
└────────┬────────┘     CSV 응답 파싱 → DataFrame
         │
         ↓
┌─────────────────┐
│ data/eod/       │  ← Parquet zstd 압축
│ &lt;SYM&gt;/...      │     Hive 친화 디렉토리
│ manifest.csv    │     이어받기용 영구 기록
└─────────────────┘</div>

    <h2 class="section-header">v2 → v3 핵심 변경 (함정 모음)</h2>

    <p class="body-text">2026년에 v2 → v3로 메이저 업그레이드되면서 거의 모든 게 바뀌었다. 옛날 블로그·튜토리얼은 거의 다 v2 기준이라 그대로 따라하면 동작 안 한다.</p>

    <table class="data-table">
        <tr><th>항목</th><th>v2</th><th>v3 (현재)</th></tr>
        <tr><td>포트</td><td class="mono">25510</td><td class="mono">25503</td></tr>
        <tr><td>경로 prefix</td><td class="mono">/v2/...</td><td class="mono">/v3/...</td></tr>
        <tr><td>심볼 파라미터</td><td class="mono">root=SPY</td><td class="mono">symbol=SPY</td></tr>
        <tr><td>만기 파라미터</td><td class="mono">exp=20251219</td><td class="mono">expiration=20251219</td></tr>
        <tr><td>응답 기본 형식</td><td>JSON</td><td>CSV</td></tr>
        <tr><td>Bulk 엔드포인트</td><td>있음</td><td><strong>없음</strong> (만기별 루프 필수)</td></tr>
        <tr><td>페이지네이션</td><td>next_page</td><td><strong>없음</strong></td></tr>
        <tr><td>날짜 범위 제한</td><td>없음</td><td><strong>365일</strong> (초과 시 HTTP 400)</td></tr>
        <tr><td>strike 단위</td><td>1/1000 달러</td><td>실제 달러</td></tr>
        <tr><td>right 표기</td><td class="mono">C, P</td><td class="mono">CALL, PUT</td></tr>
    </table>

    <div class="warning-box">
        <div class="warning-label">⚠️ HTTP 410 만나면 v2 흔적</div>
        <p class="body-text" style="margin-bottom:0;">
        v3 서버가 v2 경로 호출에 410 Gone을 돌려준다. 메시지에 "Update your endpoint URLs to /v3/* format"라고 친절히 알려준다. 410 보이면 무조건 코드의 BASE_URL과 경로 점검.
        </p>
    </div>

    <h2 class="section-header">Step 1. ThetaTerminal 설치</h2>

    <div class="step-box">
        <span class="step-number">1</span>
        <span class="step-title">Java 11+ 설치</span>
        <p class="body-text" style="margin-top:10px;">macOS 기준:</p>
        <div class="code-block">brew install --cask temurin
java -version   <span class="code-cm"># openjdk 21.x.x 등이 보이면 OK</span></div>
    </div>

    <div class="step-box">
        <span class="step-number">2</span>
        <span class="step-title">jar 파일 다운로드</span>
        <p class="body-text" style="margin-top:10px;">https://www.thetadata.net 로그인 → Dashboard → Download Theta Terminal. 받은 <code>ThetaTerminalv3.jar</code>를 프로젝트 폴더에 둔다.</p>
        <div class="code-block">mkdir -p ~/projects/thetadata/terminal
mv ~/Downloads/ThetaTerminalv3.jar ~/projects/thetadata/terminal/ThetaTerminal.jar</div>
    </div>

    <div class="step-box">
        <span class="step-number">3</span>
        <span class="step-title">creds.txt로 자동 로그인 (권장)</span>
        <p class="body-text" style="margin-top:10px;">명령줄 인자로 비번 넣으면 <code>ps -ef</code> 에 평문 노출된다. <code>creds.txt</code> 두 줄로 처리:</p>
        <div class="code-block"><span class="code-kw">cd</span> ~/projects/thetadata/terminal
<span class="code-fn">echo</span> <span class="code-str">"your-email@example.com"</span> &gt; creds.txt
<span class="code-fn">echo</span> <span class="code-str">"your-password"</span> &gt;&gt; creds.txt
<span class="code-fn">chmod</span> 600 creds.txt   <span class="code-cm"># 본인만 읽기</span>

nohup java -jar ThetaTerminal.jar &gt; terminal.log <span class="code-num">2</span>&gt;&amp;<span class="code-num">1</span> &amp;
disown</div>
    </div>

    <div class="step-box">
        <span class="step-number">4</span>
        <span class="step-title">동작 확인</span>
        <p class="body-text" style="margin-top:10px;">10초 후:</p>
        <div class="code-block">curl -s -m 30 http://127.0.0.1:25503/v3/option/list/symbols | head -c 200</div>
        <p class="body-text">CSV 형식 심볼 리스트가 나오면 성공. 한 줄에 한 종목씩, 약 15,000개.</p>
    </div>

    <h2 class="section-header">Step 2. v3 핵심 엔드포인트 4개</h2>

    <p class="body-text">전체 옵션 시장에서 EOD 데이터를 받는 데 필요한 엔드포인트는 4개뿐이다.</p>

    <table class="data-table">
        <tr><th>용도</th><th>경로</th><th>파라미터</th></tr>
        <tr><td>전 종목 리스트</td><td class="mono">/v3/option/list/symbols</td><td>없음</td></tr>
        <tr><td>만기 리스트</td><td class="mono">/v3/option/list/expirations</td><td><code>symbol</code></td></tr>
        <tr><td>EOD + 그릭스</td><td class="mono">/v3/option/history/greeks/eod</td><td><code>symbol, expiration, strike, right, start_date, end_date</code></td></tr>
        <tr><td>Open Interest</td><td class="mono">/v3/option/history/open_interest</td><td>위와 동일</td></tr>
    </table>

    <div class="formula-box">
        <div class="formula-label">한 번 호출로 한 만기 전체 받기</div>
        <div class="formula-content">strike=*  →  그 만기의 모든 행사가
right=both  →  콜·풋 둘 다</div>
        <div class="formula-note">→ 한 (종목, 만기) 조합당 호출 1번이면 충분 (단, 365일 제한)</div>
    </div>

    <p class="body-text"><strong>중요:</strong> <code>/v3/option/history/eod</code> (그릭스 없는 OHLC만) 도 있지만, <code>greeks/eod</code> 가 OHLC + bid/ask + IV + 그릭스 16개를 한 번에 주므로 <strong>greeks/eod 만 부르면 된다</strong>. 둘 다 부르면 호출 비용 2배.</p>

    <h2 class="section-header">Step 3. 클라이언트 코드 — 얇은 래퍼</h2>

    <div class="code-block"><span class="code-cm"># theta_client.py 핵심 부분</span>

BASE = <span class="code-str">"http://127.0.0.1:25503"</span>

<span class="code-kw">def</span> <span class="code-fn">_get_csv</span>(path, params, timeout=<span class="code-num">120</span>):
    <span class="code-cm"># CSV로 받아서 pandas DataFrame 으로 파싱</span>
    r = requests.get(<span class="code-fn">f</span><span class="code-str">"{BASE}{path}"</span>, params=params, timeout=timeout)
    <span class="code-kw">if</span> r.status_code == <span class="code-num">410</span>:
        <span class="code-kw">raise</span> <span class="code-cls">ThetaError</span>(<span class="code-str">"v2 path used, switch to v3"</span>)
    r.raise_for_status()
    text = r.text
    <span class="code-kw">if</span> <span class="code-kw">not</span> text.strip() <span class="code-kw">or</span> text.startswith(<span class="code-str">"&lt;html"</span>):
        <span class="code-kw">return</span> pd.<span class="code-cls">DataFrame</span>()
    <span class="code-kw">return</span> pd.read_csv(io.<span class="code-cls">StringIO</span>(text))


<span class="code-kw">def</span> <span class="code-fn">list_symbols</span>():
    df = _get_csv(<span class="code-str">"/v3/option/list/symbols"</span>, {})
    <span class="code-kw">return</span> df.iloc[:, <span class="code-num">0</span>].astype(<span class="code-cls">str</span>).tolist()


<span class="code-kw">def</span> <span class="code-fn">list_expirations</span>(symbol):
    df = _get_csv(<span class="code-str">"/v3/option/list/expirations"</span>, {<span class="code-str">"symbol"</span>: symbol})
    <span class="code-kw">return</span> df[<span class="code-str">"expiration"</span>].astype(<span class="code-cls">str</span>).tolist() <span class="code-kw">if</span> <span class="code-kw">not</span> df.empty <span class="code-kw">else</span> []


<span class="code-kw">def</span> <span class="code-fn">eod_greeks</span>(symbol, expiration, start_date, end_date):
    <span class="code-kw">return</span> _get_csv(<span class="code-str">"/v3/option/history/greeks/eod"</span>, {
        <span class="code-str">"symbol"</span>: symbol,
        <span class="code-str">"expiration"</span>: expiration.replace(<span class="code-str">"-"</span>, <span class="code-str">""</span>),
        <span class="code-str">"strike"</span>: <span class="code-str">"*"</span>,        <span class="code-cm"># 모든 행사가</span>
        <span class="code-str">"right"</span>: <span class="code-str">"both"</span>,    <span class="code-cm"># 콜+풋</span>
        <span class="code-str">"start_date"</span>: start_date,
        <span class="code-str">"end_date"</span>: end_date,
    })</div>

    <h2 class="section-header">Step 4. 365일 제한 — chunked 다운로드</h2>

    <p class="body-text">v3는 한 호출당 start ~ end가 365일 이내여야 한다. 더 길게 받으려면 호출자가 청크로 쪼개야 한다.</p>

    <div class="code-block"><span class="code-cls">CHUNK_DAYS</span> = <span class="code-num">360</span>  <span class="code-cm"># 365일보다 살짝 작게</span>

<span class="code-kw">def</span> <span class="code-fn">fetch_chunked</span>(symbol, expiration, start, end):
    s = <span class="code-fn">parse_date</span>(start)
    e = <span class="code-fn">parse_date</span>(end)
    parts = []
    cur = s
    <span class="code-kw">while</span> cur &lt;= e:
        nxt = <span class="code-fn">min</span>(cur + timedelta(days=<span class="code-cls">CHUNK_DAYS</span> - <span class="code-num">1</span>), e)
        df = <span class="code-fn">eod_greeks</span>(symbol, expiration,
                         cur.strftime(<span class="code-str">"%Y%m%d"</span>),
                         nxt.strftime(<span class="code-str">"%Y%m%d"</span>))
        <span class="code-kw">if</span> <span class="code-kw">not</span> df.empty:
            parts.append(df)
        cur = nxt + timedelta(days=<span class="code-num">1</span>)
    <span class="code-kw">return</span> pd.concat(parts, ignore_index=<span class="code-kw">True</span>) <span class="code-kw">if</span> parts <span class="code-kw">else</span> pd.<span class="code-cls">DataFrame</span>()</div>

    <h2 class="section-header">Step 5. 동시성 — 만기 단위 병렬</h2>

    <p class="body-text">STANDARD 구독은 <strong>동시 4개 요청</strong> 까지 허용한다. 5개째 보내면 HTTP 429.</p>

    <div class="warning-box">
        <div class="warning-label">⚠️ 종목 직렬 vs 만기 병렬</div>
        <p class="body-text" style="margin-bottom:0;">
        처음에는 "종목 4개 동시"로 짰다. 그러나 한 종목 안의 만기들은 직렬 처리되니, 종목 다 끝나기 전에 다른 종목으로 못 넘어간다. SPY 1만기에 3-4분 걸리는 게 보틀넥이 됐다.<br><br>
        해법: <strong>만기를 우선순위 큐에 다 넣고 4 슬롯이 만기 단위로 작업</strong>. 종목 직렬화로 인한 idle 시간이 사라진다.
        </p>
    </div>

    <div class="code-block"><span class="code-kw">from</span> concurrent.futures <span class="code-kw">import</span> <span class="code-cls">ThreadPoolExecutor</span>, as_completed

<span class="code-cm"># 1) 종목 우선순위 순서로 (symbol, expiration) 큐 빌드</span>
jobs = []
<span class="code-kw">for</span> sym <span class="code-kw">in</span> SYMBOLS:
    <span class="code-kw">for</span> exp <span class="code-kw">in</span> <span class="code-fn">list_expirations</span>(sym):
        jobs.append((sym, exp))

<span class="code-cm"># 2) 4 워커가 만기 단위로 처리</span>
<span class="code-kw">with</span> <span class="code-cls">ThreadPoolExecutor</span>(max_workers=<span class="code-num">4</span>) <span class="code-kw">as</span> ex:
    futs = {ex.submit(<span class="code-fn">archive_one_expiration</span>, sym, exp, start, end, OUT): (sym, exp)
            <span class="code-kw">for</span> (sym, exp) <span class="code-kw">in</span> jobs}
    <span class="code-kw">for</span> fut <span class="code-kw">in</span> <span class="code-fn">as_completed</span>(futs):
        sym, exp = futs[fut]
        ok, rows = fut.result()
        <span class="code-cm"># 진행 로깅, manifest 기록...</span></div>

    <h2 class="section-header">Step 6. 옵션 수명 캡 — 빈 호출 줄이기</h2>

    <p class="body-text">2025년 만기 옵션을 2018년부터 받으라고 하면 5년 동안 빈 응답만 내려온다. 옵션은 보통 <strong>만기 전 ~2년</strong> 부터만 거래된다.</p>

    <div class="formula-box">
        <div class="formula-label">자동 캡</div>
        <div class="formula-content">실제 호출 start = max(요청 start, 만기일 − 800일)
실제 호출 end   = min(요청 end,   만기일)</div>
        <div class="formula-note">→ 800일이면 LEAPS까지 대부분 커버. 빈 호출 ~50% 감소.</div>
    </div>

    <h2 class="section-header">Step 7. 영구 보관 — Parquet + Hive 파티션</h2>

    <p class="body-text">받은 데이터를 어떻게 저장할 것인가. 후보:</p>

    <table class="data-table">
        <tr><th>형식</th><th>장점</th><th>단점</th></tr>
        <tr><td>CSV</td><td>사람이 읽기 쉬움</td><td>용량 5-10배. 타입 손실</td></tr>
        <tr><td>SQLite</td><td>쿼리 편함</td><td>대용량에 느림. 동시 쓰기 X</td></tr>
        <tr><td><strong>Parquet</strong></td><td>압축 좋음, 컬럼 쿼리 빠름, DuckDB·pandas·Spark 다 호환</td><td>사람이 직접 못 읽음</td></tr>
    </table>

    <div class="formula-box">
        <div class="formula-label">디렉토리 구조</div>
        <div class="formula-content">data/eod/&lt;SYMBOL&gt;/
  ├─ &lt;SYMBOL&gt;_&lt;YYYYMMDD&gt;.parquet  # 만기 단위
  ├─ ...
  └─ _ALL_&lt;SYMBOL&gt;.parquet        # 종목 통합본 (자동 생성)</div>
        <div class="formula-note">→ 만기별로 받아서 만기 단위 파일 + 끝나면 통합본 만듦</div>
    </div>

    <p class="body-text">압축은 <code>zstd</code>가 좋다. <code>gzip</code>보다 빠르고 작다. <code>snappy</code>는 가장 빠르지만 압축률 떨어진다.</p>

    <div class="code-block">df.to_parquet(out_path, index=<span class="code-kw">False</span>, compression=<span class="code-str">"zstd"</span>)</div>

    <h2 class="section-header">Step 8. 이어받기 — manifest.csv</h2>

    <p class="body-text">8년치 다운로드는 며칠 걸린다. 끊겼다 다시 시작할 때 어디까지 받았는지 알아야 한다.</p>

    <div class="step-box">
        <span class="step-number">방법 1</span>
        <span class="step-title">파일 존재 여부로 스킵 (간단)</span>
        <p class="body-text" style="margin-top:10px;"><code>data/eod/SPY/SPY_20250619.parquet</code> 가 있으면 그 만기는 이미 받음 → 스킵.</p>
    </div>

    <div class="step-box">
        <span class="step-number">방법 2</span>
        <span class="step-title">manifest.csv 영구 기록</span>
        <p class="body-text" style="margin-top:10px;">호출 한 번마다 한 줄씩 추가:</p>
        <div class="code-block">symbol,expiration,feed,status,rows,bytes,path,started_at,finished_at,error
SPY,2025-08-15,greeks_eod,ok,432,0,,2026-06-22T...,2026-06-22T...,
SPY,2025-08-15,open_interest,ok,432,0,,...
SPY,2025-08-15,merged,ok,432,83410,/path/SPY_20250815.parquet,...</div>
        <p class="body-text">셋 다 ok면 그 만기 완료. 쿼리도 가능 ("SPY 9월 만기 중 실패한 거?").</p>
    </div>

    <h2 class="section-header">Step 9. 검증·복구 — verify_archive.py</h2>

    <p class="body-text">매니페스트 vs 디스크 정합성 체크 스크립트를 따로 만든다. 발견 가능한 문제:</p>

    <table class="data-table">
        <tr><th>문제</th><th>탐지 방법</th><th>복구</th></tr>
        <tr><td>status=error</td><td>manifest 직접 조회</td><td>해당 만기만 재호출</td></tr>
        <tr><td>greeks_eod ok인데 merged 없음</td><td>피드별 pivot</td><td>재머지 또는 재호출</td></tr>
        <tr><td>디스크에 있는데 manifest에 없음</td><td>set 차집합</td><td>orphan 처리 (수동 검토)</td></tr>
        <tr><td>만기 전체 누락</td><td>list_expirations vs 디스크</td><td>해당 만기 신규 다운로드</td></tr>
    </table>

    <h2 class="section-header">Step 10. 운영 자동화 — 매일 증분</h2>

    <p class="body-text">옵션 EOD는 미국 동부 18:00 경 ThetaData에 갱신된다. 한국 시간 다음날 새벽 7시 (서머타임 시 6시).</p>

    <div class="code-block"><span class="code-cm"># crontab -e</span>
<span class="code-num">0 7 * * 2-6</span> cd /path/to/thetadata &amp;&amp; \
              python scripts/daily_increment.py &gt;&gt; logs/cron.log <span class="code-num">2</span>&gt;&amp;<span class="code-num">1</span></div>

    <p class="body-text"><code>daily_increment.py</code>는 어제 ET 날짜를 자동 계산해서 SYMBOLS 전 종목의 그날 데이터만 받는다. 이미 받았으면 스킵.</p>

    <h2 class="section-header">함정 모음 — 우리가 직접 부딪힌 것</h2>

    <div class="warning-box">
        <div class="warning-label">⚠️ 1. HTTP 429 누적 카운터</div>
        <p class="body-text" style="margin-bottom:0;">
        STANDARD는 동시 4개 외에 <strong>시간당 누적 호출량 한도</strong>도 있는 듯. 24시간 retry 폭주 시킨 후 1-2시간 동안 계속 429. <strong>해법</strong>: Terminal 재시작하면 카운터 리셋되는 경우 많음. 그래도 안 되면 1시간 휴식.
        </p>
    </div>

    <div class="warning-box">
        <div class="warning-label">⚠️ 2. SPY 0DTE 만기는 무겁다</div>
        <p class="body-text" style="margin-bottom:0;">
        SPY는 매일 만기(0DTE) 옵션이 있고, 행사가가 매우 촘촘하다(±1$ 단위). 한 만기에 수천 행사가 × 수백 거래일. 한 만기 다운로드에 3-4분. 다른 ETF의 30배 가까이 걸린다. 시간 예산 짤 때 고려.
        </p>
    </div>

    <div class="warning-box">
        <div class="warning-label">⚠️ 3. 비번 노출 위험 3가지</div>
        <p class="body-text" style="margin-bottom:0;">
        ① 명령줄 인자 (<code>java -jar Theta.jar email pass</code>) → <code>ps -ef</code> 평문<br>
        ② 채팅·이슈 (Claude·Slack 등에 붙여넣기)<br>
        ③ <code>history</code> 파일에 영구 저장<br><br>
        해법: <code>creds.txt</code> 자동 로그인 + <code>chmod 600</code> + <code>.gitignore</code>에 추가.
        </p>
    </div>

    <div class="warning-box">
        <div class="warning-label">⚠️ 4. ThetaTerminal은 자식 프로세스를 따로 띄움</div>
        <p class="body-text" style="margin-bottom:0;">
        Terminal을 죽일 때 <code>pkill -f ThetaTerminal.jar</code>로 런처만 죽이면 실제 서버 자식 프로세스(<code>java</code>)는 살아있다. <code>lsof -i :25503</code>로 포트 점유자를 확인해서 그 PID도 명시적으로 죽여야 함.
        </p>
    </div>

    <div class="warning-box">
        <div class="warning-label">⚠️ 5. caffeinate 안 쓰면 슬립</div>
        <p class="body-text" style="margin-bottom:0;">
        macOS는 노트북 화면 닫으면 슬립. 12시간 다운로드 중 슬립되면 작업 중단. <code>caffeinate -dis nohup ...</code> 으로 감싸면 디스플레이/시스템/디스크 슬립 모두 차단.
        </p>
    </div>

    <h2 class="section-header">실측 — 뭐가 얼마나 걸리나</h2>

    <table class="data-table">
        <tr><th>작업</th><th>시간</th><th>비고</th></tr>
        <tr><td>SPY 1만기 (2025년 0DTE)</td><td>~3분</td><td>365일 데이터, 행사가 ~700개</td></tr>
        <tr><td>QQQ 1만기 (월별)</td><td>~10초</td><td>행사가 ~200개</td></tr>
        <tr><td>VXX 1만기 (주별)</td><td>~15초</td><td>0DTE 없음</td></tr>
        <tr><td>SPY 1년치 (만기 ~520개)</td><td>~26시간</td><td>4 워커 병렬</td></tr>
        <tr><td>5종목 1년치 (만기 ~900개)</td><td>~6시간</td><td>SPY 제외 시 ~1시간</td></tr>
        <tr><td>87종목 8년치 (만기 ~40,000개)</td><td>~50시간</td><td>현실적으로 분할 다운로드</td></tr>
    </table>

    <h2 class="section-header">디스크 용량 — 실측</h2>

    <table class="data-table">
        <tr><th>대상</th><th>만기당 평균</th><th>1년치 1종목</th></tr>
        <tr><td>SPY (무거움)</td><td>~350 KB</td><td>~80 MB</td></tr>
        <tr><td>QQQ (보통)</td><td>~250 KB</td><td>~30 MB</td></tr>
        <tr><td>VXX (가벼움)</td><td>~150 KB</td><td>~15 MB</td></tr>
        <tr><td>VIX (가벼움)</td><td>~100 KB</td><td>~5 MB</td></tr>
        <tr><td>5종목 1년치</td><td>—</td><td>~150 MB</td></tr>
        <tr><td>87종목 8년치</td><td>—</td><td>~10-15 GB</td></tr>
    </table>

    <h2 class="section-header">데이터 신뢰도 — OPRA 라이센스</h2>

    <div class="callout-box" style="background: #fff3e0; border: 1px solid var(--wsj-orange); padding: 20px 25px; margin: 25px 0;">
        <p class="body-text" style="margin-bottom:0;">
        ThetaData는 <strong>OPRA(Options Price Reporting Authority)</strong>의 정식 라이센시다. OPRA는 미국 SEC가 옵션거래소들에 통합 호가 보고를 의무화하면서 만들어진 공식 데이터 채널. OptionMetrics(Wharton WRDS), Bloomberg, Refinitiv가 쓰는 같은 OPRA 원천이다.<br><br>
        <strong>학술 publish 가능 수준</strong>이며, 인용 양식은 <a href="/research/thetadata-options-guide-kr/">옵션 데이터 가이드</a> 참조.
        </p>
    </div>

    <h2 class="section-header">전체 파이프라인 한 장 요약</h2>

    <div class="code-block">[설치]                  brew install temurin
                        download ThetaTerminal.jar
                        terminal/creds.txt 작성

[실행]                  java -jar terminal/ThetaTerminal.jar &amp;
                        ↓ (10초 대기)
                        curl http://127.0.0.1:25503/v3/option/list/symbols

[다운로드]              caffeinate -dis nohup python theta_archive.py \
                          --symbols SPY,QQQ,VXX --start 2025-06-24 \
                          --end 2026-06-24 --time-budget 8 &amp;

[검증]                  python verify_archive.py
                        python verify_archive.py --repair

[통합본]                python verify_archive.py --consolidate

[자동화 (cron)]         0 7 * * 2-6  python daily_increment.py

[분석]                  duckdb / pandas / DuckDB.read_parquet('_ALL_SPY.parquet')</div>

    <div class="conclusion-box">
        <h2 class="section-header">정리</h2>
        <p class="body-text">
        ThetaData는 OPRA 정식 라이센시다. 학술 신뢰도 OK. 다만 v3 API의 함정(포트, 파라미터, 응답 형식, 365일 제한, bulk 부재, rate limit)을 모르면 시간을 며칠 날린다.
        </p>
        <p class="body-text">
        핵심 설계 원칙: <strong>만기 단위 병렬 + Parquet + manifest.csv</strong>. 이 셋이 있으면 끊겨도 이어받기 자동, 검증 자동, 분석 직접 가능하다.
        </p>
        <p class="body-text">
        SPY 0DTE 만기가 압도적으로 무거우니, 시간 예산 짤 때 SPY는 별도 세션으로 분리. 다른 종목 4-5개는 1년치를 1-2시간이면 끝낼 수 있다.
        </p>
        <p class="body-text" style="color:white;">
        다음 글에서는 받은 데이터로 실제 분석을 한다 — VXX 롤 손실 정량화, SPY 변동성 위험 프리미엄 측정 등.
        </p>
    </div>

</div>
