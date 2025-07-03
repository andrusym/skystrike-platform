import React, { useEffect, useState } from 'react';
import authFetch from '../utils/authFetch';
import { Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

const CapitalPieChart = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    authFetch('/api/dashboard/capital-allocation')
      .then(res => res.json())
      .then(response => {
        const labels = Object.keys(response);
        const values = Object.values(response);
        setData({
          labels,
          datasets: [{
            data: values,
            backgroundColor: ['#2e6ad9', '#29b6f6', '#66bb6a', '#ffa726', '#ef5350'],
            borderWidth: 1,
          }]
        });
      });
  }, []);

  if (!data) return <p className="text-gray-500 text-sm">Loading allocation chart...</p>;

  return (
    <div className="bg-white shadow rounded p-4">
      <h3 className="text-lg font-bold mb-2">Capital Allocation</h3>
      <Pie /> data={data} />
    </div>
  );
};

export default CapitalPieChart;
