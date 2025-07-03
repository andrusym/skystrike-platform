import React, { useEffect, useState } from 'react';
import authFetch from '../utils/authFetch';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  LinearScale,
  Title,
  CategoryScale,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(LineElement, PointElement, LinearScale, Title, CategoryScale, Tooltip, Legend);

const DashboardChart = () => {
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    authFetch('/api/dashboard/pnl-history')
      .then(res => res.json())
      .then(data => {
        const labels = data.map(d => d.date);
        const values = data.map(d => d.pnl);
        setChartData({
          labels,
          datasets: [
            {
              label: 'Daily P&L',
              data: values,
              fill: false,
              borderColor: '#2e6ad9',
              tension: 0.3,
            },
          ],
        });
      });
  }, []);

  if (!chartData) return <p className="text-gray-500 text-sm">Loading chart...</p>;

  return (
    <div className="bg-white shadow rounded p-4">
      <h3 className="text-lg font-bold mb-2">Daily P&L</h3>
      <div style={{ height: "300px" }}>
        <Line data={chartData} options={{ responsive: true, maintainAspectRatio: false }} />
      </div>
    </div>
  );
};

export default DashboardChart;
