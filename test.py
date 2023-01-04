"""Tests the PhemexBoy Module"""

import os
from phemexboy import PhemexBoy
from dotenv import load_dotenv

load_dotenv()
client = PhemexBoy(os.getenv("KEY"), os.getenv("SECRET"))


def test_public():
    client = PhemexBoy()

    future_symbols = client.future_symbols()
    assert len(future_symbols) > 0

    spot_symbols = client.symbols()
    assert len(spot_symbols) > 0

    currencies = client.currencies()
    assert len(currencies) > 0

    spot_price = client.price("sBTCUSDT")
    assert spot_price > 0

    future_price = client.price("BTC/USD:USD")
    assert future_price > 0

    return True


def test_spot():
    global client

    balance = client.balance("USDT")
    assert balance is not None

    amt = client.usdt_converter("sBTCUSDT", 21)
    price = client.price("sBTCUSDT") * 0.50
    id = client.buy("sBTCUSDT", "limit", amt, price)
    assert id is not None

    id = client.cancel(id, "sBTCUSDT")
    assert id is not None

    amt = client.usdt_converter("sBTCUSDT", 21)
    price = client.price("sBTCUSDT") * 0.50
    id = client.buy("sBTCUSDT", "limit", amt, price)
    assert id is not None

    resp = client.cancel_all("sBTCUSDT")
    assert resp is not None

    amt = client.usdt_converter("sBTCUSDT", 90)
    client.buy("sBTCUSDT", "market", amt)

    amt = client.balance("BTC")
    id = client.sell("sBTCUSDT", "market", amt)
    assert id is not None

    return True


def test_future():
    global client

    bal = client.future_balance("USD")
    assert bal is not None

    price = client.price("BTC/USD:USD") * 0.50
    sl = price - (price * 0.01)
    tp = price + (price * 0.02)
    id = client.long("BTC/USD:USD", "limit", 1, price, sl, tp)
    assert id is not None
    assert client.cancel(id, "BTC/USD:USD") is not None

    position = client.positions("BTC/USD:USD")
    in_position = client.in_position("BTC/USD:USD")
    assert position is not None and in_position is not None

    # Manual Test
    client.leverage(10, "BTC/USD:USD")
    id = client.long("BTC/USD:USD", "market", 1)
    client.close("BTC/USD:USD", 1)
    id = client.short("BTC/USD:USD", "market", 1)
    client.close("BTC/USD:USD", 1)

    return True


if __name__ == "__main__":
    # tests = [test_public, test_spot, test_future]
    tests = [test_public]

    i = 1
    for test in tests:
        if test():
            print(f"Test {i} passed")
        else:
            print(f"Test {i} failed")
        i += 1
