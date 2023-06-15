"""Order Client Interface"""

import abc


class OrderClientInterface(abc.ABC):
    @abc.abstractmethod
    def __str__(self):
        """Outputs order data

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
        """Retrieve order information data

        Args:
          request (str): Type of data you want to retrieve from OrderClient

        Raises:
            NotImplementedError: Must implement the method when subclassing
        """
        raise NotImplementedError

    @abc.abstractmethod
    def edit(
        self,
        amount: float,
        price: float,
        sl_percent: int = None,
        tp_percent: int = None,
    ):
        """Edit pending order

        Args:
            amount (float): Amount of base currency you are using for order
            price (float): Edit limit order price
            sl_percent: Set stop loss percent from price. Defaults to None.
            tp_percent: Set take profit percent from price. Defaults to None.

        Raises:
            NotImplementedError: Must implement the method when subclassing
        """
        raise NotImplementedError

    @abc.abstractmethod
    def cancel(self):
        """Cancel pending order

        Raises:
            NotImplementedError: Must implement the method when subclassing
        """
        raise NotImplementedError

    @abc.abstractmethod
    def canceled(self):
        """Check if order was canceled

        Raises:
            NotImplementedError: Must implement when subclassing
        """
        raise NotImplementedError

    @abc.abstractmethod
    def pending(self):
        """Check if order is still open

        Raises:
            NotImplementedError: Must implement when subclassing
        """
        raise NotImplementedError

    @abc.abstractmethod
    def closed(self):
        """Check if order was filled or cancelled

        Raises:
            NotImplementedError: Must implement when subclassing
        """
        raise NotImplementedError

    @abc.abstractmethod
    def retry(
        self,
        wait: int = 2,
        price: float = None,
        sl_percent: int = None,
        tp_percent: int = None,
    ):
        """Ensure limit order was successfully placed at current ask price

        Args:
            wait (int): The amount of time to wait until retry. Defaults to 2 seconds.
            price (float): Price to retry order at. Defaults to None.
            sl_percent: Set stop loss percent from price. Defaults to None.
            tp_percent: Set take profit percent from price. Defaults to None.

        Raises:
            NotImplementedError: Must implement before subclassing
        """
        raise NotImplementedError

    @abc.abstractmethod
    def close(
        self,
        retry: bool = None,
        wait: int = 2,
        price: float = None,
        tries: int = 1,
        sl_percent: int = None,
        tp_percent: int = None,
    ):
        """Waits until order is filled

        Args:
            retry (bool): Ensure limit order was successfully placed at current ask price
            wait (int): The amount of time to wait until retry. Defaults to 2 seconds.
            price (float): Price to retry order at. Defaults to None (will use current market price).
            tries (int): Number of times to retry. Defaults to 1.
            sl_percent: Set stop loss percent from price. Defaults to None.
            tp_percent: Set take profit percent from price. Defaults to None.

        Raises:
            NotImplementedError: Must implement before subclassing
        """
        raise NotImplementedError
