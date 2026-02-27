---
layout: post
title: "바이낸스 데이터 수집기 — 비전공자도 이해하는 완전 해설"
date: 2026-02-27 18:00:00
permalink: /research/binance-collector-beginner-guide-kr/
categories: [research, data-engineering]
tags: [binance, websocket, python, beginner, tutorial]
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
    .callout { border: 1px solid var(--wsj-black); padding: 20px; margin: 30px 0; }
    .callout-header { font-weight: 700; font-size: 12px; text-transform: uppercase; margin-bottom: 10px; }
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
        <span class="section-label">Beginner's Guide</span>
        <span class="date-line">February 27, 2026</span>
    </div>

    <h1 class="headline">바이낸스 데이터 수집기<br>처음부터 끝까지 이해하기</h1>
    <p class="deck">"이 코드가 대체 뭘 하는 건데?" 라는 질문에 대한 완전한 답변.<br>프로그래밍 경험이 적어도 읽을 수 있도록 비유와 그림으로 설명합니다.</p>

    <div class="abstract">
        <div class="abstract-title">이 글의 목표</div>
        <p class="body-text" style="margin-bottom:0;">
        이 프로젝트는 12개의 파이썬 파일로 구성되어 있다. main.py를 열면 12줄의 import가 나오고, 처음 보면 "이게 다 뭐지?" 싶다. 이 글은 그 12개 파일이 각각 무슨 역할을 하는지, 왜 필요한지, 어떻게 서로 연결되는지를 <strong>비유</strong>를 통해 설명한다. 코드를 한 줄도 몰라도 전체 구조를 이해할 수 있도록 쓰여졌다.
        </p>
    </div>

    <h2 class="section-header">먼저, 이 프로그램이 하는 일</h2>

    <p class="body-text">한 문장으로 요약하면: <strong>바이낸스 거래소에서 실시간으로 쏟아지는 거래 데이터를 24시간 녹화하는 프로그램</strong>이다.</p>

    <p class="body-text">바이낸스에서는 매 순간 이런 일들이 벌어진다:</p>

    <table class="data-table">
        <tr><th>데이터</th><th>쉽게 말하면</th><th>얼마나 자주?</th></tr>
        <tr><td>오더북 (Orderbook)</td><td>"지금 이 가격에 사겠다/팔겠다"는 주문 목록</td><td>0.1초마다</td></tr>
        <tr><td>체결 (Trade)</td><td>"방금 이 가격에 거래가 성사됐다"</td><td>실시간 (초당 수십 건)</td></tr>
        <tr><td>캔들 (Kline)</td><td>1분 동안의 시가/고가/저가/종가 요약</td><td>1분마다</td></tr>
        <tr><td>청산 (Liquidation)</td><td>"누군가 빚내서 투자했다가 강제로 팔렸다"</td><td>실시간</td></tr>
        <tr><td>펀딩비 (Funding Rate)</td><td>선물 시장의 "이자율" 같은 것</td><td>8시간마다</td></tr>
    </table>

    <p class="body-text">이 데이터들을 실시간으로 받아서, 컴퓨터 파일로 저장하고, 클라우드에 백업하고, 문제가 생기면 텔레그램으로 알려주는 것. 그게 이 프로그램의 전부다.</p>

    <div class="analogy-box">
        <div class="analogy-label">🏪 비유: 편의점 CCTV</div>
        <div class="analogy-text">
            편의점에 CCTV를 설치한다고 생각해보자.<br><br>
            • <strong>카메라</strong> = Collector (바이낸스에서 데이터를 받는 부분)<br>
            • <strong>녹화기 메모리</strong> = DataBuffer (받은 데이터를 임시로 저장)<br>
            • <strong>하드디스크</strong> = Flusher (메모리에서 파일로 저장)<br>
            • <strong>클라우드 백업</strong> = Syncer (파일을 구글 드라이브에 업로드)<br>
            • <strong>모니터</strong> = TelegramReporter (상태를 핸드폰으로 알림)<br><br>
            CCTV가 24시간 돌아가면서 영상을 녹화하듯, 이 프로그램은 24시간 돌아가면서 거래 데이터를 녹화한다.
        </div>
    </div>

    <h2 class="section-header">12개 파일, 각각 뭐하는 놈인가</h2>

    <p class="body-text">main.py를 열면 이런 코드가 나온다:</p>

    <div class="code-block"><span class="code-kw">from</span> src.config <span class="code-kw">import</span> <span class="code-cls">Config</span>
