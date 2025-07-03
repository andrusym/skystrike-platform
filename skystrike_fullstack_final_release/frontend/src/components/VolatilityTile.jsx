import React, { useEffect, useState } from "react";
import authFetch from "../utils/authFetch";

const VolatilityTile = () => {
  const [vix, setVix] = useState(null);

  useEffect(() => {
    authFetch("/api/risk/vix")
      .then((res) => res.json())
      .then(setVix);
  }, []);

  if (!vix) return <div>Loading VIX...</div>;

  return (
    <div className="p-4 border rounded shadow bg-white">
      <h3 className="font-semibold">Volatility Index (VIX)</h3>
      <p>Level: {vix.vix}</p>
      <p>Regime: {vix.regime}</p>
    </div>
  );
};

export default VolatilityTile;