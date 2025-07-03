import React, { useEffect, useState } from "react";
import authFetch from "../utils/authFetch";

const Wealth = () => {
  const [cash, setCash] = useState(null);
  const [holdings, setHoldings] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      authFetch("/api/wealth/cash").then((res) => res.json()),
      authFetch("/api/wealth/holdings").then((res) => res.json()),
    ])
      .then(([cashData, holdingsData]) => {
        setCash(cashData);
        setHoldings(holdingsData);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error loading wealth data", err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="p-6 text-white">
      <h1 className="text-2xl font-bold mb-4">Wealth Summary</h1>

      {loading ? (
        <div className="text-gray-400">Loading...</div>
      ) : (
        <>
          <div className="mb-6">
            <div className="text-sm text-gray-400">Cash Available</div>
            <div className="text-3xl font-bold text-green-400">
              ${cash?.cash?.toFixed(2)}
            </div>
          </div>

          <div>
            <h2 className="text-xl font-semibold mb-2">ETF Holdings</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {holdings?.holdings?.map((item) => (
                <div
                  key={item.ticker}
                  className="bg-gray-800 p-4 rounded-lg shadow"
                >
                  <div className="text-lg font-bold">{item.ticker}</div>
                  <div className="text-sm text-gray-400">
                    Shares: {item.shares}
                  </div>
                  <div className="text-sm text-gray-400">
                    Price: ${item.price?.toFixed(2)}
                  </div>
                  <div className="text-sm text-white font-semibold">
                    Value: ${item.value?.toFixed(2)}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default Wealth;
