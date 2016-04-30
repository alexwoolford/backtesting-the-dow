package io.woolford.database.entity;

import java.math.BigInteger;
import java.util.Date;

public class IntraDayRecord {

    private Date datetime;
    private Double close;
    private Double high;
    private Double low;
    private Double open;
    private BigInteger volume;
    private String ticker;

    public Date getDatetime() {
        return datetime;
    }

    public void setDatetime(Date datetime) {
        this.datetime = datetime;
    }

    public Double getClose() {
        return close;
    }

    public void setClose(Double close) {
        this.close = close;
    }

    public Double getHigh() {
        return high;
    }

    public void setHigh(Double high) {
        this.high = high;
    }

    public Double getLow() {
        return low;
    }

    public void setLow(Double low) {
        this.low = low;
    }

    public Double getOpen() {
        return open;
    }

    public void setOpen(Double open) {
        this.open = open;
    }

    public BigInteger getVolume() {
        return volume;
    }

    public void setVolume(BigInteger volume) {
        this.volume = volume;
    }

    public String getTicker() {
        return ticker;
    }

    public void setTicker(String ticker) {
        this.ticker = ticker;
    }

    @Override
    public String toString() {
        return "IntraDayRecord{" +
                "datetime=" + datetime +
                ", close=" + close +
                ", high=" + high +
                ", low=" + low +
                ", open=" + open +
                ", volume=" + volume +
                ", ticker='" + ticker + '\'' +
                '}';
    }

}
