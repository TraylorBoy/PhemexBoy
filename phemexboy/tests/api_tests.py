"""Tests the PhemexBoy API Module"""

from phemexboy.api.public import PublicClient
from phemexboy.interfaces.public_interface import PublicClientInterface

from phemexboy.api.spot import SpotClient
from phemexboy.interfaces.spot_interface import SpotClientInterface

from phemexboy.api.order import OrderClient
from phemexboy.interfaces.order_interface import OrderClientInterface

from phemexboy.api.future import FutureClient
from phemexboy.interfaces.future_interface import FutureClientInterface


def test_public():
    pub_client = PublicClient()

    init_test = isinstance(pub_client, PublicClientInterface)
    codes_test = "future" in pub_client.codes() and "spot" in pub_client.codes()
    symbol_test = (
        pub_client.symbol(base="BTC", quote="USD", code="spot") == "sBTCUSDT"
        and pub_client.symbol(base="BTC", quote="USD", code="future") == "BTC/USD:USD"
    )
    timeframes_test = "1m" in pub_client.timeframes()

    symbol = pub_client.symbol(base="BTC", quote="USD", code="future")
    future_price = pub_client.price(symbol=symbol)
    symbol = pub_client.symbol(base="BTC", quote="USD", code="spot")
    spot_price = pub_client.price(symbol=symbol)
    price_test = spot_price > 0 and future_price > 0

    tf = "1m"
    since = "2020-12-01"
    limit = 500
    ohlcv = pub_client.ohlcv(symbol=symbol, tf=tf, since=since, limit=limit)
    ohlcv_test = len(ohlcv) > 0

    return (
        init_test
        and codes_test
        and symbol_test
        and timeframes_test
        and price_test
        and ohlcv_test
    )


def test_spot_and_order():
    # Test Spot Init
    client = SpotClient()
    init_test = isinstance(client, SpotClientInterface)

    # Test balance
    bal_test = client.balance(of="USDT") >= 0

    # Test limit buy
    from phemexboy.helpers.conversions import usdt_to_crypto

    pub_client = PublicClient()
    symbol = pub_client.symbol(base="BTC", quote="USD", code="spot")
    type = "limit"
    bal = client.balance(of="USDT")
    price = 1000
    amount = usdt_to_crypto(usdt_balance=bal, price=price, percent=50)
    order_data = client.buy(symbol=symbol, type=type, amount=amount, price=price)
    limit_buy_order_test = len(order_data) > 0

    # Test Order Init
    order = OrderClient(order_data, client)
    order_init_test = isinstance(order, OrderClientInterface)

    # Test _str__
    print(order)

    # Test query
    req = order.query("symbol")
    query_test = req == "sBTCUSDT"

    # Test edit
    price = 2000
    amount = usdt_to_crypto(usdt_balance=bal, price=price, percent=100)
    order.edit(amount=amount, price=price)
    edit_test = order.query("price") == 2000

    # Test cancel
    cancel_test = order.cancel()

    # Test market buy
    symbol = pub_client.symbol(base="BTC", quote="USD", code="spot")
    type = "market"
    price = pub_client.price(symbol)
    amount = usdt_to_crypto(usdt_balance=bal, price=price, percent=50)
    order_data = client.buy(symbol, type, amount)
    market_buy_order_test = len(order_data) > 0

    # Test limit sell
    symbol = pub_client.symbol(base="BTC", quote="USD", code="spot")
    type = "limit"
    price = 100000
    amount = client.balance(of="BTC")
    order_data = client.sell(symbol=symbol, type=type, amount=amount, price=price)
    limit_sell_order_test = len(order_data) > 0
    order = OrderClient(order_data, client)
    print(order)
    price = 90000
    order.edit(amount, price)
    order.cancel()

    # Test market sell
    symbol = pub_client.symbol(base="BTC", quote="USD", code="spot")
    type = "market"
    amount = client.balance(of="BTC")
    order_data = client.sell(symbol, type, amount)
    market_sell_order_test = len(order_data) > 0

    return (
        init_test
        and bal_test
        and limit_buy_order_test
        and order_init_test
        and query_test
        and edit_test
        and cancel_test
        and market_buy_order_test
        and limit_sell_order_test
        and market_sell_order_test
    )


def test_future_and_position():
    # Test init
    client = FutureClient()
    init_test = isinstance(client, FutureClientInterface)

    # Test balance
    bal = client.balance()
    bal_test = bal >= 0

    return init_test and bal_test


def test_all():
    test_codes = {
        "public": test_public,
        "spot": test_spot_and_order,
        "future": test_future_and_position,
    }
    print(f"Test Codes: {list(test_codes.keys())}")
    tests = input("Enter test code(s) separated by commas (ex. public, spot, etc...): ")
    tests = tests.split(",")

    results = []
    for test in tests:
        results.append({"test": test, "result": test_codes[test]()})

    all_passed = True
    for result in results:
        outcome = result["result"]

        if not outcome:
            all_passed = False
            print(f'\n{result["test"]} did not pass\n')

    return all_passed
