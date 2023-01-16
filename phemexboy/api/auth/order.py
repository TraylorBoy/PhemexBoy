"""Implements OrderClientInterface"""

from ccxt.base.errors import InsufficientFunds

from phemexboy.interfaces.auth.order_interface import OrderClientInterface
from phemexboy.interfaces.auth.client_interface import AuthClientInterface
from phemexboy.api.public import PublicClient
from phemexboy.exceptions import OrderTypeError, CancellationError, InvalidRequestError

from copy import deepcopy
from time import sleep
from ccxt import NetworkError, ExchangeError


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
            InvalidRequestError: Please print this object in order to see the correct request params

        Returns:
            String: Requested order data
        """
        if request not in list(self._order.keys()):
            raise InvalidRequestError(
                "Please print this object in order to see the correct request params"
            )
        return self._order[request]

    def edit(self, amount: float, price: float):
        """Edit pending order

        Args:
            amount (float): Amount of base currency you are using for order
            price (float): Edit limit order price

        Raises:
            OrderTypeError: Order type must be limit in order to edit
            NetworkError: AuthClient failed to place order
            ExchangeError: AuthClient failed to place order
            Exception: AuthClient failed to place order
        """
        symbol = self.query("symbol")
        type = self.query("type")
        side = self.query("side")

        if type == "market":
            raise OrderTypeError("Order type must be limit in order to edit")

        # Reopen order
        if self.pending():
            self.cancel()

        # Retrieve new order data from OrderClient
        client = None
        try:
            if side == "buy":
                client = self._client.buy(symbol, type, amount, price)
            if side == "sell":
                client = self._client.sell(symbol, type, amount, price)
        except NetworkError as e:
            print(f"NetworkError - AuthClient failed to place order: {e}")
        except ExchangeError as e:
            print(f"ExchangeError - AuthClient failed to place order: {e}")
        except Exception as e:
            print(f"AuthClient failed to place order: {e}")

        self._order = deepcopy(client._order)

    def cancel(self):
        """Cancel pending order

        Raises:
            CancellationError: Typically this means order was not found
            OrderTypeError: Order type must be limit in order to cancel
            NetworkError: AuthClient failed to cancel order for {symbol} with id {id}
            ExchangeError: AuthClient failed to cancel order for {symbol} with id {id}
            Exception: AuthClient failed to cancel order for {symbol} with id {id}
        """
        type = self.query("type")
        if type == "market":
            raise OrderTypeError("Order type must be limit in order to cancel")

        id = self.query("id")
        symbol = self.query("symbol")
        data = None
        try:
            # Cancel order
            data = self._client.cancel(id, symbol)
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

        # Update state
        if data:
            self._update(order_data=data, state="canceled")
        else:
            raise CancellationError("Typically this means order was not found")

    def canceled(self):
        """Check if order was canceled

        Returns:
            Bool: Order was successfully canceled
        """
        return self._state == "canceled"

    def pending(self):
        """Check if order is still open

        Raises:
            NetworkError: AuthClient failed to retrieve orders for {symbol}
            ExchangeError: AuthClient failed to retrieve orders for {symbol}
            Exception: AuthClient failed to retrieve orders for {symbol}

        Returns:
            Bool: Order is still open
        """
        id = self.query("id")
        symbol = self.query("symbol")

        try:
            data = self._client.orders(symbol)
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

        if data:
            for order in data:
                if order["id"] == id:
                    self._update(order_data=order, state="pending")
                    break

        return self._state == "pending"

    def closed(self):
        """Check if order was filled or cancelled

        Raises:
            NetworkError: AuthClient failed to retrieve orders for {symbol}
            ExchangeError: AuthClient failed to retrieve orders for {symbol}
            Exception: AuthClient failed to retrieve orders for {symbol}

        Returns:
            Bool: Order was successfully filled
        """
        id = self.query("id")
        symbol = self.query("symbol")

        found = False
        data = None
        try:
            data = self._client.orders(symbol)
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
            OrderTypeError: Order type must be limit in order to retry
            InsufficientFundsError: More than likely tried to place order that was already closed
            NetworkError: PublicClient failed to retrieve price
            ExchangeError: PublicClient failed to retrieve price
            Exception: PublicClient failed to retrieve price

        Returns:
            Bool: Order successfully placed
        """
        if type == "market":
            raise OrderTypeError("Order type must be limit in order to retry")

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
        except NetworkError as e:
            print(
                f"NetworkError - PublicClient failed to retrieve price for {symbol}: {e}"
            )
        except ExchangeError as e:
            print(
                f"ExchangeError - PublicClient failed to retrieve price for {symbol}: {e}"
            )
        except Exception as e:
            print(f"PublicClient failed to retrieve price for {symbol}: {e}")
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
