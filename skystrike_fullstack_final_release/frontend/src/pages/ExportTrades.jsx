import React, { useState } from "react";
import authFetch from "../utils/authFetch";

const ExportTrades = () => {
  const [message, setMessage] = useState("");

  const handleExport = () => {
    authFetch("/api/trades/export")
      .then((res) => res.blob())
      .then((blob) => {
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = "trades_export.csv";
        link.click();
        setMessage("CSV downloaded!");
      })
      .catch(() => setMessage("Export failed."));
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Export Trades</h1>
      <button onClick={handleExport} className="bg-blue-600 text-white px-4 py-2 rounded">
        Download CSV
      </button>
      {message && <div className="mt-2 text-green-600">{message}</div>}
    </div>
  );
};

export default ExportTrades;
