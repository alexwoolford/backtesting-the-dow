package io.woolford.database.mapper;

import io.woolford.database.entity.IntraDayRecord;
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
    public List<IntraDayRecord> getIntraDayForTicker(String ticker);

}