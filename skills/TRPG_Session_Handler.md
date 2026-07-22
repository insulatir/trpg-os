---
name: TRPG_Session_Handler
description: TRPG 세션을 관리하는 핵심 엔진. Core State (xlsx)를 읽고, 플레이어 입력을 처리하며, 상태 업데이트와 서사를 생성합니다. 장기 일관성과 emergent를 관리합니다.
---

# TRPG Session Handler

## Core State File
- File path: TRPG_Campaign_State.xlsx (Phase 1에서 만든 파일)

## Main Functions

def load_state():
    # xlsx에서 Players, NPCs, Quests, Timeline, World_Facts 로드
    # 최근 Timeline 3~5개 + 관련 World_Facts 요약 반환

def handle_session(player_input):
    # 1. Load current state
    state = load_state()
    
    # 2. Generate response with context
    response = generate_narrative(state, player_input)
    
    # 3. Parse updates
    updates = extract_state_updates(response)
    
    # 4. Apply updates (safe)
    apply_updates(updates)
    
    # 5. Log
    append_to_log(response)
    
    return {
        "narrative": response["narrative"],
        "choices": response["choices"],
        "gm_notes": response.get("gm_notes", "")
    }
