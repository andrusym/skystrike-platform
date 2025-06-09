
import datetime
from trade_logger import get_trade_log

def generate_dashboard_summary():
    logs = get_trade_log()
    summary = {
        "total_trades": len(logs),
        "open_trades": 0,
        "closed_trades": 0,
        "total_pnl": 0.0,
        "active_strategies": {},
        "last_updated": datetime.datetime.now().isoformat()
    }

    for log in logs:
        if log["status"] == "OPEN":
            summary["open_trades"] += 1
        elif log["status"] == "CLOSED":
            summary["closed_trades"] += 1
            summary["total_pnl"] += log.get("pnl", 0.0)

        strategy = log.get("strategy")
        if strategy:
            if strategy not in summary["active_strategies"]:
                summary["active_strategies"][strategy] = 0
            summary["active_strategies"][strategy] += 1

    summary["total_pnl"] = round(summary["total_pnl"], 2)
    return summary

def print_summary(summary):
    print("\n=== SKYSTRIKE DASHBOARD SUMMARY ===")
    print(f"Last Updated: {summary['last_updated']}")
    print(f"Total Trades: {summary['total_trades']}")
    print(f"Open Trades: {summary['open_trades']}")
    print(f"Closed Trades: {summary['closed_trades']}")
    print(f"Total P&L: ${summary['total_pnl']}")
    print("Active Strategies:")
    for strategy, count in summary["active_strategies"].items():
        print(f"  - {strategy}: {count} trades")
    print("====================================\n")
