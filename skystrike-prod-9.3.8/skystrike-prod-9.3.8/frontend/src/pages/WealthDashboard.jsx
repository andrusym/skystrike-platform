
import React, { useEffect, useState } from 'react';

const WealthDashboard = () => {
  const [etfData, setEtfData] = useState(null);
  const [cspStatus, setCspStatus] = useState(null);

  useEffect(() => {
    fetch('/api/wealth/etf-allocation')
      .then(res => res.json())
      .then(data => setEtfData(data))
      .catch(err => console.error("ETF fetch error:", err));
  }, []);

  const handleAllocateCSP = () => {
    fetch('/api/wealth/allocate-csp', {
      method: 'POST'
    })
      .then(res => res.json())
      .then(data => setCspStatus(data))
      .catch(err => console.error("CSP allocation error:", err));
  };

  return (
    <div className="wealth-dashboard">
      <h2>Wealth Engine</h2>
      <div>
        <h3>ETF Allocation</h3>
        {etfData ? <pre>{JSON.stringify(etfData, null, 2)}</pre> : "Loading..."}
      </div>
      <div>
        <button onClick={handleAllocateCSP}>Allocate CSP</button>
        {cspStatus && <pre>{JSON.stringify(cspStatus, null, 2)}</pre>}
      </div>
    </div>
  );
};

export default WealthDashboard;
