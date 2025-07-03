import React, { useEffect, useState } from "react";
import authFetch from "../utils/authFetch";

const Orders = () => {
  const [orders, setOrders] = useState([]);
  const [bots, setBots] = useState({});
  const [mlScores, setMlScores] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchOrders();
    fetchBots();
    fetchMlScores();
  }, []);

  const fetchOrders = () => {
    setLoading(true);
    authFetch("/api/broker/orders/summary")
      .then((res) => setOrders(res || []))
      .catch((err) => console.error("Failed to load orders:", err))
      .finally(() => setLoading(false));
  };

  const fetchBots = () => {
    authFetch("/api/bots/status")
      .then((res) => setBots(res || {}))
      .catch((err) => console.error("Failed to load bots:", err));
  };

  const fetchMlScores = () => {
    authFetch("/api/ml/scores")
      .then((res) => setMlScores(res || {}))
      .catch((err) => console.error("Failed to load ML scores:", err));
  };

  const runBot = (botName, ticker, contracts) => {
    authFetch(`/api/bots/trigger/${botName}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ticker, contracts }),
    })
      .then(() => {
        alert(`Bot ${botName} triggered for ${ticker} (${contracts} contracts)`);
        fetchOrders();
      })
      .catch(() => alert("Error triggering bot"));
  };

  return (
    <div className="p-6 text-white">
      <h1 className="text-2xl font-bold mb-6">Orders</h1>

      <div className="mb-10">
        <h2 className="text-lg font-semibold mb-4">Trigger a Bot</h2>
        <div className="space-y-4">
          {Object.entries(bots).map(([botName, botData]) => {
            const defaultTicker = Object.keys(botData.tickers || {})[0] || "SPY";
            const defaultContracts = Object.values(botData.tickers || {})[0] || 1;
            const score = mlScores?.[botName]?.confidence || 0;
            const isDisabled =
              botData.status === "cooldown" ||
              botData.fallback_active === true ||
              score < 0.5;

            return (
              <div key={botName} className="bg-gray-900 p-4 rounded shadow">
                <div className="mb-2 font-bold capitalize">{botName}</div>

                <div className="mb-1 text-sm text-gray-300">
                  ML Confidence:{" "}
                  <span
                    className={
                      score >= 0.75
                        ? "text-green-400"
                        : score >= 0.5
                        ? "text-yellow-300"
                        : "text-red-400"
                    }
                    title="Confidence from ML scoring engine"
                  >
                    {score ? `${(score * 100).toFixed(1)}%` : "n/a"}
                  </span>
                </div>

                <div className="flex flex-wrap items-center gap-2">
                  <input
                    type="text"
                    id={`ticker-${botName}`}
                    defaultValue={defaultTicker}
                    placeholder="Ticker"
                    className="p-2 rounded text-black"
                  />
                  <input
                    type="number"
                    id={`contracts-${botName}`}
                    defaultValue={defaultContracts}
                    min={1}
                    className="p-2 rounded text-black"
                  />
                  <button
                    className={`px-4 py-2 rounded text-sm ${
                      isDisabled
                        ? "bg-gray-600 cursor-not-allowed"
                        : "bg-blue-600 hover:bg-blue-700"
                    }`}
                    onClick={() => {
                      if (isDisabled) {
                        alert("Bot is in cooldown, fallback, or confidence too low");
                        return;
                      }
                      const ticker = document
                        .getElementById(`ticker-${botName}`)
                        .value.toUpperCase();
                      const contracts = parseInt(
                        document.getElementById(`contracts-${botName}`).value
                      );
                      runBot(botName, ticker, contracts);
                    }}
                    disabled={isDisabled}
                  >
                    ?? Run {botName}
                  </button>

                  {botData.status === "cooldown" && (
                    <span className="text-yellow-400 text-xs ml-2">Cooldown Active</span>
                  )}
                  {botData.fallback_active && (
                    <span className="text-red-400 text-xs ml-2">Fallback Triggered</span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div>
        <h2 className="text-lg font-semibold mb-4">Recent Orders</h2>
        {loading ? (
          <div>Loading orders...</div>
        ) : orders.length === 0 ? (
          <div className="text-gray-400">No orders found.</div>
        ) : (
          <div className="space-y-2">
            {orders.map((order, idx) => (
              <div key={idx} className="p-4 bg-gray-800 rounded shadow text-sm">
                <div className="text-gray-300">Symbol: {order.symbol}</div>
                <div className="text-gray-300">Status: {order.status}</div>
                <div className="text-gray-300">Quantity: {order.quantity}</div>
                <div className="text-gray-300">Price: {order.price}</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Orders;
