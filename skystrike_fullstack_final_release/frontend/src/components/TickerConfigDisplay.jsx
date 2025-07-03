import React, { useEffect, useState } from "react";
import authFetch from "../utils/authFetch";

const TickerConfigDisplay = () => {
  const [data, setData] = useState({});

  useEffect(() => {
    const fetchConfig = async () => {
      const res = await authFetch("/data/strategy_allocation.json"); // Static load
      if (res.ok) {
        const json = await res.json();
        setData(json);
      }
    };
    fetchConfig();
  }, []);

  return (
    <div className="p-4 bg-white dark:bg-gray-800 rounded shadow">
      <h2 className="text-lg font-semibold mb-4">Per-Ticker Allocation</h2>
      {Object.entries(data).map(([bot, config]) => (
        <div key={bot} className="mb-4">
          <h3 className="font-bold text-md mb-1">{bot}</h3>
          <table className="w-full text-sm border">
            <thead className="bg-gray-100 dark:bg-gray-700">
              <tr>
                <th className="text-left p-2">Ticker</th>
                <th className="text-right p-2">Capital</th>
                <th className="text-right p-2">Contracts</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(config.tickers).map(([ticker, val]) => (
                <tr key={ticker} className="border-t">
                  <td className="p-2">{ticker}</td>
                  <td className="p-2 text-right">${val.capital.toLocaleString()}</td>
                  <td className="p-2 text-right">{val.contracts}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
    </div>
  );
};

export default TickerConfigDisplay;
