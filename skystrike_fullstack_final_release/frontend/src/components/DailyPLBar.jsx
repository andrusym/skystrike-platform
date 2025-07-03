import React from "react";
const DailyPLBar = ({ pl }) => {
  return (
    <div className="bg-white p-4 shadow rounded">
      <h4 className="text-lg font-semibold">Daily P&L: ${pl}</h4>
    </div>
  );
};

export default DailyPLBar;