<span class="code-kw">from</span> src.models <span class="code-kw">import</span> *
<span class="code-kw">from</span> src.orderbook_manager <span class="code-kw">import</span> <span class="code-cls">OrderBookManager</span>
<span class="code-kw">from</span> src.buffer <span class="code-kw">import</span> <span class="code-cls">DataBuffer</span>
<span class="code-kw">from</span> src.flusher <span class="code-kw">import</span> <span class="code-cls">Flusher</span>
<span class="code-kw">from</span> src.collector <span class="code-kw">import</span> <span class="code-cls">Collector</span>
<span class="code-kw">from</span> src.integrity_logger <span class="code-kw">import</span> <span class="code-cls">IntegrityLogger</span>
<span class="code-kw">from</span> src.syncer <span class="code-kw">import</span> <span class="code-cls">Syncer</span>
<span class="code-kw">from</span> src.telegram_reporter <span class="code-kw">import</span> <span class="code-cls">TelegramReporter</span>
<span class="code-kw">from</span> src.funding_rate_collector <span class="code-kw">import</span> <span class="code-cls">FundingRateCollector</span>
<span class="code-kw">from</span> src.time_sync_monitor <span class="code-kw">import</span> <span class="code-cls">TimeSyncMonitor</span>
<span class="code-kw">from</span> src.environment_recorder <span class="code-kw">import</span> <span class="code-cls">EnvironmentRecorder</span></div>

    <p class="body-text">"from A import B"는 "A라는 파일에서 B라는 도구를 가져와라"라는 뜻이다. 즉 main.py는 12개의 도구를 가져와서 조립하는 "조립 설명서"인 셈이다. 각 도구가 뭔지 하나씩 보자.</p>

    <div class="step-box">
        <span class="step-number">1</span>
        <span class="step-title">Config — 설정 파일 읽기</span>
        <p class="body-text" style="margin-top:10px;">config.yaml이라는 설정 파일을 읽어서 "어떤 코인을 수집할지", "몇 시간마다 저장할지", "텔레그램 알림을 보낼지" 같은 설정값을 가져온다.</p>
        <div class="analogy-box" style="margin-bottom:0;">
            <div class="analogy-label">비유</div>
            <div class="analogy-text">CCTV 설치할 때 "몇 번 카메라를 어디에 설치할지" 적어놓은 <strong>설치 계획서</strong>.</div>
        </div>
    </div>

    <div class="step-box">
        <span class="step-number">2</span>
        <span class="step-title">models — 데이터의 "틀"</span>
        <p class="body-text" style="margin-top:10px;">바이낸스에서 오는 데이터의 형태를 미리 정의해둔 것이다. "오더북 데이터에는 심볼, 시간, 가격 목록이 있다"처럼 데이터의 구조를 정해놓은 설계도.</p>
        <div class="analogy-box" style="margin-bottom:0;">
            <div class="analogy-label">비유</div>
            <div class="analogy-text">엑셀 시트의 <strong>헤더 행</strong>. "이름 | 나이 | 주소" 같은 칸 제목을 미리 정해놓는 것.</div>
        </div>
    </div>

    <div class="step-box">
        <span class="step-number">3</span>
        <span class="step-title">Collector — 데이터 수신기</span>
        <p class="body-text" style="margin-top:10px;">바이낸스 서버에 WebSocket이라는 "실시간 전화선"을 연결해서, 쏟아지는 데이터를 받는다. 오더북, 체결, 캔들, 청산 데이터를 동시에 수신한다.</p>
        <div class="analogy-box" style="margin-bottom:0;">
            <div class="analogy-label">비유</div>
            <div class="analogy-text">CCTV의 <strong>카메라</strong>. 24시간 바이낸스를 "촬영"하고 있다.</div>
        </div>
    </div>

    <div class="step-box">
        <span class="step-number">4</span>
        <span class="step-title">OrderBookManager — 오더북 조립기</span>
        <p class="body-text" style="margin-top:10px;">오더북 데이터는 특별하다. 바이낸스는 전체 오더북을 매번 보내주지 않고, "변경된 부분"만 보내준다. 이 모듈은 처음에 전체 오더북을 한 번 받아온 다음, 이후에 오는 변경 사항을 하나씩 적용해서 항상 최신 오더북을 유지한다.</p>
        <div class="analogy-box" style="margin-bottom:0;">
            <div class="analogy-label">비유</div>
            <div class="analogy-text">위키피디아의 <strong>편집 기록</strong>. 전체 문서를 매번 다시 보내는 게 아니라, "3번째 줄을 이렇게 고쳤다"는 변경 내역만 보내면 우리가 직접 적용해서 최신 문서를 유지하는 것.</div>
        </div>
    </div>

    <div class="step-box">
        <span class="step-number">5</span>
        <span class="step-title">DataBuffer — 임시 저장소</span>
        <p class="body-text" style="margin-top:10px;">받은 데이터를 바로 파일로 저장하면 너무 느리다 (초당 수백 건이니까). 그래서 일단 컴퓨터 메모리(RAM)에 쌓아두고, 1시간마다 한꺼번에 파일로 저장한다.</p>
        <div class="analogy-box" style="margin-bottom:0;">
            <div class="analogy-label">비유</div>
            <div class="analogy-text">CCTV 녹화기의 <strong>RAM</strong>. 영상을 실시간으로 하드디스크에 쓰면 느리니까, 일단 메모리에 모아뒀다가 한 번에 저장한다.</div>
        </div>
    </div>

    <div class="step-box">
        <span class="step-number">6</span>
        <span class="step-title">Flusher — 파일 저장기</span>
        <p class="body-text" style="margin-top:10px;">1시간마다 DataBuffer에 쌓인 데이터를 가져와서 Parquet라는 형식의 파일로 저장한다. 저장할 때 파일이 깨지지 않도록 "임시 파일에 먼저 쓰고, 완성되면 이름을 바꾸는" 안전한 방식을 사용한다. 저장 후에는 파일의 "지문"(SHA-256 해시)도 기록한다.</p>
        <div class="analogy-box" style="margin-bottom:0;">
            <div class="analogy-label">비유</div>
            <div class="analogy-text">CCTV 녹화기의 <strong>하드디스크 저장 기능</strong>. 1시간치 영상을 하나의 파일로 묶어서 저장한다. 저장 중에 전원이 꺼져도 이전 파일이 깨지지 않도록 안전장치가 있다.</div>
        </div>
    </div>

    <div class="step-box">
        <span class="step-number">7</span>
        <span class="step-title">Syncer — 클라우드 백업</span>
        <p class="body-text" style="margin-top:10px;">Flusher가 저장한 파일을 구글 드라이브나 AWS S3 같은 클라우드에 업로드한다. 업로드 실패하면 다음에 다시 시도한다. 7일 지나고 + 클라우드 백업 완료된 파일만 로컬에서 삭제한다.</p>
        <div class="analogy-box" style="margin-bottom:0;">
            <div class="analogy-label">비유</div>
            <div class="analogy-text">CCTV 영상을 <strong>클라우드에 자동 백업</strong>하는 기능. 백업 안 된 영상은 절대 삭제하지 않는다.</div>
        </div>
    </div>

    <div class="step-box">
        <span class="step-number">8</span>
        <span class="step-title">IntegrityLogger — 품질 감시관</span>
        <p class="body-text" style="margin-top:10px;">데이터에 빠진 부분(갭)이 있는지, 연결이 끊긴 적이 있는지, 파일이 제대로 저장됐는지 등을 기록한다. 나중에 "이 데이터가 얼마나 완전한가?"를 수치로 보여줄 수 있다.</p>
        <div class="analogy-box" style="margin-bottom:0;">
            <div class="analogy-label">비유</div>
            <div class="analogy-text">CCTV 영상의 <strong>품질 검사 보고서</strong>. "24시간 중 23시간 59분 녹화 성공, 1분 끊김" 같은 기록.</div>
        </div>
    </div>

    <div class="step-box">
        <span class="step-number">9</span>
        <span class="step-title">TelegramReporter — 알림봇</span>
        <p class="body-text" style="margin-top:10px;">시스템 시작, 연결 끊김, 재연결, 일별 요약 등을 텔레그램 메시지로 보내준다. 설정 안 하면 조용히 꺼져있고, 알림 전송이 실패해도 데이터 수집에는 영향 없다.</p>
        <div class="analogy-box" style="margin-bottom:0;">
            <div class="analogy-label">비유</div>
            <div class="analogy-text">CCTV가 꺼지면 <strong>핸드폰으로 알림</strong> 보내주는 기능. 알림이 안 와도 CCTV는 계속 녹화한다.</div>
        </div>
    </div>

    <div class="step-box">
        <span class="step-number">10</span>
        <span class="step-title">FundingRateCollector — 펀딩비 수집기</span>
        <p class="body-text" style="margin-top:10px;">8시간마다 바이낸스 선물 시장의 펀딩비를 조회한다. 다른 데이터는 WebSocket(실시간 전화)으로 받지만, 펀딩비는 REST API(일반 웹 요청)로 가져온다.</p>
        <div class="analogy-box" style="margin-bottom:0;">
            <div class="analogy-label">비유</div>
            <div class="analogy-text">CCTV와 별개로, 8시간마다 <strong>온도계를 확인</strong>해서 기록하는 것.</div>
        </div>
    </div>

    <div class="step-box">
        <span class="step-number">11</span>
        <span class="step-title">TimeSyncMonitor — 시계 검사기</span>
        <p class="body-text" style="margin-top:10px;">10분마다 "내 컴퓨터 시계가 정확한지" 확인한다. 바이낸스 서버 시간과 내 컴퓨터 시간의 차이를 측정해서 기록한다. 데이터에 찍히는 시간이 정확해야 나중에 분석할 때 의미가 있기 때문이다.</p>
        <div class="analogy-box" style="margin-bottom:0;">
            <div class="analogy-label">비유</div>
            <div class="analogy-text">CCTV 영상에 찍히는 <strong>시간 표시가 정확한지</strong> 주기적으로 확인하는 것.</div>
        </div>
    </div>

    <div class="step-box">
        <span class="step-number">12</span>
        <span class="step-title">EnvironmentRecorder — 환경 기록기</span>
        <p class="body-text" style="margin-top:10px;">프로그램 시작할 때 딱 한 번 실행된다. "어떤 컴퓨터에서, 어떤 파이썬 버전으로, 어떤 설정으로 수집했는지"를 기록한다. 나중에 같은 조건으로 다시 수집하고 싶을 때 참고할 수 있다.</p>
        <div class="analogy-box" style="margin-bottom:0;">
            <div class="analogy-label">비유</div>
            <div class="analogy-text">CCTV 설치 후 <strong>"설치 완료 보고서"</strong>를 작성하는 것. 카메라 모델, 설치 위치, 설정값 등을 기록.</div>
        </div>
    </div>

    <h2 class="section-header">WebSocket이 뭔데?</h2>

    <p class="body-text">보통 웹사이트를 볼 때는 이런 식이다:</p>

    <div class="formula-box">
        <div class="formula-label">일반 웹 요청 (REST API)</div>
        <div class="formula-content">
            나: "지금 BTC 가격 알려줘" → 바이낸스: "68,347원이야"<br>
            (1초 후)<br>
            나: "지금 BTC 가격 알려줘" → 바이낸스: "68,348원이야"<br>
            (1초 후)<br>
            나: "지금 BTC 가격 알려줘" → 바이낸스: "68,346원이야"<br>
            <br>
            → 매번 내가 물어봐야 답을 준다. 비효율적.
        </div>
    </div>

    <div class="formula-box">
        <div class="formula-label">WebSocket (실시간 연결)</div>
        <div class="formula-content">
            나: "BTC 데이터 실시간으로 보내줘" → 바이낸스: "알겠어, 연결 유지할게"<br>
            <br>
            바이낸스 → 나: "68,347원에 0.5개 거래됨"<br>
            바이낸스 → 나: "68,348원에 1.2개 거래됨"<br>
            바이낸스 → 나: "오더북 변경: 68,346원에 매수 3개 추가"<br>
            바이낸스 → 나: "68,347원에 0.1개 거래됨"<br>
            ... (끊임없이 계속)<br>
            <br>
            → 한 번 연결하면 바이낸스가 알아서 계속 보내준다. 효율적.
        </div>
    </div>

    <p class="body-text">WebSocket은 "전화 통화"와 비슷하다. 한 번 전화를 걸면 끊기 전까지 계속 대화할 수 있다. REST API는 "문자 메시지"와 비슷하다 — 매번 보내고 답장을 기다려야 한다.</p>

    <p class="body-text">이 프로그램은 바이낸스에 WebSocket "전화"를 걸어서, 6개 코인(BTC, ETH, XRP, SOL, BNB, DOGE)의 데이터를 동시에 받는다. 하나의 전화선으로 18개 채널(6코인 × 3종류)을 동시에 듣는 셈이다.</p>

    <h2 class="section-header">오더북이 뭔데? 왜 복잡한 거야?</h2>

    <p class="body-text">오더북(Order Book)은 "지금 이 가격에 사고 싶다 / 팔고 싶다"는 주문들의 목록이다.</p>

    <div class="formula-box">
        <div class="formula-label">BTC/USDT 오더북 예시</div>
        <div class="formula-content">
            <span style="color:var(--wsj-red);">매도 (팔겠다)</span>                    <span style="color:var(--wsj-green);">매수 (사겠다)</span>
            ─────────────                ─────────────
            68,350원 × 2.0개              68,347원 × 1.5개  ← 최우선 매수
            68,349원 × 0.8개              68,346원 × 3.2개
            68,348원 × 1.2개  ← 최우선 매도  68,345원 × 0.5개
            
            스프레드 = 68,348 − 68,347 = 1원 (최우선 매도 − 최우선 매수)
        </div>
    </div>

    <p class="body-text">문제는, 이 오더북이 0.1초마다 바뀐다는 것이다. 누군가 주문을 넣거나 취소할 때마다 변한다. 바이낸스가 매번 전체 오더북(수천 개 가격대)을 보내주면 데이터가 너무 많아진다.</p>

    <p class="body-text">그래서 바이낸스는 이렇게 한다:</p>

    <div class="formula-box">
        <div class="formula-label">오더북 업데이트 방식</div>
        <div class="formula-content">
            1단계: 처음에 전체 오더북을 한 번 보내줌 (REST API로 "스냅샷")<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ "현재 오더북은 이렇게 생겼어"<br><br>
            2단계: 이후에는 변경된 부분만 보내줌 (WebSocket으로 "diff")<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ "68,346원의 매수가 3.2개에서 4.0개로 바뀌었어"<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ "68,351원에 새로운 매도 0.5개가 생겼어"<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ "68,345원의 매수가 취소됐어 (수량 = 0)"
        </div>
    </div>

    <p class="body-text">우리 프로그램(OrderBookManager)은 1단계에서 받은 전체 오더북에 2단계의 변경 사항을 하나씩 적용해서, 항상 최신 오더북을 유지한다.</p>

    <div class="warning-box">
        <div class="warning-label">⚠️ 여기서 문제가 생길 수 있다</div>
        <p class="body-text" style="margin-bottom:0;">인터넷이 잠깐 끊기면 변경 사항 몇 개를 놓칠 수 있다. 예를 들어 변경 #100 다음에 #101, #102를 놓치고 #103이 오면, 우리 오더북은 더 이상 정확하지 않다. 이걸 "갭(gap)"이라고 한다.<br><br>
        OrderBookManager는 매번 "번호가 연속인지" 확인한다. 갭이 발견되면 전체 오더북을 처음부터 다시 받아온다. 이게 "자동 재초기화"다.</p>
    </div>

    <h2 class="section-header">asyncio가 뭔데? 왜 쓰는 거야?</h2>

    <p class="body-text">이 프로그램은 동시에 여러 가지 일을 해야 한다:</p>

    <div class="formula-box">
        <div class="formula-content">
            • WebSocket에서 데이터 받기 (24시간 계속)<br>
            • 1시간마다 파일 저장하기<br>
            • 클라우드에 업로드하기<br>
            • 10분마다 시간 동기화 체크하기<br>
            • 30초마다 메모리 사용량 체크하기<br>
            • 8시간마다 펀딩비 조회하기<br>
            • 24시간마다 일별 요약 만들기
        </div>
    </div>

    <p class="body-text">이걸 어떻게 동시에 할까? 세 가지 방법이 있다:</p>

    <div class="analogy-box">
        <div class="analogy-label">🍳 비유: 요리사가 여러 요리를 동시에 만드는 법</div>
        <div class="analogy-text">
            <strong>방법 1 — 멀티프로세싱 (요리사 여러 명 고용)</strong><br>
            각 요리사가 하나의 요리를 담당. 효과적이지만 비용이 많이 들고, 요리사끼리 재료를 공유하기 어렵다.<br><br>
            <strong>방법 2 — 멀티스레딩 (한 요리사가 여러 화구 사용)</strong><br>
            한 요리사가 여러 냄비를 동시에 관리. 하지만 두 손으로 동시에 두 냄비를 저을 수는 없다 (파이썬의 GIL 제약).<br><br>
            <strong>방법 3 — asyncio (한 요리사가 "기다리는 시간"을 활용)</strong><br>
            파스타 물이 끓을 때까지 기다리는 동안 샐러드를 만든다. 물이 끓으면 파스타를 넣고, 다시 소스를 만든다. <strong>기다리는 시간을 낭비하지 않는다.</strong>
        </div>
    </div>

    <p class="body-text">이 프로그램의 대부분의 작업은 "기다리는 시간"이 길다:</p>

    <table class="data-table">
        <tr><th>작업</th><th>실제 계산 시간</th><th>기다리는 시간</th></tr>
        <tr><td>WebSocket 메시지 수신</td><td>0.001초 (JSON 파싱)</td><td>0.1초 (다음 메시지 올 때까지)</td></tr>
        <tr><td>Parquet 파일 저장</td><td>0.1초 (압축+쓰기)</td><td>3,600초 (다음 플러시까지)</td></tr>
        <tr><td>rclone 업로드</td><td>거의 없음</td><td>수 초~수십 초 (네트워크)</td></tr>
        <tr><td>NTP 시간 체크</td><td>거의 없음</td><td>600초 (다음 체크까지)</td></tr>
    </table>

    <p class="body-text">asyncio는 이 "기다리는 시간"에 다른 작업을 끼워넣는다. WebSocket 메시지를 기다리는 동안 파일 저장을 하고, 파일 저장이 끝나면 다시 WebSocket으로 돌아오는 식이다. 한 명의 요리사(단일 프로세스)로 7~8가지 요리를 동시에 만드는 셈이다.</p>

    <div class="code-block"><span class="code-cm"># main.py에서 7개 작업을 동시에 실행하는 코드</span>
