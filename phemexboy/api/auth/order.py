"""Implements OrderClientInterface"""

from ccxt.base.errors import InsufficientFunds

from phemexboy.interfaces.auth.order_interface import OrderClientInterface
from phemexboy.interfaces.auth.client_interface import AuthClientInterface
from phemexboy.api.public import PublicClient

from copy import deepcopy
from time import sleep


class OrderClient(OrderClientInterface):
    def __init__(self, order_data: dict, client: AuthClientInterface):
        self._update(order_data=order_data, state="None")
        self._client = client
        self._pub_client = PublicClient()

    def __str__(self):
        out = ""
        for key in self._order.keys():
            out += f"{key}: {self._order[key]}\n"
        return out

    def _update(self, order_data: dict = None, state: str = None):
        """Set order data and state

        Args:
            order_data (Dictionary): Created order data. Defaults to None.
            state (str): Pending, Cancelled, or Closed. Defaults to None.
        """
        if order_data:
            if "info" in order_data.keys():
                # Extract proper symbol and remove status
                # Status is managed by client state
                # Info is original request, not needed
                symbol = order_data["info"]["symbol"]
                del order_data["info"]
                del order_data["status"]

            self._order = order_data
            self._order["symbol"] = symbol

        if state:
            self._state = state

    def query(self, request: str):
        """Retrieve order information data

        Args:
            request (str): Type of data you want to retrieve from OrderClient

        Raises:
            Exception: InvalidRequestError

        Returns:
            String: Requested order data
        """
        if request not in list(self._order.keys()):
            raise Exception("InvalidRequestError")
        return self._order[request]

    def edit(self, amount: float, price: float):
        """Edit pending order

        Args:
            amount (float): Amount of base currency you are using for order
            price (float): Edit limit order price

        Raises:
            Exception: OrderTypeError
            Exception: EditError
        """
        symbol = self.query("symbol")
        type = self.query("type")
        side = self.query("side")

        if type == "market":
            raise Exception("OrderTypeError")

        # Reopen order
        if self.pending():
            self.cancel()

        # Retrieve new order data from OrderClient
        client = None
        if side == "buy":
            client = self._client.buy(symbol, type, amount, price)
        if side == "sell":
            client = self._client.sell(symbol, type, amount, price)

        self._order = deepcopy(client._order)

    def cancel(self):
        """Cancel pending order

        Raises:
            Exception: CancellationError
            Exception: OrderTypeError
        """
        type = self.query("type")
        if type == "market":
            raise Exception("OrderTypeError")

        id = self.query("id")
        symbol = self.query("symbol")
        # Cancel order
        data = self._client.cancel(id, symbol)
        # Update state
        if data:
            self._update(order_data=data, state="canceled")
        else:
            raise Exception("CancellationError")

    def canceled(self):
        """Check if order was canceled

        Returns:
            Bool: Order was successfully canceled
        """
        return self._state == "canceled"

    def pending(self):
        """Check if order is still open

        Returns:
            Bool: Order is still open
        """
        id = self.query("id")
        symbol = self.query("symbol")

        data = self._client.orders(symbol)

        if data:
            for order in data:
                if order["id"] == id:
                    self._update(order_data=order, state="pending")
                    break

        return self._state == "pending"

    def closed(self):
        """Check if order was filled or cancelled

        Returns:
            Bool: Order was successfully filled
        """
        id = self.query("id")
        symbol = self.query("symbol")

        found = False
        data = self._client.orders(symbol)

        if data:
            for res in data:
                if res["id"] == id:
                    found = True

        if not found:
            self._update(state="closed")

        return self._state == "closed"

    def retry(self, wait: int = 2, price: float = None):
        """Ensure limit order was successfully placed at current ask price, if None then will use current ask price

        Args:
            wait (int): The amount of time to wait until retry. Defaults to 2 seconds.
            price (float): Price to retry order at. Defaults to None.

        Raises:
            Exception: OrderTypeError
            InsufficientFundsError: More than likely tried to place order that was already closed

        Returns:
            Bool: Order successfully placed
        """
        if type == "market":
            raise Exception("OrderTypeError")

        if self.pending():
            self.cancel()

        symbol = self.query("symbol")
        amount = self.query("amount")

        try:
            while not self.pending() and self.closed():
                self.edit(amount=amount, price=price) if price else self.edit(
                    amount=amount, price=self._pub_client.price(symbol=symbol) - 0.1
                )
                sleep(wait)
        except InsufficientFunds:
            print(
                "InsufficientFundsError, more than likely tried to place order that was already closed"
            )
            pass
        finally:
            self.closed()

        return True

    def close(
        self, retry: bool = False, wait: int = 2, price: float = None, tries: int = 1
    ):
        """Waits until order is filled

        Args:
            retry (bool): Ensure limit order was successfully placed at current ask price. Defaults to None.
            wait (int): The amount of time to wait until retry. Defaults to 2 seconds.
            price (float): Price to retry order at. Defaults to None (will use current market price).
            tries (int): Number of times to retry. Defaults to 1.

        Returns:
            Bool: Order successfully filled
        """
        i = 0
        closed = False
        while i <= tries:
            sleep(wait)

            if self.closed():
                closed = True
                break

            if retry and not self.closed():
                self.retry(price=price)

            i += 1

        if not closed and self.pending():
            self.cancel()

        return closed
