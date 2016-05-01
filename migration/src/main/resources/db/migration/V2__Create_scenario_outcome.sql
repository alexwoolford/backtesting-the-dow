CREATE TABLE scenario_outcome (
  ticker VARCHAR(10),
  initial_cash FLOAT,
  initial_shares INTEGER,
  start DATETIME,
  end DATETIME,
  transaction_cost FLOAT,
  transaction_size INTEGER,
  fall_trigger FLOAT,
  climb_trigger FLOAT,
  initial_portfolio_value FLOAT,
  sell_transaction_count INTEGER,
  buy_transaction_count INTEGER,
  final_cash FLOAT,
  final_shares INTEGER,
  final_portfolio_value FLOAT,
  portfolio_percentage_change FLOAT
);
