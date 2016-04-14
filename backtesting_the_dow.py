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
        self.mysql_user = config.get('mysql', 'user')
        self.mysql_password = config.get('mysql', 'password')
        self.mysql_host = config.get('mysql', 'host')
        self.mysql_port = config.get('mysql', 'port')
        self.mysql_database = config.get('mysql', 'database')

    def get_intraday_data(self, ticker, interval_seconds=61, num_days=60):
        # Credit to http://www.theodor.io/scraping-google-finance-data-using-pandas/
        mysql_connection = mysql.connector.connect(user=self.mysql_user,
                                                   password=self.mysql_password,
                                                   host=self.mysql_host,
                                                   database=self.mysql_database,
                                                   port=self.mysql_port)

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

        df.to_sql("intra_day_schx", mysql_connection, flavor='mysql', schema=self.mysql_database, if_exists='append',
                  index=False, index_label=None, chunksize=None, dtype=None)


if __name__ == "__main__":
    collectIntraday = CollectIntraday()
    collectIntraday.get_intraday_data("SCHX")
    del collectIntraday
