# PhemexBoy
Phemex API Wrapper in Python

## Notes
- All spot symbols begin with a lowercase s and utilize USDT (ex. sBTCUSDT).
- All future symbols are in the following format *BTC/USD:USD, ETH/USD:USD, etc.*
- Use spot symbols for buy and sell and future symbols for long and short
- Spot uses USDT and future uses USD
- Currently future methods only work for USD future account
- Contracts close by last price
- Orders are Post Only

## Installation
```
pip install phemexboy
```

## Usage
### Instantiate Proxy with API Key and Secret obtained from Phemex
- Uses *python-dotenv* package for security
- Simply place your api key and secret in a .env file in your root folder (add
  .env to .gitignore)
```
from phemexboy.proxy import Proxy

proxy = Proxy(verbose=False) # Defaults to True

# Turn logging on/off
proxy.verbose()
proxy.silent()
```

### Optionally instantiate AuthClient and PublicClient
- Proxy contains both auth and public methods
- PublicClient does not require .env file
```
from phemexboy.api.client import AuthClient
from phemexboy.public import PublicClient

auth_client = AuthClient()
pub_client = PublicClient()
```

## PublicClient API
---

### Retrieve all timeframes offered on Phemex
```
proxy.timeframes()
```

### Retrieve all market codes currently offered on Phemex
```
proxy.codes()
```

### Retrieve all currencies offered on Phemex
```
proxy.currencies()
```

### Create a unified market symbol needed to interact with other methods
```
proxy.symbol(base='BTC', quote='USD', code='spot') # sBTCUSDT
proxy.symbol(base='BTC', quote='USD', code='future') # BTC/USD:USD
```

### Retrieve the price of a specific pairing
```
spot_symbol = proxy.symbol(base='BTC', quote='USD', code='spot')
spot_price = proxy.price(symbol=spot_symbol)

future_symbol = proxy.symbol(base='BTC', quote='USD', code='future')
future_price = proxy.price(symbol=future_symbol)
```

### Retrieve candlestick data
```
spot_symbol = proxy.symbol(base='BTC', quote='USD', code='spot')
future_symbol = proxy.symbol(base='BTC', quote='USD', code='future')
since = "2022-01-30" # Start at date

spot_ohlcv = proxy.ohlcv(symbol=spot_symbol, tf="1m", since=since)
future_ohlcv = proxy.ohlcv(symbol=future_symbol, tf="1m")
```

### Retrieve exchange status
```
proxy.status()
```

### Retrieve exchange orderbook for symbol
```
spot_symbol = proxy.symbol(base='BTC', quote='USD', code='spot')
future_symbol = proxy.symbol(base='BTC', quote='USD', code='future')

spot_book = proxy.orderbook(symbol=spot_symbol)
future_book = proxy.orderbook(symbol=future_symbol)
```

## AuthClient API
---
### Retrieve spot and future balances
- Uses currencies instead of symbols
```
spot_bal = proxy.balance(currency="USDT", code="spot")
fut_bal = proxy.balance(currency="USD", code="future")
```

### Convert percent of USDT account into crypto amount
- Used for spot purchases, when selling crypto you do not need to use this method
```
from phemexboy.helpers.conversions import usdt_to_crypto

# Buy BTC with 90% of full account
type = 'limit'
symbol = proxy.symbol(base='BTC', quote='USD', code='spot')

price = proxy.price(symbol=symbol) - 0.1
usdt_bal = proxy.balance(currency="USDT", code="spot")
amount = usdt_to_crypto(usdt_balance=usdt_bal, price=price, percent=90)

order = proxy.buy(symbol=symbol, type=type, amount=amount, price=price)
```

### Buy/sell crypto on spot
```
# Limit Buy
type = 'limit'
symbol = proxy.symbol(base='BTC', quote='USD', code='spot')

price = proxy.price(symbol=symbol) - 0.1 # Price to place limit order at
usdt_bal = proxy.balance(currency="USDT", code="spot")
amount = usdt_to_crypto(usdt_balance=usdt_bal, price=price, percent=90) # Amount to purchase

order = proxy.buy(symbol=symbol, type=type, amount=amount, price=price) # Returns OrderClient

# Market Buy
type = "market"
symbol = proxy.symbol(base='BTC', quote='USD', code='spot')
amount = usdt_to_crypto(usdt_balance=usdt_bal, price=pub_client.price(symbol), percent=90)

order = proxy.buy(symbol=symbol, type=type, amount=amount)

# Limit Sell
type = "limit"
price = 100000
symbol = proxy.symbol(base='BTC', quote='USD', code='spot')
amount = auth_client.balance(currency="BTC", code="spot") # Just need current BTC balance

order = proxy.sell(symbol=symbol, type=type, amount=amount, price=price)

# Market Sell
type = "market"
symbol = proxy.symbol(base='BTC', quote='USD', code='spot')
amount = auth_client.balance(currency="BTC", code="spot")

order = auth_client.sell(symbol=symbol, type=type, amount=amount)
```

### Change leverage on future
```
symbol = proxy.symbol(base='BTC', quote='USD', code='future')
lev_amount = 10

success = proxy.leverage(amount=lev_amount, symbol=symbol) # Returns True/False
```

