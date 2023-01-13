"""Public Client Interface"""

import abc


class PublicClientInterface(abc.ABC):
    @abc.abstractmethod
    def timeframes(self):
        """Retrieve all timeframes available for exchange

        Raises:
            NotImplementedError: Must implement the method when subclassing
        """
        raise NotImplementedError

    @abc.abstractmethod
    def codes(self):
        """A list of markets that the exchange offers

        Raises:
            NotImplementedError: Must implement the method when subclassing
        """
        raise NotImplementedError

    @abc.abstractmethod
    def symbol(self, base: str, quote: str, code: str):
        """Creates a symbol representing the asset pairing

        Args:
            base (str): Currency you are buying (ex. 'btc')
            quote (str): Currency you are selling (ex. 'usdt')
            code (str): Market code (ex. 'spot')

        Raises:
            NotImplementedError: Must implement the method when subclassing
        """
        raise NotImplementedError

    @abc.abstractmethod
    def price(self, symbol: str):
        """Retrieve price of asset pair

        Args:
            symbol (str): Created symbol for base and quote currencies

        Raises:
            NotImplementedError: Must implement the method when subclassing
        """
        raise NotImplementedError

    @abc.abstractmethod
    def ohlcv(self, symbol: str, tf: str, since: str):
        """Retrieve the open - high - low - close - volume data from exchange

        Args:
            symbol (str): Created symbol for base and quote currencies
            tf (str): Timeframe to retrieve OHLCV data for
            since (str): Optional start date for retrieving OHLCV data, YEAR-MONTH-DAY (ex. 2018-12-01)

        Raises:
            NotImplementedError: Must implement the method when subclassing
        """
        raise NotImplementedError

    @abc.abstractmethod
    def currencies(self):
        """Retrieve all currencies the exchange offers

        Raises:
            NotImplementedError: Must implement the method when subclassing
        """
        raise NotImplementedError

    @abc.abstractmethod
    def status(self):
        """Retrieve the current network status of exchange

        Raises:
            NotImplementedError: Must implement the method when subclassing
        """
        raise NotImplementedError

    @abc.abstractmethod
    def orderbook(self, symbol: str):
        """Retrieve orderbook for symbol

        Args:
            symbol (str): Created symbol for base and quote currencies

        Raises:
            NotImplementedError: Must implement the method when subclassing
        """
        raise NotImplementedError
