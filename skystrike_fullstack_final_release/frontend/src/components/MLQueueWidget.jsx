import React from "react";
const MLQueueWidget = ({ queue }) => {
  return (
    <div className="bg-white shadow rounded p-4 w-full max-w-lg mx-auto mb-4">
      <h3 className="text-lg font-semibold mb-3">🧠 Upcoming ML Trades</h3>
      {queue.length === 0 ? (
        <p className="text-gray-500 text-sm">Queue is empty</p>
      ) : (
        <ul className="list-disc list-inside text-sm text-gray-700 space-y-1">
          {queue.map((trade, idx) => (
            <li key={idx}>{trade}</li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default MLQueueWidget;
