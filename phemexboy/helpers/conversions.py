"""Asset conversions"""


def usdt_to_crypto(usdt_balance, price, percent):
    """Converts USDT quote currency to base currency based on percentage

    Args:
        usdt_balance (float): Amount of USDT currently in exchange wallet
        price (float): Current price of crypto you want to convert to
        percent (int): Percentage of USDT balance to convert

    Returns:
        Float: Converted crypto amount
    """
    amount = (usdt_balance / price) * (percent / 100)
    return round(amount, 5)
