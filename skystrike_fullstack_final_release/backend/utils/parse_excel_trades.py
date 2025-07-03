import pandas as pd
import json
import os
from datetime import datetime

UPLOAD_DIR = "excel_trades"
OUTPUT_FILE = "ml/historical_trades.json"

def parse_excel_trades():
    all_trades = []

    if not os.path.exists(UPLOAD_DIR):
        print(f"[ERROR] Upload directory '{UPLOAD_DIR}' not found.")
        return

    for file in os.listdir(UPLOAD_DIR):
        if file.endswith(".xlsx") or file.endswith(".csv"):
            filepath = os.path.join(UPLOAD_DIR, file)
            try:
                df = pd.read_excel(filepath) if file.endswith(".xlsx") else pd.read_csv(filepath)
                for _, row in df.iterrows():
                    trade = {
                        "date": str(pd.to_datetime(row.get("Date", ""))),
                        "symbol": str(row.get("Symbol", "")).upper(),
                        "strategy": str(row.get("Strategy", "unknown")).lower(),
                        "side": row.get("Side", "SELL").upper(),
                        "entry_price": float(row.get("Entry Price", 0)),
                        "exit_price": float(row.get("Exit Price", 0)),
                        "pnl": float(row.get("P&L", 0)),
                        "dte": int(row.get("DTE", 0)),
                        "iv": float(row.get("IV", 0)),
                        "source": file
                    }
                    all_trades.append(trade)
            except Exception as e:
                print(f"[ERROR] Failed to parse {file}: {e}")

    if all_trades:
        with open(OUTPUT_FILE, "w") as f:
            json.dump(all_trades, f, indent=2)
        print(f"[SUCCESS] Parsed {len(all_trades)} trades.")
    else:
        print("[WARNING] No trades parsed.")

if __name__ == "__main__":
    parse_excel_trades()
