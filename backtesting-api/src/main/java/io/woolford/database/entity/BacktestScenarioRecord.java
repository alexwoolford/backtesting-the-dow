package io.woolford.database.entity;


import java.util.Date;

public class BacktestScenarioRecord {

    private String ticker;
    private Double initialCash;
    private Integer initialShares;
    private Date start;
    private Date end;
    private Double transactionCost;
    private Integer transactionSize;
    private Double fallTrigger;
    private Double climbTrigger;
    private Double initialPortfolioValue;
    private Integer sellTransactionCount;
    private Integer buyTransactionCount;
    private Double finalCash;
    private Integer finalShares;
    private Double finalPortfolioValue;
    private Double portfolioPercentageChange;

    public String getTicker() {
        return ticker;
    }

    public void setTicker(String ticker) {
        this.ticker = ticker;
    }

    public Double getInitialCash() {
        return initialCash;
    }

    public void setInitialCash(Double initialCash) {
        this.initialCash = initialCash;
    }

    public Integer getInitialShares() {
        return initialShares;
    }

    public void setInitialShares(Integer initialShares) {
        this.initialShares = initialShares;
    }

    public Date getStart() {
        return start;
    }

    public void setStart(Date start) {
        this.start = start;
    }

    public Date getEnd() {
        return end;
    }

    public void setEnd(Date end) {
        this.end = end;
    }

    public Double getTransactionCost() {
        return transactionCost;
    }

    public void setTransactionCost(Double transactionCost) {
        this.transactionCost = transactionCost;
    }

    public Integer getTransactionSize() {
        return transactionSize;
    }

    public void setTransactionSize(Integer transactionSize) {
        this.transactionSize = transactionSize;
    }

    public Double getFallTrigger() {
        return fallTrigger;
    }

    public void setFallTrigger(Double fallTrigger) {
        this.fallTrigger = fallTrigger;
    }

    public Double getClimbTrigger() {
        return climbTrigger;
    }

    public void setClimbTrigger(Double climbTrigger) {
        this.climbTrigger = climbTrigger;
    }

    public Double getInitialPortfolioValue() {
        return initialPortfolioValue;
    }

    public void setInitialPortfolioValue(Double initialPortfolioValue) {
        this.initialPortfolioValue = initialPortfolioValue;
    }

    public Integer getSellTransactionCount() {
        return sellTransactionCount;
    }

    public void setSellTransactionCount(Integer sellTransactionCount) {
        this.sellTransactionCount = sellTransactionCount;
    }

    public Integer getBuyTransactionCount() {
        return buyTransactionCount;
    }

    public void setBuyTransactionCount(Integer buyTransactionCount) {
        this.buyTransactionCount = buyTransactionCount;
    }

    public Double getFinalCash() {
        return finalCash;
    }

    public void setFinalCash(Double finalCash) {
        this.finalCash = finalCash;
    }

    public Integer getFinalShares() {
        return finalShares;
    }

    public void setFinalShares(Integer finalShares) {
        this.finalShares = finalShares;
    }

    public Double getFinalPortfolioValue() {
        return finalPortfolioValue;
    }

    public void setFinalPortfolioValue(Double finalPortfolioValue) {
        this.finalPortfolioValue = finalPortfolioValue;
    }

    public Double getPortfolioPercentageChange() {
        return portfolioPercentageChange;
    }

    public void setPortfolioPercentageChange(Double portfolioPercentageChange) {
        this.portfolioPercentageChange = portfolioPercentageChange;
    }

    @Override
    public String toString() {
        return "BacktestScenarioRecord{" +
                "ticker='" + ticker + '\'' +
                ", initialCash=" + initialCash +
                ", initialShares=" + initialShares +
                ", start=" + start +
                ", end=" + end +
                ", transactionCost=" + transactionCost +
                ", transactionSize=" + transactionSize +
                ", fallTrigger=" + fallTrigger +
                ", climbTrigger=" + climbTrigger +
                ", initialPortfolioValue=" + initialPortfolioValue +
                ", sellTransactionCount=" + sellTransactionCount +
                ", buyTransactionCount=" + buyTransactionCount +
                ", finalCash=" + finalCash +
                ", finalShares=" + finalShares +
                ", finalPortfolioValue=" + finalPortfolioValue +
                ", portfolioPercentageChange=" + portfolioPercentageChange +
                '}';
    }

}
