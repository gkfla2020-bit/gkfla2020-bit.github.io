# Albatross Syllabus Navigator

2026 서강대학교 생성형 AI 기반 아이디어 공모전 출품 데모.

**라이브 데모**: https://gkfla2020-bit.github.io/syllabus-navigator/

## 개요

서강대 트랙제·졸업요건·선수과목 그래프를 RAG로 엮어, 학생이 관심사 한 줄만 넣으면 AI 에이전트가 4년치 수강 로드맵을 역산해주는 설계 도구.

## 구성

- `index.html` — 단일 파일 SPA (Jekyll permalink로 `/syllabus-navigator/`에 배포)
- `data/courses.json` — 가상 강의계획서 24건 + 졸업요건 + 트랙 정의

## 에이전트 체인

1. **RequirementRAG** — 학칙 벡터DB에서 학과 졸업요건 조회
2. **PrereqGraph** — 트랙 코어과목에서 선수과목 역추적
3. **TimetableSAT** — 시간표 충돌 + 자유 제약 풀이
4. **Explainer** — 자연어 rationale 생성

본 데모는 브라우저 내 결정론적 시뮬레이션. 실구현은 Claude API + pgvector + LlamaParse로 확장.

## 심사 어필

| 기준 | 근거 |
|---|---|
| 혁신성 | 역산 플래닝 + RAG 결합은 국내 대학 최초 |
| 타당성 | 전 구성원이 학기마다 겪는 보편 문제 |
| 구현가능성 | 본 데모로 핵심 로직 실증 |
| AI 적절성 | LLM 없이는 불가능한 자연어 설명 + RAG로 할루시네이션 제어 |

## 데이터 면책

`data/courses.json`은 공모전 데모용 **가상 데이터**로, 실제 서강대 강의계획서·교수명·시간표와 무관합니다.
