from neopapi.shops import Bank
from neopapi.core import Time
from neopapi.shops.Exceptions import BankException

def  run():
    try:
        Bank.collect_interest()
    except BankException:
        pass
    return Time.NST_tomorrow()