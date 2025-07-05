#!/usr/bin/env python3
# coding: utf-8

from backend.ml.ml_engine import run as run_ml
from backend.engine.self_tuning_engine import tune_strategies_daily
from backend.engine.goal_aware_shift_engine import apply_goal_allocation
from backend.engine.final_recommendation_engine import generate_final_recommendation

def full_daily_engine_run() -> dict:
    print("Loading ML results...")
    ml_results = run_ml({})

    print("Running strategy self-tuning...")
    tune_strategies_daily()

    print("Applying goal-aware shift...")
    apply_goal_allocation(ml_results)

    print("Generating final recommendation...")
    return generate_final_recommendation()
