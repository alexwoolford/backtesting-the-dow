#!/usr/bin/env python

import logging
from jproperties import Properties
import mysql.connector
import requests
import pandas as pd
from datetime import datetime
import sys

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='collect_intraday.log',
                    filemode='a')


class CollectIntraday:

    def __init__(self):
        config_file_name = 'backtesting_the_dow.properties'
        try:
            # Read properties
            properties = Properties()
            with open(config_file_name, "rb") as f:
                properties.load(f, "utf-8")

            # MySQL
            self.mysql_user = properties.properties['mysql.user']
            self.mysql_password = properties.properties['mysql.password']
            self.mysql_host = properties.properties['mysql.host']
            self.mysql_port = properties.properties['mysql.port']
            self.mysql_database = properties.properties['mysql.database']
        except:
            logging.error("Error reading config file {0}: {1}".format(config_file_name, str(sys.exc_info())))
            sys.exit(1)

        try:
            self.mysql_connection = mysql.connector.connect(user=self.mysql_user,
                                                            password=self.mysql_password,
                                                            host=self.mysql_host,
                                                            database=self.mysql_database,
                                                            port=self.mysql_port)
            logging.info("Connected to MySQL host: {0}, port: {1}, database: {2}".format(self.mysql_host,
                                                                                         self.mysql_port,
                                                                                         self.mysql_database))
        except:
            logging.error("Error connecting to MySQL: {0}".format(str(sys.exc_info())))
            sys.exit(1)

    def get_intraday_data(self, ticker, interval_seconds=61, num_days=30):
        # Credit to http://www.theodor.io/scraping-google-finance-data-using-pandas/

        try:
            # Specify URL string based on function inputs.
            url_string = "http://www.google.com/finance/getprices?q={0}&i={1}&p={2}d&f=d,o,h,l,c,v".format(ticker,
                                                                                                           interval_seconds,
                                                                                                           num_days)
            # Request the text, and split by each line
            r = requests.get(url_string).text.split()

            # Split each line by a comma, starting at the 8th line
            r = [line.split(',') for line in r[7:]]

            # Save data in Pandas DataFrame
            df = pd.DataFrame(r, columns=['datetime', 'close', 'high', 'low', 'open', 'volume'])

            # Convert UNIX to Datetime format
            df['datetime'] = df['datetime'].apply(lambda x: datetime.fromtimestamp(int(x[1:])))

            df['ticker'] = ticker

            df.to_sql("intra_day",
                      self.mysql_connection,
                      flavor='mysql',
                      schema=self.mysql_database,
                      if_exists='append',
                      index=False)

            logging.info("Collected {0} rows for ticker {1}".format(len(df.index), ticker))

        except:
            logging.error("Error writing pandas dataframe for ticker {0}: {1}".format(ticker, str(sys.exc_info())))
            sys.exit(1)

    def get_tickers(self):
        try:
            cursor = self.mysql_connection.cursor()
            cursor.execute("SELECT ticker FROM tickers")
            tickers = [ticker[0] for ticker in cursor.fetchall()]
            logging.info("Got tickers: {0}".format(", ".join(tickers)))
        except:
            logging.error("Error getting tickers: ".format(str(sys.exc_info())))
            sys.exit(1)

        return tickers

    def run(self):
        tickers = self.get_tickers()
        for ticker in tickers:
            self.get_intraday_data(ticker)

if __name__ == "__main__":
    collectIntraday = CollectIntraday()
    collectIntraday.run()
    del collectIntraday
