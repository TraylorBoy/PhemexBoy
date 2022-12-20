"""Proxy for FutureBoy's and SpotBoy's API Wrapper Module"""

import ccxt

from futureboy import FutureBoy
from spotboy import SpotBoy


# TODO: ADD ASYNC (BotBoy?)
# TODO: Upgrade to CCXT Pro


class PhemexBoy:
    def __init__(self, api_key, secret):
        self.spot_client = SpotBoy(api_key, secret)
        self.futures_client = FutureBoy(api_key, secret)

    def balance(self, of):
        """Retrieves balance of asset from spot account

        of (String) - Asset to retrieve balance for ex. 'BTC'
        """
        return self.spot_client.balance(of)

    def futures_balance(self, of):
        """Retrieves balance of asset from futures account

        of (String) - Asset to retrieve balance for ex. 'BTC'
        """
        return self.futures_client.balance(of)

    def futures_position(self, symbol):
        """Retrieves position of asset from exchange

        symbol (String) - Asset to retrieve position for ex. 'BTC/USD:USD'
        """

        return self.futures_client.position(symbol)

    def futures_symbols(self):
        """Retrieves the list of asset symbols available"""
        return self.futures_client.symbols()
