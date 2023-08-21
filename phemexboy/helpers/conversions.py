"""Asset conversions"""

from phemexboy.exceptions import InvalidPositionError


def usdt_to_crypto(usdt_balance: float, price: float, percent: int):
    """Converts USDT quote currency to base currency based on percentage

    Args:
        usdt_balance (float): Amount of USDT currently in exchange wallet
        price (object): Proxy
        percent (int): Percentage of USDT balance to convert

    Returns:
        Float: Converted crypto amount
    """
    amount = (usdt_balance / price) * (percent / 100)
    return amount


def stop_loss(price: float, percent: int, pos: str):
    """Calculate stop loss price

    Args:
        price (float): Limit order price
        percent (int): Percent from price
        pos (str): Position type ('long' or 'short')

    Raises:
        InvalidPositionError: Pos must be either "short" or "long"

    Returns:
        Float: Stop loss price
    """
    if pos == "short":
        return price + (price * (percent / 100))
    elif pos == "long":
        return price - (price * (percent / 100))
    else:
        raise InvalidPositionError('Pos must be either "short" or "long"')


def take_profit(price: float, percent: int, pos: str):
    """Calculate take profit price

    Args:
        price (float): Limit order price
        percent (int): Percent from price
        pos (str): Position type ('long' or 'short')

    Raises:
        InvalidPositionError: Pos must be either "short" or "long"

    Returns:
        Float: Take profit price
    """
    if pos == "short":
        return price - (price * (percent / 100))
    elif pos == "long":
        return price + (price * (percent / 100))
    else:
        raise InvalidPositionError('Pos must be either "short" or "long"')
