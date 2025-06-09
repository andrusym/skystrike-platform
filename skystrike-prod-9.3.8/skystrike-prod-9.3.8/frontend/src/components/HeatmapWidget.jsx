import React from 'react';

const HeatmapWidget = ({ data }) => {
  return (
    <div className="heatmap-widget">
      <h3>Strategy Heatmap</h3>
      {data.map((item, idx) => (
        <div key={idx}>
          <strong>{item.strategy}</strong>: {item.intensity}%
        </div>
      ))}
    </div>
  );
};

export default HeatmapWidget;
