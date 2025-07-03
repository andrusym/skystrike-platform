import React, { useEffect, useState } from "react";
import authFetch from "../utils/authFetch";

const LifecycleStatusTile = () => {
  const [status, setStatus] = useState(null);

  useEffect(() => {
    authFetch("/api/lifecycle/status")
      .then((res) => res.json())
      .then(setStatus);
  }, []);

  if (!status) return <div>Loading lifecycle...</div>;

  return (
    <div className="p-4 border rounded shadow bg-white">
      <h3 className="font-semibold">ML Lifecycle</h3>
      <p>Engine: {status.ml_engine}</p>
      <p>Cooldown: {status.cooldown_active ? "Yes" : "No"}</p>
      <p>Fallbacks: {status.fallbacks_triggered}</p>
    </div>
  );
};

export default LifecycleStatusTile;