tasks = [
    collector.<span class="code-fn">run</span>(),           <span class="code-cm"># WebSocket 수신 (기다림이 대부분)</span>
    flusher.<span class="code-fn">run</span>(),             <span class="code-cm"># 1시간마다 저장 (3600초 기다림)</span>
    syncer.<span class="code-fn">run</span>(),              <span class="code-cm"># 클라우드 업로드 (네트워크 기다림)</span>
    time_sync.<span class="code-fn">run</span>(),           <span class="code-cm"># 10분마다 체크 (600초 기다림)</span>
    ...
]
<span class="code-kw">await</span> asyncio.<span class="code-fn">gather</span>(*tasks)  <span class="code-cm"># "전부 동시에 시작해!"</span></div>

    <p class="body-text"><code>asyncio.gather</code>는 "이 작업들을 전부 동시에 돌려라"라는 명령이다. 각 작업은 <code>await</code>를 만나면 "나 지금 기다리는 중이야, 다른 거 먼저 해"라고 양보한다.</p>

    <h2 class="section-header">메모리 500MB 초과? 강제 플러시?</h2>

    <p class="body-text">데이터를 파일로 저장하기 전까지 컴퓨터 메모리(RAM)에 쌓아둔다고 했다. 보통은 1시간마다 저장하는데, 시장이 미친 듯이 활발하면 1시간 안에 메모리가 꽉 찰 수 있다.</p>

    <div class="analogy-box">
        <div class="analogy-label">🪣 비유: 양동이에 물 받기</div>
        <div class="analogy-text">
            수도꼭지(바이낸스)에서 물(데이터)이 나온다.<br>
            양동이(메모리)에 물을 받고 있다.<br>
            1시간마다 양동이를 비워서 큰 통(파일)에 옮긴다.<br><br>
            <strong>평소:</strong> 물이 졸졸 나옴 → 1시간 후 양동이 반쯤 참 → 비움<br>
            <strong>폭주:</strong> 물이 콸콸 나옴 → 30분만에 양동이 넘칠 것 같음 → <strong>바로 비움!</strong><br><br>
            이 "바로 비움"이 강제 플러시다. 양동이가 넘치면(메모리 부족 = OOM) 프로그램이 죽으니까.
        </div>
    </div>

    <div class="code-block"><span class="code-cm"># 30초마다 양동이(메모리)가 넘칠 것 같은지 체크</span>
