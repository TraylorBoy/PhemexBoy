"""API Wrapper Module"""
__version__ = "2.0.0"

# TODO: Update README - Add examples
# TODO: Add logging
# TODO: Test auth methods

from ccxt import NetworkError, ExchangeError

from .api.public import PublicClient
from .api.auth.client import AuthClient
from .exceptions import InvalidCodeError
from .interfaces.auth.client_interface import AuthClientInterface
from .interfaces.public_interface import PublicClientInterface


class Proxy(PublicClientInterface, AuthClientInterface):
    def __init__(self):
        try:
            self._pub_client = PublicClient()
            self._auth_client = AuthClient()
        except NetworkError as e:
            print(
                f"NetworkError - Failed to initialize PublicClient and AuthClient: {e}"
            )
        except ExchangeError as e:
            print(
                f"ExchangeError - Failed to initialize PublicClient and AuthClient: {e}"
            )
        except Exception as e:
            print(f"Failed to initialize PublicClient and AuthClient: {e}")

    # --------------------------- PublicClient Methods --------------------------- #

    def timeframes(self):
        """Retrieve all timeframes available for exchange

        Raises:
            Exception: PublicClient failed to retrieve timeframes

        Returns:
            List: All available timeframes
        """
        try:
            return self._pub_client.timeframes()
        except Exception as e:
            print(f"PublicClient failed to retrieve timeframes: {e}")

    def codes(self):
        """A list of markets that the exchange offers

        Raises:
            Exception: PublicClient failed to retrieve codes

        Returns:
            List: Available markets
        """
        try:
            return self._pub_client.codes()
        except Exception as e:
            print(f"PublicClient failed to retrieve codes: {e}")

    def currencies(self):
        """Retrieve all currencies the exchange offers

        Raises:
            NetworkError: PublicClient failed to retrieve currencies
            ExchangeError: PublicClient failed to retrieve currencies
            Exception: PublicClient failed to retrieve currencies

        Returns:
            Dictionary: All exchange currencies
        """
        try:
            return self._pub_client.currencies()
        except NetworkError as e:
            print(f"NetworkError - PublicClient failed to retrieve currencies: {e}")
        except ExchangeError as e:
            print(f"ExchangeError - PublicClient failed to retrieve currencies: {e}")
        except Exception as e:
            print(f"PublicClient failed to retrieve currencies: {e}")

    def symbol(self, base: str, quote: str, code: str):
        """Creates a symbol representing the asset pairing

        Args:
            base (str): Currency you are buying (ex. 'btc')
            quote (str): Currency you are selling (ex. 'usd')
            code (str): Market code (ex. 'spot')

        Raises:
            InvalidCode: Codes may be found by calling proxy.codes()
            Exception: PublicClient failed to create symbol

        Returns:
            String: Formatted base and quote currency symbol
        """
        try:
            return self._pub_client.symbol(base, quote, code)
        except InvalidCodeError as e:
            print(f"PublicClient failed to create symbol: {e}")
            print(
                "\nPlease call proxy.codes() in order to retrieve the current market codes that are offered\n"
            )
            self.codes()
        except Exception as e:
            print(f"PublicClient failed to create symbol: {e}")

    def price(self, symbol: str):
        """Retrieve price of asset pair

        Args:
            symbol (str): Created symbol for base and quote currencies

        Raises:
            NetworkError: PublicClient failed to retrieve price
            ExchangeError: PublicClient failed to retrieve price
            Exception: PublicClient failed to retrieve price

        Returns:
            Float: Current ask price for base currency
        """
        try:
            return self._pub_client.price(symbol)
        except NetworkError as e:
            print(f"NetworkError - PublicClient failed to retrieve price: {e}")
        except ExchangeError as e:
            print(f"ExchangeError - PublicClient failed to retrieve price: {e}")
        except Exception as e:
            print(f"PublicClient failed to retrieve price: {e}")

    def ohlcv(self, symbol: str, tf: str, since: str = None):
        """Retrieve the open - high - low - close - volume data from exchange

        Args:
            symbol (str): Created symbol for base and quote currencies
            tf (str): Timeframe to retrieve OHLCV data for
            since (str): Optional start date for retrieving OHLCV data, YEAR-MONTH-DAY (ex. 2018-12-01), Default is None.

        Raises:
            NetworkError: PublicClient failed to retrieve candlestick data
            ExchangeError: PublicClient failed to retrieve candlestick data
            Exception: PublicClient failed to retrieve candlestick data

        Returns:
            List: Candle data for timeframe
        """
        try:
            return self._pub_client.ohlcv(symbol, tf, since)
        except NetworkError as e:
            print(
                f"NetworkError - PublicClient failed to retrieve candlestick data: {e}"
            )
        except ExchangeError as e:
            print(
                f"ExchangeError - PublicClient failed to retrieve candlestick data: {e}"
            )
        except Exception as e:
            print(f"PublicClient failed to retrieve candlestick data: {e}")

    def status(self):
        """Retrieve the current network status of exchange

        Raises:
            NetworkError: PublicClient failed to retrieve exchange status
            ExchangeError: PublicClient failed to retrieve exchange status
            Exception: PublicClient failed to retrieve exchange status

        Returns:
            Dictionary: Current exchange status
        """
        try:
            return self._pub_client.status()
        except NetworkError as e:
            print(
                f"NetworkError - PublicClient failed to retrieve exchange status: {e}"
            )
        except ExchangeError as e:
            print(
                f"ExchangeError - PublicClient failed to retrieve exchange status: {e}"
            )
        except Exception as e:
            print(f"PublicClient failed to retrieve exchange status: {e}")

    def orderbook(self, symbol: str):
        """Retrieve orderbook for symbol

        Args:
            symbol (str): Created symbol for base and quote currencies

        Raises:
            NetworkError: PublicClient failed to retrieve orderbook
            ExchangeError: PublicClient failed to retrieve orderbook
            Exception: PublicClient failed to retrieve orderbook

        Returns:
            Dictionary: Current orderbook for symbol
        """
        try:
            return self._pub_client.orderbook(symbol)
        except NetworkError as e:
            print(
                f"NetworkError - PublicClient failed to retrieve orderbook for {symbol}: {e}"
            )
        except ExchangeError as e:
            print(
                f"ExchangeError - PublicClient failed to retrieve orderbook for {symbol}: {e}"
            )
        except Exception as e:
            print(f"PublicClient failed to retrieve orderbook for {symbol}: {e}")

    # ---------------------------- AuthClient Methods ---------------------------- #

    def balance(self, currency: str, code: str):
        """Retrieve the balance of an asset on exchange

        Args:
            currency (str): The currency balance to retrieve (ex. 'BTC')
            code (str): Market code (ex. 'spot')

        Raises:
            InvalidCodeError: Codes may be found by calling proxy.codes()
            NetworkError: AuthClient failed to retrieve balance for {currency} on {code} market
            ExchangeError: AuthClient failed to retrieve balance for {currency} on {code} market
            Exception: AuthClient failed to retrieve balance for {currency} on {code} market

        Returns:
            Float: Balance for account
        """
        try:
            return self._auth_client.balance(currency, code)
        except InvalidCodeError as e:
            print(f"PublicClient failed to create symbol: {e}")
            print(
                "\nPlease call proxy.codes() in order to retrieve the current market codes that are offered\n"
            )
            self.codes()
        except NetworkError as e:
            print(
                f"NetworkError - AuthClient failed to retrieve balance for {currency} on {code} market: {e}"
            )
        except ExchangeError as e:
            print(
                f"ExchangeError - AuthClient failed to retrieve balance for {currency} on {code} market: {e}"
            )
        except Exception as e:
            print(
                f"AuthClient failed to retrieve balance for {currency} on {code} market: {e}"
            )

    def buy(
        self,
        symbol: str,
        type: str,
        amount: float,
        price: float = None,
        config: dict = {},
    ):
        """Places a buy order

        Args:
            symbol (str): Created symbol for base and quote currencies
            type (str): Type of order (only supports 'market' and 'limit')
            amount (float): Amount of base currency you would like to buy
            price (float, optional): Set limit order price. Defaults to None.
            config (dict, optional): Optional parameters to send to exchange. Defaults to None.

        Raises:
            NetworkError: AuthClient failed to place order
            ExchangeError: AuthClient failed to place order
            Exception: AuthClient failed to place order

        Returns:
            OrderClient: Object that represents open order and allows for interaction
        """
        try:
            return self._auth_client.buy(symbol, type, amount, price, config)
        except NetworkError as e:
            print(f"NetworkError - AuthClient failed to place order: {e}")
        except ExchangeError as e:
            print(f"ExchangeError - AuthClient failed to place order: {e}")
        except Exception as e:
            print(f"AuthClient failed to place order: {e}")

    def sell(
        self,
        symbol: str,
        type: str,
        amount: float,
        price: float = None,
        config: dict = {},
    ):
        """Places a sell order

        Args:
            symbol (str): Created symbol for base and quote currencies
            type (str): Type of order (only supports 'market' and 'limit')
            amount (float): Amount of base currency you would like to buy
            price (float, optional): Set limit order price. Defaults to None.
            config (dict, optional): Optional parameters to send to exchange. Defaults to None.

        Raises:
            NetworkError: AuthClient failed to place order
            ExchangeError: AuthClient failed to place order
            Exception: AuthClient failed to place order

        Returns:
            OrderClient: Object that represents open order and allows for interaction
        """
        try:
            return self._auth_client.sell(symbol, type, amount, price, config)
        except NetworkError as e:
            print(f"NetworkError - AuthClient failed to place order: {e}")
        except ExchangeError as e:
            print(f"ExchangeError - AuthClient failed to place order: {e}")
        except Exception as e:
            print(f"AuthClient failed to place order: {e}")

    def long(
        self,
        symbol: str,
        type: str,
        amount: int,
        price: float = None,
        sl: float = None,
        tp: float = None,
        config: dict = {},
    ):
        """Open a long position

        Args:
            symbol (str): Created symbol for base and quote currencies
            type (str): Type of order (only supports 'market' and 'limit')
            amount (int): Number of contracts to open
            price (float, optional): Set limit order price. Defaults to None.
            sl (float, optional): Set stop loss price. Defaults to None.
            tp (float, optional): Set take profit price. Defaults to None.
            config (dict, optional): Optional parameters to send to exchange. Defaults to None.

        Raises:
            Exception: AuthClient failed to open long position

        Returns:
            OrderClient: Object that represents open order and allows for interaction
        """
        try:
            return self._auth_client.long(symbol, type, amount, price, sl, tp, config)
        except Exception as e:
            print(f"AuthClient failed to open long position: {e}")

    def short(
        self,
        symbol: str,
        type: str,
        amount: int,
        price: float = None,
        sl: float = None,
        tp: float = None,
        config: dict = {},
    ):
        """Open a short position

        Args:
            symbol (str): Created symbol for base and quote currencies
            type (str): Type of order (only supports 'market' and 'limit')
            amount (int): Number of contracts to open
            price (float, optional): Set limit order price. Defaults to None.
            sl (float, optional): Set stop loss price. Defaults to None.
            tp (float, optional): Set take profit price. Defaults to None.
            config (dict, optional): Optional parameters to send to exchange. Defaults to None.

        Raises:
            Exception: AuthClient failed to open short position

        Returns:
            OrderClient: Object that represents open order and allows for interaction
        """
        try:
            return self._auth_client.short(symbol, type, amount, price, sl, tp, config)
        except Exception as e:
            print(f"AuthClient failed to open short position: {e}")

    def leverage(self, amount: int, symbol: str):
        """Set future account leverage

        Args:
            amount (int): Set leverage to this amount
            symbol (str): Created symbol for base and quote currencies

        Raises:
            NetworkError: AuthClient failed to modify leverage
            ExchangeError: AuthClient failed to modify leverage
            Exception: AuthClient failed to modify leverage

        Returns:
            Bool: Leverage successfully set or not
        """
        try:
            return self._auth_client.leverage(amount, symbol)
        except NetworkError as e:
            print(f"NetworkError - AuthClient failed to modify leverage: {e}")
        except ExchangeError as e:
            print(f"ExchangeError - AuthClient failed to modify leverage: {e}")
        except Exception as e:
            print(f"AuthClient failed to modify leverage: {e}")

    def position(self, symbol: str):
        """Create a PositionClient representing the open position for symbol

        Args:
            symbol(str): Created symbol for base and quote currencies

        Raises:
            NetworkError: AuthClient failed to retrieve position for {symbol}
            ExchangeError: AuthClient failed to retrieve position for {symbol}
            Exception: AuthClient failed to retrieve position for {symbol}

        Returns:
            PositionClient: Represents open position and allows for interaction
        """
        try:
            return self._auth_client.position(symbol)
        except NetworkError as e:
            print(
                f"NetworkError - AuthClient failed to retrieve position for {symbol}: {e}"
            )
        except ExchangeError as e:
            print(
                f"ExchangeError - AuthClient failed to retrieve position for {symbol}: {e}"
            )
        except Exception as e:
            print(f"AuthClient failed to retrieve position for {symbol}: {e}")

    def cancel(self, id: str, symbol: str):
        """Cancel open order

        Args:
            id (str): Order id
            symbol (str): Created symbol for base and quote currencies

        Raises:
            NetworkError: AuthClient failed to cancel order for {symbol} with id {id}
            ExchangeError: AuthClient failed to cancel order for {symbol} with id {id}
            Exception: AuthClient failed to cancel order for {symbol} with id {id}

        Returns:
            Dictionary: Order data
        """
        try:
            return self._auth_client.cancel(id, symbol)
        except NetworkError as e:
            print(
                f"NetworkError - AuthClient failed to cancel order for {symbol} with id {id}: {e}"
            )
        except ExchangeError as e:
            print(
                f"ExchangeError - AuthClient failed to cancel order for {symbol} with id {id}: {e}"
            )
        except Exception as e:
            print(f"AuthClient failed to cancel order for {symbol} with id {id}: {e}")

    def orders(self, symbol: str):
        """Retrieve all open orders for symbol

        Args:
            symbol (str): Created symbol for base and quote currencies

        Raises:
            NetworkError: AuthClient failed to retrieve orders for {symbol}
            ExchangeError: AuthClient failed to retrieve orders for {symbol}
            Exception: AuthClient failed to retrieve orders for {symbol}

        Returns:
            List: All open orders
        """
        try:
            return self._auth_client.orders(symbol)
        except NetworkError as e:
            print(
                f"NetworkError - AuthClient failed to retrieve orders for {symbol}: {e}"
            )
        except ExchangeError as e:
            print(
                f"ExchangeError - AuthClient failed to retrieve orders for {symbol}: {e}"
            )
        except Exception as e:
            print(f"AuthClient failed to retrieve orders for {symbol}: {e}")
