"""PositionClient Tests"""

import unittest

from phemexboy.proxy import Proxy
from phemexboy.interfaces.auth.client_interface import AuthClientInterface
from phemexboy.interfaces.public_interface import PublicClientInterface
from phemexboy.exceptions import InvalidCodeError


class TestProxy(unittest.TestCase):
    def test_init(self):
        proxy = Proxy()
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

    def test_errors(self):
        pass
