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
                    filename='backtest.log',
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
                     fall_trigger_percent,
                     climb_trigger_percent):
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

            for record in records:

                current_price = record['open']
                datetime = record['datetime']
                price_change_percent = (current_price - last_transacted_price) / last_transacted_price

                # should we try to buy or sell?
                transaction = None
                if price_change_percent > 0 and price_change_percent > climb_trigger_percent:
                    # try and sell
                    if shares > transaction_size:
                        cash -= transaction_cost
                        cash += transaction_size * current_price
                        shares = shares - transaction_size

                        last_transacted_price = current_price
                        transaction = "sell"

                elif price_change_percent < 0 and abs(price_change_percent) > fall_trigger_percent:
                    # try and buy
                    if cash - transaction_cost > current_price * transaction_size:
                        cash -= transaction_cost
                        cash -= transaction_size * current_price
                        shares += transaction_size

                        last_transacted_price = current_price
                        transaction = "buy"

                if transaction:
                    portfolio_value = cash + (shares * last_transacted_price)
                    logging.debug("Transaction: {0} executed on {1}, {2} shares at {3}. Balance: shares={4}; cash={5}; portfolio value={6}".format(
                        transaction,
                        datetime,
                        transaction_size,
                        current_price,
                        shares,
                        cash,
                        portfolio_value))

            percentage_change = (portfolio_value - initial_portfolio_value) / initial_portfolio_value
            logging.info("percentage change: {0}".format(percentage_change))

            sql = "INSERT INTO scenario_outcome " \
                  "    (transaction_cost, transaction_size, fall_trigger_percentage, climb_trigger_percentage, percentage_change) " \
                  "VALUES ({0}, {1}, {2}, {3}, {4})".format(transaction_cost,
                                                            transaction_size,
                                                            fall_trigger_percentage,
                                                            climb_trigger_percentage,
                                                            percentage_change)
            logging.debug("sql: " + sql)
            cursor.execute(sql)
            cursor.execute('commit')
            logging.debug("Saved scenario outcome to MySQL.")

            mysql_connection.close()
            logging.debug("Closed MySQL connection.")

        except:
            logging.error("error running scenario {0}, ".format(str(sys.exc_info())))

    @staticmethod
    def get_scenarios():

        transaction_costs = [5, 6, 7, 8, 9, 10]
        transaction_sizes = [1, 2, 3, 4, 5, 6]
        fall_trigger_percentages = [0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04]
        climb_trigger_percentages = [0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04]

        scenario_lists = [transaction_costs, transaction_sizes, fall_trigger_percentages, climb_trigger_percentages]

        return list(itertools.product(*scenario_lists))

if __name__ == "__main__":
    backTest = BackTest()
    for scenario in backTest.get_scenarios():
        transaction_cost, transaction_size, fall_trigger_percentage, climb_trigger_percentage = scenario

        backTest.run_scenario(cash=1000,                                        # initial condition
                              shares=10,                                        # initial condition
                              transaction_cost=transaction_cost,                # scenario parameter
                              transaction_size=transaction_size,                # scenario parameter
                              fall_trigger_percent=fall_trigger_percentage,     # scenario parameter
                              climb_trigger_percent=climb_trigger_percentage)   # scenario parameter
    del backTest
