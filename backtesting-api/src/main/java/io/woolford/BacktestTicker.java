package io.woolford;

import io.woolford.database.entity.BacktestScenarioRecord;
import io.woolford.database.entity.IntraDayRecord;
import io.woolford.database.mapper.DbMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.logging.Logger;


@Component
public class BacktestTicker {

    static Logger logger = Logger.getLogger(BacktestTicker.class.getName());

    @Autowired
    DbMapper dbMapper;

    public BacktestScenarioRecord backtest(String ticker, Double cash, Integer shares, Double transactionCost, Integer transactionSize, Double fallTrigger, Double climbTrigger){

        List<IntraDayRecord> intraDayRecordList = dbMapper.getIntraDayForTicker(ticker.toUpperCase());

        BacktestScenarioRecord backtestScenarioRecord = new BacktestScenarioRecord();
        backtestScenarioRecord.setTicker(ticker);
        backtestScenarioRecord.setInitialCash(cash);
        backtestScenarioRecord.setInitialShares(shares);
        backtestScenarioRecord.setTransactionCost(transactionCost);
        backtestScenarioRecord.setTransactionSize(transactionSize);
        backtestScenarioRecord.setFallTrigger(fallTrigger);
        backtestScenarioRecord.setClimbTrigger(climbTrigger);

        Double lastTransactedPrice = intraDayRecordList.get(0).getOpen();
        Double initialPortfolioValue = shares * lastTransactedPrice + cash;

        backtestScenarioRecord.setInitialPortfolioValue(initialPortfolioValue);

        Integer sellTransactionCount = 0;
        Integer buyTransactionCount = 0;

        for (IntraDayRecord intraDayRecord : intraDayRecordList){

            if (intraDayRecord.getOpen() > lastTransactedPrice + climbTrigger){
                if (shares > transactionSize) {
                    // Sell
                    logger.info("Sell " + transactionSize + " shares at " + intraDayRecord.getOpen() + " on " + intraDayRecord.getDatetime() + ".");
                    lastTransactedPrice = intraDayRecord.getOpen();
                    sellTransactionCount++;
                    shares -= transactionSize;
                    cash -= transactionCost;
                    cash += transactionSize * intraDayRecord.getOpen();
                }
            }

            if (intraDayRecord.getOpen() < lastTransactedPrice - fallTrigger){
                if (cash - transactionCost > transactionSize * intraDayRecord.getOpen()){
                    // Buy
                    logger.info("Buy " + transactionSize + " shares at " + intraDayRecord.getOpen() + " on " + intraDayRecord.getDatetime() + ".");
                    lastTransactedPrice = intraDayRecord.getOpen();
                    buyTransactionCount++;
                    cash -= transactionCost;
                    cash -= transactionSize * intraDayRecord.getOpen();
                }
            }

        }

        backtestScenarioRecord.setSellTransactionCount(sellTransactionCount);
        backtestScenarioRecord.setBuyTransactionCount(buyTransactionCount);
        backtestScenarioRecord.setFinalCash(cash);
        backtestScenarioRecord.setFinalShares(shares);

        Double finalPortfolioValue = shares * lastTransactedPrice + cash;
        backtestScenarioRecord.setFinalPortfolioValue(finalPortfolioValue);

        Double portfolioPercentageChange = (finalPortfolioValue - initialPortfolioValue) / initialPortfolioValue;
        backtestScenarioRecord.setPortfolioPercentageChange(portfolioPercentageChange);

        return backtestScenarioRecord;

    }

}
