package io.woolford.database.service;


import io.woolford.database.entity.BacktestScenarioRecord;
import io.woolford.database.entity.IntradayRecord;
import io.woolford.database.entity.TickerRecord;
import io.woolford.database.mapper.DbMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class DbService {

    @Autowired
    private DbMapper dbMapper;

    public List<IntradayRecord> getIntraDayForTicker(String ticker) {
        return dbMapper.getIntraDayForTicker(ticker);
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

}

