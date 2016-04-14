#!/usr/bin/env python

import ConfigParser
import mysql.connector
import requests
import pandas as pd
from datetime import datetime


class CollectIntraday:

    def __init__(self):
        config = ConfigParser.RawConfigParser()
        config.read('collect_intraday.cfg')

        # MySQL
        mysql_user = config.get('mysql', 'user')
        mysql_password = config.get('mysql', 'password')
        mysql_host = config.get('mysql', 'host')
        mysql_port = config.get('mysql', 'port')
        self.mysql_database = config.get('mysql', 'database')

        self.mysql_connection = mysql.connector.connect(user=mysql_user,
                                                        password=mysql_password,
                                                        host=mysql_host,
                                                        database=self.mysql_database,
                                                        port=mysql_port)

    def get_intraday_data(self, ticker, interval_seconds=61, num_days=60):
        # Credit to http://www.theodor.io/scraping-google-finance-data-using-pandas/

        # Specify URL string based on function inputs.
        url_string = "http://www.google.com/finance/getprices?q={0}&i={1}&p={2}d&f=d,o,h,l,c,v".format(ticker, interval_seconds, num_days)

        # Request the text, and split by each line
        r = requests.get(url_string).text.split()

        # Split each line by a comma, starting at the 8th line
        r = [line.split(',') for line in r[7:]]

        # Save data in Pandas DataFrame
        df = pd.DataFrame(r, columns=['Datetime', 'Close', 'High', 'Low', 'Open', 'Volume'])

        # Convert UNIX to Datetime format
        df['Datetime'] = df['Datetime'].apply(lambda x: datetime.fromtimestamp(int(x[1:])))

        df['ticker'] = ticker

        df.to_sql("intra_day", self.mysql_connection, flavor='mysql', schema=self.mysql_database, if_exists='append',
                  index=False, index_label=None, chunksize=None, dtype=None)

    def get_tickers(self):
        cursor = self.mysql_connection.cursor()
        cursor.execute("SELECT ticker FROM tickers")

        tickers = [ticker[0] for ticker in cursor.fetchall()]

        return tickers

    def run(self):
        tickers = self.get_tickers()
        for ticker in tickers:
            self.get_intraday_data(ticker)

if __name__ == "__main__":
    collectIntraday = CollectIntraday()
    collectIntraday.run()
    del collectIntraday
