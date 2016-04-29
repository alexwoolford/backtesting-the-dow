#!/usr/bin/env python

import logging
from jproperties import Properties
import mysql.connector
from mysql.connector.cursor import MySQLCursorDict
import sys
import itertools

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='backtest_fixed.log',
                    filemode='w')


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
                     cash,
                     shares,
                     transaction_cost,
                     transaction_size,
                     fall_trigger,
                     climb_trigger):
        try:
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
            initial_portfolio_value = cash + shares * last_transacted_price
            portfolio_value = initial_portfolio_value
            sell_transaction_count = 0

            for record in records:

                current_price = record['open']
                datetime = record['datetime']
                price_change = current_price - last_transacted_price

                # should we try to buy or sell?
                transaction = None
                if price_change > 0 and price_change > climb_trigger:
                    # try and sell
                    if shares > transaction_size:
                        cash -= transaction_cost
                        cash += transaction_size * current_price
                        shares = shares - transaction_size

                        last_transacted_price = current_price
                        transaction = "sell"
                        sell_transaction_count += 1

                elif price_change < 0 and abs(price_change) > fall_trigger:
                    # try and buy
                    if cash - transaction_cost > current_price * transaction_size:
                        cash -= transaction_cost
                        cash -= transaction_size * current_price
                        shares += transaction_size

                        last_transacted_price = current_price
                        transaction = "buy"


            profit_per_transaction = transaction_size * climb_trigger
            profit = profit_per_transaction * sell_transaction_count

            logging.info("sells: {0}, profit: {1}".format(sell_transaction_count, profit))

            sql = "INSERT INTO scenario_outcome_fixed (transaction_cost, transaction_size, fall_trigger, climb_trigger, sell_transaction_count, profit_per_transaction, profit) VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6})".format(transaction_cost, transaction_size, fall_trigger, climb_trigger, sell_transaction_count, profit_per_transaction, profit)

            cursor = mysql_connection.cursor()
            cursor.execute(sql)
            cursor.execute('commit')

            mysql_connection.close()
            logging.debug("Closed MySQL connection.")

        except:
            logging.error("error running scenario {0}, ".format(str(sys.exc_info())))

    @staticmethod
    def get_scenarios():

        transaction_costs = [0.05]
        transaction_sizes = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70]
        fall_trigger = [0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.20, 0.21, 0.22, 0.23, 0.24, 0.25]
        climb_trigger = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.4, 0.45, 0.5]

        # transaction_costs = [0.05]
        # transaction_sizes = [46]
        # fall_trigger = [0.18]
        # climb_trigger = [0.25]

        scenario_lists = [transaction_costs, transaction_sizes, fall_trigger, climb_trigger]

        return list(itertools.product(*scenario_lists))

if __name__ == "__main__":
    backTest = BackTest()
    for scenario in backTest.get_scenarios():
        transaction_cost, transaction_size, fall_trigger, climb_trigger = scenario

        backTest.run_scenario(cash=100000,                                        # initial condition
                              shares=1000,                                        # initial condition
                              transaction_cost=transaction_cost,                 # scenario parameter
                              transaction_size=transaction_size,                 # scenario parameter
                              fall_trigger=fall_trigger,                         # scenario parameter
                              climb_trigger=climb_trigger)                       # scenario parameter
    del backTest
