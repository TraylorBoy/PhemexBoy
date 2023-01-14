"""AuthClient Tests"""

import unittest

from phemexboy.api.public import PublicClient
from phemexboy.api.auth.client import AuthClient
from phemexboy.interfaces.auth.client_interface import AuthClientInterface


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
