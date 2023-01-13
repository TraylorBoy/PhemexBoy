"""AuthClient Tests"""

import unittest

from phemexboy.api.public import PublicClient
from phemexboy.api.auth.client import AuthClient
from phemexboy.interfaces.auth.client_interface import AuthClientInterface
from phemexboy.interfaces.auth.order_interface import OrderClientInterface
from phemexboy.helpers.conversions import usdt_to_crypto


class TestAuthClient(unittest.TestCase):
    def test_init(self):
        client = AuthClient()
        self.assertIsInstance(client, AuthClientInterface)

    def test_worker(self):
        client = AuthClient()
        task = lambda x, y: x + y

        result = client._worker(task, 1, 2)
        self.assertEqual(result, 3)

    def test_leverage(self):
        auth_client = AuthClient()
        pub_client = PublicClient()
        symbol = pub_client.symbol(base="BTC", quote="USD", code="future")
        success = auth_client.leverage(amount=10, symbol=symbol)

        self.assertEqual(success, True)

    def test_balance(self):
        client = AuthClient()
        spot_currency = "USDT"
        future_currency = "USD"
        spot_balance = client.balance(currency=spot_currency, code="spot")
        future_balance = client.balance(currency=future_currency, code="future")

        self.assertGreaterEqual(spot_balance, 0)
        self.assertGreaterEqual(future_balance, 0)

    def test_orders(self):
        auth_client = AuthClient()
        pub_client = PublicClient()
        spot_symbol = pub_client.symbol(base="BTC", quote="USD", code="spot")
        future_symbol = pub_client.symbol(base="BTC", quote="USD", code="future")
        spot_orders = auth_client.orders(symbol=spot_symbol, code="spot")
        future_orders = auth_client.orders(symbol=future_symbol, code="spot")

        self.assertEqual(len(spot_orders), 0)
        self.assertEqual(len(future_orders), 0)

    def test_limit_buy(self):
        auth_client = AuthClient()
        pub_client = PublicClient()
        symbol = pub_client.symbol(base="BTC", quote="USD", code="future")
        type = "limit"
        price = 1000
        usdt_bal = auth_client.balance(currency="USDT", code="spot")
        amount = usdt_to_crypto(usdt_balance=usdt_bal, price=price, percent=99)
        order = auth_client.buy(symbol=symbol, type=type, amount=amount, price=price)
        orders = auth_client.orders(symbol=symbol, code="spot")
        print(order.query("id"))
        print(orders)
        order.cancel()
