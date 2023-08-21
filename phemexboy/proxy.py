"""API Wrapper Module"""

from ccxt import NetworkError, ExchangeError

from .api.public import PublicClient
from .api.auth.client import AuthClient
from .exceptions import InvalidCodeError
from .interfaces.auth.client_interface import AuthClientInterface
from .interfaces.public_interface import PublicClientInterface


class Proxy(PublicClientInterface, AuthClientInterface):
    def __init__(self, verbose: bool = False):
        self._verbose = verbose
        try:
            self._log("Connecting to PublicClient and AuthClient", end=", ")
            self._pub_client = PublicClient()
            self._auth_client = AuthClient()
        except NetworkError as e:
            print(
                f"NetworkError - Failed to initialize PublicClient and AuthClient: {e}"
            )
            raise
        except ExchangeError as e:
            print(
                f"ExchangeError - Failed to initialize PublicClient and AuthClient: {e}"
            )
            raise
        except Exception as e:
            print(f"Failed to initialize PublicClient and AuthClient: {e}")
            raise
        else:
            self._log("done.")

    def _log(self, msg: str, end: str = None):
        """Print message to output if not silent

        Args:
            msg (str): Message to print to output
            end (str): String appended after the last value. Default a newline.
        """
        if self._verbose:
            print(msg, end=end)

    # --------------------------- PublicClient Methods --------------------------- #

    def timeframes(self):
        """Retrieve all timeframes available for exchange

        Raises:
            Exception: PublicClient failed to retrieve timeframes

        Returns:
            List: All available timeframes
        """
        tfs = None
        try:
            self._log("Attempting to retrieve timeframes,", end=" ")
            tfs = self._pub_client.timeframes()
        except Exception as e:
            print(f"PublicClient failed to retrieve timeframes: {e}")
            raise
        else:
            self._log("done.")

        return tfs

    def codes(self):
        """A list of markets that the exchange offers

        Raises:
            Exception: PublicClient failed to retrieve codes

        Returns:
            List: Available markets
        """
        codes = None
        try:
            self._log("Attempting to retrieve market codes,", end=" ")
            codes = self._pub_client.codes()
        except Exception as e:
            print(f"PublicClient failed to retrieve codes: {e}")
            raise
        else:
            self._log("done.")

        return codes

    def currencies(self):
        """Retrieve all currencies the exchange offers

        Raises:
            NetworkError: PublicClient failed to retrieve currencies
            ExchangeError: PublicClient failed to retrieve currencies
            Exception: PublicClient failed to retrieve currencies

        Returns:
            Dictionary: All exchange currencies
        """
        currencies = None
        try:
            self._log("Attempting to retrieve currencies,", end=" ")
            currencies = self._pub_client.currencies()
        except NetworkError as e:
            print(f"NetworkError - PublicClient failed to retrieve currencies: {e}")
            raise
        except ExchangeError as e:
            print(f"ExchangeError - PublicClient failed to retrieve currencies: {e}")
            raise
        except Exception as e:
            print(f"PublicClient failed to retrieve currencies: {e}")
            raise
        else:
            self._log("done.")

        return currencies

    def symbol(self, base: str, quote: str, code: str):
        """Creates a symbol representing the asset pairing

        Args:
            base (str): Currency you are buying (ex. 'btc')
            quote (str): Currency you are selling (ex. 'usd')
            code (str): Market code (ex. 'spot')

        Raises:
            InvalidCodeError: Wrong market code
            Exception: PublicClient failed to create symbol

        Returns:
            String: Formatted base and quote currency symbol
        """
        symbol = None
        try:
            if code not in self.codes():
                raise InvalidCodeError()

            self._log(
                f"Creating symbol - base: {base}, quote: {quote}, code: {code},",
                end=" ",
            )
            symbol = self._pub_client.symbol(base, quote, code)
        except InvalidCodeError as e:
            print(f"PublicClient failed to create symbol for {base} and {quote}: {e}")
            print(
                "\nPlease call proxy.codes() in order to retrieve the current market codes that are offered\n"
            )
            print(f"Codes: {self.codes()}")
        except Exception as e:
            print(f"PublicClient failed to create symbol: {e}")
            raise
        else:
            self._log("done.")

        return symbol

    def price(self, symbol: str):
        """Retrieve price of asset pair

        Args:
            symbol (str): Created symbol for base and quote currencies

        Raises:
            NetworkError: PublicClient failed to retrieve price for {symbol}
            ExchangeError: PublicClient failed to retrieve price for {symbol}
            Exception: PublicClient failed to retrieve price for {symbol}

        Returns:
            Float: Current ask price for base currency
        """
        price = None
        try:
            self._log(f"Attempting to retrieve price for {symbol},", end=" ")
            price = self._pub_client.price(symbol)
        except NetworkError as e:
            print(
                f"NetworkError - PublicClient failed to retrieve price for {symbol}: {e}"
            )
            raise
        except ExchangeError as e:
            print(
                f"ExchangeError - PublicClient failed to retrieve price for {symbol}: {e}"
            )
            raise
        except Exception as e:
            print(f"PublicClient failed to retrieve price for {symbol}: {e}")
            raise
        else:
            self._log("done.")

        return price

    def ohlcv(self, symbol: str, tf: str, since: str = None):
        """Retrieve the open - high - low - close - volume data from exchange

        Args:
            symbol (str): Created symbol for base and quote currencies
            tf (str): Timeframe to retrieve OHLCV data for
            since (str): Optional start date for retrieving OHLCV data, YEAR-MONTH-DAY (ex. 2018-12-01), Default is None.

        Raises:
            NetworkError: PublicClient failed to retrieve candlestick data for {symbol} on timeframe {tf} since {since}
            ExchangeError: PublicClient failed to retrieve candlestick data for {symbol} on timeframe {tf} since {since}
            Exception: PublicClient failed to retrieve candlestick data for {symbol} on timeframe {tf} since {since}

        Returns:
            List: Candle data for timeframe
        """
        ohlcv = None
        try:
            self._log(
                f"Attempting to retrieve candlestick data for {symbol} on timeframe {tf} since {since},",
                end=" ",
            )
            ohlcv = self._pub_client.ohlcv(symbol, tf, since)
        except NetworkError as e:
            print(
                f"NetworkError - PublicClient failed to retrieve candlestick data for {symbol} on timeframe {tf} since {since}: {e}"
            )
            raise
        except ExchangeError as e:
            print(
                f"ExchangeError - PublicClient failed to retrieve candlestick data for {symbol} on timeframe {tf} since {since}: {e}"
            )
            raise
        except Exception as e:
            print(
                f"PublicClient failed to retrieve candlestick data for {symbol} on timeframe {tf} since {since}: {e}"
            )
            raise
        else:
            self._log("done.")

        return ohlcv

    def status(self):
        """Retrieve the current network status of exchange

        Raises:
            NetworkError: PublicClient failed to retrieve exchange status
            ExchangeError: PublicClient failed to retrieve exchange status
            Exception: PublicClient failed to retrieve exchange status

        Returns:
            Dictionary: Current exchange status
        """
        status = None
        try:
            self._log("Attempting to retrieve exchange status,", end=" ")
            status = self._pub_client.status()
        except NetworkError as e:
            print(
                f"NetworkError - PublicClient failed to retrieve exchange status: {e}"
            )
            raise
        except ExchangeError as e:
            print(
                f"ExchangeError - PublicClient failed to retrieve exchange status: {e}"
            )
            raise
        except Exception as e:
            print(f"PublicClient failed to retrieve exchange status: {e}")
            raise
        else:
            self._log("done.")

        return status

    def orderbook(self, symbol: str):
        """Retrieve orderbook for symbol

        Args:
            symbol (str): Created symbol for base and quote currencies

        Raises:
            NetworkError: PublicClient failed to retrieve orderbook for {symbol}
            ExchangeError: PublicClient failed to retrieve orderbook for {symbol}
            Exception: PublicClient failed to retrieve orderbook for {symbol}

        Returns:
            Dictionary: Current orderbook for symbol
        """
        orderbook = None
        try:
            self._log(f"Attempting to retrieve orderbook for {symbol},", end=" ")
            orderbook = self._pub_client.orderbook(symbol)
        except NetworkError as e:
            print(
                f"NetworkError - PublicClient failed to retrieve orderbook for {symbol}: {e}"
            )
            raise
        except ExchangeError as e:
            print(
                f"ExchangeError - PublicClient failed to retrieve orderbook for {symbol}: {e}"
            )
            raise
        except Exception as e:
            print(f"PublicClient failed to retrieve orderbook for {symbol}: {e}")
            raise
        else:
            self._log("done.")

        return orderbook

    # ---------------------------- AuthClient Methods ---------------------------- #

    def balance(self, currency: str, code: str):
        """Retrieve the balance of an asset on exchange

        Args:
            currency (str): The currency balance to retrieve (ex. 'BTC')
            code (str): Market code (ex. 'spot')

        Raises:
            InvalidCodeError: Wrong code
            NetworkError: AuthClient failed to retrieve balance for {currency} on {code} market
            ExchangeError: AuthClient failed to retrieve balance for {currency} on {code} market
            Exception: AuthClient failed to retrieve balance for {currency} on {code} market

        Returns:
            Float: Balance for account
        """
        balance = None
        try:
            if code not in self.codes():
                raise InvalidCodeError()

            self._log(
                f"Attempting to retrieve the balance for {currency} on {code} market",
                end=", ",
            )
            balance = self._auth_client.balance(currency, code)
        except InvalidCodeError as e:
            print(f"AuthClient failed to retrieve balance for {currency}: {e}")
            print(
                "\nPlease call proxy.codes() in order to retrieve the current market codes that are offered\n"
            )
            print(f"Codes: {self.codes()}")
        except NetworkError as e:
            print(
                f"NetworkError - AuthClient failed to retrieve balance for {currency} on {code} market: {e}"
            )
            raise
        except ExchangeError as e:
            print(
                f"ExchangeError - AuthClient failed to retrieve balance for {currency} on {code} market: {e}"
            )
            raise
        except Exception as e:
            print(
                f"AuthClient failed to retrieve balance for {currency} on {code} market: {e}"
            )
            raise
        else:
            self._log("done.")

        return balance

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
        client = None
        try:
            self._log(
                f"Attempting to place {type} buy order for {symbol} at {price} using {amount} with settings {config}",
                end=", ",
            )
            client = self._auth_client.buy(symbol, type, amount, price, config)
            self._log(f"OrderClient retrieved", end=", ")
        except NetworkError as e:
            print(f"NetworkError - AuthClient failed to place order: {e}")
            raise
        except ExchangeError as e:
            print(f"ExchangeError - AuthClient failed to place order: {e}")
            raise
        except Exception as e:
            print(f"AuthClient failed to place order: {e}")
            raise
        else:
            self._log("done.")

        return client

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
        client = None
        try:
            self._log(
                f"Attempting to place {type} sell order for {symbol} at {price} using {amount} with settings {config}",
                end=", ",
            )
            client = self._auth_client.sell(symbol, type, amount, price, config)
            self._log(f"OrderClient retrieved", end=", ")
        except NetworkError as e:
            print(f"NetworkError - AuthClient failed to place order: {e}")
            raise
        except ExchangeError as e:
            print(f"ExchangeError - AuthClient failed to place order: {e}")
            raise
        except Exception as e:
            print(f"AuthClient failed to place order: {e}")
            raise
        else:
            self._log("done.")

        return client

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
        client = None
        try:
            self._log(
                f"Attempting to open long position with {type} buy order for {symbol} at {price} using {amount} with settings {config}",
                end=", ",
            )
            client = self._auth_client.long(symbol, type, amount, price, sl, tp, config)
            self._log(f"OrderClient retrieved", end=", ")
        except Exception as e:
            print(f"AuthClient failed to open long position: {e}")
            raise
        else:
            self._log("done.")

        return client

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
        client = None
        try:
            self._log(
                f"Attempting to open short position with {type} buy order for {symbol} at {price} using {amount} with settings {config}",
                end=", ",
            )
            client = self._auth_client.short(
                symbol, type, amount, price, sl, tp, config
            )
            self._log(f"OrderClient retrieved", end=", ")
        except Exception as e:
            print(f"AuthClient failed to open short position: {e}")
            raise
        else:
            self._log("done.")

        return client

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
        success = False
        try:
            self._log(
                f"Attempting to modify future account leverage to {amount} for {symbol}",
                end=", ",
            )
            success = self._auth_client.leverage(amount, symbol)
        except NetworkError as e:
            print(f"NetworkError - AuthClient failed to modify leverage: {e}")
            raise
        except ExchangeError as e:
            print(f"ExchangeError - AuthClient failed to modify leverage: {e}")
            raise
        except Exception as e:
            print(f"AuthClient failed to modify leverage: {e}")
            raise
        else:
            self._log("done.")

        return success

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
        client = None
        try:
            self._log(f"Attempting to retrieve position for {symbol}", end=", ")
            client = self._auth_client.position(symbol)
            self._log(f"PositionClient retrieved", end=", ")
        except NetworkError as e:
            print(
                f"NetworkError - AuthClient failed to retrieve position for {symbol}: {e}"
            )
            raise
        except ExchangeError as e:
            print(
                f"ExchangeError - AuthClient failed to retrieve position for {symbol}: {e}"
            )
            raise
        except Exception as e:
            print(f"AuthClient failed to retrieve position for {symbol}: {e}")
            raise
        else:
            self._log("done.")

        return client

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
        data = None
        try:
            self._log(f"Attempting to cancel order for {symbol} with id {id}", end=", ")
            data = self._auth_client.cancel(id, symbol)
        except NetworkError as e:
            print(
                f"NetworkError - AuthClient failed to cancel order for {symbol} with id {id}: {e}"
            )
            raise
        except ExchangeError as e:
            print(
                f"ExchangeError - AuthClient failed to cancel order for {symbol} with id {id}: {e}"
            )
            raise
        except Exception as e:
            print(f"AuthClient failed to cancel order for {symbol} with id {id}: {e}")
            raise
        else:
            self._log("done.")

        return data

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
        data = None
        try:
            self._log(f"Attempting to retrieve orders for {symbol}", end=", ")
            data = self._auth_client.orders(symbol)
        except NetworkError as e:
            print(
                f"NetworkError - AuthClient failed to retrieve orders for {symbol}: {e}"
            )
            raise
        except ExchangeError as e:
            print(
                f"ExchangeError - AuthClient failed to retrieve orders for {symbol}: {e}"
            )
            raise
        except Exception as e:
            print(f"AuthClient failed to retrieve orders for {symbol}: {e}")
            raise
        else:
            self._log("done.")

        return data

    # ------------------------------ Client Methods ------------------------------ #

    def verbose(self):
        """Turn on logging"""
        self._verbose = False

    def silent(self):
        """Turn off logging"""
        self._verbose = False
