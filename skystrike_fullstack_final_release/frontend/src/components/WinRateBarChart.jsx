import React, { useEffect, useState } from 'react';
import authFetch from '../utils/authFetch';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

const WinRateBarChart = () => {
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    authFetch('/api/summary/win-rates')
      .then(res => res.json())
      .then(data => {
        const labels = Object.keys(data);
        const values = Object.values(data);
        setChartData({
          labels,
          datasets: [{
            label: 'Win Rate (%)',
            data: values,
            backgroundColor: '#2e6ad9',
          }]
        });
      });
  }, []);

  if (!chartData) return <p className="text-gray-500 text-sm">Loading win rate chart...</p>;

  return (
    <div className="bg-white shadow rounded p-4">
      <h3 className="text-lg font-bold mb-2">Win Rate by Strategy</h3>
      <Bar data={chartData} />
    </div>
  );
};

export default WinRateBarChart;
