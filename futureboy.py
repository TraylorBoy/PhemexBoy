"""Phemex Futures API Wrapper Module"""

import ccxt


class FutureBoy:
    def __init__(self, api_key, secret):
        self.client = ccxt.phemex(
            {"apiKey": api_key, "secret": secret, "enableRateLimit": True}
        )

    def balance(self, of):
        """Retrieves balance of token from exchange wallet

        of (String) - Token to retrieve balance for ex. 'BTC'
        """
        return self.client.fetch_balance(params={"type": "swap", "code": of})[of]
