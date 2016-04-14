CREATE DATABASE backtesting_the_dow;

USE backtesting_the_dow;

CREATE TABLE tickers (
    ticker VARCHAR(10)
);

CREATE TABLE intra_day (
  `Datetime` datetime,
  `Close` VARCHAR(63),
  `High` VARCHAR(63),
  `Low` VARCHAR(63),
  `Open` VARCHAR(63),
  `Volume` VARCHAR(63),
  `ticker` VARCHAR(63)
);
