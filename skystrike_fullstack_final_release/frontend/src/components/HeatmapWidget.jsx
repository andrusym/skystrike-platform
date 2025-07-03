import React from "react";
const HeatmapWidget = ({ heatmap }) => {
  return (
    <div className="bg-white shadow p-4 rounded">
      <h4 className="text-lg font-bold mb-2">Strategy Heatmap</h4>
      <pre className="text-xs bg-gray-100 p-2 rounded overflow-x-auto">{JSON.stringify(heatmap, null, 2)}</pre>
    </div>
  );
};

export default HeatmapWidget;
