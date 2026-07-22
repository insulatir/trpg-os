from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.session_handler import SessionHandler
from app.core.state_manager import StateManager

router = APIRouter()
handler = SessionHandler()

class SessionRequest(BaseModel):
    player_input: str
    campaign_id: str = "default"

class SessionResponse(BaseModel):
    narrative: str
    choices: list
    gm_notes: str = ""

@router.post("/session", response_model=SessionResponse)
async def run_session(req: SessionRequest):
    try:
        result = await handler.handle_session(req.player_input)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/state")
async def get_state(campaign_id: str = "default"):
    sm = StateManager()
    return sm.get_full_state()
