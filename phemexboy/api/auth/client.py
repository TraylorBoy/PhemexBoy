"""Implements AuthClientInterface"""

import os
import ccxt

from botboy import BotBoy
from phemexboy.interfaces.auth.client_interface import AuthClientInterface
from phemexboy.api.auth.order import OrderClient
from dotenv import load_dotenv

load_dotenv()


class AuthClient(AuthClientInterface):
    def __init__(self):
        self._endpoint = ccxt.phemex(
            {
                "apiKey": os.getenv("KEY"),
                "secret": os.getenv("SECRET"),
                "enableRateLimit": True,
            }
        )
        self._bot = BotBoy(name="AuthBot")

    def _worker(self, task: object, *args: tuple, wait: bool = True):
        """Runs tasks on separate thread

        Args:
            task (object): Method to execute on separate thread
            *args (list): Parameters for task
            wait (bool, optional): Wait for execution to finish. Defaults to True.

        Returns:
            Any: Result from task execution
        """

        self._endpoint.load_markets(reload=True)
        self._bot.task = task
        if len(args) > 0:
            self._bot.execute(*args, wait=wait)
        else:
            self._bot.execute(wait=wait)
        return self._bot.result

    def leverage(self, amount: int, symbol: str):
        """Set future account leverage

        Args:
            amount (int): Set leverage to this amount
            symbol (str): Created symbol for base and quote currencies

        Returns:
            Bool: Leverage successfully set or not
        """
        return self._worker(self._endpoint.set_leverage, amount, symbol)["data"] == "OK"

    def orders(self, symbol: str):
        """Retrieve all open orders for symbol

        Args:
            symbol (str): Created symbol for base and quote currencies

        Returns:
            List: All open orders
        """
        return self._worker(self._endpoint.fetch_open_orders, symbol)

    def cancel(self, id: str, symbol: str):
        """Cancel open order

        Args:
            id (str): Order id
            symbol (str): Created symbol for base and quote currencies

        Returns:
            Dictionary: Order data
        """
        return self._worker(self._endpoint.cancel_order, id, symbol)

    def balance(self, currency: str, code: str):
        """Retrieve the balance of an asset on exchange

        Args:
            currency (str): The currency balance to retrieve (ex. 'BTC')
            code (str): Market code (ex. 'spot')

        Raises:
            Exception: InvalidCode

        Returns:
            Float: Balance for account
        """
        if code == "spot":
            return self._worker(self._endpoint.fetch_balance)[currency]["free"]
        elif code == "future":
            params = {"type": "swap", "code": "USD"}
            return self._worker(self._endpoint.fetch_balance, params)[currency]["free"]
        else:
            raise Exception("Invalid code")

    def buy(self, symbol: str, type: str, amount: float, price: float = None):
        """Places a buy order

        Args:
            symbol (str): Created symbol for base and quote currencies
            type (str): Type of order (only supports 'market' and 'limit')
            amount (float): Amount of base currency you would like to buy
            price (float, optional): Set limit order price. Defaults to None.

        Returns:
            OrderClient: Object that represents open order and allows for interaction
        """
        params = {"timeInForce": "PostOnly"}
        data = self._worker(
            self._endpoint.create_order, symbol, type, "buy", amount, price, params
        )
        return OrderClient(data, self)

    def sell(self, symbol: str, type: str, amount: float, price: float = None):
        """Places a sell order

        Args:
            symbol (str): Created symbol for base and quote currencies
            type (str): Type of order (only supports 'market' and 'limit')
            amount (float): Amount of base currency you would like to buy
            price (float, optional): Set limit order price. Defaults to None.

        Returns:
            OrderClient: Object that represents open order and allows for interaction
        """
        params = {"timeInForce": "PostOnly"}
        data = self._worker(
            self._endpoint.create_order, symbol, type, "sell", amount, price, params
        )
        return OrderClient(data, self)

    def position(self, symbol: str):
        """Create a PositionClient representing the open position for symbol

        Args:
            symbol(str): Created symbol for base and quote currencies

        Raises:
            NotImplementedError: Must implement when subclassing
        """
        raise NotImplementedError

    def long(
        self,
        symbol: str,
        type: str,
        amount: int,
        price: float = None,
        sl: float = None,
        tp: float = None,
    ):
        """Open a long position

        Args:
            symbol (str): Created symbol for base and quote currencies
            type (str): Type of order (only supports 'market' and 'limit')
            amount (int): Number of contracts to open
            price (float, optional): Set limit order price. Defaults to None.
            sl (float, optional): Set stop loss price. Defaults to None.
            tp (float, optional): Set take profit price. Defaults to None.

        Raises:
            NotImplementedError: Must implement the method when subclassing
        """
        params = {
            "type": "swap",
            "code": "USD",
            "stopLossPrice": sl,
            "takeProfitPrice": tp,
            "slTrigger": "ByLastPrice",
            "tpTrigger": "ByLastPrice",
            "timeInForce": "PostOnly",
        }
        try:
            data = self._worker(
                self._endpoint.create_order, symbol, type, "buy", amount, price, params
            )
        except Exception as e:
            raise Exception(e)

    def short(
        self,
        symbol: str,
        type: str,
        amount: int,
        price: float = None,
        sl: float = None,
        tp: float = None,
    ):
        """Open a short position

        Args:
            symbol (str): Created symbol for base and quote currencies
            type (str): Type of order (only supports 'market' and 'limit')
            amount (int): Number of contracts to open
            price (float, optional): Set limit order price. Defaults to None.
            sl (float, optional): Set stop loss price. Defaults to None.
            tp (float, optional): Set take profit price. Defaults to None.

        Raises:
            NotImplementedError: Must implement the method when subclassing
        """
        params = {
            "type": "swap",
            "code": "USD",
            "stopLossPrice": sl,
            "takeProfitPrice": tp,
            "slTrigger": "ByLastPrice",
            "tpTrigger": "ByLastPrice",
            "timeInForce": "PostOnly",
        }
        try:
            data = self._worker(
                self._endpoint.create_order, symbol, type, "sell", amount, price, params
            )
        except Exception as e:
            raise Exception(e)
