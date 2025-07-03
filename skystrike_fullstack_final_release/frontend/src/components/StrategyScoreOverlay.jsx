import React from "react";
const StrategyScoreOverlay = ({ score }) => {
  return (
    <div className="bg-blue-50 border border-blue-300 p-4 rounded shadow text-sm">
      <h5 className="font-semibold text-blue-800">ML Score: {score}</h5>
    </div>
  );
};

export default StrategyScoreOverlay;
