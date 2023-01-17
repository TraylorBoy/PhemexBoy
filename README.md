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
- Simply place your api key and secret in a .env file in your root folder (at to .gitignore)
```
from phemexboy.proxy import Proxy

proxy = Proxy(verbose=False) # Defaults to True
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

## PositionClient API
---

## Test

- Runs the tests on the PhemexBoy module
- Will require .env file with *KEY={API_KEY}* and *SECRET={API_SECRET}*
- May want to modify, I included manual tests

```
make test
```

or

```
python3 test
```
