
# scenario_stress_tester.py

import logging
utils.market_data import simulate_market_event
utils.database import get_portfolio_snapshot, save_stress_test_result

class ScenarioStressTester:
    def __init__(self, user_id):
        self.user_id = user_id

    def run_scenarios(self, scenarios=None):
        scenarios = scenarios or ["vix_spike", "rate_hike", "earnings_crash", "macro_shock"]
        snapshot = get_portfolio_snapshot(self.user_id)
        results = {}

        for scenario in scenarios:
            try:
                stress_result = simulate_market_event(snapshot, scenario)
                results[scenario] = stress_result
                save_stress_test_result(self.user_id, scenario, stress_result)
                logging.info(f"[StressTester] Scenario '{scenario}' completed for user {self.user_id}")
            except Exception as e:
                logging.error(f"[StressTester] Failed scenario '{scenario}': {e}")
                results[scenario] = {"error": str(e)}

        return results
