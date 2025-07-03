import React, { useEffect, useState } from "react";
import authFetch from "../utils/authFetch";
import GoalSelector from "../components/GoalSelector";
import BotMetricsTile from "../components/BotMetricsTile";
import ContractSizingTile from "../components/ContractSizingTile";

const Dashboard = () => {
  const [metrics, setMetrics] = useState(null);
  const [recommendation, setRecommendation] = useState(null);
  const [lastUpdate, setLastUpdate] = useState(null);
  const [reloadFlag, setReloadFlag] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);

    Promise.all([
      authFetch("/api/dashboard"),
      authFetch("/api/portfolio/final-recommendation"),
      authFetch("/api/config/last-update")
    ])
      .then(([metricsRes, recRes, configLog]) => {
        setMetrics(metricsRes);
        setRecommendation(recRes?.final_profile || "Unknown");
        setLastUpdate(configLog?.timestamp || null);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to load dashboard data:", err);
        setLoading(false);
      });
  }, [reloadFlag]);

  const triggerReload = () => setReloadFlag((prev) => !prev);
  const safe = (val, fallback = "N/A") => (val !== null && val !== undefined ? val : fallback);

  return (
    <div className="p-6 space-y-6 text-white">
      <h1 className="text-3xl font-bold mb-4">SkyStrike Dashboard</h1>

      {loading && <div>Loading metrics...</div>}

      {!loading && metrics && (
        <>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            <Tile label="Net P&L" value={`$${safe(metrics.netPnL?.toFixed(2))}`} />
            <Tile label="Win Rate" value={`${safe((metrics.winRate * 100).toFixed(1))}%`} />
            <Tile label="Active Strategies" value={safe(metrics.activeStrategies)} />
            <Tile label="Fallback Triggered" value={safe(metrics.mlEngine?.fallbacksTriggered)} color="text-yellow-400" />
            <Tile label="SPY Price" value={`$${safe(metrics.spyPrice?.last?.toFixed(2))}`} />
            <Tile label="VIX" value={safe(metrics.vixPrice?.last?.toFixed(2))} />
            <Tile label="Capital Allocated" value={`$${safe(metrics.capital?.allocated)}`} />
            <Tile label="Capital Available" value={`$${safe(metrics.capital?.available)}`} />
            {recommendation && (
              <div className="col-span-2 md:col-span-3 p-4 bg-gray-800 rounded-xl shadow">
                <div className="text-sm text-gray-400">?? ML Final Recommendation</div>
                <div className="text-xl font-bold mt-1">{recommendation}</div>
                <div className="mt-2 text-sm text-gray-300">
                  Based on win rate, volatility, cash, and tuning logic.
                </div>
                {lastUpdate && (
                  <div className="flex items-center text-xs text-green-400 mt-2">
                    <span title={`Synced at ${new Date(lastUpdate).toLocaleString()}`}>?? Last Sync</span>
                  </div>
                )}
              </div>
            )}
          </div>

          <GoalSelector onUpdate={triggerReload} />
          <BotMetricsTile />
          <ContractSizingTile />
        </>
      )}

      {!loading && !metrics && (
        <div className="text-red-400">Failed to load dashboard data.</div>
      )}
    </div>
  );
};

const Tile = ({ label, value, color = "text-white" }) => (
  <div className="p-4 bg-gray-900 rounded-xl shadow">
    <div className="text-sm text-gray-400">{label}</div>
    <div className={`text-2xl font-bold ${color}`}>{value}</div>
  </div>
);

export default Dashboard;
