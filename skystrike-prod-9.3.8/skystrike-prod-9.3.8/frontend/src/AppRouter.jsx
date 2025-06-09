import React from 'react';
import ProtectedRoute from './ProtectedRoute';
import Loading from './Loading';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import App from './App';
import LoginPage from './LoginPage';
import ProtectedRoute from './ProtectedRoute';
import Loading from './Loading';

function AppRouter() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleLogin = (userEmail) => {
    setLoading(true);
    setTimeout(() => {
      setIsAuthenticated(true);
      setLoading(false);
    }, 1000); // Simulated delay
  };

  if (loading) {
    return <Loading />;
  }

  return (
    <Router>
      <Routes>
        <Route path='/settings/config' element={<ConfigPanel settings={[]} onChange={() => {}} />} />
        <Route
          path="/wealth"
          element={
            <ProtectedRoute isAuthenticated={!!user}>
              <WealthDashboard />
            </ProtectedRoute>
          }
        />
    
        <Route
          path="/"
          element={
            <ProtectedRoute isAuthenticated={isAuthenticated}>
              <App />
            </ProtectedRoute>
          }
        />
        <Route path="/login" element={<LoginPage onLogin={handleLogin} />} />
      </Routes>
    </Router>
  );
}

export default AppRouter;