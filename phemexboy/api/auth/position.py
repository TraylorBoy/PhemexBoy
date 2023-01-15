"""Implements PositionClientInterface"""

from phemexboy.interfaces.auth.position_interface import PositionClientInterface
from phemexboy.interfaces.auth.client_interface import AuthClientInterface

from copy import deepcopy


class PositionClient(PositionClientInterface):
    def __init__(self, position_data: dict, client: AuthClientInterface):
        self._update(position_data, "open")
        self._client = client

    def __str__(self):
        out = ""
        for key in self._position.keys():
            out += f"{key}: {self._position[key]}\n"
        return out

    def _update(self, position_data: dict = None, state: str = None):
        """Set position and state

        Args:
            position_data (dict): Data received when future order is filled. Default is None.
            state (str): Open or Closed. Default is None.
        """
        if position_data:
            # Info is original request, not needed
            del position_data["info"]
            self._position = position_data

        if state:
            self._state = state

    def _check_closed(self):
        """Checks if position was fully closed

        Returns:
            Bool: All contracts in position was closed
        """
        # Get new position data
        symbol = self.query("symbol")
        pos = self._client.position(symbol)
        self._position = deepcopy(pos._position)

        # Check if position closed
        contracts = self.query("contracts")
        if contracts == 0:
            return True
        return False

    def query(self, request: str):
        """Retrieve position information data

        Args:
          request (str): Type of data you want to retrieve from PositionClient

        Raises:
            Exception: Invalid request

        Returns:
            String: Requested order data
        """
        if request not in list(self._position.keys()):
            raise Exception("Invalid request")
        return self._position[request]

    def close(self, amount: int = 1, all: bool = False):
        """Close open position

        Args:
            amount (int): How many contracts to close. Defaults to 1.
            all (bool): Close all contracts. Defaults to False.
        """
        side = self.query("side")
        symbol = self.query("symbol")
        type = "market"

        if all:
            amount = self.query("contracts")

        if side == "long":
            self._client.short(symbol, type, amount)
        if side == "short":
            self._client.long(symbol, type, amount)

        if self._check_closed():
            self._update(state="closed")

    def closed(self):
        """Retrieves closed state

        Returns:
            Bool: Position successfully closed or not
        """
        return self._state == "closed"
