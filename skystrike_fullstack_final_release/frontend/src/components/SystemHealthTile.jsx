import React, { useEffect, useState } from "react";
import authFetch from "../utils/authFetch";

const SystemHealthTile = () => {
  const [health, setHealth] = useState(null);

  useEffect(() => {
    authFetch("/api/system/health")
      .then(res => res.json())
      .then(data => setHealth(data));
  }, []);

  if (!health) return <div>Loading health...</div>;

  return (
    <div>
      <h3>System Health</h3>
      <ul>
        {Object.entries(health).map(([key, value]) => (
          <li key={key}>{key}: {value}</li>
        ))}
      </ul>
    </div>
  );
};

export default SystemHealthTile;
