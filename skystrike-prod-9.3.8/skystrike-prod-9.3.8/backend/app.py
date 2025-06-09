
import time
from strategy_engine import StrategyEngine
from dashboard import generate_dashboard_summary, print_summary

def run_live_session():
    config = {
        "min_score": 0.6
    }

    engine = StrategyEngine(
        ticker="SPX",
        capital=10000,
        strategy_type="iron_condor",
        config=config,
        mode="paper"
    )

    print("=== SKYSTRIKE TRADE ENGINE STARTED ===")
    result = engine.run()
    print(f"Trade Result: {result}")
    time.sleep(1)

    # Check exits (simulate daily check)
    engine.check_exits()

    # Generate and print dashboard
    summary = generate_dashboard_summary()
    print_summary(summary)

    print("=== SKYSTRIKE SESSION COMPLETE ===")

if __name__ == "__main__":
    run_live_session()
