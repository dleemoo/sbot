"""
Provides access to the candles measurements
"""

from .client import client

def candles(period, limit=1):
    """
    Returns the candlesticks given the desired period

    This function intentionally allows any period value and try to make the query.
    Validation about valid periods are delegated to the caller.
    """
    measurement = f"candles_{period}"
    return flatten_list(query(measurement, limit))

def query(measurement, limit):
    """
    Returns the result from some candle measurement

    This metethod filters the pairs of USDC * crypto and does not return the
    entiry dataset.
    """
    return client().query(
        f"""
            SELECT pair, open, high, low, close
            FROM {measurement} WHERE pair =~ /^USDC_*/
            GROUP BY pair
            ORDER BY time DESC LIMIT {limit}
        """)

def flatten_list(result_set):
    """ Returns a plain list given a gouped result set """
    return sum(list(result_set), [])
