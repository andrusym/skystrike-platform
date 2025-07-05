"""
SkyStrike Engine: Strategy Entry, Lifecycle Management, and ML Tuning
"""

import logging

from .bot_entry_engine            import run_all_bots
from .dynamic_dte_selector        import choose_optimal_dte
from .explainability_engine       import get_explanation
from .final_recommendation_engine import generate_final_recommendation
from .goal_aware_shift_engine     import apply_goal_allocation
from .market_event_filter         import should_skip_today
from .ml_engine                   import load_ml_scores, evaluate_ml_status
from .performance_engine          import compute_metrics
from .position_tracker            import update_open_positions
from .plugin_loader               import run_hook
from .quote_stream_engine         import start_streaming_quotes
from .reinforcement_engine        import adapt_allocation
from .risk_budget_engine          import enforce_risk_budget
from .runner_dispatcher           import dispatch_bot_by_name
from .self_tuning_engine          import tune_strategies_daily
from .strategy_config             import load_strategy_config
from .strategy_cooldown_engine    import check_and_apply_cooldowns
from .strategy_lifecycle          import evaluate_strategy_lifecycle
from .trade_router                import route_trade_execution
from .trading_engine              import execute_trade
from .volatility_engine           import get_vix_level, classify_volatility_regime
from .adaptive_sizing_engine      import adjust_contract_size
from .bot_decay_monitor           import check_drawdown, should_deactivate_bot
from .alert_engine                import send_alert

logger = logging.getLogger(__name__)

__all__ = [
    "run_all_bots",
    "dispatch_bot_by_name",
    "generate_final_recommendation",
    "load_ml_scores",
    "evaluate_ml_status",
    "tune_strategies_daily",
    "apply_goal_allocation",
    "load_strategy_config",
    "check_and_apply_cooldowns",
    "evaluate_strategy_lifecycle",
    "route_trade_execution",
    "execute_trade",
    "run_hook",
    "get_vix_level",
    "classify_volatility_regime",
    "compute_metrics",
    "update_open_positions",
    "start_streaming_quotes",
    "check_drawdown",
    "should_deactivate_bot",
    "adjust_contract_size",
    "choose_optimal_dte",
    "get_explanation",
    "adapt_allocation",
    "enforce_risk_budget",
    "send_alert",
    "should_skip_today",
]
