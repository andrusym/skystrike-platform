import React, { useEffect, useState } from "react";
import authFetch from "../utils/authFetch";

const DrawdownGuardTile = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    authFetch("/api/risk/status")
      .then((res) => res.json())
      .then(setData);
  }, []);

  if (!data) return <div>Loading drawdown guard...</div>;

  return (
    <div className="p-4 border rounded shadow bg-white">
      <h3 className="font-semibold">Drawdown Guard</h3>
      <p>Status: {data.status}</p>
      <p>Threshold: {data.threshold}%</p>
      <p>Current: {data.current_drawdown}%</p>
    </div>
  );
};

export default DrawdownGuardTile;