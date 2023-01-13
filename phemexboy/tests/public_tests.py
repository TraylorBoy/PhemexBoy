"""PublicClient Tests"""

import unittest

from phemexboy.api.public import PublicClient
from phemexboy.interfaces.public_interface import PublicClientInterface


class TestPublicClient(unittest.TestCase):
    def test_init(self):
        client = PublicClient()
        self.assertIsInstance(client, PublicClientInterface)

    def test_worker(self):
        client = PublicClient()
        task = lambda x, y: x + y

        result = client._worker(task, 1, 2)
        self.assertEqual(result, 3)

    def test_timeframes(self):
        client = PublicClient()
        timeframes = client.timeframes()

        expected = {
            "1m": "60",
            "3m": "180",
            "5m": "300",
            "15m": "900",
            "30m": "1800",
            "1h": "3600",
            "2h": "7200",
            "3h": "10800",
            "4h": "14400",
            "6h": "21600",
            "12h": "43200",
            "1d": "86400",
            "1w": "604800",
            "1M": "2592000",
        }
        for tf in expected.keys():
            self.assertIn(tf, timeframes)

    def test_codes(self):
        client = PublicClient()
        codes = client.codes()

        expected = ["future", "spot"]
        for val in expected:
            self.assertIn(val, codes)

    def test_symbol(self):
        client = PublicClient()
        spot_symbol = client.symbol(base="BTC", quote="USD", code="spot")
        future_symbol = client.symbol(base="BTC", quote="USD", code="future")

        self.assertEqual(spot_symbol, "sBTCUSDT")
        self.assertEqual(future_symbol, "BTC/USD:USD")

    def test_price(self):
        client = PublicClient()
        spot_symbol = client.symbol(base="BTC", quote="USD", code="spot")
        future_symbol = client.symbol(base="BTC", quote="USD", code="future")
        spot_price = client.price(symbol=spot_symbol)
        future_price = client.price(symbol=future_symbol)

        self.assertGreater(spot_price, 0)
        self.assertGreater(future_price, 0)

    def test_ohlcv(self):
        client = PublicClient()
        spot_symbol = client.symbol(base="BTC", quote="USD", code="spot")
        future_symbol = client.symbol(base="BTC", quote="USD", code="future")
        tf = "1d"
        since = "2018-01-30"
        spot_ohlcv = client.ohlcv(symbol=spot_symbol, tf=tf, since=since)
        future_ohlcv = client.ohlcv(symbol=future_symbol, tf=tf)

        self.assertGreater(len(spot_ohlcv), 0)
        self.assertGreater(len(future_ohlcv), 0)

    def test_currencies(self):
        client = PublicClient()
        currencies = client.currencies()

        self.assertGreater(len(currencies), 0)

    def test_status(self):
        client = PublicClient()
        status = client.status()

        self.assertGreater(len(status), 0)

    def test_orderbook(self):
        client = PublicClient()
        symbol = client.symbol(base="BTC", quote="USD", code="spot")
        orderbook = client.orderbook(symbol)

        self.assertGreater(len(orderbook), 0)
