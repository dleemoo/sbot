"""
Encapsulates the access configuration for influx database
"""

from os import environ as env
from influxdb import InfluxDBClient as db

def client():
    """ Returns a valid configuration to connect with the influx database """
    return db(env["INFLUX_HOST"], env["INFLUX_PORT"], env["INFLUX_USER"],
              env["INFLUX_PASS"], env["INFLUX_DB"])
