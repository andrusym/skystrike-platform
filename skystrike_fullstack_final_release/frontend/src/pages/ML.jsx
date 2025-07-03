import React, { useEffect, useState } from "react";
import authFetch from "../utils/authFetch";

const ML = () => {
  const [mlStatus, setMlStatus] = useState(null);

  useEffect(() => {
    authFetch("/api/ml/status")
      .then(res => res.json())
      .then(data => setMlStatus(data));
  }, []);

  if (!mlStatus) return <div>Loading...</div>;

  return (
    <div>
      <h2>ML Engine Status</h2>
      <pre>{JSON.stringify(mlStatus, null, 2)}</pre>
    </div>
  );
};

export default ML;
