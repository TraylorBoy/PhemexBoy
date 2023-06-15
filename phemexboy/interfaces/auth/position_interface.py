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
    def requests(self):
        """Returns a list of all request params

        Raises:
            NotImplementedError: Must implement before subclassing
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
    def close(self, amount: int):
        """Close open position

        Args:
            amount (int): How many contracts to close
            all (bool): Close all contracts. Defaults to False.

        Raises:
            NotImplementedError: Must implement the method when subclassing
        """
        raise NotImplementedError

    @abc.abstractmethod
    def closed(self):
        """Retrieves closed state

        Raises:
            NotImplementedError: Must implement before subclassing
        """
        raise NotImplementedError
