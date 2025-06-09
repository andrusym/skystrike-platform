import React from 'react';

const BacktestOverlay = ({ stats, visible }) => {
  if (!visible) return null;

  return (
    <div className="backtest-overlay">
      <h4>Backtest Results</h4>
      <ul>
        <li>Win Rate: {stats.winRate}%</li>
        <li>Avg Profit: ${stats.avgProfit}</li>
        <li>Max Drawdown: ${stats.maxDrawdown}</li>
        <li>Sample Size: {stats.sampleSize} trades</li>
      </ul>
    </div>
  );
};

export default BacktestOverlay;
