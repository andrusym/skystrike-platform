import React, { useEffect, useState } from "react";
import authFetch from "../utils/authFetch";

const JournalPage = () => {
  const [trades, setTrades] = useState([]);

  useEffect(() => {
    authFetch("/api/journal/enhanced")
      .then((res) => res.json())
      .then(data => setTrades(data.trades || []));
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-2">Trade Journal</h1>
      <table className="table-auto w-full text-sm">
        <thead><tr><th>Strategy</th><th>Ticker</th><th>P&L</th></tr></thead>
        <tbody>
          {trades.map((t, i) => (
            <tr key={i}><td>{t.strategy}</td><td>{t.ticker}</td><td>{t.pnl}</td></tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default JournalPage;