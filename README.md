## Backtesting the Dow

My brother-in-law, Eric, and I were talking about investment strategies: specifically, if we buy the Dow Jones when prices fall and sell when prices climb, how much should the price change between transactions to maximize yield?

We collected some intra-day data for the SCHX ticker, which tracks the Dow Jones, between March 29th and April 29th and backtested various scenarios.

The backtesting model is accessible via an API. Here's an example call:

    http://localhost:8080/scenario?ticker=schx&cash=20000&shares=100&transactionCost=0.05&transactionSize=30&fallTrigger=0.06&climbTrigger=0.05

The (mandatory) input parameters are:
+ cash: the initial amount of cash
+ shares: the initial quantity of shares
+ ticker: the stock symbol
+ transactionCost: this can vary widely according the the terms of your brokerage.
+ transactionSize: the quantity of shares transacted on any given buy or sell.
+ fallTrigger: the dollar amount the stock has to fall, from the previous transaction, to trigger a buy.
+ climbTrigger: the dollar amount the stock has to climb, from the previous transaction, to trigger a sell.

The backtest runs the scenario, e.g. :

    Buy 30 shares at 48.23 on Mon Mar 28 01:40:00 MDT 2016.
    Buy 30 shares at 48.16 on Mon Mar 28 02:39:00 MDT 2016.
    Sell 30 shares at 48.22 on Mon Mar 28 03:52:00 MDT 2016.
    Sell 30 shares at 48.31 on Mon Mar 28 04:40:00 MDT 2016.
    Sell 30 shares at 48.37 on Mon Mar 28 06:07:00 MDT 2016.
    Buy 30 shares at 48.281 on Mon Mar 28 06:34:00 MDT 2016.
    etc...

The simulation results are returned as JSON:

    {
     	"ticker": "SCHX",
    	"initialCash": 20000.0,
    	"initialShares": 100,
    	"start": 1459150200000,
     	"end": 1461938400000,
    	"transactionCost": 0.05,
    	"transactionSize": 30,
    	"fallTrigger": 0.06,
    	"climbTrigger": 0.05,
    	"initialPortfolioValue": 24832.0,
    	"sellTransactionCount": 40,
    	"buyTransactionCount": 37,
    	"finalCash": 24466.810000000063,
    	"finalShares": 10,
    	"finalPortfolioValue": 24955.41000000006,
    	"portfolioPercentageChange": 0.0049697970360849586
    }


## Prediction markets: 2016 election

I find prediction markets fascinating, and notice that predictit.org has made pricing accessible via API.

My son, Miles, was curious to know if there are pricing differences throughout the day. Our hypothesis was that there may be predictable price swings at certain times of the day, since Democrats are more highly concentrated in the (vertical) coastal areas, and Republicans are more concentrated in the center. 

We thought that the price might swing, by some small but predictable amount, as the demographics of the active internet users changes throughout the day, e.g. a possible surge of democrats first thing in the morning, that swings back as the central southern states wake up. We started to collect some data to test our theory:

![PredictIt.org last trade prices](predictit_election_last_trade_prices.png)

### What we saw ###

The prices generally don't fluctuate within more than a couple of cents over a 24 hour period. Given that there's a one-cent spread between the buy price and cell price, we need to see a movement of at least two cents to make any money. The price fluctuations were too small to trade, regardless of whether there's any intra-day seasonality.

