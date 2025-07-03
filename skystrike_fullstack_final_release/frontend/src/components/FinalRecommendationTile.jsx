import React, { useEffect, useState } from "react";
import authFetch from "../utils/authFetch";

const FinalRecommendationTile = () => {
  const [allocation, setAllocation] = useState({});
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await authFetch("/api/portfolio/final-recommendation");
        const json = await res.json();
        if (res.ok) {
          setAllocation(json.adjusted_allocation || {});
        } else {
          setError("Failed to fetch recommendation");
        }
      } catch (err) {
        setError("Error loading recommendation");
      }
    };

    fetchData();
  }, []);

  if (error) return <div className="text-red-500">{error}</div>;

  return (
    <div className="bg-white rounded-xl shadow p-4 border">
      <div className="text-lg font-semibold text-gray-800 mb-2">Final Allocation Recommendation</div>
      {Object.keys(allocation).length === 0 ? (
        <div className="text-sm text-gray-500">No recommendation data available.</div>
      ) : (
        <ul className="text-sm text-gray-700 list-disc list-inside">
          {Object.entries(allocation).map(([bot, value]) => (
            <li key={bot}>
              {bot}: {value}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default FinalRecommendationTile;
