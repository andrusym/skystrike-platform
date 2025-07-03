import React, { useState } from "react";
import authFetch from "../utils/authFetch";

const BacktestPage = () => {
  const [result, setResult] = useState(null);

  const runBacktest = async () => {
    const res = await authFetch("/api/backtest/run?strategy=ironcondor&ticker=SPY&start=2024-01-01&end=2024-12-31", { method: "POST" });
    const json = await res.json();
    setResult(json);
  };

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-2">Backtest</h1>
      <button onClick={runBacktest} className="bg-blue-600 text-white px-3 py-1 rounded">Run</button>
      {result && <pre className="mt-4 bg-gray-100 p-2">{JSON.stringify(result, null, 2)}</pre>}
    </div>
  );
};

export default BacktestPage;