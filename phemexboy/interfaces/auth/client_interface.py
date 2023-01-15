"""Auth Client Interface"""

import abc


class AuthClientInterface(abc.ABC):
    @abc.abstractmethod
    def leverage(self, amount: int, symbol: str):
        """Set future account leverage

        Args:
            amount (int): Set leverage to this amount
            symbol (str): Created symbol for base and quote currencies

        Raises:
            NotImplementedError: Must implement when subclassing
        """
        raise NotImplementedError

    @abc.abstractmethod
    def balance(self, currency: str, code: str):
        """Retrieve the balance of an asset on exchange

        Args:
            currency (str): The currency balance to retrieve (ex. 'BTC')
            code (str): Market code (ex. 'spot')

        Raises:
            NotImplementedError: Must implement when subclassing
        """
        raise NotImplementedError

    @abc.abstractmethod
    def position(self, symbol: str):
        """Create a PositionClient representing the open position for symbol

        Args:
            symbol(str): Created symbol for base and quote currencies

        Raises:
            NotImplementedError: Must implement when subclassing
        """
        raise NotImplementedError

    @abc.abstractmethod
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
            NotImplementedError: Must implement the method when subclassing
        """
        raise NotImplementedError

    @abc.abstractmethod
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
            NotImplementedError: Must implement the method when subclassing
        """
        raise NotImplementedError

    @abc.abstractmethod
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
            NotImplementedError: Must implement the method when subclassing
        """
        raise NotImplementedError

    @abc.abstractmethod
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
            NotImplementedError: Must implement the method when subclassing
        """
        raise NotImplementedError

    @abc.abstractmethod
    def orders(self, symbol: str):
        """Retrieve all open orders for symbol

        Args:
            symbol (str): Created symbol for base and quote currencies

        Raises:
            NotImplementedError: Must implement before subclassing
        """
        raise NotImplementedError

    @abc.abstractmethod
    def cancel(self, id: str, symbol: str):
        """Cancel open order

        Args:
            id (str): Order id
            symbol (str): Created symbol for base and quote currencies

        Raises:
            NotImplementedError: Must implement before subclassing
        """
        raise NotImplementedError
