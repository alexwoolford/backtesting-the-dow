#!/usr/bin/env python

import itertools
import urllib
import requests


def get_scenarios():

    transaction_costs = [0.05]
    transaction_sizes = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70]
    fall_trigger = [0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.20, 0.21, 0.22, 0.23, 0.24, 0.25]
    climb_trigger = [0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.20, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.30, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.40]

    # transaction_costs = [0.05]
    # transaction_sizes = [46]
    # fall_trigger = [0.18]
    # climb_trigger = [0.25]

    scenario_lists = [transaction_costs, transaction_sizes, fall_trigger, climb_trigger]

    return list(itertools.product(*scenario_lists))


def run_scenario(ticker,
                 cash,
                 shares,
                 transaction_cost,
                 transaction_size,
                 fall_trigger,
                 climb_trigger):

    scenario_dict = {'ticker': ticker,
                     'cash': cash,
                     'shares': shares,
                     'transactionCost': transaction_cost,
                     'transactionSize': transaction_size,
                     'fallTrigger': fall_trigger,
                     'climbTrigger': climb_trigger}
    url = 'http://localhost:8080/scenario?' + urllib.urlencode(scenario_dict)
    requests.get(url)

if __name__ == "__main__":
    for scenario in get_scenarios():
        transaction_cost, transaction_size, fall_trigger, climb_trigger = scenario
        run_scenario(ticker='SCHX',
                     cash=100000,                                        # initial condition
                     shares=1000,                                        # initial condition
                     transaction_cost=transaction_cost,                 # scenario parameter
                     transaction_size=transaction_size,                 # scenario parameter
                     fall_trigger=fall_trigger,                         # scenario parameter
                     climb_trigger=climb_trigger)                       # scenario parameter
