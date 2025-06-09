import BacktestOverlay from './components/BacktestOverlay';
import StrategyScoreOverlay from './components/StrategyScoreOverlay';
import React from "react";

const StrategyCard = ({ strategy }) => {
  return (
    <div className="strategy-card">
      <h2>{strategy.name}</h2>
      <p>Status: {strategy.status}</p>
      <p>Contracts: {strategy.contracts}</p>
      <p>P&L: ${strategy.pnl}</p>
    </div>
  );
};


const mockScore = 87;
const mockBacktest = {
  winRate: 72.4,
  avgProfit: 185.6,
  maxDrawdown: -640.0,
  sampleSize: 140
};

return (
  <div className="strategy-card">
    <StrategyScoreOverlay score={mockScore} />
    <BacktestOverlay stats={mockBacktest} visible={true} />
    {/* existing card content here */}
  </div>
);
export default StrategyCard;
