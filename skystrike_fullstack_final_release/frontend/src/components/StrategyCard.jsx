import StrategyScoreOverlay from './components/StrategyScoreOverlay';
import BacktestOverlay from './components/BacktestOverlay';

const StrategyCard = ({ strategy }) => {
  const mockScore = 87;
  const mockBacktest = {
    winRate: 72.4,
    avgProfit: 185.6,
    maxDrawdown: -640.0,
    sampleSize: 140
  };

  return (
    <div className="bg-white shadow rounded p-4 relative w-full max-w-md mx-auto mb-4">
      <StrategyScoreOverlay score={mockScore} />
      <BacktestOverlay stats={mockBacktest} visible={true} />
      <h2 className="text-lg font-bold mb-2">{strategy.name}</h2>
      <p className="text-sm text-gray-700">Status: {strategy.status}</p>
      <p className="text-sm text-gray-700">Contracts: {strategy.contracts}</p>
      <p className="text-sm text-gray-700">P&L: ${strategy.pnl}</p>
    </div>
  );
};

export default StrategyCard;
