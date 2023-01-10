"""Spot Client Interface"""

import abc


class SpotClientInterface(abc.ABC):
    @abc.abstractclassmethod
    def balance(self, of: str):
        """Retrieves SPOT account balance for specified asset

        Args:
            of (str): Asset to retrieve balance for (ex. 'BTC')

        Raises:
            NotImplementedError: Must implement the method when subclassing
        """
        raise NotImplementedError

    @abc.abstractclassmethod
    def buy(self, symbol: str, type: str, amount: float, price: float = None):
        """Places a buy order

        Args:
            symbol (str): Created symbol for base and quote currencies
            type (str): Type of order (only supports 'market' and 'limit')
            amount (float): Amount of base currency you would like to buy
            price (float, optional): Set limit order price. Defaults to None.

        Raises:
            NotImplementedError: Must implement the method when subclassing
        """
        raise NotImplementedError

    @abc.abstractclassmethod
    def sell(self, symbol: str, type: str, amount: float, price: float = None):
        """Places a sell order

        Args:
            symbol (str): Created symbol for base and quote currencies
            type (str): Type of order (only supports 'market' and 'limit')
            amount (float): Amount of base currency you would like to buy
            price (float, optional): Set limit order price. Defaults to None.

        Raises:
            NotImplementedError: Must implement the method when subclassing
        """
        raise NotImplementedError
