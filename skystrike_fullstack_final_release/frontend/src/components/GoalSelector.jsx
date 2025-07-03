import React, { useState } from "react";
import authFetch from "../utils/authFetch";

const GoalSelector = ({ onUpdate }) => {
  const [selected, setSelected] = useState("growth");

  const handleSelect = async (goal) => {
    setSelected(goal);
    try {
      await authFetch("/api/portfolio/goal", {
        method: "POST",
        body: JSON.stringify({ goal }),
      });
      if (onUpdate) onUpdate(); // callback to refresh data
    } catch (err) {
      console.error("Failed to update goal", err);
    }
  };

  const goals = ["growth", "income", "preserve"];

  return (
    <div className="mb-4 p-3 bg-gray-800 rounded-xl text-sm text-white shadow-md">
      <span className="mr-4 font-semibold">Goal:</span>
      {goals.map((goal) => (
        <button
          key={goal}
          className={`mr-2 px-3 py-1 rounded-full ${selected === goal ? "bg-blue-600" : "bg-gray-600"}`}
          onClick={() => handleSelect(goal)}
        >
          {goal.charAt(0).toUpperCase() + goal.slice(1)}
        </button>
      ))}
    </div>
  );
};

export default GoalSelector;
