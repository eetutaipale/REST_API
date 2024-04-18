import React from 'react';

const DataList = ({ dataList }) => {
  return (
    <div>
      <h2>Data List</h2>
      <ul>
        {dataList.map(item => (
          <li key={item.id}>
            <strong>Name:</strong> {item.name}<br />
            <strong>ID:</strong> {item.id}<br />
            <strong>Last Day's Price:</strong> {item.last_days_price}<br />
            <strong>Date:</strong> {item.date}<br />
            <strong>Today's Price:</strong> {item.price_today}<br />
            <strong>Ticker:</strong> {item.ticker}<br />
            <strong>Volume:</strong> {item.volume}<br />
            <br />
          </li>
        ))}
      </ul>
    </div>
  );
};

export default DataList;