import React, { useEffect, useState } from "react";
import authFetch from "../utils/authFetch";

const BotMetricsTile = () => {
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    authFetch("/api/bots/metrics")
      .then((res) => setMetrics(res))
      .catch((err) => console.error("Failed to load bot metrics", err));
  }, []);

  if (!metrics) return <div className="p-4 bg-gray-800 text-white rounded-xl">Loading bot metrics...</div>;

  return (
    <div className="p-4 bg-gray-900 text-white rounded-xl shadow-lg w-full max-w-4xl overflow-auto">
      <h2 className="text-xl font-semibold mb-2">Bot Performance Metrics</h2>
      <table className="w-full text-sm border-collapse">
        <thead>
          <tr className="text-left border-b border-gray-700">
            <th className="pb-1">Strategy</th>
            <th className="pb-1">Trades</th>
            <th className="pb-1">Win Rate</th>
            <th className="pb-1">Net P&L</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(metrics).map(([bot, stat]) => (
            <tr key={bot} className="border-b border-gray-700">
              <td className="py-1 capitalize">{bot}</td>
              <td className="py-1">{stat.trades}</td>
              <td className="py-1">{(stat.winRate * 100).toFixed(1)}%</td>
              <td className="py-1">{stat.netPnl.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default BotMetricsTile;