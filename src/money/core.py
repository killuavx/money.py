# -*- encoding=utf-8
from decimal import Decimal
from money.base import Expression, OperatorError, currency_provider

__all__ = [ 'Currency', 'Money', 'Bank' ]


class BaseCurrency(object):

    def __repr__(self):
        return self.code

    def __eq__(self, other):
        if isinstance(other, BaseCurrency) or hasattr(other, 'code'):
            return self.code == other.code
        if isinstance(other, str):
            return self.code == other
        return False #don't know how to compare otherwise

class Currency(BaseCurrency):

    def __init__(self, code="", numeric="999", name="", countries=[],
            prefix=u'', prefix2=u'', suffix=u'', suffix2=u''):
        self.code = code
        self.prefix = prefix
        self.prefix2 = prefix2
        self.suffix = suffix
        self.suffix2 = suffix2
        self.numeric = numeric
        self.name = name
        self.countries = countries

    def strformat(self, amount, toformat="{prefix}{amount}{suffix}"):
        d = {"amount":amount}
        d.update(**self.__dict__)
        return toformat.format(**d)

class MoneyComparisonError(TypeError):

    def __init__(self, other):
        assert not isinstance(other, Money)
        self.other = other

    def __str__(self):
        return "Cannot compare instances of Money and %s" \
               % self.other.__class__.__name__

class DifferentCurrencyMoneyComparisonError(TypeError):

    def __str__(self):
        return "Cannot compare Money with different currencies"

class CurrencyNotExist(Exception):

    def __init__(self, code):
        super(CurrencyDoesNotExist, self).__init__(
            u"No currency with code %s is defined." % code)

class ExchangeRateNotExist(Exception):

    def __init__(self, src, dst):
        super(ExchangeRateNotExist, self).__init__()
        self.src = src
        self.dst = dst

    def __str__(self):
        return 'missing exchanged rate from %s to %s' % (
            str(self.src), str(self.dst))

import math

class Money(Expression):

    CURRENCY = None

    @classmethod
    def factory(cls, amount):
        return cls(amount, currency=cls.CURRENCY)

    _amount = None

    _currency = None

    @property
    def amount(self):
        return self._amount

    @property
    def currency(self):
        return self._currency

    def strformat(self):
        return currency_provider()[str(self.currency)].strformat(self.amount)

    def __init__(self, amount=Decimal('0.0'), currency=None):
        super(Money, self).__init__()
        self._amount = Decimal(str(amount))
        self._currency = currency

    def __bool__(self):
        return self.amount != 0 and self.currency

    def __ceil__(self):
        return self.__class__(math.ceil(self.amount), self.currency)

    def __floor__(self):
        return self.__class__(math.floor(self.amount), self.currency)

    # TODO FIXME
    # Floating Point Arithmetic: Issues and Limitations http://docs.python.org/3.3/tutorial/floatingpoint.html
    def __round__(self, ndigits=False):
        return self.__class__(round(self.amount, ndigits), self.currency)

    def __neg__(self):
        return self.__class__(-abs(self.amount), self.currency)

    def __pos__(self):
        return self.__class__(self.amount, self.currency)

    def __abs__(self):
        return self.__class__(abs(self.amount), self.currency)

    def __int__(self):
        return int(self.amount)

    def __float__(self):
        return float(self.amount)

    # compare operation
    def _check_currency_to_compare(self, other):
        if not isinstance(other, Money):
            raise MoneyComparisonError(other)
        elif self.currency != other.currency:
            raise DifferentCurrencyMoneyComparisonError(other)

    def __eq__(self, other):
        self._check_currency_to_compare(other)
        return self.amount == other.amount

    def __gt__(self, other):
        self._check_currency_to_compare(other)
        return self.amount > other.amount

    def __lt__(self, other):
        self._check_currency_to_compare(other)
        return self.amount < other.amount

    def __ge__(self, other):
        self._check_currency_to_compare(other)
        return self.amount >= other.amount

    def __le__(self, other):
        self._check_currency_to_compare(other)
        return self.amount <= other.amount

    def reduce(self, bank, to):
        if self.amount==0: return Money(0, to)
        rate = bank.rate(self.currency, to)
        return Money(self.amount / rate, to)

    def __str__(self):
        return "%s %s" % (self.amount, self.currency)

    def __repr__(self):
        return "<Money(%s %s)>" % (self.amount, self.currency)


from collections import namedtuple


class Bank(object):

    """
        Pair(src, dst):
            src: str source
            dst: str destination
    """
    Pair = namedtuple("Pair", ["src", "dst"])

    rates = {}

    def rate(self, src, dst):
        """
        @param str src
        @param str dst
        """
        if src == dst:
            return Decimal(1)

        pair = self.Pair(src=str(src), dst=str(dst))
        if pair not in self.rates:
            raise ExchangeRateNotExist(src, dst)
        return self.rates[pair]

    def add_rate(self, src, dst, rate):
        """
        @param str src
        @param str dst
        @param int/float rate
        """
        self.rates[self.Pair(src=str(src), dst=str(dst))] = Decimal(str(rate))

    def reduce(self, expr, to):
        """
        @param Expression expr
        @param str to
        """
        return expr.reduce(self, to)
