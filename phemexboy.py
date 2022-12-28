"""API Wrapper Module"""
__version__ = "1.0.0"

import ccxt

from botboy import BotBoy


class PhemexBoy:
    def __init__(self, api_key, secret):
        self.client = ccxt.phemex(
            {"apiKey": api_key, "secret": secret, "enableRateLimit": True}
        )
        self.bot = BotBoy(name="PhemexBot")
        self.position = None

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

    def price(self, symbol):
        """Retrieve SPOT price of asset

        symbol (String) - Pairing to retrieve price for (ex. sBTCUSDT)
        """
        return self._bot(self.client.fetch_ticker, symbol)["last"]

    # ------------------------------- SPOT Methods ------------------------------- #

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

    def balance(self, of):
        """Retrieve SPOT account balance for specified asset

        of (String) - Asset to retrieve balance for (ex. BTC)
        """
        return self._bot(self.client.fetch_balance)[of]["free"]

    def usdt_converter(self, symbol, percent):
        """Returns the percentage of your account that you would like to use when trading symbol

        symbol (String) - Trading symbol to perform calculations for (ex. sBTCUSDT)
        percent (Integer) - Percent of account that you would like to use while trading
        """
        bal = self.balance("USDT")
        price = self.price(symbol)
        amount = (bal / price) * (percent / 100)
        return round(amount, 6)

    def buy(self, symbol, type, amount, price=None):
        """Place a buy order

        symbol (String) - Pairing to place order for
        type (String) - Either 'market' or 'limit'
        amount (Float) - Amount of currency to use for order
        price (Float) - Price to place limit order at
        """
        # Format
        if price is not None:
            price = round(price, 2)

        return self._bot(self.client.create_order, symbol, type, "buy", amount, price)[
            "info"
        ]["orderID"]

    def sell(self, symbol, type, amount, price=None):
        """Place a sell order

        symbol (String) - Pairing to place order for
        type (String) - Either 'market' or 'limit'
        amount (Integer) - Amount of currency to use for order
        price (Float) - Price to place limit order at
        """
        # Format
        if price is not None:
            price = round(price, 2)

        return self._bot(self.client.create_order, symbol, type, "sell", amount, price)[
            "info"
        ]["orderID"]

    # ------------------------------- FUTURE Methods ------------------------------- #

    def future_symbols(self):
        """Retrieve all symbols from futures market"""
        self.client.load_markets()
        symbols = []
        for symbol in self.client.symbols:
            if ":" in symbol:
                symbols.append(symbol)
        return symbols

    def future_balance(self, of):
        """Retrieve FUTURE account balance for specified asset

        of (String) - Asset to retrieve balance for (ex. BTC)
        """
        params = {"type": "swap", "code": "USD"}
        return self._bot(self.client.fetch_balance, params)[of]["free"]

    def leverage(self, amount, symbol):
        """Set leverage

        amount (Integer) - Leverage to set to
        symbol (String) - Symbol to set the leverage for
        """
        return self._bot(self.client.set_leverage, amount, symbol)

    def long(self, symbol, type, amount, price=None, sl=None, tp=None):
        """Open a long position

        symbol (String) - Pairing to place order for
        type (String) - Either 'market' or 'limit'
        amount (Float) - Amount of currency to use for order
        price (Float) - Price to open position at for limit orders
        sl (Float) - Price to trigger stop loss
        tp (Float) - Price to trigger take profit
        """
        if not self.position:
            self.position = "long"

        # Format
        if price is not None:
            price = round(price, 2)
        if sl is not None:
            sl = round(sl, 2)
        if tp is not None:
            tp = round(tp, 2)

        if sl and tp:
            params = {
                "type": "swap",
                "code": "USD",
                "stopLossPrice": sl,
                "takeProfitPrice": tp,
            }
            return self._bot(
                self.client.create_order, symbol, type, "buy", amount, price, params
            )["info"]["orderID"]
        elif sl and not tp:
            params = {"type": "swap", "code": "USD", "stopLossPrice": sl}
            return self._bot(
                self.client.create_order, symbol, type, "buy", amount, price, params
            )["info"]["orderID"]
        elif tp and not sl:
            params = {"type": "swap", "code": "USD", "takeProfitPrice": tp}
            return self._bot(
                self.client.create_order, symbol, type, "buy", amount, price, params
            )["info"]["orderID"]
        else:
            params = {"type": "swap", "code": "USD"}
            return self._bot(
                self.client.create_order, symbol, type, "buy", amount, price, params
            )["info"]["orderID"]

    def short(self, symbol, type, amount, price=None, sl=None, tp=None):
        """Open a short position

        symbol (String) - Pairing to place order for
        type (String) - Either 'market' or 'limit'
        amount (Float) - Amount of currency to use for order
        price (Float) - Price to open position at for limit orders
        sl (Float) - Price to trigger stop loss
        tp (Float) - Price to trigger take profit
        """
        if not self.position:
            self.position = "short"
        # Format
        if price is not None:
            price = round(price, 2)
        if sl is not None:
            sl = round(sl, 2)
        if tp is not None:
            tp = round(tp, 2)

        if sl and tp:
            params = {
                "type": "swap",
                "code": "USD",
                "stopLossPrice": sl,
                "takeProfitPrice": tp,
            }
            return self._bot(
                self.client.create_order, symbol, type, "sell", amount, price, params
            )["info"]["orderID"]
        elif sl and not tp:
            params = {"type": "swap", "code": "USD", "stopLossPrice": sl}
            return self._bot(
                self.client.create_order, symbol, type, "sell", amount, price, params
            )["info"]["orderID"]
        elif tp and not sl:
            params = {"type": "swap", "code": "USD", "takeProfitPrice": tp}
            return self._bot(
                self.client.create_order, symbol, type, "sell", amount, price, params
            )["info"]["orderID"]
        else:
            params = {"type": "swap", "code": "USD"}
            return self._bot(
                self.client.create_order, symbol, type, "sell", amount, price, params
            )["info"]["orderID"]

    def close(self, symbol, amount):
        """Closes open position"""
        if self.position == "long":
            self.short(symbol, "market", amount)
            self.position = None
        if self.position == "short":
            self.long(symbol, "market", amount)
            self.position = None

    # --------------------------- SPOT & FUTURE Methods -------------------------- #

    def cancel(self, id, symbol):
        """Cancel an open order

        id (String) - Order ID to cancel
        symbol (String) - Pairing that the order is tied to (ex. sBTCUSDT)
        """
        return self._bot(self.client.cancel_order, id, symbol)["info"]["orderID"]

    def cancel_all(self, symbol):
        """Cancel all open orders

        symbol (String) - Pairing to cancel all open orders for (ex. sBTCUSDT)
        """
        return self._bot(self.client.cancel_all_orders, symbol)
