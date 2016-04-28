CREATE DATABASE backtesting_the_dow;

USE backtesting_the_dow;

CREATE TABLE tickers (
    ticker VARCHAR(10)
);

CREATE TABLE intra_day (
  `datetime` datetime,
  `close` FLOAT,
  `high` FLOAT,
  `low` FLOAT,
  `open` FLOAT,
  `volume` BIGINT,
  `ticker` VARCHAR(63),
  UNIQUE KEY intra_day_snapshot_key (`datetime`, `ticker`)
);

CREATE TABLE scenario_outcome (
    transaction_cost FLOAT,
    transaction_size INTEGER,
    fall_trigger_percentage FLOAT,
    climb_trigger_percentage FLOAT,
    percentage_change DOUBLE
);

INSERT INTO tickers (ticker) VALUES ('SCHX');

CREATE TABLE predictit_prices (
  `ticker` VARCHAR(63),
  `short_name` VARCHAR(63),
  `last_trade_price` FLOAT,
  `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE scenario_outcome_fixed (
transaction_cost float,
transaction_size integer,
fall_trigger float,
climb_trigger float,
sell_transaction_count integer,
profit_per_transaction float,
profit float
)


