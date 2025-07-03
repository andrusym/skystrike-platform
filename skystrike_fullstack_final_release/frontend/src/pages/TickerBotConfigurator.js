
import React, { useState } from "react";
import authFetch from "../utils/authFetch";

const TickerBotConfigurator = () => {
  const [rows, setRows] = useState([{ ticker: "", contracts: 1 }]);
  const [bot, setBot] = useState("ironcondor");
  const [log, setLog] = useState(null);

  const handleChange = (index, field, value) => {
    const updated = [...rows];
    updated[index][field] = field === "contracts" ? parseInt(value, 10) || 0 : value;
    setRows(updated);
  };

  const addRow = () => {
    setRows([...rows, { ticker: "", contracts: 1 }]);
  };

  const removeRow = (index) => {
    const updated = rows.filter((_, i) => i !== index);
    setRows(updated);
  };

  const activate = async () => {
    const responses = await Promise.all(
      rows.map((row) =>
        authFetch(`/api/bots/trigger/${bot}`, {
          method: "POST",
          body: JSON.stringify(row),
        })
      )
    );
    setLog(responses);
  };

  const estimatedBudget = rows.reduce((sum, row) => sum + row.contracts * 200, 0);

  return (
    <div>
      <h2>Start Automation</h2>
      <label>Select Bot:</label>
      <select value={bot} onChange={(e) => setBot(e.target.value)}>
        {[
          "ironcondor", "kingcondor", "wheel", "trend",
          "spread", "replicator", "gridbot", "dcabot",
          "scalper", "pairstrader", "momentumbot", "copybot"
        ].map((b) => (
          <option key={b} value={b}>{b}</option>
        ))}
      </select>

      <table>
        <thead>
          <tr>
            <th>Ticker</th>
            <th>Contracts</th>
            <th>Budget</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row, idx) => (
            <tr key={idx}>
              <td>
                <input
                  value={row.ticker}
                  onChange={(e) => handleChange(idx, "ticker", e.target.value)}
                  placeholder="e.g. QQQ"
                />
              </td>
              <td>
                <input
                  type="number"
                  value={row.contracts}
                  onChange={(e) => handleChange(idx, "contracts", e.target.value)}
                  min="1"
                />
              </td>
              <td>${row.contracts * 200}</td>
              <td>
                <button onClick={() => removeRow(idx)}>❌</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <button onClick={addRow}>+ Add Ticker</button>

      <h4>Total Estimated: ${estimatedBudget}</h4>

      <button onClick={activate}>Activate</button>

      {log && (
        <div>
          <h4>Execution Log:</h4>
          <pre>{JSON.stringify(log, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default TickerBotConfigurator;
