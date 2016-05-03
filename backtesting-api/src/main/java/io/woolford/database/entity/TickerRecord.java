package io.woolford.database.entity;

public class TickerRecord {

    private String ticker;

    public String getTicker() {
        return ticker;
    }

    public void setTicker(String ticker) {
        this.ticker = ticker;
    }

    @Override
    public String toString() {
        return "TickerRecord{" +
                "ticker='" + ticker + '\'' +
                '}';
    }

}
