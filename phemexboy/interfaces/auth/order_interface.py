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
    def query(self, request: str):
        """Retrieve order information data

        Args:
          request (str): Type of data you want to retrieve from OrderClient

        Raises:
            NotImplementedError: Must implement the method when subclassing
        """
        raise NotImplementedError

    @abc.abstractmethod
    def edit(self, amount: float, price: float):
        """Edit pending order

        Args:
            amount (float): Amount of base currency you are using for order
            price (float): Edit limit order price

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
