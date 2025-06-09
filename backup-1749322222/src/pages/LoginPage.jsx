import React, { useState } from "react";
import { useAuth } from "./AuthContext";
import { useNavigate } from "react-router-dom";
import { useTheme } from "./ThemeContext";
import './LoginPage.css';

const LoginPage = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (login(email, password)) {
      navigate("/dashboard");
    } else {
      alert("Invalid credentials. Try admin/password");
    }
  };

  const logoSrc = theme === "dark"
    ? "/skystrike-logo-dark.png"
    : "/skystrike-logo-light.png";

  return (
    <div className="login-page">
      <div className="theme-toggle">
        <button onClick={toggleTheme}>
          Switch to {theme === "dark" ? "Light" : "Dark"} Mode
        </button>
      </div>

      <img
        src={logoSrc}
        alt="SkyStrike Logo"
        className="logo"
        style={{ width: 180, marginBottom: 20 }}
      />

      <h2>Login to SkyStrike</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default LoginPage;