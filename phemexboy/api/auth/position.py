"""Implements PositionClientInterface"""

from phemexboy.interfaces.auth.position_interface import PositionClientInterface
from phemexboy.interfaces.auth.client_interface import AuthClientInterface
from phemexboy.exceptions import InvalidRequestError

from copy import deepcopy
from ccxt import NetworkError, ExchangeError


class PositionClient(PositionClientInterface):
    def __init__(
        self, position_data: dict, client: AuthClientInterface, verbose: bool = False
    ):
        self._verbose = verbose
        self._update(position_data, "open")
        self._client = client

    def __str__(self):
        out = ""
        for key in self._position.keys():
            out += f"{key}: {self._position[key]}\n"
        return out

    def _log(self, msg: str, end: str = None):
        """Print message to output if not silent

        Args:
            msg (str): Message to print to output
            end (str): String appended after the last value. Default a newline.
        """
        if self._verbose:
            print(msg, end=end)

    def _update(self, position_data: dict = None, state: str = None):
        """Set position and state

        Args:
            position_data (dict): Data received when future order is filled. Default is None.
            state (str): Open or Closed. Default is None.
        """
        if position_data:
            self._log("Updating position data", end=", ")
            # Info is original request, not needed
            del position_data["info"]
            self._position = position_data
            self._log("done.")

        if state:
            self._log(f"Updating state to {state}", end=", ")
            self._state = state
            self._log("done.")

    def _check_closed(self):
        """Checks if position was fully closed

        Raises:
            NetworkError: AuthClient failed to retrieve position for {symbol}
            ExchangeError: AuthClient failed to retrieve position for {symbol}
            Exception: AuthClient failed to retrieve position for {symbol}

        Returns:
            Bool: All contracts in position was closed
        """
        # Get new position data
        symbol = self.query("symbol")

        pos = None
        contracts = None
        try:
            self._log(f"Attempting to retrieve position for {symbol}", end=", ")
            pos = self._client.position(symbol)
            self._log(f"PositionClient retrieved", end=", ")
        except NetworkError as e:
            print(
                f"NetworkError - AuthClient failed to retrieve position for {symbol}: {e}"
            )
            raise
        except ExchangeError as e:
            print(
                f"ExchangeError - AuthClient failed to retrieve position for {symbol}: {e}"
            )
            raise
        except Exception as e:
            print(f"AuthClient failed to retrieve position for {symbol}: {e}")
            raise
        else:
            self._position = deepcopy(pos._position)
            self._log("done.")
        finally:
            contracts = self.query("contracts")

        # Check if position closed
        if contracts == 0:
            return True
        return False

    def requests(self):
        """Returns a list of all request params

        Returns:
            List: Request params
        """
        return list(self._position.keys())

    def query(self, request: str):
        """Retrieve position information data

        Args:
            request (str): Type of data you want to retrieve from PositionClient

        Raises:
            InvalidRequestError: PositionClient failed to retrieve data for {request}

        Returns:
            String: Requested order data
        """
        data = None
        try:
            if request not in self.requests():
                raise InvalidRequestError()

            self._log(f"Retrieving position data based on {request}", end=", ")
            data = self._position[request]
        except InvalidRequestError:
            print(
                f"InvalidRequestError - PositionClient failed to retrieve data for {request}"
            )
            print("Call requests() in order to retrieve valid params")
            print(f"Params: {self.requests()}")
        else:
            self._log("done.")
        return data

    def close(self, amount: int = 1, all: bool = False):
        """Close open position

        Args:
            amount (int): How many contracts to close. Defaults to 1.
            all (bool): Close all contracts. Defaults to False.

        Raises:
            NetworkError: PositionClient failed to close position
            ExchangeError: PositionClient failed to close position
            Exception: PositionClient failed to close position
        """
        side = self.query("side")
        symbol = self.query("symbol")
        type = "market"

        if all:
            amount = self.query("contracts")

        self._log(f"Attempting to close {amount} contracts for position")

        try:
            if side == "long":
                self._log("Attempting to close long position")
                self._client.short(symbol, type, amount)
            if side == "short":
                self._log("Attempting to close short position")
                self._client.long(symbol, type, amount)
        except NetworkError as e:
            print(f"NetworkError - PositionClient failed to close position: {e}")
            raise
        except ExchangeError as e:
            print(f"ExchangeError - PositionClient failed to close position: {e}")
            raise
        except Exception as e:
            print(f"PositionClient failed to close position: {e}")
            raise
        else:
            self._log("Position closed, done.")
        finally:
            if self._check_closed():
                self._update(state="closed")

    def closed(self):
        """Retrieves closed state

        Returns:
            Bool: Position successfully closed or not
        """
        return self._state == "closed"

    def verbose(self):
        """Turn on logging"""
        self._verbose = True

    def silent(self):
        """Turn off logging"""
        self._verbose = False