<span class="code-kw">async def</span> <span class="code-fn">force_flush_monitor</span>():
    <span class="code-kw">while</span> <span class="code-kw">True</span>:
        <span class="code-kw">await</span> asyncio.<span class="code-fn">sleep</span>(<span class="code-num">30</span>)                <span class="code-cm"># 30초마다 확인</span>
        <span class="code-kw">if</span> buffer.<span class="code-fn">needs_force_flush</span>():       <span class="code-cm"># 500MB 넘었나?</span>
            <span class="code-kw">await</span> flusher.<span class="code-fn">flush_now</span>()           <span class="code-cm"># 넘었으면 즉시 저장!</span></div>

    <p class="body-text">config.yaml에서 <code>max_buffer_mb: 500</code>을 조절할 수 있다. 메모리가 8GB인 컴퓨터라면 500MB면 충분하고, 4GB라면 200MB 정도로 낮추는 게 안전하다.</p>

    <h2 class="section-header">연결이 끊기면? — 자동 재연결</h2>

    <p class="body-text">24시간 돌아가는 프로그램에서 인터넷 연결이 끊기는 건 피할 수 없다. 와이파이가 잠깐 끊기거나, 바이낸스 서버가 점검하거나. 이때 프로그램이 그냥 죽으면 안 된다.</p>

    <div class="formula-box">
        <div class="formula-label">지수 백오프 (Exponential Backoff)</div>
        <div class="formula-content">
            연결 끊김 → 1초 기다림 → 재연결 시도<br>
            또 실패 → 2초 기다림 → 재연결 시도<br>
            또 실패 → 4초 기다림 → 재연결 시도<br>
            또 실패 → 8초 기다림 → 재연결 시도<br>
            또 실패 → 16초 → 32초 → 60초 (최대)<br>
            <br>
            성공하면 → 대기 시간을 다시 1초로 리셋
        </div>
        <div class="formula-note">왜 바로 재연결하지 않고 기다릴까? 서버가 과부하 상태일 때 수천 개의 클라이언트가 동시에 재연결하면 서버가 더 죽는다. 기다리는 시간을 점점 늘려서 서버에 부담을 줄인다.</div>
    </div>

    <p class="body-text">재연결에 성공하면 두 가지를 한다: (1) 대기 시간을 1초로 리셋, (2) 모든 코인의 오더북을 처음부터 다시 받아온다. 연결이 끊긴 동안 놓친 변경 사항이 있으니까, 깨끗한 상태에서 다시 시작하는 거다.</p>

    <h2 class="section-header">Parquet가 뭔데? CSV 쓰면 안 돼?</h2>

    <p class="body-text">CSV도 되긴 하는데, 데이터가 많아지면 Parquet가 훨씬 낫다.</p>

    <table class="data-table">
        <tr><th>비교</th><th>CSV</th><th>Parquet</th></tr>
        <tr><td>파일 크기</td><td>100MB</td><td>~20MB (5배 작음)</td></tr>
        <tr><td>읽기 속도</td><td>느림 (전체 파일 읽어야 함)</td><td>빠름 (필요한 열만 읽기 가능)</td></tr>
        <tr><td>데이터 타입</td><td>전부 문자열</td><td>숫자, 문자열, 날짜 등 구분</td></tr>
        <tr><td>사람이 읽기</td><td>메모장으로 열 수 있음</td><td>전용 도구 필요</td></tr>
        <tr><td>분석 도구</td><td>pandas, Excel</td><td>pandas, Spark, DuckDB 등</td></tr>
    </table>

    <p class="body-text">1시간에 수만~수십만 건의 데이터가 쌓이므로, CSV로 저장하면 파일이 너무 커지고 분석할 때 느리다. Parquet는 snappy라는 압축을 적용해서 파일 크기를 1/5로 줄이면서도 읽기 속도는 빠르다.</p>

    <div class="analogy-box">
        <div class="analogy-label">📦 비유</div>
        <div class="analogy-text">CSV = 물건을 그냥 상자에 던져넣은 것. 찾으려면 전부 뒤져야 한다.<br>
        Parquet = 물건을 종류별로 정리해서 라벨 붙여놓은 것. "가격"만 보고 싶으면 "가격" 서랍만 열면 된다.</div>
    </div>

    <h2 class="section-header">원자적 쓰기? SHA-256? 무결성?</h2>

    <div class="subsection">원자적 쓰기 (Atomic Write)</div>

    <p class="body-text">파일을 저장하는 도중에 컴퓨터가 꺼지면 어떻게 될까? 반쪽짜리 파일이 남는다. 이 파일은 열 수도 없고, 데이터도 복구할 수 없다.</p>

    <p class="body-text">이걸 방지하기 위해 "원자적 쓰기"를 사용한다:</p>

    <div class="formula-box">
        <div class="formula-label">원자적 쓰기 과정</div>
        <div class="formula-content">
            1. 임시 파일(xxx.tmp)에 데이터를 쓴다<br>
            2. 쓰기가 완전히 끝나면, 임시 파일의 이름을 진짜 이름으로 바꾼다<br>
            3. 이름 바꾸기는 "순간적"이라 중간에 끊길 수 없다<br>
            <br>
            → 파일이 "없거나" "완전하거나" 둘 중 하나. 반쪽짜리는 절대 없다.
        </div>
    </div>

    <div class="analogy-box">
        <div class="analogy-label">비유</div>
        <div class="analogy-text">편지를 쓸 때, 연습장에 먼저 쓰고 다 쓰면 깨끗한 종이에 옮겨 적는 것. 연습장에서 실수하면 버리면 되고, 깨끗한 종이에는 완성된 편지만 남는다.</div>
    </div>

    <div class="subsection">SHA-256 체크섬</div>

    <p class="body-text">저장된 파일이 나중에 손상되지 않았는지 확인하는 "지문"이다.</p>

    <div class="formula-box">
        <div class="formula-label">체크섬의 원리</div>
        <div class="formula-content">
            파일 내용 → SHA-256 함수 → "a1b2c3d4e5f6..." (64자리 고유 문자열)<br>
            <br>
            파일이 1비트라도 바뀌면 → 완전히 다른 문자열이 나옴<br>
            <br>
            나중에 확인: 파일을 다시 SHA-256 돌려서 저장된 값과 비교<br>
            → 같으면: 파일 정상<br>
            → 다르면: 파일 손상됨!
        </div>
    </div>

    <div class="analogy-box">
        <div class="analogy-label">비유</div>
        <div class="analogy-text">택배 보낼 때 무게를 재서 송장에 적어놓는 것. 받는 사람이 무게를 다시 재서 송장과 같으면 내용물이 그대로인 거고, 다르면 뭔가 빠졌거나 바뀐 것.</div>
    </div>

    <div class="subsection">데이터 커버리지</div>

    <p class="body-text">24시간 수집했는데, 중간에 연결이 5분 끊겼다면 데이터의 완전성은 어떻게 될까?</p>

    <div class="formula-box">
        <div class="formula-content">
            커버리지 = (전체 시간 − 끊긴 시간) / 전체 시간<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= (1440분 − 5분) / 1440분<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= 99.65%
        </div>
        <div class="formula-note">논문에서 "본 데이터의 커버리지는 99.65%이며, 총 1건의 연결 끊김이 발생하였다"와 같이 보고할 수 있다.</div>
    </div>

    <h2 class="section-header">전체 흐름을 한 그림으로</h2>

    <p class="body-text">지금까지 설명한 모든 것을 하나의 흐름으로 정리하면 이렇다:</p>

    <div class="formula-box">
        <div class="formula-label">프로그램 실행부터 종료까지</div>
        <div class="formula-content">
