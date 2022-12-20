"""Proxy for FutureBoy's and SpotBoy's API Wrapper Module"""

import ccxt

from futureboy import FutureBoy
from spotboy import SpotBoy


class PhemexBoy:
    def __init__(self, api_key, secret):
        self.spot_client = SpotBoy(api_key, secret)
        self.futures_client = FutureBoy(api_key, secret)

    def balance(self, of):
        """Retrieves balance of token from spot account

        of (String) - Token to retrieve balance for ex. 'BTC'
        """
        return self.spot_client.balance(of)

    def futures_balance(self, of):
        """Retrieves balance of token from futures account

        of (String) - Token to retrieve balance for ex. 'BTC'
        """
        return self.futures_client.balance(of)
