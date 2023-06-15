"""Implements PublicClientInterface"""

import ccxt

from phemexboy.interfaces.public_interface import PublicClientInterface
from phemexboy.exceptions import InvalidCodeError
from botboy.core import BotBoy


class PublicClient(PublicClientInterface):
    def __init__(self):
        self._endpoint = ccxt.phemex({"enableRateLimit": True})

    def _worker(self, task: object, *args):
        """Runs tasks on separate thread

        Args:
            task (object): Method to execute on separate thread

        Raises:
            Exception: Any

        Returns:
            Any: Result from task execution
        """
        try:
            self._endpoint.load_markets(reload=True)
            worker = BotBoy(name="PublicWorker", task=task, params=args)
            result = worker.execute()
            return result
        except Exception:
            raise

    def timeframes(self):
        """Retrieve all timeframes available for exchange

        Returns:
            List: All available timeframes
        """
        return self._endpoint.timeframes

    def codes(self):
        """A list of markets that the exchange offers

        Returns:
            List: Available markets
        """
        return ["future", "spot"]

    def symbol(self, base: str, quote: str, code: str):
        """Creates a symbol representing the asset pairing

        Args:
            base (str): Currency you are buying (ex. 'btc')
            quote (str): Currency you are selling (ex. 'usd')
            code (str): Market code (ex. 'spot')

        Raises:
            InvalidCode: Codes may be found by calling proxy.codes()

        Returns:
            String: Formatted base and quote currency symbol
        """
        if code not in self.codes():
            raise InvalidCodeError()

        base_curr = base.upper()
        quote_curr = quote.upper()

        if code == "spot":
            if quote_curr == "USD":
                quote_curr = "USDT"
            return "s" + base_curr + quote_curr

        if code == "future":
            return base_curr + "/" + quote_curr + ":" + quote_curr

    def price(self, symbol: str):
        """Retrieve price of asset pair

        Args:
            symbol (str): Created symbol for base and quote currencies

        Returns:
            Float: Current ask price for base currency
        """
        return self._worker(self._endpoint.fetch_order_book, symbol)["asks"][0][0]

    def ohlcv(self, symbol: str, tf: str, since: str = None):
        """Retrieve the open - high - low - close - volume data from exchange

        Args:
            symbol (str): Created symbol for base and quote currencies
            tf (str): Timeframe to retrieve OHLCV data for
            since (str): Optional start date for retrieving OHLCV data, YEAR-MONTH-DAY (ex. 2018-12-01), Default is None.

        Returns:
            List: Candle data for timeframe
        """
        # Get as much data as possible
        limit = 1000000
        formatted_date = None
        if since:
            formatted_date = since + "T00:00:00Z"
            formatted_date = self._endpoint.parse8601(formatted_date)

        return self._worker(
            self._endpoint.fetch_ohlcv, symbol, tf, formatted_date, limit
        )

    def currencies(self):
        """Retrieve all currencies the exchange offers

        Returns:
            Dictionary: All exchange currencies
        """
        return self._worker(self._endpoint.fetch_currencies)

    def status(self):
        """Retrieve the current network status of exchange

        Returns:
            Dictionary: Current exchange status
        """
        return self._worker(self._endpoint.fetch_status)

    def orderbook(self, symbol: str):
        """Retrieve orderbook for symbol

        Args:
            symbol (str): Created symbol for base and quote currencies

        Returns:
            Dictionary: Current orderbook for symbol
        """
        return self._worker(self._endpoint.fetch_order_book, symbol)
