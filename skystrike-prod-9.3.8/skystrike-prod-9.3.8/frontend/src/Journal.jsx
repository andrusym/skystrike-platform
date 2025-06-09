import React, { useState } from "react";

const Journal = () => {
  const [entries, setEntries] = useState([]);
  const [text, setText] = useState("");

  const handleAdd = () => {
    if (text.trim()) {
      setEntries([...entries, { text, time: new Date().toLocaleString() }]);
      setText("");
    }
  };

  return (
    <div className="app-container">
      <h1>Journal</h1>
      <textarea
        rows="4"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Write a note..."
      />
      <br />
      <button onClick={handleAdd}>Save Entry</button>
      <ul>
        {entries.map((entry, idx) => (
          <li key={idx}>
            <strong>{entry.time}</strong>: {entry.text}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Journal;
