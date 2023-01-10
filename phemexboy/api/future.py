"""Implements FutureClientInterface"""

import os, ccxt

from botboy import BotBoy
from phemexboy.interfaces.future_interface import FutureClientInterface
from dotenv import load_dotenv

load_dotenv()


class FutureClient(FutureClientInterface):
    def __init__(self):
        try:
            self._endpoint = ccxt.phemex(
                {"apiKey": os.getenv("KEY"), "secret": os.getenv("SECRET")}
            )
            self._bot = BotBoy(name="FutureBoy")
        except Exception as e:
            raise Exception(e)

    def _worker(self, task, *args, wait=True):
        """Runs tasks on separate thread

        Args:
            task (object): Method to execute on separate thread
            *args (list): Parameters for task
            wait (bool, optional): Wait for execution to finish. Defaults to True.

        Raises:
            Exception: Worker failed to execute task

        Returns:
            Any: Result from task execution
        """
        try:
            self._endpoint.load_markets(reload=True)
            self._bot.task = task
            if len(args) > 0:
                self._bot.execute(*args, wait=wait)
            else:
                self._bot.execute(wait=wait)
            return self._bot.result
        except Exception as e:
            raise Exception(e)

    def balance(self):
        """Retrieves FUTURE account USD balance

        Raises:
            Exception: Failed to retrieve FUTURE account USD balance

        Returns:
            Float: FUTURE account USD balance
        """
        params = {"type": "swap", "code": "USD"}
        try:
            return self._worker(self._endpoint.fetch_balance, params)["USD"]["free"]
        except Exception as e:
            raise Exception(e)

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
            Exception: Failed to open long position

        Returns:
            Dictionary: Order data
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
            return self._worker(
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
            return self._worker(
                self._endpoint.create_order, symbol, type, "sell", amount, price, params
            )
        except Exception as e:
            raise Exception(e)
