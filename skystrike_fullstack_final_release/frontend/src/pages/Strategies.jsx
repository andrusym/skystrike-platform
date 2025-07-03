import React, { useEffect, useState } from "react";
import authFetch from "../utils/authFetch";

const TICKERS = ["SPX", "NDX", "QQQ", "SPY", "XSP", "IWM"];

const Strategies = () => {
  const [bots, setBots] = useState([]);
  const [mlScores, setMlScores] = useState({});
  const [sizing, setSizing] = useState({});
  const [loading, setLoading] = useState(true);
  const [isTriggering, setIsTriggering] = useState(false);

  useEffect(() => {
    Promise.all([
      authFetch("/api/bots/status").then((res) => res.json()),
      authFetch("/api/ml/scores").then((res) => res.json()),
      authFetch("/api/portfolio/sizing-preview").then((res) => res.json()),
    ])
      .then(([botData, scoreData, sizingData]) => {
        setBots(botData);
        setMlScores(scoreData);
        setSizing(sizingData);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to load strategy data:", err);
        setLoading(false);
      });
  }, []);

  const runBot = async (botName, ticker) => {
    try {
      setIsTriggering(true);
      const res = await authFetch(`/api/bots/trigger/${botName}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ticker, contracts: 2 }),
      });
      const data = await res.json();
      alert(`? ${botName} triggered on ${ticker}: ${data.message || "OK"}`);
    } catch (err) {
      alert(`?? Error triggering ${botName} on ${ticker}`);
    } finally {
      setIsTriggering(false);
    }
  };

  return (
    <div className="p-6 text-white">
      <h1 className="text-2xl font-bold mb-4">Strategy Controls</h1>

      {loading ? (
        <div className="text-gray-400">Loading strategies...</div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
            {bots.map((bot) => (
              <div key={bot.name} className="bg-gray-900 p-4 rounded-xl shadow-md">
                <div className="text-xl font-semibold capitalize mb-1">{bot.name || "Unnamed Bot"}</div>
                <div className="text-sm text-gray-400 mb-1">
                  Status: <span className="font-medium text-white">{bot.status}</span>
                </div>
                <div className="mb-2">
                  {TICKERS.map((ticker) => {
                    const score = mlScores?.[bot.name]?.[ticker]?.confidence ?? null;
                    return (
                      <div key={ticker} className="flex items-center justify-between mb-1">
                        <div className="text-sm">{ticker}</div>
                        <div className="flex items-center gap-2">
                          <span className="text-sm text-green-400">
                            {score !== null ? `Confidence: ${(score * 100).toFixed(1)}%` : "N/A"}
                          </span>
                          <button
                            disabled={isTriggering}
                            className={`px-2 py-1 text-xs rounded ${
                              isTriggering ? "bg-gray-600" : "bg-blue-600 hover:bg-blue-700"
                            }`}
                            onClick={() => runBot(bot.name, ticker)}
                          >
                            ? Run
                          </button>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>

          <h2 className="text-xl font-bold mb-3">Contract Sizing Preview</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.keys(sizing).map((bot) => (
              <div key={bot} className="bg-gray-800 p-4 rounded-lg">
                <div className="font-semibold text-lg mb-2 capitalize">{bot}</div>
                {Object.entries(sizing[bot]).map(([ticker, qty]) => (
                  <div key={ticker} className="flex justify-between text-sm border-b border-gray-700 py-1">
                    <span>{ticker}</span>
                    <span className="text-yellow-300">{qty} contracts</span>
                  </div>
                ))}
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
};

export default Strategies;
