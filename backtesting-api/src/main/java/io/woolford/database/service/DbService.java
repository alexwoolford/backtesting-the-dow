package io.woolford.database.service;


import io.woolford.database.entity.BacktestScenarioRecord;
import io.woolford.database.entity.IntradayRecord;
import io.woolford.database.entity.TickerRecord;
import io.woolford.database.mapper.DbMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class DbService {

    @Autowired
    private DbMapper dbMapper;

    public List<IntradayRecord> getIntradayForTicker(String ticker) {
        return dbMapper.getIntradayForTicker(ticker);
    }

    public void insertScenarioOutcome(BacktestScenarioRecord backtestScenarioRecord){
        dbMapper.insertScenarioOutcome(backtestScenarioRecord);
    }

    public List<TickerRecord> getTickers() {
        return dbMapper.getTickers();
    }

    public void insertIntradayRecord(IntradayRecord intradayRecord){
        dbMapper.insertIntradayRecord(intradayRecord);
    }

    // Don't do this at home
    private void simulateSlowService() {
        try {
            long time = 5000L;
            Thread.sleep(time);
        } catch (InterruptedException e) {
            throw new IllegalStateException(e);
        }
    }

}

