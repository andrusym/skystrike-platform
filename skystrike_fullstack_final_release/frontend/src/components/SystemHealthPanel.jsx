import React, { useEffect, useState } from "react";
import authFetch from "@/utils/authFetch";

const Badge = ({ label, status }) => {
  const color = status === "OK" ? "bg-green-500" :
                status === "STALE" ? "bg-yellow-500" : "bg-red-500";
  return (
    <span className={`inline-block px-2 py-1 text-white text-xs rounded ${color}`}>
      {label}
    </span>
  );
};

const SystemHealthPanel = () => {
  const [health, setHealth] = useState(null);

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const res = await authFetch("/api/system/health");
        const data = await res.json();
        setHealth(data);
      } catch (err) {
        console.error("Health fetch error:", err);
      }
    };

    fetchHealth();
    const interval = setInterval(fetchHealth, 15000);
    return () => clearInterval(interval);
  }, []);

  if (!health) return <p className="text-gray-500 text-sm">Loading system health...</p>;

  return (
    <div className="bg-white shadow p-4 rounded mt-6">
      <h3 className="text-lg font-bold mb-2">System Health</h3>
      <ul className="space-y-1 text-sm text-gray-700">
        <li>ML Engine: <Badge label={health.ml_heartbeat} status={health.ml_heartbeat} /></li>
        <li>Retry Loop: {health.retry_loop_status}</li>
        <li>Broker Ping: {health.broker_ping_ms} ms</li>
        <li>Degrade Mode: {health.degrade_state ? "Yes" : "No"}</li>
        <li>Last Updated: {new Date(health.last_updated).toLocaleString()}</li>
      </ul>
    </div>
  );
};

export default SystemHealthPanel;
