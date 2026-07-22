# TRPG OS

Autonomous TRPG Campaign Manager & Session Engine  
장기 캠페인 관리 + emergent 서사 + 상태 일관성 + Hybrid LLM 엔진

## Features
- Core State Management (xlsx + SQLite)
- Session Handler with Temporal Reasoning
- Lorebook-style World Facts
- Emergent detection & Guardrails
- GitHub 기반 버전 관리

## Quick Start
```bash
git clone https://github.com/insulatir/trpg-os.git
cd trpg-os
cd backend
pip install -r requirements.txt
cp .env.example .env
# API 키 입력
uvicorn app.main:app --reload
```

## Campaign 관리
- `campaigns/default/` 에 기본 캠페인
- 새 캠페인: `campaigns/my_campaign/` 폴더 생성 후 템플릿 복사

## Development
Phase 0 스코프: 장기 캠페인 + 서사 중심 + 가벼운 규칙

## Structure
- `backend/` : FastAPI 코드
- `campaigns/` : 캠페인 데이터
- `skills/` : skill 템플릿
- `data/templates/` : 초기 템플릿
