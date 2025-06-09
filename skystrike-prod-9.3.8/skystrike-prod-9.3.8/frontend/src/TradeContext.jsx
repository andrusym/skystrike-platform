import React from 'react';
import { createContext, useContext, useState } from "react";

const TradeContext = createContext(null);

export const TradeProvider = ({ children }) => {
  const [trades, setTrades] = useState([]);

  const addTrade = (trade) => setTrades((prev) => [...prev, trade]);
  const clearTrades = () => setTrades([]);

  return (
    <TradeContext.Provider value={{ trades, addTrade, clearTrades }}>
      {children}
    </TradeContext.Provider>
  );
};

export const useTrade = () => useContext(TradeContext);

export default TradeContext;
