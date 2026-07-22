import pandas as pd
from pathlib import Path
from typing import Dict, Any, List
from app.config import settings

class StateManager:
    def __init__(self, campaign_path: str = None):
        self.base_path = Path(campaign_path or settings.CAMPAIGN_PATH)
        self.xlsx_path = self.base_path / settings.XLSX_FILE
        self.sheets = ["Players", "NPCs", "Quests", "Timeline", "World_Facts", "Session_Log"]

    def load_sheet(self, sheet_name: str) -> pd.DataFrame:
        if not self.xlsx_path.exists():
            return pd.DataFrame()
        try:
            return pd.read_excel(self.xlsx_path, sheet_name=sheet_name)
        except Exception:
            return pd.DataFrame()

    def get_full_state(self) -> Dict[str, Any]:
        state = {}
        for sheet in self.sheets:
            df = self.load_sheet(sheet)
            state[sheet] = df.to_dict(orient="records") if not df.empty else []
        return state

    def get_recent_timeline(self, n: int = 5) -> List[Dict]:
        df = self.load_sheet("Timeline")
        if df.empty:
            return []
        return df.tail(n).to_dict(orient="records")

    def append_timeline(self, event: Dict):
        df = self.load_sheet("Timeline")
        new_row = pd.DataFrame([event])
        df = pd.concat([df, new_row], ignore_index=True)
        self._save_sheet("Timeline", df)

    def update_row(self, sheet: str, id_col: str, id_value: str, changes: Dict):
        df = self.load_sheet(sheet)
        if df.empty or id_col not in df.columns:
            return
        mask = df[id_col] == id_value
        for key, value in changes.items():
            if key in df.columns:
                df.loc[mask, key] = value
        self._save_sheet(sheet, df)

    def _save_sheet(self, sheet_name: str, df: pd.DataFrame):
        # Simple save - for production use more robust method
        if not self.xlsx_path.exists():
            # Create new workbook with all sheets
            with pd.ExcelWriter(self.xlsx_path, engine="openpyxl") as writer:
                for s in self.sheets:
                    if s == sheet_name:
                        df.to_excel(writer, sheet_name=s, index=False)
                    else:
                        pd.DataFrame().to_excel(writer, sheet_name=s, index=False)
        else:
            with pd.ExcelWriter(self.xlsx_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
