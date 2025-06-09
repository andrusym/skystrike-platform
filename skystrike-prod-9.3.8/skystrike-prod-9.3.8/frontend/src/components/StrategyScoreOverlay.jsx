import React from 'react';

const StrategyScoreOverlay = ({ score }) => {
  const color = score >= 80 ? 'green' : score >= 50 ? 'orange' : 'red';
  return (
    <div className="strategy-score" style={{ color }}>
      ML Score: {score}%
    </div>
  );
};

export default StrategyScoreOverlay;
