"""Implements OrderClientInterface"""

from ccxt.base.errors import InsufficientFunds

from phemexboy.interfaces.auth.order_interface import OrderClientInterface
from phemexboy.interfaces.auth.client_interface import AuthClientInterface
from phemexboy.api.public import PublicClient
from phemexboy.exceptions import OrderTypeError, InvalidRequestError, InvalidCodeError
from phemexboy.helpers.conversions import stop_loss, take_profit

from copy import deepcopy
from time import sleep
from ccxt import NetworkError, ExchangeError


class OrderClient(OrderClientInterface):
    def __init__(
        self,
        order_data: dict,
        client: AuthClientInterface,
        code: str,
        verbose: bool = False,
    ):
        self._verbose = verbose
        self._code = code
        self._update(order_data=order_data, state="None")
        self._client = client
        self._pub_client = PublicClient()

    def __str__(self):
        out = ""
        for key in self._order.keys():
            out += f"{key}: {self._order[key]}\n"

        out += f"code: {self._code}\n"
        return out

    def _log(self, msg: str, end: str = None):
        """Print message to output if not silent

        Args:
            msg (str): Message to print to output
            end (str): String appended after the last value. Default a newline.
        """
        if self._verbose:
            print(msg, end=end)

    def _update(self, order_data: dict = None, state: str = None):
        """Set order data and state

        Args:
            order_data (Dictionary): Created order data. Defaults to None.
            state (str): Pending, Cancelled, or Closed. Defaults to None.
        """
        if order_data:
            self._log("Updating order data", end=", ")

            if "info" in order_data.keys():
                # Extract proper symbol and remove status
                # Status is managed by client state
                # Info is original request, not needed
                symbol = order_data["info"]["symbol"]
                del order_data["info"]
                del order_data["status"]

            self._order = order_data
            self._order["symbol"] = symbol

            self._log("done.")

        if state:
            self._log(f"Updating state to {state}", end=", ")
            self._state = state
            self._log("done.")

    def requests(self):
        """Returns a list of all request params

        Returns:
            List: Request params
        """
        return list(self._order.keys())

    def query(self, request: str):
        """Retrieve order information data

        Args:
            request (str): Type of data you want to retrieve from OrderClient

        Raises:
            InvalidRequestError: OrderClient failed to retrieve data for {request}

        Returns:
            String: Requested order data
        """
        data = None
        try:
            if request not in self.requests():
                raise InvalidRequestError()

            self._log(f"Retrieving order data based on {request}", end=", ")
            data = self._order[request]
        except InvalidRequestError:
            print(
                f"InvalidRequestError - OrderClient failed to retrieve data for {request}"
            )
            print("Call requests() in order to retrieve valid params")
            print(f"Params: {self.requests()}")
        else:
            self._log("done.")
        return data

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
            OrderTypeError: Order type must be limit in order to edit
            NetworkError: OrderClient failed to edit order
            ExchangeError: OrderClient failed to edit order
            Exception: OrderClient failed to edit order
        """
        symbol = self.query("symbol")
        type = self.query("type")
        side = self.query("side")

        if type == "market":
            raise OrderTypeError("Order type must be limit in order to edit")

        if side == 'buy':
            price = price - 0.01
        else:
            price = price + 0.01

        self._log(
            f"Attempting to edit order with {amount} amount at price {price}", end=", "
        )

        # Reopen order
        if self.pending():
            self.cancel()

        # Format sl and tp
        sl = None
        if sl_percent:
            sl = (
                stop_loss(price, sl_percent, "long")
                if side == "buy"
                else stop_loss(price, sl_percent, "short")
            )

        tp = None
        if tp_percent:
            tp = (
                take_profit(price, tp_percent, "long")
                if side == "buy"
                else take_profit(price, tp_percent, "short")
            )

        # Retrieve new order data from OrderClient
        client = None
        try:
            if self._code == "spot":
                if side == "buy":
                    self._log(
                        f"Attempting to place {type} buy order for {symbol} at {price} using {amount}",
                        end=", ",
                    )
                    client = self._client.buy(symbol, type, amount, price)
                if side == "sell":
                    self._log(
                        f"Attempting to place {type} sell order for {symbol} at {price} using {amount}",
                        end=", ",
                    )
                    client = self._client.sell(symbol, type, amount, price)
            elif self._code == "future":
                if side == "buy":
                    self._log(
                        f"Attempting to open long position with {type} long order for {symbol} at {price} using {amount} with stop loss at {sl} and take profit at {tp}",
                        end=", ",
                    )
                    client = self._client.long(symbol, type, amount, price, sl, tp)
                if side == "sell":
                    self._log(
                        f"Attempting to open short position with {type} short order for {symbol} at {price} using {amount} with stop loss at {sl} and take profit at {tp}",
                        end=", ",
                    )
                    client = self._client.short(symbol, type, amount, price, sl, tp)
            else:
                raise InvalidCodeError("Wrong code")
        except InvalidCodeError as e:
            print(f"OrderClient failed to edit order: {e}")
            print(
                "\nPlease call proxy.codes() in order to retrieve the current market codes that are offered\n"
            )
            print(f"Codes: {self._pub_client.codes()}")
        except NetworkError as e:
            print(f"NetworkError - OrderClient failed to edit order: {e}")
            raise
        except ExchangeError as e:
            print(f"ExchangeError - OrderClient failed to edit order: {e}")
            raise
        except Exception as e:
            print(f"OrderClient failed to edit order: {e}")
            raise
        else:
            self._order = deepcopy(client._order)
            self._log("done.")

    def cancel(self):
        """Cancel pending order

        Raises:
            OrderTypeError: Order type must be limit in order to cancel
            NetworkError: OrderClient failed to cancel order for {symbol} with id {id}
            ExchangeError: OrderClient failed to cancel order for {symbol} with id {id}
            Exception: OrderClient failed to cancel order for {symbol} with id {id}
        """
        type = self.query("type")
        if type == "market":
            raise OrderTypeError("Order type must be limit in order to cancel")

        id = self.query("id")
        symbol = self.query("symbol")
        data = None
        try:
            self._log(f"Attempting to cancel order for {symbol} with id {id}", end=", ")
            # Cancel order
            if not self.closed():
                data = self._client.cancel(id, symbol)
        except NetworkError as e:
            print(
                f"NetworkError - OrderClient failed to cancel order for {symbol} with id {id}: {e}"
            )
            raise
        except ExchangeError as e:
            print(
                f"ExchangeError - OrderClient failed to cancel order for {symbol} with id {id}: {e}"
            )
            raise
        except Exception as e:
            print(f"OrderClient failed to cancel order for {symbol} with id {id}: {e}")
            raise
        else:
            self._log("done.")
        finally:
            # Update state
            if data:
                self._update(order_data=data, state="canceled")

    def canceled(self):
        """Check if order was canceled

        Returns:
            Bool: Order was successfully canceled
        """
        return self._state == "canceled"

    def pending(self):
        """Check if order is still open

        Raises:
            NetworkError: OrderClient failed to check pending state
            ExchangeError: OrderClient failed to check pending state
            Exception: OrderClient failed to check pending state

        Returns:
            Bool: Order is still open
        """
        id = self.query("id")
        symbol = self.query("symbol")

        data = None
        try:
            self._log(f"Attempting to retrieve orders for {symbol}", end=", ")
            data = self._client.orders(symbol)
        except NetworkError as e:
            print(f"NetworkError - OrderClient failed to check pending state: {e}")
            raise
        except ExchangeError as e:
            print(f"ExchangeError - OrderClient failed to check pending state: {e}")
            raise
        except Exception as e:
            print(f"OrderClient failed to check pending state: {e}")
            raise
        else:
            self._log("done.")
        finally:
            if data:
                for order in data:
                    if order["id"] == id:
                        self._update(order_data=order, state="pending")
                        break

        return self._state == "pending"

    def closed(self):
        """Check if order was filled or cancelled

        Raises:
            NetworkError: OrderClient failed to check closed state
            ExchangeError: OrderClient failed to check closed state
            Exception: OrderClient failed to check closed state

        Returns:
            Bool: Order was successfully filled
        """
        id = self.query("id")
        symbol = self.query("symbol")

        found = False
        data = None
        try:
            self._log(f"Attempting to retrieve orders for {symbol}", end=", ")
            data = self._client.orders(symbol)
        except NetworkError as e:
            print(f"NetworkError - OrderClient failed to check closed state: {e}")
            raise
        except ExchangeError as e:
            print(f"ExchangeError - OrderClient failed to check closed state: {e}")
            raise
        except Exception as e:
            print(f"OrderClient failed to check closed state: {e}")
            raise
        else:
            self._log("done.")
        finally:
            if data:
                for res in data:
                    if res["id"] == id:
                        found = True

            if not found:
                self._update(state="closed")

        return self._state == "closed"

    def retry(
        self,
        price: float = None,
        sl_percent: int = None,
        tp_percent: int = None,
    ):
        """Ensure limit order was successfully placed at current ask price, if None then will use current ask price

        Args:
            price (float): Price to retry order at. Defaults to None.
            sl_percent: Set stop loss percent from price. Defaults to None.
            tp_percent: Set take profit percent from price. Defaults to None.

        Raises:
            OrderTypeError: Order type must be limit in order to retry
            NetworkError: OrderClient failed to retry
            ExchangeError: OrderClient failed to retry
            Exception: OrderClient failed to retry

        Returns:
            Bool: Order successfully placed
        """
        type = self.query("type")
        if type == "market":
            raise OrderTypeError("Order type must be limit in order to retry")

        if self.pending():
            self.cancel()

        symbol = self.query("symbol")
        amount = self.query("amount")

        try:
            while not self.pending() and self.closed():
                self._log(f"Retrying order placement...")
                self.edit(
                    amount=amount,
                    price=price,
                    sl_percent=sl_percent,
                    tp_percent=tp_percent,
                ) if price else self.edit(
                    amount=amount,
                    price=self._pub_client.price(symbol=symbol),
                    sl_percent=sl_percent,
                    tp_percent=tp_percent,
                )

        except InsufficientFunds:
            print(
                "InsufficientFundsError, more than likely tried to place order that was already closed"
            )
            pass
        except NetworkError as e:
            print(f"NetworkError - OrderClient failed to retry: {e}")
            raise
        except ExchangeError as e:
            print(f"ExchangeError - OrderClient failed to retry: {e}")
            raise
        except Exception as e:
            print(f"OrderClient failed to retry: {e}")
            raise
        else:
            self._log("Order placed, done.")
        finally:
            self.closed()

        return True

    def close(
        self,
        retry: bool = False,
        wait: int = 1,
        price: float = None,
        tries: int = 1,
        sl_percent: int = None,
        tp_percent: int = None,
    ):
        """Waits until order is filled

        Args:
            retry (bool): Ensure limit order was successfully placed at current ask price. Defaults to None.
            wait (int): The amount of time to wait until retry. Defaults to 2 seconds.
            price (float): Price to retry order at. Defaults to None (will use current market price).
            tries (int): Number of times to retry. Defaults to 1.
            sl_percent: Set stop loss percent from price. Defaults to None.
            tp_percent: Set take profit percent from price. Defaults to None.

        Raises:
            OrderTypeError: Order type must be limit in order to close
            NetworkError: OrderClient failed to close order
            ExchangeError: OrderClient failed to close order
            Exception: OrderClient failed to close order

        Returns:
            Bool: Order successfully filled
        """
        type = self.query("type")
        if type == "market":
            raise OrderTypeError("Order type must be limit in order to close")

        self._log(
            f"Waiting until order is filled is canceled after {tries} number of retries...",
            end=", ",
        )

        i = 0
        closed = False
        try:
            while i <= tries:
                sleep(wait)

                if self.closed():
                    closed = True
                    break

                if retry and not self.closed():
                    self.retry(
                        price=price, sl_percent=sl_percent, tp_percent=tp_percent)

                i += 1

            if not closed and self.pending():
                self.cancel()
        except NetworkError as e:
            print(f"NetworkError - OrderClient failed to close order: {e}")
            raise
        except ExchangeError as e:
            print(f"ExchangeError - OrderClient failed to close order: {e}")
            raise
        except Exception as e:
            print(f"OrderClient failed to close order: {e}")
            raise
        else:
            self._log("done.")

        return closed

    def verbose(self):
        """Turn on logging"""
        self._verbose = True

    def silent(self):
        """Turn off logging"""
        self._verbose = False
