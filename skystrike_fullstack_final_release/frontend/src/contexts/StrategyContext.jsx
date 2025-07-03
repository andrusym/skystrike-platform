import { createContext, useContext, useState } from "react";

const StrategyContext = createContext(null);

export const StrategyProvider = ({ children }) => {
  const [strategies, setStrategies] = useState([]);

  const updateStrategies = (newStrategies) => setStrategies(newStrategies);

  return (
    <StrategyContext.Provider value={{ strategies, updateStrategies }}>
      {children}
    </StrategyContext.Provider>
  );
};

export const useStrategy = () => useContext(StrategyContext);

export default StrategyContext;
