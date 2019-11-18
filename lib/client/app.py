import asyncio
import sys
import json
import websockets

def update_screen(data):
    print("\x1b[2J")
    print("%20s %7s %17s %17s %17s %17s" % ("time", "crypto", "open", "high", "low", "close"))
    print("-" * 100)
    for item in data:
        print("%s %7s %17f %17f %17f %17f" % (item["time"], item["pair"][5:], item["open"], item["high"], item["low"], item["close"]))

async def candles(size):
    uri = f"ws://sb-websocket:6789/{size}"
    async with websockets.connect(uri) as socket:
        while True:
            response = await socket.recv()
            update_screen(json.loads(response))

if __name__ == "__main__":
    VALID_OPTIONS = ["1m", "5m", "10m"]
    if len(sys.argv) < 2 or not sys.argv[1] in VALID_OPTIONS:
        print(f"Usage: {sys.argv[0]} [{'|'.join(VALID_OPTIONS)}]")
        exit(1)
    PERIOD = sys.argv[1]

    LIMIT = 1
    if len(sys.argv) == 3:
        if int(sys.argv[2]) in range(4):
            LIMIT = sys.argv[2]
        else:
            print(f"Usage: {sys.argv[0]} [{'|'.join(VALID_OPTIONS)}] [1|2|3]")
            exit(2)

    LOOP = asyncio.get_event_loop()
    TASK = asyncio.ensure_future(candles(f"{PERIOD}-{LIMIT}"))

    try:
        LOOP.run_until_complete(TASK)
    except KeyboardInterrupt:
        print("\nBye!")
