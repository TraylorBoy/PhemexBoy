"""Implements PositionClientInterface"""

from phemexboy.interfaces.auth.position_interface import PositionClientInterface


class PositionClient(PositionClientInterface):
    def __init__(self, position_data, client):
        self._update(position_data)
        self._client = client

    def __str__(self):
        out = ""
        for key in self._position.keys():
            out += f"{key}: {self._position[key]}\n"
        return out

    def _update(self, position_data):
        """Updates position data"""
        del position_data["info"]
        self._position = position_data

    def query(self, request):
        """Retrieve position information data

        Args:
          request (str): Type of data you want to retrieve from PositionClient

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
            amount (float): Amount of contracts you are using for order
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

            position_data = None
            if side == "buy":
                position_data = self._client._worker(
                    self._client.long, symbol, type, amount, price
                )
            if side == "sell":
                position_data = self._client._worker(
                    self._client.short, symbol, type, amount, price
                )

            self._update(position_data)
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
            self._client._worker(self._client._endpoint.cancel_order, id, symbol)
            return True
        except Exception as e:
            raise Exception(e)

    def close(self, amount):
        """Close open position

        Args:
            amount (int): How many contracts to close

        Raises:
            Exception: Failed to close position

        Returns:
            Bool: Position successfully closed
        """
        side = self.query("side")
        symbol = self.query("symbol")
        type = "market"

        try:
            if side == "long":
                self._client._worker(self._client.short, symbol, type, amount)
            if side == "short":
                self._client._worker(self._client.long, symbol, type, amount)
            self._
            return True
        except Exception as e:
            raise Exception(e)
