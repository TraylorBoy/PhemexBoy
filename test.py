"""Tests the PhemexBoy Module"""

import os
from phemexboy import PhemexBoy
from dotenv import load_dotenv

load_dotenv()
client = PhemexBoy(os.getenv("KEY"), os.getenv("SECRET"))

print(client.client.has)

# Test PhemexBoy
def test_spot():
    global client

    # Test SPOT Properties
    symbols = client.symbols()
    assert len(symbols) > 0

    currencies = client.currencies()
    assert len(currencies) > 0

    timeframes = client.timeframes()
    assert len(timeframes) > 0

    time = client.time("2022-12-22T00:00:00Z")
    assert time is not None

    # Test SPOT Methods
    orderbook = client.orderbook("sBTCUSDT")
    assert len(orderbook) > 0

    price = client.price("sBTCUSDT")
    assert len(price) > 0

    day_candle = client.candle("sBTCUSDT", "1d")
    candle = client.candle("sBTCUSDT", "1d", since=client.time("2022-12-22T00:00:00Z"))
    assert len(day_candle) > 0
    assert len(candle) > 0

    trades = client.trades("sBTCUSDT")
    day_trades = client.trades("sBTCUSDT", client.time("2022-12-22T00:00:00Z"))
    assert len(trades) > 0
    assert len(day_trades) > 0

    status = client.status()
    assert len(status) > 0

    return True


if __name__ == "__main__":
    tests = [test_spot]
    i = 1
    for test in tests:
        if test():
            print(f"Test {i} passed")
        else:
            print(f"Test {i} failed")
        i += 1
