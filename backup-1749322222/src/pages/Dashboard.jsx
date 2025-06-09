
import React, { useEffect, useState } from 'react';
import { useAuth } from '../AuthContext';
import { fetchDashboardData } from '../api/dashboard';

export default function Dashboard() {
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    const load = async () => {
      try {
        const result = await fetchDashboardData();
        setData(result);
      } catch {
        setError('Failed to load dashboard data.');
      }
    };
    load();
  }, []);

  if (error) {
    return (
      <div className="app-container">
        <p style={{ color: 'red' }}>{error}</p>
      </div>
    );
  }

  if (!data) {
    return <div className="app-container">Loading summary...</div>;
  }

  const formatUSD = (val) => (val != null ? `$${val}` : '$—');
  const filteredStrategies = data.strategies?.filter(
    (s) => s.ticker.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div className="app-container">
      <img
        src={document.body.className === 'dark' ? "/skystrike-logo-dark.png" : "/skystrike-logo-light.png"}
        alt="SkyStrike Logo"
        className="logo"
      />

      <h1>Welcome, {user?.email || "SkyStrike User"}</h1>

      <div className="card-container">
        <div className="card">
          <strong>Daily P&L</strong><br />{formatUSD(data.daily_pl)}
        </div>
        <div className="card">
          <strong>Weekly Target</strong><br />{formatUSD(data.weekly_target)}
        </div>
        <div className="card">
          <strong>Active Capital</strong><br />{formatUSD(data.active_capital)}
        </div>
      </div>

      <div className="panel">
        <h2>Strategies</h2>
        <input
          type="text"
          placeholder="Filter by ticker..."
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          style={{ padding: '8px', marginBottom: '12px', width: '100%' }}
        />

        {filteredStrategies?.length > 0 ? (
          <ul>
            {filteredStrategies.map((s, i) => (
              <li key={i}>
                {s.name} – {s.ticker} – {s.contracts} contracts – PnL: {formatUSD(s.pnl)} – Score: {s.ml_score ?? 'N/A'}
              </li>
            ))}
          </ul>
        ) : (
          <p>No matching strategies.</p>
        )}
      </div>
    </div>
  );
}
