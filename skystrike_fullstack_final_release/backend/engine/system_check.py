import os
import json
import importlib

files = [
    "data/trade_log.json",
    "data/ml_scores.json",
    "data/final_recommendation.json",
    "data/bot_config.json",
    "data/bot_metrics.json",
    "data/reinforcement_summary.json",
    "data/portfolio_profiles.json"
]

modules = [
    "engine.final_recommendation_engine",
    "engine.reinforcement_engine",
    "engine.performance_engine",
    "engine.bot_decay_monitor",
    "engine.orchestration_engine",
    "engine.explainability_engine",
    "engine.risk_budget_engine"
]

def check_files():
    print("🔍 Checking critical files...")
    for f in files:
        if not os.path.exists(f):
            print(f"❌ Missing: {f}")
        else:
            try:
                with open(f, "r") as jf:
                    json.load(jf)
                print(f"✅ File OK: {f}")
            except:
                print(f"⚠️ Corrupt or unreadable: {f}")

def check_modules():
    print("\n📦 Importing engine modules...")
    for mod in modules:
        try:
            importlib.import_module(mod)
            print(f"✅ Module loaded: {mod}")
        except Exception as e:
            print(f"❌ Failed to import {mod}: {e}")

def main():
    print("🧪 Running SkyStrike System Check")
    check_files()
    check_modules()
    print("\n✅ System check complete. Ready to orchestrate.")

if __name__ == "__main__":
    main()