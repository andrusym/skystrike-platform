import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Layout from "./components/Layout";
import ProtectedRoute from "./components/ProtectedRoute";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import TradesPage from "./pages/TradesPage";
import OrdersPage from "./pages/OrdersPage";
import WealthPage from "./pages/WealthPage";
import MLPage from "./pages/MLPage";
import RiskPage from "./pages/RiskPage";
import SetupPage from "./pages/SetupPage";
import SupportPage from "./pages/SupportPage";
import ConfigPage from "./pages/ConfigPage";
import PerformanceSummary from "./pages/PerformanceSummary";
import BotPanel from "./pages/BotPanel"; // ? NEW

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/dashboard" />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      <Route path="/dashboard" element={
        <ProtectedRoute>
          <Layout><Dashboard /></Layout>
        </ProtectedRoute>
      } />
      <Route path="/trades" element={
        <ProtectedRoute>
          <Layout><TradesPage /></Layout>
        </ProtectedRoute>
      } />
      <Route path="/strategies" element={
        <ProtectedRoute>
          <Layout><BotPanel /></Layout> {/* ? Updated to use BotPanel */}
        </ProtectedRoute>
      } />
      <Route path="/orders" element={
        <ProtectedRoute>
          <Layout><OrdersPage /></Layout>
        </ProtectedRoute>
      } />
      <Route path="/wealth" element={
        <ProtectedRoute>
          <Layout><WealthPage /></Layout>
        </ProtectedRoute>
      } />
      <Route path="/ml" element={
        <ProtectedRoute>
          <Layout><MLPage /></Layout>
        </ProtectedRoute>
      } />
      <Route path="/risk" element={
        <ProtectedRoute>
          <Layout><RiskPage /></Layout>
        </ProtectedRoute>
      } />
      <Route path="/setup" element={
        <ProtectedRoute>
          <Layout><SetupPage /></Layout>
        </ProtectedRoute>
      } />
      <Route path="/support" element={
        <ProtectedRoute>
          <Layout><SupportPage /></Layout>
        </ProtectedRoute>
      } />
      <Route path="/config" element={
        <ProtectedRoute>
          <Layout><ConfigPage /></Layout>
        </ProtectedRoute>
      } />
      <Route path="/summary" element={
        <ProtectedRoute>
          <Layout><PerformanceSummary /></Layout>
        </ProtectedRoute>
      } />
    </Routes>
  );
};

export default AppRoutes;
