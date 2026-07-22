#!/usr/bin/env python3
"""Generate TRPG_Campaign_State.xlsx from CSV templates."""

import pandas as pd
from pathlib import Path

TEMPLATE_DIR = Path(__file__).parent
OUTPUT_PATH = TEMPLATE_DIR / "TRPG_Campaign_State.xlsx"

SHEETS = [
    "Players",
    "NPCs",
    "Quests",
    "Timeline",
    "World_Facts",
    "Session_Log",
]

def main():
    with pd.ExcelWriter(OUTPUT_PATH, engine="openpyxl") as writer:
        for sheet in SHEETS:
            csv_path = TEMPLATE_DIR / f"{sheet}.csv"
            if csv_path.exists():
                df = pd.read_csv(csv_path)
                df.to_excel(writer, sheet_name=sheet, index=False)
                print(f"Added sheet: {sheet}")
            else:
                pd.DataFrame().to_excel(writer, sheet_name=sheet, index=False)
                print(f"Empty sheet: {sheet}")

    print(f"\nGenerated: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
