import React from 'react';

const ConfigPanel = ({ settings, onChange }) => {
  return (
    <div className="config-panel">
      <h2>Platform Strategy Settings</h2>
      {settings.map((item) => (
        <div key={item.key}>
          <label>{item.label}</label>
          <input
            type="checkbox"
            checked={item.enabled}
            onChange={() => onChange(item.key)}
          />
        </div>
      ))}
    </div>
  );
};

export default ConfigPanel;
