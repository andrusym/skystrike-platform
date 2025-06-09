import React from 'react';

const DailyPLBar = ({ dailyPL, weeklyPL, target }) => {
  return (
    <div className="daily-pl-bar">
      <span>📈 Daily P&L: ${dailyPL}</span>
      <span>📅 Weekly P&L: ${weeklyPL}</span>
      <span>🎯 Target: ${target}</span>
    </div>
  );
};

export default DailyPLBar;
