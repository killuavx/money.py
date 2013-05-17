# -*- encoding=utf-8

VERSION = (0, 8, 0)
__version__ = '.'.join(map(str, VERSION))
__author__ = "Killua.VX"
__contact__ = "killua.vx@gmail.com"
__homepage__ = ""
__docformat__ = "markdown"
__doc__ = 'Money, Currency, many currencies exchange rates library.'
__license__ = 'BSD'

from money.base import set_currency_provider, set_default_currency
from money.core import *
from money.operations import Operation
from money.factory import MoneyFactory
from money.currencies import CURRENCY
set_currency_provider(CURRENCY)
set_default_currency("USD")
