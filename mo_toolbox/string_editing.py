from datetime import datetime

import pandas
from pytz import timezone


def rfn(number: int | float | str, k_divider: str = '.', f_divider: str = ',', round_float: int = 2) -> str:
    """
    Reformat Number. Creates . 1000 divider, and round floating point numbers
    :param number: int | float | str
    :param k_divider: divider for thousands
    :param f_divider: divider for floating points
    :param round_float: number of floating points
    :return: str
    """
    numbercheck = number
    #  Check if String is a number and converting it to a float
    if isinstance(numbercheck, str):
        if not numbercheck.replace('.', '', 1).isnumeric():
            raise ValueError(f'{number} ist keine Zahl')
    number = float(number)

    #  Inserting thousandseperators and replacing it with wanted k_divider
    num_str = f'{number:,.{round_float}f}'.replace(',', k_divider)

    #  Replacing floating point divider
    if len(num_str) > 2 and round_float > 0:
        if num_str[-1 - round_float] == '.':
            num_str = num_str[::-1].replace('.', f_divider, 1)[::-1]
    return num_str


def convert_utc_to_cet(timestring: pandas.Timestamp, _format='%d.%m.%Y') -> str:
    """
    Zeitangaben sind in der GDB als Datetimefelder in UTC gespeichert.
    Das führt dazu, dass Geburtsdaten die in CET erfasst sind falsch angezeigt werden.
    Eingabe 01.01.2022 -> So wird es gespeichert 2021-12-31T23:00:00+00:00 --> das wuerde ausgegeben 31.12.2021
    """
    try:
        timestring = pandas.Timestamp(timestring)
        if isinstance(timestring, pandas.Timestamp):
            return timestring.astimezone('Europe/Helsinki').strftime(_format)

    except ValueError:
        return ''
