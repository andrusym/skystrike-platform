import React from "react";

const PerformanceSummary = ({ summary }) => {
  return (
    <div className="performance-summary">
      <h3>Daily P&L: ${summary.daily}</h3>
      <h3>Weekly P&L: ${summary.weekly}</h3>
    </div>
  );
};

export default PerformanceSummary;
