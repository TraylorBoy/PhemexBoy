"""Future Client Interface"""

import abc


class FutureClientInterface(abc.ABC):
    @abc.abstractclassmethod
    def balance(self):
        """Retrieves FUTURE account USD balance

        Raises:
            NotImplementedError: Must implement the method when subclassing
        """
        raise NotImplementedError

    @abc.abstractclassmethod
    def long(
        self,
        symbol: str,
        type: str,
        amount: int,
        price: float = None,
        sl: float = None,
        tp: float = None,
    ):
        """Open a long position

        Args:
            symbol (str): Created symbol for base and quote currencies
            type (str): Type of order (only supports 'market' and 'limit')
            amount (int): Number of contracts to open
            price (float, optional): Set limit order price. Defaults to None.
            sl (float, optional): Set stop loss price. Defaults to None.
            tp (float, optional): Set take profit price. Defaults to None.

        Raises:
            NotImplementedError: Must implement the method when subclassing
        """
        raise NotImplementedError

    @abc.abstractclassmethod
    def short(
        self,
        symbol: str,
        type: str,
        amount: int,
        price: float = None,
        sl: float = None,
        tp: float = None,
    ):
        """Open a short position

        Args:
            symbol (str): Created symbol for base and quote currencies
            type (str): Type of order (only supports 'market' and 'limit')
            amount (int): Number of contracts to open
            price (float, optional): Set limit order price. Defaults to None.
            sl (float, optional): Set stop loss price. Defaults to None.
            tp (float, optional): Set take profit price. Defaults to None.

        Raises:
            NotImplementedError: Must implement the method when subclassing
        """
        raise NotImplementedError
