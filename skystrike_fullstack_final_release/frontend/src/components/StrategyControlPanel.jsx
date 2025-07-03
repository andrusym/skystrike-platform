import React from "react";

const statusColor = {
  active: "bg-green-100 text-green-800",
  cooldown: "bg-yellow-100 text-yellow-800",
  disabled: "bg-red-100 text-red-800",
};

const getStrategyTypeStyle = (type) => {
  switch (type) {
    case "condor":
      return "border-l-4 border-blue-500";
    case "trend":
      return "border-l-4 border-purple-500";
    case "wheel":
      return "border-l-4 border-orange-500";
    case "replicator":
      return "border-l-4 border-teal-500";
    default:
      return "border-l-4 border-gray-300";
  }
};

const StrategyControlPanel = ({ bots, onRun, onToggle }) => {
  const entries = Object.entries(bots || {});

  if (entries.length === 0) {
    return <div className="text-gray-500">No strategies found.</div>;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {entries.map(([botName, botData]) => {
        const {
          status = "unknown",
          confidence = null,
          ticker = "SPY",
          last_run = "N/A",
          pnl = null,
          type = "other",
        } = botData;

        const statusClass = statusColor[status] || "bg-gray-100 text-gray-800";
        const styleClass = getStrategyTypeStyle(type);

        return (
          <div key={botName} className={`p-4 border rounded shadow bg-white ${styleClass}`}>
            <div className="flex justify-between items-center mb-2">
              <h2 className="text-lg font-semibold">{botName}</h2>
              <span className={`text-xs px-2 py-1 rounded ${statusClass}`}>
                {status.toUpperCase()}
              </span>
            </div>
            <div className="text-sm text-gray-700">
              <div>Ticker: <span className="font-medium">{ticker}</span></div>
              {confidence !== null && (
                <div>Confidence: <span className="font-medium">{(confidence * 100).toFixed(1)}%</span></div>
              )}
              {pnl !== null && (
                <div>P&L: <span className={`font-medium ${pnl >= 0 ? "text-green-600" : "text-red-600"}`}>
                  ${pnl.toFixed(2)}
                </span></div>
              )}
              <div>Last Run: <span className="text-gray-600">{last_run}</span></div>
            </div>
            <div className="flex gap-2 mt-4">
              <button
                onClick={() => onRun(botName)}
                className="bg-blue-600 hover:bg-blue-700 text-white text-sm px-3 py-1 rounded"
                disabled={status === "disabled"}
              >
                Run Now
              </button>
              <button
                onClick={() => onToggle(botName)}
                className="bg-gray-200 hover:bg-gray-300 text-sm px-3 py-1 rounded"
              >
                Toggle
              </button>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default StrategyControlPanel;