"""Tests the PhemexBoy Module"""

import os
from phemexboy import PhemexBoy
from dotenv import load_dotenv

load_dotenv()
client = PhemexBoy(os.getenv("KEY"), os.getenv("SECRET"))

# Test balance
def test_one():
    global client

    spot_bal = client.balance("USD")
    futures_bal = client.futures_balance("USD")

    assert spot_bal is not None and futures_bal is not None

    return True


# Test future methods
def test_two():
    global client

    position = client.futures_position("ETH/USD:USD")
    print(position)
    assert position is not None

    symbols = client.futures_symbols()
    print(symbols)
    assert len(symbols) > 0

    return True


if __name__ == "__main__":
    tests = [test_one, test_two]
    i = 1
    for test in tests:
        if test():
            print(f"Test {i} passed")
        else:
            print(f"Test {i} failed")
        i += 1
