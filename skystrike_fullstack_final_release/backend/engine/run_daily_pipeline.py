from backend.engine.system_orchestrator import full_daily_engine_run

if __name__ == "__main__":
    print("? Running full daily ML + tuning pipeline...")
    result = full_daily_engine_run()
    print("? Pipeline complete. Final recommendation:")
    print(result)
