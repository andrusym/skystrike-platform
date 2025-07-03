
import React, { useEffect, useState } from "react";
import authFetch from "../utils/authFetch";

const MLPage = () => {
  const [status, setStatus] = useState(null);
  const [response, setResponse] = useState(null);

  const runTune = async () => {
    const res = await authFetch("/api/system/self-tune", { method: "POST" });
    setResponse(res);
  };

  useEffect(() => {
    authFetch("/api/ml/status").then(setStatus);
  }, []);

  return (
    <div>
      <h2>ML Engine Status</h2>
      <pre>{JSON.stringify(status, null, 2)}</pre>
      <button onClick={runTune}>Run Self-Tune</button>
      {response && <pre>{JSON.stringify(response, null, 2)}</pre>}
    </div>
  );
};

export default MLPage;
