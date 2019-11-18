"""
This module defines the continuous queries used at influxdb that do the candles
aggregation. This module are used only in the setup phase.
"""

from lib.db.client import client

def run():
    """ creates the continues queries for 1m, 5m and 10m candles """

    # 1m candles
    client().query(
        """
        CREATE CONTINUOUS QUERY tickers_to_candles_1m ON smart_development
        RESAMPLE EVERY 10s FOR 2m
        BEGIN
            SELECT first(value) AS open, last(value) AS close, max(value) AS high, min(value) AS low
            INTO candles_1m
            FROM tickers
            GROUP BY time(1m), pair
        END
        """
    )

    # 5m candles
    client().query(
        """
        CREATE CONTINUOUS QUERY candles_1m_to_candles_5m ON smart_development
        RESAMPLE EVERY 10s FOR 10m
        BEGIN
            SELECT first(open) AS open, last(close) AS close, max(high) AS high, min(low) AS low
            INTO candles_5m
            FROM candles_1m
            GROUP BY time(5m), pair
        END
        """
    )

    # 10m candles
    client().query(
        """
        CREATE CONTINUOUS QUERY candles_1m_to_candles_10m ON smart_development
        RESAMPLE EVERY 10s FOR 20m
        BEGIN
            SELECT first(open) AS open, last(close) AS close, max(high) AS high, min(low) AS low
            INTO candles_10m
            FROM candles_1m
            GROUP BY time(10m), pair
        END
        """
    )

if __name__ == "__main__":
    run()
