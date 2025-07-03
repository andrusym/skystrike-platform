from fastapi import APIRouter
utils.trade_logger import get_trade_log

router = APIRouter()

@router.get("/api/bots/metrics")
def get_bot_metrics():
    logs = get_trade_log()
    bot_stats = {}

    for log in logs:
        strategy = log.get("strategy")
        if not strategy:
            continue

        bot_stats.setdefault(strategy, {
            "trades": 0,
            "wins": 0,
            "netPnl": 0.0
        })

        bot_stats[strategy]["trades"] += 1
        pnl = log.get("pnl", 0)
        bot_stats[strategy]["netPnl"] += pnl
        if pnl > 0:
            bot_stats[strategy]["wins"] += 1

    for bot in bot_stats:
        stats = bot_stats[bot]
        stats["winRate"] = round(stats["wins"] / stats["trades"], 2) if stats["trades"] > 0 else 0.0

    return bot_stats