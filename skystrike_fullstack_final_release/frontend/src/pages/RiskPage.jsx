
import React, { useEffect, useState } from "react";
import authFetch from "../utils/authFetch";

const RiskPage = () => {
  const [metrics, setMetrics] = useState({});
  useEffect(() => {
    const fetchAll = async () => {
      const m = await authFetch("/api/risk/metrics");
      const c = await authFetch("/api/risk/correlation");
      const d = await authFetch("/api/risk/drawdown");
      const t = await authFetch("/api/risk/throttle");
      setMetrics({ m, c, d, t });
    };
    fetchAll();
  }, []);

  return (
    <div>
      <h2>Risk Metrics</h2>
      <pre>{JSON.stringify(metrics, null, 2)}</pre>
    </div>
  );
};

export default RiskPage;
