import React, { useEffect, useState } from "react";
import authFetch from "../utils/authFetch";

const TradesPage = () => {
  const [trades, setTrades] = useState([]);

  useEffect(() => {
    authFetch("/api/trades")
      .then(res => res.json())
      .then(setTrades)
      .catch(console.error);
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Trade History</h2>
      <table className="min-w-full bg-white rounded shadow">
        <thead><tr><th>Strategy</th><th>Status</th><th>PnL</th></tr></thead>
        <tbody>
          {trades.map((t, i) => (
            <tr key={i}>
              <td>{t.strategy}</td>
              <td>{t.status}</td>
              <td>{t.pnl}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TradesPage;