from typing import Dict, Any
from app.core.state_manager import StateManager
from app.llm.client import LLMClient
from app.llm.prompts import SESSION_PROMPT
import json

class SessionHandler:
    def __init__(self):
        self.state = StateManager()
        self.llm = LLMClient()

    async def handle_session(self, player_input: str) -> Dict[str, Any]:
        full_state = self.state.get_full_state()
        recent = self.state.get_recent_timeline()

        context = {
            "state_summary": full_state,
            "recent_timeline": recent,
            "player_input": player_input
        }
        prompt = SESSION_PROMPT.format(**context)

        raw_response = await self.llm.generate(prompt)
        response = self._parse_response(raw_response)

        for update in response.get("state_updates", []):
            self.state.update_row(
                sheet=update.get("sheet", ""),
                id_col="ID",
                id_value=update.get("id", ""),
                changes=update.get("changes", {})
            )

        if "event" in response:
            self.state.append_timeline(response["event"])

        return {
            "narrative": response.get("narrative", ""),
            "choices": response.get("choices", []),
            "gm_notes": response.get("gm_notes", "")
        }

    def _parse_response(self, text: str) -> Dict:
        try:
            # Try to extract JSON if wrapped in markdown
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            return json.loads(text)
        except Exception:
            return {
                "narrative": text,
                "choices": [],
                "state_updates": [],
                "gm_notes": "Parse failed - raw response returned"
            }
