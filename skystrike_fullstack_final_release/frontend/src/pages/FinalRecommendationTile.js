
import React, { useEffect, useState } from "react";
import authFetch from "../utils/authFetch";

const FinalRecommendationTile = () => {
  const [rec, setRec] = useState(null);

  useEffect(() => {
    authFetch("/api/portfolio/final-recommendation").then(setRec);
  }, []);

  if (!rec) return <div>Loading Final Recommendation...</div>;

  return (
    <div>
      <h3>Final Allocation Recommendation</h3>
      <ul>
        {Object.entries(rec.adjusted_allocation).map(([bot, value]) => (
          <li key={bot}>{bot}: {value} contracts</li>
        ))}
      </ul>
    </div>
  );
};

export default FinalRecommendationTile;
