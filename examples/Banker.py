from neopapi.shops import Bank
from neopapi.core import Time
from neopapi.shops.Exceptions import BankException
import logging

logger = logging.getLogger(__name__)

def  run():
    try:
        logger.info('Trying to collect interest')
        Bank.collect_interest()
        logger.info('Collected interest for today')
    except BankException:
        logger.info('Interest was already collected today')
    return Time.NST_tomorrow()