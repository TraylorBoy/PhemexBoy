"""Phemex Spot API Wrapper Module"""

import ccxt


class SpotBoy:
    def __init__(self, api_key, secret):
        self.client = ccxt.phemex(
            {"apiKey": api_key, "secret": secret, "enableRateLimit": True}
        )
        self.markets = self.client.load_markets()

    def balance(self, of):
        """Retrieves balance of asset from exchange wallet

        of (String) - Asset to retrieve balance for ex. 'BTC'
        """
        return self.client.fetch_balance()[of]