<span style="color:var(--wsj-accent); font-weight:700;">프로그램 시작</span>
  │
  ├─ Config: config.yaml 읽기 ("어떤 코인? 몇 시간마다 저장?")
  ├─ EnvironmentRecorder: 환경 정보 기록 ("맥북, 파이썬 3.14, ...")
  ├─ TelegramReporter: "시스템 시작됨" 알림 전송
  │
  ▼
<span style="color:var(--wsj-accent); font-weight:700;">동시 실행 (asyncio.gather)</span>
  │
  ├─ <span style="color:var(--wsj-accent);">Collector</span>: 바이낸스 WebSocket 연결
  │   ├─ 오더북 diff 수신 → OrderBookManager가 검증+적용 → Buffer에 저장
  │   ├─ 체결 데이터 수신 → Buffer에 저장
  │   ├─ 캔들 데이터 수신 → Buffer에 저장
  │   └─ (연결 끊기면 → 지수 백오프 재연결 → 오더북 재초기화)
  │
  ├─ <span style="color:var(--wsj-green);">Flusher</span>: 1시간마다
  │   ├─ Buffer에서 데이터 가져오기
  │   ├─ Parquet 파일로 저장 (임시파일 → 이름변경)
  │   ├─ SHA-256 체크섬 기록
  │   └─ Syncer에게 "새 파일 생겼어" 알림
  │
  ├─ <span style="color:var(--wsj-orange);">Syncer</span>: 새 파일이 오면
  │   ├─ rclone으로 클라우드 업로드
  │   ├─ 실패하면 다음에 재시도
  │   └─ 7일 지난 + 백업 완료된 파일만 삭제
  │
  ├─ <span style="color:var(--wsj-red);">TimeSyncMonitor</span>: 10분마다 시계 정확도 체크
  ├─ <span style="color:var(--wsj-red);">FundingRateCollector</span>: 8시간마다 펀딩비 조회
  ├─ 강제 플러시 감시: 30초마다 메모리 500MB 초과 체크
  └─ 일별 요약: 24시간마다 통계 정리 + 텔레그램 리포트
  │
  ▼
