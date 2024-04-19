import React from 'react';
import { SiApple, SiTesla, SiNvidia, SiMicrosoft, SiAmazon, SiGoogle, SiCocacola } from "react-icons/si";

export const getIconByTicker = (ticker) => {
  switch (ticker) {
    case 'AAPL':
      return <SiApple size={24} />;
    case 'TSLA':
      return <SiTesla size={24} />;
    case 'NVDA':
      return <SiNvidia size={24} />;
    case 'MSFT':
      return <SiMicrosoft size={24} />;
    case 'AMZN':
      return <SiAmazon size={24} />;
    case 'GOOG':
      return <SiGoogle size={24} />;
    case 'KO':
      return <SiCocacola size={24} />;
    default:
      return null;
  }
};