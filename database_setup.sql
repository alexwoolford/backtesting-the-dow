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
  `ticker` VARCHAR(63)
);

INSERT INTO tickers (ticker) VALUES ('SCHX');
