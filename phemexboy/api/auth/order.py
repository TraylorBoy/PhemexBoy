"""Implements OrderClientInterface"""

from phemexboy.interfaces.auth.order_interface import OrderClientInterface


class OrderClient(OrderClientInterface):
    def __init__(self, order_data, client):
        self._update(order_data)
        self._client = client

    def __str__(self):
        out = ""
        for key in self._order.keys():
            out += f"{key}: {self._order[key]}\n"
        return out

    def _update(self, order_data):
        """Updates order data"""
        # Extract proper symbol
        symbol = order_data["info"]["symbol"]
        del order_data["info"]

        self._order = order_data
        self._order["symbol"] = symbol

    def query(self, request):
        """Retrieve order information data

        Args:
          request (str): Type of data you want to retrieve from OrderClient

        Raises:
            Exception: Invalid request

        Returns:
            String: Requested order data
        """
        if request not in list(self._order.keys()):
            raise Exception("Invalid request")
        return self._order[request]

    def edit(self, amount, price):
        """Edit pending order

        Args:
            amount (float): Amount of base currency you are using for order
            price (float): Edit limit order price

        Raises:
            Exception: Order type error
        """
        symbol = self.query("symbol")
        type = self.query("type")
        side = self.query("side")

        if type == "market":
            raise Exception("Order type error")

        # Reopen order
        self.cancel()

        order_data = None
        if side == "buy":
            order_data = self._client._worker(
                self._client.buy, symbol, type, amount, price
            )
        if side == "sell":
            order_data = self._client._worker(
                self._client.sell, symbol, type, amount, price
            )

        self._update(order_data)

    def cancel(self):
        """Cancel pending order

        Returns:
          Bool: Order cancellation was successful
        """

        id = self.query("id")
        symbol = self.query("symbol")

        order_data = self._client._worker(
            self._client._endpoint.cancel_order, id, symbol
        )
        self._update(order_data)
        return True
