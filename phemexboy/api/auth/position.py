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
