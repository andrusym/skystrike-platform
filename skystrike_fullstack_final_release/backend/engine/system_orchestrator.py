# backend/engine/system_orchestrator.py

from engine.ml_engine import load_ml_scores
from engine.self_tuning_engine import tune_strategies_daily
from engine.goal_aware_shift_engine import shift_portfolio_by_goal
from engine.final_recommendation_engine import generate_final_recommendation

def full_daily_engine_run() -> dict:
    print("?? Loading ML scores...")
    load_ml_scores()

    print("??? Running strategy self-tuning...")
    tune_strategies_daily()

    print("?? Shifting portfolio by user goal...")
    shift_portfolio_by_goal()

    print("?? Generating final recommendation...")
    result = generate_final_recommendation()

    return result
