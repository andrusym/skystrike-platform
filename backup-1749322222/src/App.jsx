import React, { useEffect, useState } from 'react';
import axios from 'axios';
import TradePanel from './TradePanel';
import StrategyCards from './StrategyCards';
import DashboardSummary from './DashboardSummary';
import ToggleTheme from './ToggleTheme';
import './App.css';

const API_BASE = 'http://localhost:8000';

function App() {
  const [summary, setSummary] = useState({});
  const [theme, setTheme] = useState('light');

  useEffect(() => {
    fetchSummary();
  }, []);

  const fetchSummary = async () => {
    try {
      const res = await axios.get(\`\${API_BASE}/dashboard\`);
      setSummary(res.data);
    } catch (err) {
      console.error('Error fetching dashboard summary:', err);
    }
  };

  const handleThemeToggle = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    document.body.className = newTheme;
    setTheme(newTheme);
  };

  const logoPath = theme === 'light'
    ? '/skystrike-logo-dark.png'
    : '/skystrike-logo-light.png';

  return (
    <div className="app-container">
      <ToggleTheme theme={theme} onToggle={handleThemeToggle} />
      <img src={logoPath} alt="SkyStrike Logo" className="logo" />
      <h1 className="title">SkyStrike Trading Dashboard</h1>
      <DashboardSummary summary={summary} />
      <TradePanel onTradeSuccess={fetchSummary} />
      <StrategyCards summary={summary} />
    </div>
  );
}

export default App;