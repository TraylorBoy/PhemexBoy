"""Phemex Futures API Wrapper Module"""

import ccxt


class FutureBoy:
    def __init__(self, api_key, secret):
        self.client = ccxt.phemex(
            {"apiKey": api_key, "secret": secret, "enableRateLimit": True}
        )

    def symbols(self):
        """Retrieves the list of asset symbols available"""
        markets = self.client.load_markets()
        tmp = list(markets.keys())
        symbols = [x for x in list(markets.keys()) if ":" in x]

        return symbols

    def balance(self, of):
        """Retrieves balance of asset from exchange wallet

        of (String) - Asset to retrieve balance for ex. 'BTC'
        """
        return self.client.fetch_balance(params={"type": "swap", "code": of})[of]

    def position(self, symbol):
        """Retrieves position of asset from exchange

        symbol (String) - Asset to retrieve position for ex. 'BTC/USD:USD'
        """

        positions = self.client.fetch_positions()
        pos = None

        for position in positions:
            if position["symbol"] == symbol:
                pos = position

        return pos
