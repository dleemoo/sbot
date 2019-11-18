"""
This module implements a simple websocket service that returns the n last
candlestick for each crypto associated with USDC currency. The requests need to
be in the following formats:

ws://0.0.0.0:WEBSOCKET_PORT/[1m,5m,10m][1,2,3]

The allowed values for n are 1, 2 or 3
"""

from os import environ as env

import logging
import asyncio
import json
import websockets

from lib.db.candles import candles

async def serve_candles(websocket, path):
    """ Returns the candles given the path """
    logging.info(path)
    period, limit = path[1:].split("-", 1)
    logging.info(period)
    logging.info(limit)
    if period in ["1m", "5m", "10m"] and int(limit) in range(4):
        while True:
            await websocket.send(
                json.dumps(candles(period, int(limit)))
            )
            await asyncio.sleep(float(env["WEBSOCKET_UPDATE_INTERVAL"]))
    else:
        logging.error(f"Invalid candle path received: {path}")

if __name__ == "__main__":
    START_SERVER = websockets.serve(serve_candles, "0.0.0.0", int(env["WEBSOCKET_PORT"]))

    asyncio.get_event_loop().run_until_complete(START_SERVER)
    asyncio.get_event_loop().run_forever()
