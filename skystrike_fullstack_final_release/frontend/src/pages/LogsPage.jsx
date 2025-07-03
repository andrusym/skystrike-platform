import React, { useEffect, useState } from 'react';
import authFetch from "../utils/authFetch";

const LogsPage = () => {
  const [logs, setLogs] = useState("");

  useEffect(() => {
    const fetchLogs = async () => {
      const result = await authFetch('/api/logs');
      setLogs(result.logs || "No logs found.");
    };
    fetchLogs();
    const interval = setInterval(fetchLogs, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-xl mb-2">📜 Real-Time Logs</h1>
      <pre className="bg-black text-green-400 p-2 overflow-scroll h-[400px]">{logs}</pre>
    </div>
  );
};

export default LogsPage;
