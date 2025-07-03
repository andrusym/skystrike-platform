import sys, os, pytz
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
services.condor_bot import run_iron_condor_bot
services.king_condor_bot import run_king_condor_bot

def is_midday_window():
    now = datetime.now(pytz.timezone("US/Eastern"))
    return now.hour == 12 and now.minute < 30

def main():
    if is_midday_window():
        run_iron_condor_bot()
        run_king_condor_bot()
    else:
        print("[Cron] Skipping — not in midday window.")

if __name__ == "__main__":
    main()
