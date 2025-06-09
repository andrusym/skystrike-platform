import React from 'react';

const StrategyControlPanel = ({ strategy, onToggle }) => {
  return (
    <div className="strategy-control-panel">
      <h4>{strategy.name}</h4>
      <button onClick={() => onToggle(strategy.id)}>
        {strategy.active ? "Pause" : "Resume"}
      </button>
    </div>
  );
};

export default StrategyControlPanel;