<span style="color:var(--wsj-accent); font-weight:700;">종료 (Ctrl+C 또는 kill)</span>
  ├─ 마지막 플러시: Buffer에 남은 데이터 전부 저장
  └─ 프로그램 종료
        </div>
    </div>

    <h2 class="section-header">자주 나오는 용어 정리</h2>

    <table class="data-table">
        <tr><th>용어</th><th>뜻</th><th>비유</th></tr>
        <tr><td>WebSocket</td><td>서버와 실시간 양방향 통신 채널</td><td>전화 통화 (한 번 연결하면 계속 대화)</td></tr>
        <tr><td>REST API</td><td>서버에 요청을 보내고 응답을 받는 방식</td><td>문자 메시지 (보내고 답장 기다림)</td></tr>
        <tr><td>asyncio</td><td>파이썬의 비동기 프로그래밍 도구</td><td>한 요리사가 기다리는 시간을 활용해 여러 요리 동시 진행</td></tr>
        <tr><td>await</td><td>"이 작업이 끝날 때까지 기다려, 그동안 다른 거 해"</td><td>파스타 물 끓을 때까지 샐러드 만들기</td></tr>
        <tr><td>Buffer</td><td>데이터를 임시로 저장하는 메모리 공간</td><td>양동이 (물을 모아뒀다가 한 번에 비움)</td></tr>
        <tr><td>Flush</td><td>버퍼의 데이터를 파일로 저장하고 비우는 것</td><td>양동이를 큰 통에 비우는 것</td></tr>
        <tr><td>Parquet</td><td>열 기반 데이터 저장 형식 (압축 효율 높음)</td><td>종류별로 정리된 서랍장</td></tr>
        <tr><td>Snappy</td><td>빠른 압축 알고리즘</td><td>진공 포장 (크기 줄이되 꺼내기 쉬움)</td></tr>
        <tr><td>SHA-256</td><td>파일의 고유 지문 (해시)</td><td>택배 무게 재서 송장에 적기</td></tr>
        <tr><td>원자적 쓰기</td><td>파일이 "완전하거나 없거나" 둘 중 하나인 저장 방식</td><td>연습장에 먼저 쓰고 완성되면 옮겨적기</td></tr>
        <tr><td>지수 백오프</td><td>재시도 간격을 1→2→4→8초로 늘리는 전략</td><td>전화 안 받으면 점점 늦게 다시 거는 것</td></tr>
        <tr><td>오더북</td><td>매수/매도 주문 목록</td><td>경매장의 입찰 현황판</td></tr>
        <tr><td>diff</td><td>전체가 아닌 변경된 부분만</td><td>위키피디아 편집 기록</td></tr>
        <tr><td>갭 (Gap)</td><td>데이터 시퀀스에서 빠진 부분</td><td>책에서 페이지가 찢겨나간 것</td></tr>
        <tr><td>Grace Period</td><td>초기화 직후 잠깐 오류를 허용하는 시간</td><td>새 직원 적응 기간</td></tr>
        <tr><td>rclone</td><td>클라우드 스토리지 동기화 도구</td><td>자동 백업 프로그램</td></tr>
        <tr><td>OOM</td><td>Out of Memory, 메모리 부족으로 프로그램 죽음</td><td>양동이가 넘쳐서 물바다</td></tr>
        <tr><td>Graceful Shutdown</td><td>데이터 유실 없이 안전하게 종료</td><td>퇴근 전에 작업 저장하고 컴퓨터 끄기</td></tr>
        <tr><td>dataclass</td><td>파이썬에서 데이터 구조를 정의하는 간편한 방법</td><td>엑셀 시트의 헤더 행</td></tr>
        <tr><td>defaultdict</td><td>없는 키에 접근하면 자동으로 빈 값을 만들어주는 딕셔너리</td><td>서류함에 새 폴더가 자동으로 생기는 것</td></tr>
        <tr><td>Lock</td><td>여러 작업이 동시에 같은 데이터를 건드리지 못하게 하는 잠금장치</td><td>화장실 문 잠금 (한 명씩만 사용)</td></tr>
    </table>

    <div class="conclusion-box">
        <h2 class="section-header">정리</h2>
        <p class="body-text">이 프로그램은 결국 하나의 일을 한다: <strong>바이낸스에서 데이터를 받아서 파일로 저장한다.</strong></p>
        <p class="body-text">그런데 "24시간 안정적으로, 데이터 하나도 안 빠뜨리고, 문제 생기면 알아서 복구하면서" 하려면 12개의 모듈이 필요한 것이다.</p>
        <p class="body-text">
            • Collector가 데이터를 받고<br>
            • OrderBookManager가 오더북을 조립하고<br>
            • DataBuffer가 임시로 모아두고<br>
            • Flusher가 파일로 저장하고<br>
            • Syncer가 클라우드에 백업하고<br>
            • IntegrityLogger가 품질을 감시하고<br>
            • TelegramReporter가 상태를 알려주고<br>
            • TimeSyncMonitor가 시계를 확인하고<br>
            • Config가 설정을 관리하고<br>
            • models가 데이터 형태를 정의하고<br>
            • EnvironmentRecorder가 환경을 기록하고<br>
            • main.py가 이 모든 걸 조립해서 동시에 실행한다.
        </p>
        <p class="body-text">각각은 단순하다. 복잡해 보이는 건 이것들이 동시에 돌아가기 때문이다.</p>
        <p class="body-text" style="margin-top:20px;">
            전체 소스 코드: <a href="https://github.com/gkfla2020-bit/binance-hft-data-collector" style="color:var(--wsj-accent);">GitHub</a><br>
            아키텍처 상세: <a href="/research/binance-hft-data-collector-kr/" style="color:var(--wsj-accent);">시스템 아키텍처 글</a><br>
            코드 레벨 해설: <a href="/research/binance-collector-code-deepdive-kr/" style="color:var(--wsj-accent);">코드 딥다이브 글</a>
        </p>
    </div>
</div>
