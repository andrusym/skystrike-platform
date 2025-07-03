import React, { useEffect, useState } from "react";
import authFetch from "../utils/authFetch";

const ContractSizingTile = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    authFetch("/api/portfolio/sizing-preview")
      .then((res) => setData(res))
      .catch((err) => console.error("Failed to load sizing preview", err));
  }, []);

  if (!data) return <div className="p-4 bg-gray-800 text-white rounded-xl">Loading sizing preview...</div>;

  return (
    <div className="p-4 bg-gray-900 text-white rounded-xl shadow-lg w-full max-w-3xl">
      <h2 className="text-xl font-semibold mb-2">Contract Sizing Preview</h2>
      <table className="w-full text-sm border-collapse">
        <thead>
          <tr className="text-left border-b border-gray-700">
            <th className="pb-1">Strategy</th>
            <th className="pb-1">Recommended Contracts</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(data).map(([bot, count]) => (
            <tr key={bot} className="border-b border-gray-700">
              <td className="py-1 capitalize">{bot}</td>
              <td className="py-1">{count}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ContractSizingTile;