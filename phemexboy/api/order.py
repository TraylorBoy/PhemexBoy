"""Implements OrderClientInterface"""

from phemexboy.interfaces.order_interface import OrderClientInterface


class OrderClient(OrderClientInterface):
    def __init__(self, order, client):
        self._update(order)
        self._client = client

    def __str__(self):
        out = ""
        for key in self._order.keys():
            out += f"{key}: {self._order[key]}\n"
        return out

    def _update(self, order):
        """Updates order data"""
        # Extract proper symbol
        symbol = order["info"]["symbol"]
        del order["info"]

        self._order = order
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
            Exception: Order type must be limit
            Exception: Failed to edit order
        """
        symbol = self.query("symbol")
        type = self.query("type")
        side = self.query("side")

        if type == "market":
            raise Exception("Order type must be limit")

        try:
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
        except Exception as e:
            raise Exception(e)

    def cancel(self):
        """Cancel pending order

        Raises:
            Exception: Failed to cancel order

        Returns:
          Bool: Order cancellation was successful
        """
        try:
            id = self.query("id")
            symbol = self.query("symbol")
            order_data = self._client._worker(
                self._client._endpoint.cancel_order, id, symbol
            )
            return True
        except Exception as e:
            raise Exception(e)
