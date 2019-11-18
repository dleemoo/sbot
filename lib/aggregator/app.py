import logging
import time

from os import environ as env
from schedule import run_pending, every

from lib.aggregator.ticker import write, fetch

def write_current_info():
    try:
        write(fetch())
    except BaseException as error:
        logging.error(str(error))

if __name__ == "__main__":
    every(float(env["TICKER_FETCH_INTERVAL"])).seconds.do(write_current_info)
    logging.info("Starting ticker loop ...")
    while True:
        run_pending()
        time.sleep(float(env["TICKER_WAIT_INTERVAL"]))
