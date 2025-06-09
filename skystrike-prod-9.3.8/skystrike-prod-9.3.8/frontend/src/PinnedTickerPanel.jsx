import React from "react";

const PinnedTickerPanel = ({ tickers }) => {
  return (
    <aside className="pinned-ticker-panel">
      <h4>Watchlist</h4>
      <ul>
        {tickers.map((ticker, idx) => (
          <li key={idx}>
            {ticker.symbol}: {ticker.price}
          </li>
        ))}
      </ul>
    </aside>
  );
};

export default PinnedTickerPanel;
