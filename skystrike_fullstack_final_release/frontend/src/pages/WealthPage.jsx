
import React, { useEffect, useState } from "react";
import authFetch from "../utils/authFetch";

const WealthPage = () => {
  const [overview, setOverview] = useState(null);
  const [holdings, setHoldings] = useState(null);

  useEffect(() => {
    authFetch("/api/wealth/overview").then(setOverview);
    authFetch("/api/wealth/holdings").then(setHoldings);
  }, []);

  if (!overview || !holdings) return <div>Loading...</div>;

  return (
    <div>
      <h2>Wealth Overview</h2>
      <pre>{JSON.stringify(overview, null, 2)}</pre>
      <h3>ETF Holdings</h3>
      <ul>
        {Object.entries(holdings.etfs).map(([ticker, data]) => (
          <li key={ticker}>{ticker}: {data.shares} shares @ ${data.price}</li>
        ))}
      </ul>
      <p>Cash: ${holdings.cash}</p>
    </div>
  );
};

export default WealthPage;
