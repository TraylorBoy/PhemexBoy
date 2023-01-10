"""Implements SpotClientInterface"""

import os
import ccxt

from botboy import BotBoy
from phemexboy.interfaces.spot_interface import SpotClientInterface
from dotenv import load_dotenv

load_dotenv()


class SpotClient(SpotClientInterface):
    def __init__(self):
        try:
            self._endpoint = ccxt.phemex(
                {"apiKey": os.getenv("KEY"), "secret": os.getenv("SECRET")}
            )
            self._bot = BotBoy(name="SpotBoy")
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

    def balance(self, of: str):
        """Retrieves SPOT account balance for specified asset

        Args:
            of (str): Asset to retrieve balance for (ex. 'BTC')

        Raises:
            Exception: Failed to retrieve SPOT balance

        Returns:
            Float: Current SPOT balance for asset
        """
        try:
            return self._worker(self._endpoint.fetch_balance)[of]["free"]
        except Exception as e:
            raise Exception(e)

    def buy(self, symbol: str, type: str, amount: float, price: float = None):
        """Places a buy order

        Args:
            symbol (str): Created symbol for base and quote currencies
            type (str): Type of order (only supports 'market' and 'limit')
            amount (float): Amount of base currency you would like to buy
            price (float, optional): Set limit order price. Defaults to None.

        Raises:
            Exception: Failed to place buy order

        Returns:
            Dictionary: Order data
        """
        params = {"timeInForce": "PostOnly"}
        try:
            return self._worker(
                self._endpoint.create_order, symbol, type, "buy", amount, price, params
            )
        except Exception as e:
            raise Exception(e)

    def sell(self, symbol: str, type: str, amount: float, price: float = None):
        """Places a sell order

        Args:
            symbol (str): Created symbol for base and quote currencies
            type (str): Type of order (only supports 'market' and 'limit')
            amount (float): Amount of base currency you would like to buy
            price (float, optional): Set limit order price. Defaults to None.

        Raises:
            Exception: Failed to place sell order

        Returns:
            Dictionary: Order data
        """
        params = {"timeInForce": "PostOnly"}
        try:
            return self._worker(
                self._endpoint.create_order, symbol, type, "sell", amount, price, params
            )
        except Exception as e:
            raise Exception(e)
