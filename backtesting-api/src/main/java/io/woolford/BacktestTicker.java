package io.woolford;

import io.woolford.database.entity.BacktestScenarioRecord;
import io.woolford.database.entity.IntradayRecord;
import io.woolford.database.mapper.DbMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.Date;
import java.util.List;
import java.util.logging.Logger;


@Component
public class BacktestTicker {

    static Logger logger = Logger.getLogger(BacktestTicker.class.getName());

    @Autowired
    DbMapper dbMapper;

    public BacktestScenarioRecord backtest(String ticker, Double cash, Integer shares, Double transactionCost, Integer transactionSize, Double fallTrigger, Double climbTrigger){

        List<IntradayRecord> intradayRecordList = dbMapper.getIntraDayForTicker(ticker.toUpperCase());

        BacktestScenarioRecord backtestScenarioRecord = new BacktestScenarioRecord();
        backtestScenarioRecord.setTicker(ticker.toUpperCase());
        backtestScenarioRecord.setInitialCash(cash);

        Date startDate = intradayRecordList.get(0).getDatetime();
        backtestScenarioRecord.setStart(startDate);

        backtestScenarioRecord.setInitialShares(shares);
        backtestScenarioRecord.setTransactionCost(transactionCost);
        backtestScenarioRecord.setTransactionSize(transactionSize);
        backtestScenarioRecord.setFallTrigger(fallTrigger);
        backtestScenarioRecord.setClimbTrigger(climbTrigger);

        Double lastTransactedPrice = intradayRecordList.get(0).getOpen();
        Double initialPortfolioValue = shares * lastTransactedPrice + cash;

        backtestScenarioRecord.setInitialPortfolioValue(initialPortfolioValue);

        Integer sellTransactionCount = 0;
        Integer buyTransactionCount = 0;

        for (IntradayRecord intradayRecord : intradayRecordList){

            if (intradayRecord.getOpen() > lastTransactedPrice + climbTrigger){
                if (shares > transactionSize) {
                    // Sell
                    logger.info("Sell " + transactionSize + " shares at " + intradayRecord.getOpen() + " on " + intradayRecord.getDatetime() + ".");
                    lastTransactedPrice = intradayRecord.getOpen();
                    sellTransactionCount++;
                    shares -= transactionSize;
                    cash -= transactionCost;
                    cash += transactionSize * intradayRecord.getOpen();
                }
            }

            if (intradayRecord.getOpen() < lastTransactedPrice - fallTrigger){
                if (cash - transactionCost > transactionSize * intradayRecord.getOpen()){
                    // Buy
                    logger.info("Buy " + transactionSize + " shares at " + intradayRecord.getOpen() + " on " + intradayRecord.getDatetime() + ".");
                    lastTransactedPrice = intradayRecord.getOpen();
                    buyTransactionCount++;
                    shares += transactionSize;
                    cash -= transactionCost;
                    cash -= transactionSize * intradayRecord.getOpen();
                }
            }

        }

        Date end = intradayRecordList.get(intradayRecordList.size() - 1).getDatetime();
        backtestScenarioRecord.setEnd(end);

        backtestScenarioRecord.setSellTransactionCount(sellTransactionCount);
        backtestScenarioRecord.setBuyTransactionCount(buyTransactionCount);
        backtestScenarioRecord.setFinalCash(cash);
        backtestScenarioRecord.setFinalShares(shares);

        Double finalPortfolioValue = shares * lastTransactedPrice + cash;
        backtestScenarioRecord.setFinalPortfolioValue(finalPortfolioValue);

        Double portfolioPercentageChange = (finalPortfolioValue - initialPortfolioValue) / initialPortfolioValue;
        backtestScenarioRecord.setPortfolioPercentageChange(portfolioPercentageChange);

        dbMapper.insertScenarioOutcome(backtestScenarioRecord);

        logger.info("backtestScenarioRecord: " + backtestScenarioRecord.toString());

        return backtestScenarioRecord;

    }

}
