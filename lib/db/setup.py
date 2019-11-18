"""
Setup influxdb
"""

from os import environ as env
from .client import client

def run():
    """ creates the database to be used """
    client().create_database(env["INFLUX_DB"])

if __name__ == "__main__":
    run()
