"""API Wrapper Module"""
__version__ = "2.0.0"

# TODO: Refactor
# TODO: Add errors
# TODO: Interface for public and private clients
# TODO: Add examples for public methods to README
# TODO: Separate public and auth clients to separate classes
# TODO: Add logging
# TODO: Add change_account
# TODO: If possible retrieve current trading fees


class PhemexClient:
    def __init__(self):
        pass

    # ------------------------------- FUTURE Methods ------------------------------- #

    def future_balance(self, of):
        """Retrieve FUTURE account balance for specified asset

        of (String) - Asset to retrieve balance for (ex. BTC)
        """
        params = {"type": "swap", "code": "USD"}
        return self._bot(self._client.fetch_balance, params)[of]["free"]

    def leverage(self, amount, symbol):
        """Set leverage

        amount (Integer) - Leverage to set to
        symbol (String) - Symbol to set the leverage for
        """
        return self._bot(self._client.set_leverage, amount, symbol)

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
                "slTrigger": "ByLastPrice",
                "tpTrigger": "ByLastPrice",
            }
            return self._bot(
                self._client.create_order, symbol, type, "buy", amount, price, params
            )["info"]["orderID"]
        elif sl and not tp:
            params = {"type": "swap", "code": "USD", "stopLossPrice": sl}
            return self._bot(
                self._client.create_order, symbol, type, "buy", amount, price, params
            )["info"]["orderID"]
        elif tp and not sl:
            params = {"type": "swap", "code": "USD", "takeProfitPrice": tp}
            return self._bot(
                self._client.create_order, symbol, type, "buy", amount, price, params
            )["info"]["orderID"]
        else:
            params = {"type": "swap", "code": "USD"}
            return self._bot(
                self._client.create_order, symbol, type, "buy", amount, price, params
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
                "slTrigger": "ByLastPrice",
                "tpTrigger": "ByLastPrice",
            }
            return self._bot(
                self._client.create_order, symbol, type, "sell", amount, price, params
            )["info"]["orderID"]
        elif sl and not tp:
            params = {"type": "swap", "code": "USD", "stopLossPrice": sl}
            return self._bot(
                self._client.create_order, symbol, type, "sell", amount, price, params
            )["info"]["orderID"]
        elif tp and not sl:
            params = {"type": "swap", "code": "USD", "takeProfitPrice": tp}
            return self._bot(
                self._client.create_order, symbol, type, "sell", amount, price, params
            )["info"]["orderID"]
        else:
            params = {"type": "swap", "code": "USD"}
            return self._bot(
                self._client.create_order, symbol, type, "sell", amount, price, params
            )["info"]["orderID"]

    def close(self, symbol, amount):
        """Closes open position"""
        if self.position == "long":
            self.short(symbol, "market", amount)
            self.position = None
        if self.position == "short":
            self.long(symbol, "market", amount)
            self.position = None

    def positions(self, symbol):
        """Returns future account positions

        symbol (String) - The symbol to retrieve position for (ex. BTC/USD:USD)
        """
        pos = self._bot(self._client.fetch_positions)

        for position in pos:
            if position["symbol"] == symbol:
                return position

    def in_position(self, symbol):
        """Returns true if currently in position for symbol, false otherwise

        symbol (String) - The symbol to check if in position for (ex. BTC/USD:USD)
        """

        return self.positions(symbol)["contracts"] > 0

    # --------------------------- SPOT & FUTURE Methods -------------------------- #

    def cancel(self, id, symbol):
        """Cancel an open order

        id (String) - Order ID to cancel
        symbol (String) - Pairing that the order is tied to (ex. sBTCUSDT)
        """
        return self._bot(self._client.cancel_order, id, symbol)
