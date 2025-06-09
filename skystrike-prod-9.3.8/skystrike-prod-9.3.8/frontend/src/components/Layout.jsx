import React from 'react';
import { Link } from 'react-router-dom';
import './Layout.css';
import DailyPLBar from './DailyPLBar';
import logoLight from '../frontend/public/skystrike-logo-light.png';
import logoDark from '../frontend/public/skystrike-logo-dark.png';

const Layout = ({ children }) => {
  const theme = document.body.classList.contains('dark') ? 'dark' : 'light';
  const logo = theme === 'dark' ? logoDark : logoLight;

  return (
    <div className={`layout ${theme}`}>
      <aside className="sidebar">
        <div className="logo-container">
          <img src={logo} alt="SkyStrike Logo" className="logo" />
        </div>
        <nav>
          <ul>
            <li><Link to="/dashboard">Dashboard</Link></li>
            <li><Link to="/journal">Journal</Link></li>
            <li><Link to="/performance">Performance</Link></li>
            <li><Link to="/wealth">Wealth</Link></li>
            <li><Link to="/settings">Settings</Link></li>
          </ul>
        </nav>
      </aside>
      <main className="main-content">
        <DailyPLBar dailyPL={540} weeklyPL={3250} target={5000} />
        {children}
      </main>
    </div>
  );
};

export default Layout;
