import React from "react";
import { Link, useLocation } from "react-router-dom";

const Sidebar = () => {
  const location = useLocation();

  const navItems = [
    { path: "/dashboard", label: "Dashboard" },
    { path: "/trades", label: "Trades" },
    { path: "/strategies", label: "Strategies" },
    { path: "/wealth", label: "Wealth" },
    { path: "/ml", label: "ML" },
    { path: "/risk", label: "Risk" },
    { path: "/setup", label: "Setup" },
    { path: "/orders", label: "Orders" },
    { path: "/config", label: "Config" },
    { path: "/summary", label: "Summary" },
    { path: "/support", label: "Support" },
  ];

  return (
    <div className="w-64 bg-white border-r p-6 space-y-4 h-full">
      <h2 className="text-xl font-bold mb-6">SkyStrike</h2>
      {navItems.map(({ path, label }) => (
        <Link
          key={path}
          to={path}
          className={`block px-4 py-2 rounded hover:bg-blue-100 ${
            location.pathname === path ? "bg-blue-200 font-semibold" : ""
          }`}
        >
          {label}
        </Link>
      ))}
    </div>
  );
};

export default Sidebar;
