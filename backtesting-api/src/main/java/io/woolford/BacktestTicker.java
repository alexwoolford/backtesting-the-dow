package io.woolford;

import io.woolford.database.entity.IntraDayRecord;
import io.woolford.database.mapper.DbMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import org.apache.log4j.Logger;

import javax.annotation.PostConstruct;
import java.math.BigInteger;
import java.util.List;


@Component
public class BacktestTicker {

    static Logger logger = Logger.getLogger(BacktestTicker.class.getName());

    @Autowired
    DbMapper dbMapper;

    @PostConstruct
    public void backTestTest(){
        backtest("schx", 100000.0, 1000, 0.05, 46, 0.18, 0.18);
    }


    public void backtest(String ticker, Double cash, Integer shares, Double transactionCost, Integer transactionSize, Double fallTrigger, Double climbTrigger){

        List<IntraDayRecord> intraDayRecordList = dbMapper.getIntraDayForTicker(ticker.toUpperCase());

        Double lastTransactedPrice = intraDayRecordList.get(0).getOpen();
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

        logger.info("Scenario: ticker " + ticker.toUpperCase() + "; cash: " + cash + "; initial shares: " + shares + "; transaction cost: " + transactionCost + "; transaction size: " + transactionSize + "; fall trigger: " + fallTrigger + "; climb trigger: " + climbTrigger + " resulted in " + sellTransactionCount + " sell transactions.");

    }

}
