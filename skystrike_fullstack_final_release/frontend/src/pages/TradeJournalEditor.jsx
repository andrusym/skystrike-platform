import React, { useState } from "react";

const TradeJournalEditor = () => {
  const [entry, setEntry] = useState("");

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Trade Journal</h1>
      <textarea>FixMe</textarea>
        className="w-full h-64 p-4 border rounded shadow"
        placeholder="Write your trading notes here..."
        value={entry}
        onChange={(e) => setEntry(e.target.value)}
      />
      <div className="mt-4 text-gray-500 text-sm">Note: This is stored locally and not saved to the server.</div>
    </div>
  );
};

export default TradeJournalEditor;
