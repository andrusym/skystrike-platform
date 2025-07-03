import React from "react";

const DashboardCard = ({ label, value, highlight = "#2e6ad9" }) => {
  return (
    <div
      className="bg-white p-4 rounded-lg shadow border-l-4"
      style={{ borderColor: highlight }}
    >
      <div className="text-sm text-gray-500">{label}</div>
      <div className="text-xl font-semibold">{value}</div>
    </div>
  );
};

export default DashboardCard;
