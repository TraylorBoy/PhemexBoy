"""OrderClient Tests"""

import unittest

from phemexboy.api.public import PublicClient
from phemexboy.api.auth.client import AuthClient
from phemexboy.interfaces.auth.order_interface import OrderClientInterface
from phemexboy.helpers.conversions import usdt_to_crypto


class TestSpot(unittest.TestCase):
    AUTH_CLIENT = AuthClient()
    PUB_CLIENT = PublicClient()

    def test_spot(self):
        auth_client = self.AUTH_CLIENT
        pub_client = self.PUB_CLIENT
        symbol = pub_client.symbol(base="BTC", quote="USD", code="spot")

        # Limit Buy
        type = "limit"
        price = 1000
        usdt_bal = auth_client.balance(currency="USDT", code="spot")
        amount = usdt_to_crypto(usdt_balance=usdt_bal, price=price, percent=90)

        order = auth_client.buy(symbol=symbol, type=type, amount=amount, price=price)
        self.assertIsInstance(order, OrderClientInterface)
        self.assertEqual(order.pending(), True)
        print(f"Testing __str__: \n{order}")

        price = 1001
        amount = usdt_to_crypto(usdt_balance=usdt_bal, price=price, percent=90)
        order.edit(amount=amount, price=price)
        self.assertEqual(order.query(request="price"), price)

        order.cancel()
        self.assertEqual(order.canceled(), True)

        # Market Buy
        type = "market"
        amount = usdt_to_crypto(
            usdt_balance=usdt_bal, price=pub_client.price(symbol), percent=90
        )
        order = auth_client.buy(symbol=symbol, type=type, amount=amount)
        self.assertEqual(order.closed(), True)
        self.assertEqual(order.pending(), False)

        # Limit Sell
        type = "limit"
        price = 100000
        amount = auth_client.balance(currency="BTC", code="spot")
        order = auth_client.sell(symbol=symbol, type=type, amount=amount, price=price)
        self.assertEqual(order.pending(), True)

        price = 90000
        order.edit(amount=amount, price=price)
        self.assertEqual(order.query(request="price"), price)

        order.cancel()
        self.assertEqual(order.canceled(), True)

        # Market Sell
        type = "market"
        amount = auth_client.balance(currency="BTC", code="spot")
        order = auth_client.sell(symbol=symbol, type=type, amount=amount)
        self.assertEqual(order.closed(), True)
        self.assertEqual(order.pending(), False)

    def test_trade(self):
        auth_client = self.AUTH_CLIENT
        pub_client = self.PUB_CLIENT
        symbol = pub_client.symbol(base="BTC", quote="USD", code="spot")

        # Limit Buy
        type = "limit"
        price = pub_client.price(symbol=symbol)
        usdt_bal = auth_client.balance(currency="USDT", code="spot")
        amount = usdt_to_crypto(usdt_balance=usdt_bal, price=price, percent=90)
        order = auth_client.buy(symbol=symbol, type=type, amount=amount, price=price)

        # Make sure order was placed and closed
        print("Pending")
        if not order.pending():
            print("Retrying")
            if order.retry():
                self.assertEqual(order.pending(), True)

        print("Closing")
        if order.close(retry=True, wait=20, tries=5):
            print("Closed")
            self.assertEqual(order.closed(), True)

            # Market Sell
            print("Selling")
            type = "market"
            amount = auth_client.balance(currency="BTC", code="spot")
            auth_client.sell(symbol=symbol, type=type, amount=amount)
