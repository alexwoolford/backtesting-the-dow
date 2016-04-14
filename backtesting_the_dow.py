#!/usr/bin/env python

import ConfigParser


class BacktestingTheDow:

    def __init__(self):
        config = ConfigParser.RawConfigParser()
        config.read('backtesting_the_dow.cfg')

        self.quandl_api_key = config.get('quandl', 'api_key')

    def run(self):
        print self.quandl_api_key



if __name__ == "__main__":
    backtestingTheDow = BacktestingTheDow()
    backtestingTheDow.run()
