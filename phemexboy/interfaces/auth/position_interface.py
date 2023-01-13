"""Position Client Interface"""

import abc


class PositionClientInterface(abc.ABC):
    @abc.abstractmethod
    def __str__(self):
        """Outputs position data

        Raises:
            NotImplementedError: Must implement the method when subclassing
        """
        raise NotImplementedError

    @abc.abstractmethod
    def query(self, request: str):
        """Retrieve position information data

        Args:
          request (str): Type of data you want to retrieve from PositionClient

        Raises:
            NotImplementedError: Must implement the method when subclassing
        """
        raise NotImplementedError

    @abc.abstractmethod
    def edit(self, amount: float, price: float):
        """Edit pending order for position

        Args:
            amount (float): Amount of base currency you are using for order
            price (float): Edit limit order price

        Raises:
            NotImplementedError: Must implement the method when subclassing
        """
        raise NotImplementedError

    @abc.abstractmethod
    def cancel(self):
        """Cancel pending order for position

        Raises:
            NotImplementedError: Must implement the method when subclassing
        """
        raise NotImplementedError

    @abc.abstractmethod
    def close(self, amount: int):
        """Close open position

        Args:
            amount (int): How many contracts to close

        Raises:
            NotImplementedError: Must implement the method when subclassing
        """
        raise NotImplementedError
