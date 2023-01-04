# PhemexBoy
Phemex API Wrapper in Python

## Notes
- All spot symbols begin with a lowercase s and utilize USDT (ex. sBTCUSDT).
- All future symbols are in the following format *BTC/USD:USD, ETH/USD:USD, etc.*
- Use spot symbols for buy and sell and future symbols for long and short
- Spot uses USDT and future uses USD
- Currently future methods only work for USD future account

## Installation
```
pip install phemexboy
```

## Usage
### Instantiate PublicClient
Public methods include:
- price(symbol)
- currencies()
- symbols()
- future_symbols()
- ohlcv(symbol, tf, since)
- timeframes()
- timestamp(date)
```
from phemexboy import PhemexBoy
pub_client = PhemexBoy()
```
### Instantiate AuthClient with API Key and Secret obtained from Phemex
- Use *python-dotenv* package for security
```
import os
from phemexboy import PhemexBoy
from dotenv import load_dotenv

load_dotenv()
client = PhemexBoy(os.getenv("KEY"), os.getenv("SECRET"))
```

### Retrieve all currencies offered on Phemex
```
client.currencies()
```

### Retrieve the price of a specific pairing
```
client.price(symbol='sBTCUSDT') # Spot price
client.price(symbol='BTC/USD:USD') # Future price
```

### Retrieve all spot and future symbols
```
client.symbols() # Spot symbols
client.future_symbols() # Future symbols
```

### Retrieve spot and future balances
- Uses currencies instead of symbols
```
client.balance(of='USDT') # Spot balance
client.balance(of='USD') # Future balance
```

### Convert percent of USDT account into crypto amount
- Used for spot purchases, when selling crypto you do not need to use this method
```
# Buy BTC with 21% of full account
amt = client.usd_converter(symbol='sBTCUSDT', percent=21)
order_id = client.buy(symbol='sBTCUSDT', type='market', amt)
```

### Buy/sell crypto on spot
```
# Limit Buy
amt = client.usd_converter(symbol='sBTCUSDT', percent=100) # Amount to purchase
price = client.price(symbol='sBTCUSDT') # Price to place limit order at
order_id = client.buy(symbol='sBTCUSDT', type='limit', amount=amt, price=price)

# Market Buy
amt = client.usd_converter(symbol='sBTCUSDT', percent=100)
order_id = client.buy(symbol='sBTCUSDT', type='market', amount=amt)

# Limit Sell
amt = client.balance(of='BTC') # Amount to sell
price = client.price(symbol='sBTCUSDT')
order_id = client.sell(symbol='sBTCUSDT', type='limit', amount=amt, price=price)

# Market Sell
amt = client.balance(of='BTC')
order_id = client.sell(symbol='sBTCUSDT', type='market', amount=amt)

# Cancel limit order
resp = client.cancel(id=order_id, symbol='sBTCUSDT')

# Cancel all orders
resp = client.cancel_all(symbol='sBTCUSDT')
```

### Change leverage on future
```
client.leverage(amount=10, symbol='BTC/USD:USD')
```

### Open a long/short position
- Amount is in contracts
- Stoploss (sl) and Takeprofit (tp) are not needed
```
# Limit Long
price = client.price('BTC/USD:USD')
sl = price - (price * 0.01) # 1% from current price
tp = price + (price * 0.02) # 2% above current price
order_id = client.long(symbol='BTC/USD:USD', type='limit', amount=1, price=price, sl=sl, tp=tp)

# Cancel order
client.cancel(id=order_id, symbol='BTC/USD:USD')

# Market Long
order_id = client.long(symbol='BTC/USD:USD', type='market', amount=1)

# Limit Short
price = client.price('BTC/USD:USD')
sl = price + (price * 0.01) # 1% above current price
tp = price - (price * 0.02) # 2% from current price
order_id = client.short(symbol='BTC/USD:USD', type='limit', amount=1, price=price, sl=sl, tp=tp)

# Market Short
order_id = client.short(symbol='BTC/USD:USD', type='market', amount=1)

# Close Position
client.close(symbol='BTC/USD:USD', amount=1)
```

### Check Position Status
```
client.positions(symbol='BTC/USD:USD') # Returns position information
client.in_position(symbol='BTC/USD:USD') # Returns if in a position or not
```

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
