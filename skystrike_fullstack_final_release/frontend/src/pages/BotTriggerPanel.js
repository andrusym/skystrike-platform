
import React, { useEffect, useState } from "react";
import authFetch from "../utils/authFetch";

const BotTriggerPanel = () => {
  const [bots] = useState([
    "ironcondor", "kingcondor", "wheel", "trend",
    "spread", "replicator", "gridbot", "dcabot",
    "scalper", "pairstrader", "momentumbot", "copybot"
  ]);
  const [log, setLog] = useState({});

  const trigger = async (bot) => {
    const res = await authFetch(`/api/bots/trigger/${bot}`, { method: "POST" });
    setLog((prev) => ({ ...prev, [bot]: res }));
  };

  return (
    <div>
      <h3>Trigger Bots</h3>
      {bots.map((b) => (
        <div key={b} style={{ marginBottom: "8px" }}>
          <button onClick={() => trigger(b)}>Trigger {b}</button>
          {log[b] && <pre>{JSON.stringify(log[b], null, 2)}</pre>}
        </div>
      ))}
    </div>
  );
};

export default BotTriggerPanel;
