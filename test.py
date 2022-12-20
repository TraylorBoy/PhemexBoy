"""Tests the PhemexBoy Module"""

import os
from phemexboy import PhemexBoy
from dotenv import load_dotenv

load_dotenv()
client = PhemexBoy(os.getenv("KEY"), os.getenv("SECRET"))

# Test balance
def test_one():
    global client

    bal = client.balance("USD")
    print(bal)

    assert bal is not None

    return True


# Test market retrieval
def test_two():
    global client

    markets = client.markets()

    assert len(markets) > 0

    return True


# Test token retrieval
def test_three():
    global client

    tokens = client.tokens()

    assert len(tokens) > 0

    return True


if __name__ == "__main__":
    tests = [test_one, test_two, test_three]
    i = 1
    for test in tests:
        if test():
            print(f"Test {i} passed")
        else:
            print(f"Test {i} failed")
        i += 1
