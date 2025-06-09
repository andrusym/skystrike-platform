import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from "../AuthContext.jsx";
import { useTheme } from "../ThemeContext";
import './Layout.css';

const Layout = ({ children }) => {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();

  const logoSrc = theme === 'dark'
    ? '/skystrike-logo-dark.png'
    : '/skystrike-logo-light.png';

  return (
    <div className={`layout-container ${theme}`}>
      <aside className="sidebar">
        <img src={logoSrc} alt="SkyStrike Logo" className="logo" />
        <button className="sidebar-logout" onClick={() => { logout(); navigate('/login'); }}>
          Logout
        </button>
      </aside>

      <main className="main-content">
        <div className="theme-toggle-global">
          <button onClick={toggleTheme}>
            Toggle {theme === 'dark' ? 'Light' : 'Dark'} Mode
          </button>
        </div>

        {children}
      </main>
    </div>
  );
};

export default Layout;