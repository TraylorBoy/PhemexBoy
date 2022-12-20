"""Phemex API Wrapper Module"""

import ccxt


class PhemexBoy:
    def __init__(self, api_key, secret):
        exchange_class = getattr(ccxt, "phemex")
        self.client = exchange_class({"apiKey": api_key, "secret": secret})

    def balance(self, of):
        """Retrieves balance of token from exchange SPOT wallet

        of (String) - Token to retrieve balance for ex. 'BTC'
        """
        return self.client.fetch_balance()[of]["free"]

    def markets(self):
        """Retrieve all markets from exchange"""
        return self.client.load_markets()

    def tokens(self):
        """Retrieve all tokens from exchange"""
        tokens = list(self.markets().keys())
        tmp = []

        for token in tokens:
            tmp.append(token.split("/")[0])

        formatted = []

        for token in tmp:
            if not token.startswith("1"):
                formatted.append(token)

        return formatted

    def order(self):
        """Retrieve all accounts from exchange"""
        return self.client.has
