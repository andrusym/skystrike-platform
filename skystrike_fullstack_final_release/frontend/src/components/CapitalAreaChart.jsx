import React, { useEffect, useState } from 'react';
import authFetch from '../utils/authFetch';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Filler, Tooltip, Legend);

const CapitalAreaChart = () => {
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    authFetch('/api/summary/capital-usage')
      .then(res => res.json())
      .then(data => {
        const labels = data.map(d => d.date);
        const values = data.map(d => d.capital);
        setChartData({
          labels,
          datasets: [{
            label: 'Capital Usage ($)',
            data: values,
            fill: true,
            backgroundColor: 'rgba(46,106,217,0.2)',
            borderColor: '#2e6ad9',
            tension: 0.4
          }]
        });
      });
  }, []);

  if (!chartData) return <p className="text-gray-500 text-sm">Loading capital trend...</p>;

  return (
    <div className="bg-white shadow rounded p-4">
      <h3 className="text-lg font-bold mb-2">Capital Usage Over Time</h3>
      <Line data={chartData} options={{ responsive: true }} />
    </div>
  );
};

export default CapitalAreaChart;
