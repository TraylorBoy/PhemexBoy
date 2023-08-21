"""General unit tests"""

import unittest

from phemexboy.proxy import Proxy
from phemexboy.helpers.conversions import usdt_to_crypto

class TestClient(unittest.TestCase):
  def test_init(self):
    proxy = Proxy()

  def test_future_trade(self):
    proxy = Proxy()
    symbol = proxy.symbol('BTC', 'USD', 'future')

    # Make sure you have enough
    bal = proxy.balance('USD', 'future')
    print(f"Retrieved future balance: {bal}")
    self.assertGreaterEqual(bal, 0)

    # Place limit order for 1 contract
    type = 'limit'
    amount = 1
    price = proxy.price(symbol) - 0.01
    tp = price + (price * 0.01)
    sl = price - (price * 0.01)

    # Long trade
    order = proxy.long(symbol, type, amount, price, tp=tp, sl=sl)
    order.verbose()
    print(f'Retrieved long order: \n{order}')
    # Ensure order was closed
    if order.close(True, tries=100, sl_percent=1, tp_percent=1):
      # Retrieved position
      pos = proxy.position(symbol)
      pos.verbose()
      print(f"Retrieved position: {pos}")

      # Close contracts
      pos.close(amount)

    # Short trade
    price = proxy.price(symbol) + 0.01
    tp = price - (price * 0.01)
    sl = price + (price * 0.01)

    order = proxy.short(symbol, type, amount, price, tp=tp, sl=sl)
    order.verbose()
    print(f'Retrieved short order: \n{order}')
    # Ensure order was closed
    if order.close(True, tries=100, sl_percent=1, tp_percent=1):
      # Retrieved position
      pos = proxy.position(symbol)
      pos.verbose()
      print(f"Retrieved position: {pos}")

      # Close contracts
      pos.close(amount)

  def test_spot_trade(self):
    proxy = Proxy()
    symbol = proxy.symbol('BTC', 'USD', 'spot')

    # Make sure you have enough
    bal = proxy.balance('USDT', 'spot')
    print(f'Retrieved bal: {bal}')
    self.assertGreaterEqual(bal, 0)

    # Buy BTC
    type = "limit"
    price = proxy.price(symbol) - 0.01
    amount = usdt_to_crypto(bal, price, 100)
    print(f"Buying {amount} worth of BTC")

    order = proxy.buy(symbol, type, amount, price)
    order.verbose()
    print(f'Retrieved buy order {order}')

    if order.close(True, tries=100):
      print('Order closed')

    # Sell BTC
    type = 'market'
    amount = proxy.balance('BTC', 'spot')
    order = proxy.sell(symbol, type, amount)
