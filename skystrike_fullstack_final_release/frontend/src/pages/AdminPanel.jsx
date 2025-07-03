import React, { useEffect, useState } from "react";
import authFetch from "../utils/authFetch";

const AdminPanel = () => {
  const [bots, setBots] = useState([]);
  const [error, setError] = useState("");

  const fetchBots = async () => {
    try {
      const res = await authFetch("/api/bots/status");
      setBots(res.bots || []);
    } catch (err) {
      console.error("Failed to fetch bots", err);
      setError("Unable to load bot status.");
    }
  };

  const toggleBot = async (botName, currentStatus) => {
    const newStatus = currentStatus === "active" ? "disabled" : "active";
    try {
      await authFetch("/api/bots/status", {
        method: "PATCH",
        body: JSON.stringify({ name: botName, status: newStatus }),
      });
      fetchBots();
    } catch (err) {
      console.error("Toggle failed:", err);
      setError("Failed to toggle bot.");
    }
  };

  useEffect(() => {
    fetchBots();
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Admin Panel - Bot Controls</h2>
      {error && <div className="text-red-600 mb-4">{error}</div>}
      <div className="space-y-2">
        {bots.map((bot) => (
          <div key={bot.name} className="flex justify-between items-center bg-gray-100 px-4 py-2 rounded">
            <span className="font-medium">{bot.name}</span>
            <span className={`text-sm ${bot.status === "active" ? "text-green-600" : "text-gray-500"}`}>
              {bot.status}
            </span>
            <button
              onClick={() => toggleBot(bot.name, bot.status)}
              className={`px-3 py-1 rounded text-white ${
                bot.status === "active" ? "bg-red-600" : "bg-green-600"
              }`}
            >
              {bot.status === "active" ? "Disable" : "Enable"}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AdminPanel;