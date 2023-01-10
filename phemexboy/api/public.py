"""Implements PublicClientInterface"""

import ccxt

from phemexboy.interfaces.public_interface import PublicClientInterface
from botboy import BotBoy


class PublicClient(PublicClientInterface):
    def __init__(self):
        try:
            self._endpoint = ccxt.phemex()
            self._bot = BotBoy(name="PubBot")
        except Exception as e:
            raise Exception(e)

    def _worker(self, task, *args, wait=True):
        """Runs tasks on separate thread

        Args:
            task (object): Method to execute on separate thread
            *args (list): Parameters for task
            wait (bool, optional): Wait for execution to finish. Defaults to True.

        Raises:
            Exception: Worker failed to execute task

        Returns:
            Any: Result from task execution
        """
        try:
            self._endpoint.load_markets(reload=True)
            self._bot.task = task
            if len(args) > 0:
                self._bot.execute(*args, wait=wait)
            else:
                self._bot.execute(wait=wait)
            return self._bot.result
        except Exception as e:
            raise Exception(e)

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

    def symbol(self, base, quote, code):
        """Creates a symbol representing the asset pairing

        Args:
            base (str): Currency you are buying (ex. 'btc')
            quote (str): Currency you are selling (ex. 'usd')
            code (str): The market you want to make a symbol for (ex. 'spot')

        Raises:
            Exception: Market is not available for exchange

        Returns:
            String: Formatted base and quote currency symbol
        """
        if code not in self.codes():
            raise Exception("Invalid code")

        base_curr = base.upper()
        quote_curr = quote.upper()

        if code == "spot":
            if quote_curr == "USD":
                quote_curr = "USDT"
            return "s" + base_curr + quote_curr

        if code == "future":
            return base_curr + "/" + quote_curr + ":" + quote_curr

    def price(self, symbol):
        """Retrieve price of asset pair

        Args:
            symbol (str): Created symbol for base and quote currencies

        Raises:
            Exception: Failed to retrieve price

        Returns:
            Float: Current ask price for base currency
        """
        try:
            return self._worker(self._endpoint.fetch_order_book, symbol)["asks"][0][0]
        except Exception as e:
            raise Exception(e)

    def ohlcv(self, symbol, tf, since, limit=1000):
        """Retrieve the open - high - low - close - volume data from exchange

        Args:
            symbol (str): Created symbol for base and quote currencies
            tf (str): Timeframe to retrieve OHLCV data for
            since (str): Optional start date for retrieving OHLCV data, YEAR-MONTH-DAY (ex. 2018-12-01)
            limit (int): How many sets of OHLCV data (candles) to retrieve

        Raises:
            Exception: Failed to retrieve OHLCV data

        Returns:
            List: Candle data for timeframe
        """
        try:
            formatted_date = None
            if since:
                formatted_date = since + "T00:00:00Z"
                formatted_date = self._endpoint.parse8601(formatted_date)

            return self._worker(
                self._endpoint.fetch_ohlcv, symbol, tf, formatted_date, limit
            )
        except Exception as e:
            raise Exception(e)
