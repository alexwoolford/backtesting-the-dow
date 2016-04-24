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

INSERT INTO tickers (ticker) VALUES ('SCHX');

CREATE TABLE predictit_prices (
  `ticker` VARCHAR(63),
  `short_name` VARCHAR(63),
  `last_trade_price` FLOAT,
  `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);





CREATE TABLE intra_day_snapshot (
  `datetime` datetime,
  `close` FLOAT,
  `high` FLOAT,
  `low` FLOAT,
  `open` FLOAT,
  `volume` BIGINT,
  `ticker` VARCHAR(63),
  UNIQUE KEY intra_day_snapshot_key (`datetime`, `ticker`)
);

CREATE TABLE intra_day_journal (
  `datetime` datetime,
  `close` FLOAT,
  `high` FLOAT,
  `low` FLOAT,
  `open` FLOAT,
  `volume` BIGINT,
  `ticker` VARCHAR(63)
);



DELIMITER $$

CREATE TRIGGER `trg_intra_day_snapshot` AFTER UPDATE on `intra_day_snapshot`
FOR EACH ROW
  BEGIN
    IF (NEW.value != OLD.value) THEN
      INSERT INTO intra_day_journal
        (`datetime`, `close`, `high`, `low`, `open`, `volume`, `ticker`)
      VALUES
        (NEW.`datetime`, NEW.`close`, NEW.`high`, NEW.`low`, NEW.`open`, OLD.`volume`, NEW.`ticker`);
    END IF;
  END$$

DELIMITER ;
