import React from "react";
const PinnedTickerPanel = ({ tickers }) => {
  return (
    <aside className="bg-gray-100 border rounded p-4 w-full max-w-sm shadow mb-4">
      <h4 className="font-semibold text-gray-800 mb-2">📌 Watchlist</h4>
      <ul className="text-sm text-gray-700 space-y-1">
        {tickers.map((ticker, idx) => (
          <li key={idx}>
            {ticker.symbol}: <span className="font-mono">${ticker.price}</span>
          </li>
        ))}
      </ul>
    </aside>
  );
};

export default PinnedTickerPanel;
