#!/usr/bin/env python

import requests
import json
from jproperties import Properties
import mysql.connector


class ElectionPredictItTrend:

    """
    There's a prediction market for the 2016 US election:
        https://www.predictit.org/Market/1234/Who-will-win-the-2016-US-presidential-election

    In the last election, I noticed that InTrade, a prediction market that subsequently went out of business, had a
    fairly strong (and accurate) opinion about the outcome while pundits were still undecided.

    I thought that it would be interesting to track the prediction market prices for the candidates to supplement the
    news, which tends to be very verbose and might not be objective.
    """

    def __init__(self):
        # Read properties
        config_file_name = 'backtesting_the_dow.properties'
        properties = Properties()
        with open(config_file_name, "rb") as f:
            properties.load(f, "utf-8")

        self.base_url = "https://www.predictit.org/api/marketdata/ticker/"

        # MySQL
        self.mysql_user = properties.properties['mysql.user']
        self.mysql_password = properties.properties['mysql.password']
        self.mysql_host = properties.properties['mysql.host']
        self.mysql_port = properties.properties['mysql.port']
        self.mysql_database = properties.properties['mysql.database']

        self.mysql_connection = mysql.connector.connect(user=self.mysql_user,
                                                        password=self.mysql_password,
                                                        host=self.mysql_host,
                                                        database=self.mysql_database,
                                                        port=self.mysql_port)

    def capture_ticker_price(self, ticker):
        response = requests.get("https://www.predictit.org/api/marketdata/ticker/{0}".format(ticker))

        response_json = json.loads(response.content)

        for contract in response_json['Contracts']:
            cursor = self.mysql_connection.cursor()
            last_trade_price = contract['LastTradePrice']
            short_name = contract['ShortName']
            sql = """INSERT INTO predictit_prices (ticker, short_name, last_trade_price) VALUES ({0}, {1}, {2})"""\
                .format(json.dumps(ticker),
                        json.dumps(short_name),
                        last_trade_price)
            cursor.execute(sql)
        cursor.execute('commit')
        self.mysql_connection.close()

if __name__ == "__main__":
    tickers = ['CLINTON.USPREZ16']
    electionPredictItTrend = ElectionPredictItTrend()
    for ticker in tickers:
        electionPredictItTrend.capture_ticker_price(ticker)
