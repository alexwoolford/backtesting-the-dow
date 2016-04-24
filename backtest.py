#!/usr/bin/env python

import logging
from jproperties import Properties
import mysql.connector
from mysql.connector.cursor import MySQLCursorDict
import sys

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='backtest.log',
                    filemode='a')


class BackTest:

    def __init__(self):
        config_file_name = 'backtesting_the_dow.properties'
        try:
            # Read properties
            properties = Properties()
            with open(config_file_name, "rb") as f:
                properties.load(f, "utf-8")

            logging.debug("Read properties from " + config_file_name + ".")

            # MySQL
            self.mysql_user = properties.properties['mysql.user']
            self.mysql_password = properties.properties['mysql.password']
            self.mysql_host = properties.properties['mysql.host']
            self.mysql_port = properties.properties['mysql.port']
            self.mysql_database = properties.properties['mysql.database']
        except:
            logging.error("Error reading config file {0}: {1}".format(config_file_name, str(sys.exc_info())))
            sys.exit(1)

    def run_scenario(self,
                     initial_capital,
                     initial_shares,
                     transaction_cost,
                     transaction_size,
                     fall_trigger_percent,
                     climb_trigger_percent):

        mysql_connection = mysql.connector.connect(user=self.mysql_user,
                                                   password=self.mysql_password,
                                                   host=self.mysql_host,
                                                   database=self.mysql_database,
                                                   port=self.mysql_port)
        logging.debug("Connected to MySQL")

        cursor = mysql_connection.cursor(cursor_class=MySQLCursorDict)
        logging.debug("Created MySQL cursor.")

        sql = "SELECT datetime, open FROM intra_day ORDER BY datetime"
        cursor.execute(sql)
        logging.debug("Executed SQL: " + sql)

        records = cursor.fetchall()
        logging.debug("Fetched " + str(len(records)) + " records.")

        last_transacted_price = records[0]['open']

        for record in records:
            current_price = record['open']
            print last_transacted_price, current_price

        mysql_connection.close()
        logging.debug("Closed MySQL connection.")


if __name__ == "__main__":
    backTest = BackTest()
    backTest.run_scenario(initial_capital=1000,
                          initial_shares=10,
                          transaction_cost=10,
                          transaction_size=1,
                          fall_trigger_percent=0.01,
                          climb_trigger_percent=0.01)
    del backTest
