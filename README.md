## Backtesting the Dow

My brother-in-law, Eric, and I were talking about investment strategies: specifically, if we buy the Dow Jones when prices fall and sell when prices climb, how much should the price change between transactions to maximize yield?

We collected some intra-day data for the SCHX ticker, which tracks the Dow Jones, between March 29th and April 29th and backtested various scenarios.

The backtesting model is accessible via an API. Here's an example call:

    http://localhost:8080/scenario?ticker=schx&cash=20000&shares=100&transactionCost=0.05&transactionSize=1&fallTrigger=0.15&climbTrigger=0.15

The (mandatory) input parameters are:
+ cash: the initial amount of cash
+ shares: the initial quantity of shares
+ ticker: the stock symbol
+ transactionCost: this can vary widely according the the terms of your brokerage.
+ transactionSize: the quantity of shares transacted on any given buy or sell.
+ fallTrigger: the dollar amount the stock has to fall, from the previous transaction, to trigger a buy.
+ climbTrigger: the dollar amount the stock has to climb, from the previous transaction, to trigger a sell.

The backtest runs the scenario, e.g. :

    Sell 20 shares at 48.5 on Tue Mar 29 04:45:00 MDT 2016.
    Sell 20 shares at 48.67 on Tue Mar 29 06:40:00 MDT 2016.
    Sell 20 shares at 48.95 on Wed Mar 30 01:30:00 MDT 2016.
    Sell 20 shares at 49.12 on Fri Apr 01 07:35:00 MDT 2016.
    Buy 20 shares at 48.611 on Tue Apr 05 01:33:00 MDT 2016.

The simulation results are returned as JSON:

    {
        "ticker": "schx",
        "initialCash": 20000.0,
        "initialShares": 100,
        "transactionCost": 0.05,
        "transactionSize": 1,
        "fallTrigger": 0.15,
        "climbTrigger": 0.15,
        "initialPortfolioValue": 24832.0,
        "sellTransactionCount": 35,
        "buyTransactionCount": 31,
        "finalCash": 20198.422,
        "finalShares": 65,
        "finalPortfolioValue": 23389.272,
        "portfolioPercentageChange": -0.0580
    }



## Prediction markets: 2016 election

I find prediction markets fascinating, and notice that predictit.org has made pricing accessible via API.

My son, Miles, was curious to know if there are pricing differences throughout the day. Our hypothesis was that there may be predictable price swings at certain times of the day, since Democrats are more highly concentrated in the (vertical) coastal areas, and Republicans are more concentrated in the center. 

We thought that the price might swing, by some small but predictable amount, as the demographics of the active internet users changes throughout the day, e.g. a possible surge of democrats first thing in the morning, that swings back as the central southern states wake up. We started to collect some data to test our theory:

![PredictIt.org last trade prices](predictit_election_last_trade_prices.png)

### What we saw ###

The prices generally don't fluctuate within more than a couple of cents over a 24 hour period. Given that there's a one-cent spread between the buy price and cell price, we need to see a movement of at least two cents to make any money. The price fluctuations were too small to trade, regardless of whether there's any intra-day seasonality.

