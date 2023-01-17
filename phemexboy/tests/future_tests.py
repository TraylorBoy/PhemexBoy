"""PositionClient Tests"""

import unittest

from phemexboy.api.public import PublicClient
from phemexboy.api.auth.client import AuthClient
from phemexboy.helpers.conversions import stop_loss, take_profit


class TestFuture(unittest.TestCase):
    AUTH_CLIENT = AuthClient()
    PUB_CLIENT = PublicClient()

    def test_future(self):
        auth_client = self.AUTH_CLIENT
        pub_client = self.PUB_CLIENT
        symbol = pub_client.symbol(base="BTC", quote="USD", code="future")
        amount = 1

        # Set leverage
        auth_client.leverage(amount=5, symbol=symbol)

        # Limit long
        type = "limit"
        price = 9000
        sl = stop_loss(price=price, percent=1, pos="long")
        tp = take_profit(price=price, percent=2, pos="long")

        order = auth_client.long(
            symbol=symbol, type=type, amount=amount, price=price, sl=sl, tp=tp
        )
        self.assertEqual(order.pending(), True)

        # Test __str__
        print(order)

        order.cancel()
        self.assertEqual(order.canceled(), True)

        # Limit short
        type = "limit"
        price = 100000

        order = auth_client.short(symbol=symbol, type=type, amount=amount, price=price)
        self.assertEqual(order.pending(), True)

        order.cancel()
        self.assertEqual(order.canceled(), True)

        # Market long
        type = "market"
        order = auth_client.long(symbol=symbol, type=type, amount=amount)
        self.assertEqual(order.closed(), True)

        position = auth_client.position(symbol=symbol)

        # Test __str__
        print(position)

        all_contracts = position.query("contracts")
        position.close(all_contracts)
        self.assertEqual(position.closed(), True)

        # Market short
        # Tests order close amount
        type = "market"
        order = auth_client.short(symbol=symbol, type=type, amount=2)
        self.assertEqual(order.closed(), True)

        position = auth_client.position(symbol=symbol)
        position.close(1)
        self.assertEqual(position.closed(), False)
        position.close(1)
        self.assertEqual(position.closed(), True)

    def test_swap(self):
        auth_client = self.AUTH_CLIENT
        pub_client = self.PUB_CLIENT
        symbol = pub_client.symbol(base="ETH", quote="USD", code="future")
        amount = 1

        # Limit Buy
        type = "limit"
        price = pub_client.price(symbol=symbol) - 0.01
        order = auth_client.long(symbol=symbol, type=type, amount=amount, price=price)

        # Make sure order was placed and closed
        print("Pending")
        if not order.pending():
            print("Retrying")
            if order.retry():
                self.assertEqual(order.pending(), True)

        print("Closing")
        if order.close(retry=True, wait=2, tries=10):
            print("Closed")
            self.assertEqual(order.closed(), True)
            position = auth_client.position(symbol)
            position.close(all=True)
