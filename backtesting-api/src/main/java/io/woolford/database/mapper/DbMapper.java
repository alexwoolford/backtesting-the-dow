package io.woolford.database.mapper;

import io.woolford.database.entity.BacktestScenarioRecord;
import io.woolford.database.entity.IntradayRecord;
import io.woolford.database.entity.TickerRecord;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Select;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public interface DbMapper {

    @Select("SELECT      " +
            "  datetime, " +
            "  close,    " +
            "  high,     " +
            "  low,      " +
            "  open,     " +
            "  volume,   " +
            "  ticker    " +
            "FROM backtesting_the_dow.intra_day " +
            "WHERE ticker = #{ticker}           " +
            "ORDER BY datetime                  ")
    public List<IntradayRecord> getIntradayForTicker(String ticker);


    @Insert("INSERT INTO backtesting_the_dow.scenario_outcome (ticker,                      " +
            "                                                  initial_cash,                " +
            "                                                  initial_shares,              " +
            "                                                  start,                       " +
            "                                                  end,                         " +
            "                                                  transaction_cost,            " +
            "                                                  transaction_size,            " +
            "                                                  fall_trigger,                " +
            "                                                  climb_trigger,               " +
            "                                                  initial_portfolio_value,     " +
            "                                                  sell_transaction_count,      " +
            "                                                  buy_transaction_count,       " +
            "                                                  final_cash,                  " +
            "                                                  final_shares,                " +
            "                                                  final_portfolio_value,       " +
            "                                                  portfolio_percentage_change) " +
            "VALUES                             " +
            "    (#{ticker},                    " +
            "     #{initialCash},               " +
            "     #{initialShares},             " +
            "     #{start},                     " +
            "     #{end},                       " +
            "     #{transactionCost},           " +
            "     #{transactionSize},           " +
            "     #{fallTrigger},               " +
            "     #{climbTrigger},              " +
            "     #{initialPortfolioValue},     " +
            "     #{sellTransactionCount},      " +
            "     #{buyTransactionCount},       " +
            "     #{finalCash},                 " +
            "     #{finalShares},               " +
            "     #{finalPortfolioValue},       " +
            "     #{portfolioPercentageChange}) ")
    public void insertScenarioOutcome(BacktestScenarioRecord backtestScenarioRecord);

    @Select("SELECT ticker FROM backtesting_the_dow.tickers ")
    public List<TickerRecord> getTickers();

    @Insert("INSERT INTO backtesting_the_dow.intra_day                                                        " +
            "    (`datetime`, `close`, `high`, `low`, `open`, `volume`, `ticker`)                             " +
            "VALUES                                                                                           " +
            "    (#{datetime}, #{close}, #{high}, #{low}, #{open}, #{volume}, #{ticker})                      " +
            "ON DUPLICATE KEY UPDATE close=#{close}, high=#{high}, low=#{low}, open=#{open}, volume=#{volume} ")
    public void insertIntradayRecord(IntradayRecord intradayRecord);

}