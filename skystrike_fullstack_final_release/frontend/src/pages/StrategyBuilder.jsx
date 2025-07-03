
import React, { useState } from "react";
import authFetch from "../utils/authFetch";

const StrategyBuilder = () => {
  const [strategy, setStrategy] = useState({
    name: "",
    type: "Iron Condor",
    capital: 10000,
    maxLoss: 500,
    entryDelta: 0.2
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setStrategy({ ...strategy, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    authFetch("/api/strategies/create", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(strategy)
    }).then(() => alert("Strategy submitted!"));
  };

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Strategy Builder</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input />
          name="name"
          value={strategy.name}
          onChange={handleChange}
          className="w-full p-2 border rounded"
          placeholder="Strategy Name"
          required
        />
        <select><option>FixMe</option></select>
          name="type"
          value={strategy.type}
          onChange={handleChange}
          className="w-full p-2 border rounded"
        >
          <option>Iron Condor</option>
          <option>King Condor</option>
          <option>Custom Spread</option>
        </select>
        <input />
          name="capital"
          type="number"
          value={strategy.capital}
          onChange={handleChange}
          className="w-full p-2 border rounded"
          placeholder="Capital Allocation"
        />
        <input />
          name="maxLoss"
          type="number"
          value={strategy.maxLoss}
          onChange={handleChange}
          className="w-full p-2 border rounded"
          placeholder="Max Loss Threshold"
        />
        <input />
          name="entryDelta"
          type="number"
          step="0.01"
          value={strategy.entryDelta}
          onChange={handleChange}
          className="w-full p-2 border rounded"
          placeholder="Entry Delta"
        />
        <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded">
          Create Strategy
        </button>
      </form>
    </div>
  );
};

export default StrategyBuilder;
