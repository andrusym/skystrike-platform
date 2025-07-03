
import React, { useEffect, useState } from "react";
import authFetch from "../utils/authFetch";

const Positions = () => {
  const [positions, setPositions] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchPositions = async () => {
      const res = await authFetch("/api/positions");
      const json = await res.json();
      if (res.ok) setPositions(Array.isArray(json) ? json : [json]);
      else setError(json.error || "Failed to load positions");
    };
    fetchPositions();
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-xl font-bold mb-4">Current Positions</h2>
      {error && <p className="text-red-600">{error}</p>}
      <pre className="bg-gray-100 p-4 rounded text-sm">{JSON.stringify(positions, null, 2)}</pre>
    </div>
  );
};

export default Positions;