### Calculate stop loss and take profit for Future position
```
from phemexboy.helpers.conversions import stop_loss, take_profit

symbol = proxy.symbol(base="BTC", quote="USD", code="future")
amount = 1
type = "limit"
price = 9000
sl = stop_loss(price=price, percent=1, pos="long") # 1% from current price
tp = take_profit(price=price, percent=2, pos="long") # 2% above current price

order = proxy.long(symbol=symbol, type=type, amount=amount, price=price, sl=sl, tp=tp)
```

### Open a long/short position
- Amount is in contracts
- Stoploss (sl) and Takeprofit (tp) are not required, however you will have to call position.close() in order to manually close it
- You can have a sl and not a tp or vice versa
```
symbol = proxy.symbol(base="BTC", quote="USD", code="future")
amount = 1

# Limit Long
type = "limit"
price = 9000
sl = stop_loss(price=price, percent=1, pos="long")
tp = take_profit(price=price, percent=2, pos="long")

order = proxy.long(symbol=symbol, type=type, amount=amount, price=price, sl=sl, tp=tp) # TP and SL

# Market Long
type = "market"
sl = stop_loss(price=price, percent=1, pos="long")

order = proxy.long(symbol=symbol, type=type, amount=amount, sl=sl) # No TP

# Limit Short
price = proxy.price(symbol=symbol)
tp = take_profit(price=price, percent=2, pos="short") # 2% below current price
type = "limit"
price = 100000

order = proxy.short(symbol=symbol, type=type, amount=amount, price=price, tp=tp) # No SL

# Market Short
type = "market"

order = proxy.short(symbol=symbol, type=type, amount=amount) # No TP or SL
```

## OrderClient API
---
- Allows for interaction with order
- edit, close, and retry are only allowed for limit orders
- This API does not provide much use for market orders since it is automatically filled
- Works with both spot and future markets
```
# Place limit order
type = 'limit'
symbol = proxy.symbol(base='BTC', quote='USD', code='spot')

price = proxy.price(symbol=symbol) - 0.1 # Price to place limit order at
usdt_bal = proxy.balance(currency="USDT", code="spot")
amount = usdt_to_crypto(usdt_balance=usdt_bal, price=price, percent=90) # Amount to purchase

order = proxy.buy(symbol=symbol, type=type, amount=amount, price=price) # Returns OrderClient

# Turn logging on/off
order.verbose()
order.silent()

# Output all order data (also provides accurate params for query())
print(order)

# Query order data
print(order.query(request='price'))

# Check order state
print(order.pending())

# Edit order amount and price
price = 1001
usdt_bal = proxy.balance(currency="USDT", code="spot")
amount = usdt_to_crypto(usdt_balance=usdt_bal, price=price, percent=90)
order.edit(amount=amount, price=price)
print(order)

# Edit order sl and tp for long/short order
type = "limit"
amount = 1
price = 9000
sl = stop_loss(price=price, percent=1, pos="long")
tp = take_profit(price=price, percent=2, pos="long")
order = proxy.long(symbol, type, amount, price, sl, tp)
order.verbose()

price = 9001
amount = 2
sl_percent = 2
tp_percent = 3
order.edit(amount=amount, price=price, sl_percent=3, tp_percent=4) # Automatically calls stop_loss and take_profit

# Check if order was filled
print(order.closed())

# Cancel order
order.cancel()
print(order.canceled())

# Ensure order is in orderbook
if not order.pending():
  if order.retry(price=price): # Default attempts to retry at current ask price
    # Order placed in orderbook
    print(order)

# Ensure order is filled
if order.close(retry=True, wait=20, tries=5): # Attempts to fill order at current ask price
  # After waiting 20 seconds for each try
  # the order is filled
  print(order.closed())
```

## PositionClient API
---
- Allows for interaction with position
- Works only on future markets
```
# Place limit order
symbol = proxy.symbol(base="ETH", quote="USD", code="future")
amount = 2 # Contracts
type = "limit"
price = proxy.price(symbol=symbol) - 0.01
order = proxy.long(symbol=symbol, type=type, amount=amount, price=price)

# Try to close order within 1 minute at current ask price
if order.close(retry=True, wait=10, tries=6):
  # Retrieve position
  position = proxy.position(symbol=symbol)

  # Turn logging on/off
  position.verbose()
  position.silent()

  # Output all position data (also provides accurate params for query())
  print(position)

  # Query position data
  print(position.query(request='contracts'))

  # Close *n* contracts
  position.close(1)
  print(position.query('contracts') == 1)

  # Close all contracts
  position.close(all=True)

  # Check state
  print(position.closed())
```

## Test

- Runs the tests on the PhemexBoy module
- Will require .env file with *KEY={API_KEY}* and *SECRET={API_SECRET}*
- Does test auth methods which will require funds in both spot and future accounts

```
make test-client: General unit tests

make test-pub: Test PublicClient

make test-auth: Test AuthClient

make test-proxy: Test Proxy

make test-proxy-auth: Test Proxy AuthClient

make test-proxy-public: Test Proxy PublicClient

make test-order-and-position: Test OrderClient and PositionClient

make test-spot-trade: Test trade example

make test-spot: Test OrderClient

make test-future: Test PositionClient

make test-future-trade: Test trade example

make test-order-edit-update: Test order edit with sl/tp
```
