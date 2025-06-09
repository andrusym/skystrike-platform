import React, { useState } from 'react';

const TradeJournalEditor = ({ entry, onSave }) => {
  const [notes, setNotes] = useState(entry.notes || '');
  const [tags, setTags] = useState(entry.tags || '');

  const handleSave = () => {
    onSave({ ...entry, notes, tags });
  };

  return (
    <div className="journal-editor">
      <textarea value={notes} onChange={(e) => setNotes(e.target.value)} placeholder="Notes" />
      <input value={tags} onChange={(e) => setTags(e.target.value)} placeholder="Tags (comma-separated)" />
      <button onClick={handleSave}>Save</button>
    </div>
  );
};

export default TradeJournalEditor;
