import React, { useEffect, useState } from 'react';
import authFetch from '../utils/authFetch';

const MLHealthIndicator = () => {
  const [status, setStatus] = useState(null);

  useEffect(() => {
    authFetch('/api/dashboard/ml-status')
      .then(res => res.json())
      .then(data => setStatus(data.status))
      .catch(() => setStatus('offline'));
  }, []);

  const getColor = (s) => {
    switch (s) {
      case 'healthy': return 'bg-green-500';
      case 'degraded': return 'bg-yellow-500';
      case 'offline': return 'bg-red-500';
      default: return 'bg-gray-400';
    }
  };

  return (
    <div className="bg-white shadow p-4 rounded">
      <h3 className="text-lg font-bold mb-2">ML Engine Status</h3>
      <p className="flex items-center gap-2">
        <span className={`inline-block w-3 h-3 rounded-full ${getColor(status)}`} />
        {status ? status.toUpperCase() : 'Checking...'}
      </p>
    </div>
  );
};

export default MLHealthIndicator;
