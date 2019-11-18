"""
Module to interact with external APIs to fetch data and write then back at our side
"""

from poloniex import Poloniex
from lib.db.client import client

def fetch():
    """ Fetches data from the default external API """
    return Poloniex().returnTicker().items()

def write(data):
    """ Write currency pair values to the datastore """
    return client().write_points(map(db_item, data))

def db_item(item):
    """ Format the data to be writen at our datastore """
    currency_pair, values = item

    return {
        "measurement": "tickers",
        "tags": {
            "pair": currency_pair
        },
        "fields": {
            "value": values["last"]
        }
    }
