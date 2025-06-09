
import datetime
import numpy as np
from ml_scoring import StrategyScorer
from order_executor import execute_trade, close_trade
from utils.option_chain import get_option_chain
from risk_manager import check_exit_conditions
from trade_logger import log_trade
from uuid import uuid4
import random

class StrategyEngine:
    def __init__(self, ticker, capital, strategy_type, config, mode="paper"):
        self.ticker = ticker
        self.capital = capital
        self.strategy_type = strategy_type
        self.config = config
        self.mode = mode
        self.scorer = StrategyScorer()
        self.open_trades = []

    def run(self):
        score = self.scorer.score_strategy(self.ticker, self.strategy_type)
        if score < self.config.get("min_score", 0.5):
            return "Strategy skipped due to low score"
        setup = self.find_trade_setup()
        if not setup:
            return "No valid setup found"
        trade_id = str(uuid4())
        trade = execute_trade(self.ticker, setup, self.capital, trade_id=trade_id, mode=self.mode)
        self.open_trades.append(trade)
        log_trade(trade)
        return f"Trade executed: {trade_id}"

    def find_trade_setup(self):
        chain = get_option_chain(self.ticker)
        if not chain or "calls" not in chain or "puts" not in chain:
            return None
        if self.strategy_type == "iron_condor":
            return self.build_iron_condor(chain)
        elif self.strategy_type == "iron_fly":
            return self.build_iron_fly(chain)
        elif self.strategy_type == "calendar_spread":
            return self.build_calendar_spread(chain)
        return None

    def build_iron_condor(self, chain):
        calls = sorted(chain["calls"].items())
        puts = sorted(chain["puts"].items())
        if len(calls) < 4 or len(puts) < 4:
            return None
        idx = len(calls) // 2
        return {
            "type": "iron_condor",
            "legs": {
                "short_call": calls[idx],
                "long_call": calls[idx + 2],
                "short_put": puts[idx],
                "long_put": puts[idx + 2]
            },
            "entry_time": datetime.datetime.now().isoformat()
        }

    def build_iron_fly(self, chain):
        strikes = list(set(chain["calls"].keys()) & set(chain["puts"].keys()))
        if not strikes:
            return None
        atm_strike = sorted(strikes)[len(strikes) // 2]
        return {
            "type": "iron_fly",
            "legs": {
                "short_call": (atm_strike, chain["calls"][atm_strike]),
                "short_put": (atm_strike, chain["puts"][atm_strike]),
                "long_call": chain["calls"].get(atm_strike + 10),
                "long_put": chain["puts"].get(atm_strike - 10)
            },
            "entry_time": datetime.datetime.now().isoformat()
        }

    def build_calendar_spread(self, chain):
        expirations = sorted(set(option["expiration"] for option in chain["calls"].values()))
        if len(expirations) < 2:
            return None
        near_exp = expirations[0]
        far_exp = expirations[1]
        strike = sorted(chain["calls"].keys())[len(chain["calls"]) // 2]
        return {
            "type": "calendar_spread",
            "legs": {
                "short_call": (strike, near_exp),
                "long_call": (strike, far_exp)
            },
            "entry_time": datetime.datetime.now().isoformat()
        }

    def check_exits(self):
        for trade in self.open_trades[:]:
            if check_exit_conditions(trade):
                close_trade(trade)
                log_trade(trade, closed=True)
                self.open_trades.remove(trade)

    def simulate_bulk_run(self, tickers):
        results = {}
        for t in tickers:
            self.ticker = t
            result = self.run()
            results[t] = result
        return results

    def status_report(self):
        return {
            "active_trades": len(self.open_trades),
            "open_trade_ids": [trade.get("id") for trade in self.open_trades],
            "strategy": self.strategy_type,
            "mode": self.mode
        }
