CREATE TABLE tickers (
    ticker VARCHAR(10)
);

INSERT INTO tickers (ticker) VALUES ('SCHX');

CREATE TABLE intra_day (
  datetime DATETIME,
  close FLOAT,
  high FLOAT,
  low FLOAT,
  open FLOAT,
  volume BIGINT,
  ticker VARCHAR(63),
  UNIQUE KEY intra_day_snapshot_key (datetime, ticker)
);

CREATE TABLE predictit_prices (
  ticker VARCHAR(63),
  short_name VARCHAR(63),
  last_trade_price FLOAT,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

