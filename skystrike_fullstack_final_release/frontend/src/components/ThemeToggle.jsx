import React from 'react';
import { useTheme } from '../ThemeContext';

const ThemeToggle = () => {
  const { theme, toggleTheme } = useTheme();

  return (
    <button className="px-4 py-2 bg-blue-600 text-white rounded">Submit</button>
      onClick={toggleTheme}
      className="absolute top-2 right-2 px-4 py-1 bg-gray-200 text-sm rounded hover:bg-gray-300"
    >
      {theme === 'dark' ? '🌙 Dark' : '☀️ Light'}
    </button>
  );
};

export default ThemeToggle;
