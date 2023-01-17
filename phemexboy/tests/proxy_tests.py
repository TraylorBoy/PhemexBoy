"""PositionClient Tests"""

import unittest

from phemexboy.proxy import Proxy
from phemexboy.interfaces.auth.client_interface import AuthClientInterface
from phemexboy.interfaces.auth.order_interface import OrderClientInterface
from phemexboy.interfaces.auth.position_interface import PositionClientInterface
from phemexboy.interfaces.public_interface import PublicClientInterface
from phemexboy.exceptions import (
    InvalidCodeError,
    InvalidRequestError,
    OrderTypeError,
)


class TestProxy(unittest.TestCase):
    def test_init(self):
        proxy = Proxy()
        self.assertIsInstance(proxy, AuthClientInterface)
        self.assertIsInstance(proxy, PublicClientInterface)
        self.assertIsInstance(proxy._pub_client, PublicClientInterface)
        self.assertIsInstance(proxy._auth_client, AuthClientInterface)

    def test_public(self):
        proxy = Proxy()

        # Test timeframes
        tfs = proxy.timeframes()
        x = [
            "1m",
            "3m",
            "5m",
            "15m",
            "30m",
            "1h",
            "2h",
            "3h",
            "4h",
            "6h",
            "12h",
            "1d",
            "1w",
            "1M",
        ]
        for val in x:
            self.assertIn(val, tfs)

        # Test codes
        codes = proxy.codes()
        x = ["future", "spot"]
        for val in x:
            self.assertIn(val, codes)

        # Test currencies
        currencies = proxy.currencies()
        self.assertGreater(len(currencies), 0)
        self.assertIn("BTC", currencies)
        self.assertIn("USD", currencies)
        self.assertIn("USDT", currencies)

        # Test symbol
        spot_symbol = proxy.symbol(base="BTC", quote="USD", code="spot")
        future_symbol = proxy.symbol(base="BTC", quote="USD", code="future")
        self.assertEqual(spot_symbol, "sBTCUSDT")
        self.assertEqual(future_symbol, "BTC/USD:USD")
        with self.assertRaises(InvalidCodeError):
            proxy._pub_client.symbol(base="BTC", quote="USD", code="swap")

        # Test price
        spot_price = proxy.price(symbol=spot_symbol)
        future_price = proxy.price(symbol=future_symbol)
        self.assertGreater(spot_price, 0)
        self.assertGreater(future_price, 0)

        # Test ohlcv
        since = "2022-01-30"
        spot_ohlcv = proxy.ohlcv(symbol=spot_symbol, tf="1m")
        future_ohlcv = proxy.ohlcv(symbol=future_symbol, tf="1m", since=since)
        self.assertGreater(len(spot_ohlcv), 0)
        self.assertGreater(len(future_ohlcv), 0)

        # Test status
        status = proxy.status()
        self.assertGreater(len(status), 0)

        # Test orderbook
        spot_book = proxy.orderbook(symbol=spot_symbol)
        future_book = proxy.orderbook(symbol=future_symbol)
        self.assertGreater(len(spot_book), 0)
        self.assertGreater(len(future_book), 0)

    def test_auth(self):
        proxy = Proxy()

        # Test balance
        spot_bal = proxy.balance(currency="USDT", code="spot")
        fut_bal = proxy.balance(currency="USD", code="future")
        self.assertGreaterEqual(spot_bal, 0)
        self.assertGreaterEqual(fut_bal, 0)

        # Test leverage
        self.assertEqual(proxy.leverage(10, proxy.symbol("BTC", "USD", "future")), True)

    def test_order_and_position(self):
        proxy = Proxy(verbose=False)
        symbol = proxy.symbol(base="BTC", quote="USD", code="future")

        # Test init
        type = "limit"
        amount = 1
        price = 9000
        order = proxy.long(symbol, type, amount, price)
        order.verbose()
        self.assertIsInstance(order, OrderClientInterface)
        self.assertIsInstance(order._client, AuthClientInterface)
        self.assertIsInstance(order._pub_client, PublicClientInterface)
        self.assertEqual(order._state, "None")
        self.assertIsInstance(order._order, dict)

        # Test __str__
        print(f"Testing order __str__: \n{order}")

        # Test query
        self.assertEqual(order.query("price"), price)

        # Test InvalidRequestError
        with self.assertRaises(InvalidRequestError):
            order.query("not a param")

        # Test pending
        self.assertEqual(order.pending(), True)

        # Test edit
        price = 9001
        amount = 2
        order.edit(amount, price)
        self.assertEqual(order.query("price"), price)
        self.assertEqual(order.query("amount"), amount)

        # Test cancel
        order.cancel()
        self.assertEqual(order.canceled(), True)

        # Test OrderTypeError
        order._order["type"] = "market"
        with self.assertRaises(OrderTypeError):
            order.edit(amount=3, price=9002)
        with self.assertRaises(OrderTypeError):
            order.cancel()
        with self.assertRaises(OrderTypeError):
            order.retry()
        with self.assertRaises(OrderTypeError):
            order.close()

        # Test closed
        self.assertEqual(order.closed(), True)

        # Test retry and close
        order = proxy.long(symbol, type, amount, price)
        if order.close(retry=True, wait=10, tries=6):
            # Test init
            position = proxy.position(symbol)
            position.verbose()
            self.assertIsInstance(position, PositionClientInterface)
            self.assertIsInstance(position._client, AuthClientInterface)
            self.assertIsInstance(position._position, dict)
            self.assertEqual(position._state, "open")

            # Test __str__
            print(f"Testing position __str__: \n{position}")

            # Test query
            self.assertEqual(position.query("contracts"), 2)

            # Test InvalidRequestError
            with self.assertRaises(InvalidRequestError):
                position.query("not a param")

            # Test close
            position.close(1)
            self.assertEqual(position.query("contracts"), 1)
            position.close(all=True)
            self.assertEqual(position.closed(), True)
