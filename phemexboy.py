"""Proxy for FutureBoy's and SpotBoy's API Wrapper Module"""

import ccxt

from botboy import BotBoy


class PhemexBoy:
    def __init__(self, api_key, secret):
        self.client = ccxt.phemex(
            {"apiKey": api_key, "secret": secret, "enableRateLimit": True}
        )
        self.bot = BotBoy(name="PhemexBot", silent=True)

    # ------------------------------- Class Methods ------------------------------- #
    def _load(self):
        """Loads market utilizing BotBoy"""
        self.bot.task = self.client.load_markets
        self.bot.execute(True, wait=True)

    def _bot(self, task, *args, wait=True):
        """Runs tasks on separate thread"""
        self._load()
        self.bot.task = task
        if len(args) > 0:
            self.bot.execute(*args, wait=wait)
        else:
            self.bot.execute(wait=wait)
        return self.bot.result

    # ------------------------------- Utility Methods ------------------------------- #

    def time(self, format):
        """Create a timestamp from the following format (uses
        parse8601)

        format (String) - Date to create time representation from (ex. 2022-12-22T00:00:00Z)
        """
        return self.client.parse8601(format)

    def timeframes(self):
        """Retrieve all available timeframes from exchange"""
        return self.client.timeframes

    def symbols(self):
        """Retrieve all SPOT asset symbols from exchange"""
        return [
            "sBTCUSDT",
            "sETHUSDT",
            "sXRPUSDT",
            "sLINKUSDT",
            "sXTZUSDT",
            "sLTCUSDT",
            "sADAUSDT",
            "sTRXUSDT",
            "sONTUSDT",
            "sBCHUSDT",
            "sNEOUSDT",
            "sEOSUSDT",
            "sDOGEUSDT",
            "sBATUSDT",
            "sCHZUSDT",
            "sMANAUSDT",
            "sENJUSDT",
            "sSUSHIUSDT",
            "sSNXUSDT",
            "sGRTUSDT",
            "sUNIUSDT",
            "sAAVEUSDT",
            "sYFIUSDT",
            "sCOMPUSDT",
            "sMKRUSDT",
            "sDOTUSDT",
            "sALGOUSDT",
            "sVETUSDT",
            "sZECUSDT",
            "sFILUSDT",
            "sKSMUSDT",
            "sXMRUSDT",
            "sQTUMUSDT",
            "sXLMUSDT",
            "sATOMUSDT",
            "sLUNAUSDT",
            "sSOLUSDT",
            "sAXSUSDT",
            "sMATICUSDT",
            "sSHIBUSDT",
            "sFTMUSDT",
            "sDYDXUSDT",
            "sVPADUSDT",
        ]

    def currencies(self):
        """Retrieve all assets available from exchange"""
        return [
            "BTC",
            "USDT",
            "ETH",
            "XRP",
            "LINK",
            "XTZ",
            "LTC",
            "ADA",
            "TRX",
            "ONT",
            "BCH",
            "NEO",
            "EOS",
            "COMP",
            "LEND",
            "YFI",
            "DOT",
            "UNI",
            "AAVE",
            "DOGE",
            "BAT",
            "CHZ",
            "MANA",
            "ENJ",
            "SUSHI",
            "SNX",
            "GRT",
            "MKR",
            "ALGO",
            "VET",
            "ZEC",
            "FIL",
            "KSM",
            "XMR",
            "QTUM",
            "XLM",
            "ATOM",
            "LUNA",
            "SOL",
            "AXS",
            "MATIC",
            "SHIB",
            "FTM",
            "DYDX",
            "VPAD",
        ]

    # ------------------------------- SPOT Methods ------------------------------- #

    # Public API Methods
    def orderbook(self, symbol):
        """Get SPOT orderbook of asset from exchange

        symbol (String) - Pairing to retrieve orderbook for (ex. sBTCUSDT)
        """
        return self._bot(self.client.fetch_order_book, symbol)

    def price(self, symbol):
        """Retrieve SPOT price of asset

        symbol (String) - Pairing to retrieve price for (ex. sBTCUSDT)
        """
        return self._bot(self.client.fetch_ticker, symbol)

    def candle(self, symbol, tf, since=None):
        """Retrieve OHLCV of asset

        symbol (String) - Pair to retrieve OHLCV for (ex. sBTCUSDT)
        tf (String) - The timeframe to create candle for
        since (Integer) - How many candles to retrieve from supplied date
        """
        if since:
            return self._bot(self.client.fetch_ohlcv, symbol, tf, since)
        else:
            return self._bot(self.client.fetch_ohlcv, symbol, tf)

    def trades(self, symbol, since=None):
        """Retrieve trade data for specified pair

        symbol (String) - Pair to retrieve trade data for (ex. sBTCUSDT)
        since (String) - Timestamp to start fetching from
        """
        if since:
            return self._bot(self.client.fetch_trades, symbol, since)
        else:
            return self._bot(self.client.fetch_trades, symbol)

    def status(self):
        """Retrieve exchange status"""
        return self._bot(self.client.fetch_status)

    def balance(self, of):
        """Retrieve SPOT account balance for specified asset

        of (String) - Asset to retrieve balance for (ex. BTC)
        """
        pass

    # ------------------------------- FUTURE Methods ------------------------------- #

    def leverage_tiers(self, symbol):
        """Retrieve leverage data from futures

        symbol (String) - The pair to retrieve leverage data for (ex. BTC/USD:USD)
        """
        return self._bot(self.client.fetch_leverage_tiers, symbol)

    def funding_rate(self, symbol):
        """Retrieve funding rate data from futures

        symbol (String) - The pair to retrieve funding rate data for (ex. BTC/USD:USD)
        """
        return self._bot(self.client.fetch_funding_rate, symbol)

    def funding_rate_history(self, symbol, since=None):
        """Retrieve funding rate history from futures

        symbol (String) - The pair to retrieve funding rate data for (ex.
        BTC/USD:USD)
        since (String) - How far back to retrieve funding rate data
        """
        if since:
            return self._bot(self.client.fetch_funding_rate, symbol, since)
        else:
            return self._bot(self.client.fetch_funding_rate, symbol)
