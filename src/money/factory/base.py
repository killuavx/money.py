# -*- encoding=utf-8
"""
    Factory Base
"""


class FactoryBase(object):

    from money.currencies import CURRENCY
    from money.core import Bank, Money

    @classmethod
    def init(cls):
        raise AttributeError("Not yet implemented")

    @classmethod
    def dollar(cls, amount):
        return cls.Money(amount=amount, currency=cls.CURRENCY['USD'])

    @classmethod
    def franc(cls, amount):
        return cls.Money(amount=amount, currency=cls.CURRENCY['CHF'])

    @classmethod
    def yuan(cls, amount):
        return cls.Money(amount=amount, currency=cls.CURRENCY['CNY'])

    @classmethod
    def zero(cls):
        return cls.Money(amount=0, currency=None)

    @classmethod
    def bank(cls):
        rates = cls.load_exchange_rates()
        bank = cls.Bank()
        for r in rates:
            bank.add_rate(r.get('src'), r.get('dst'), r.get('rate'))

        return bank

    @classmethod
    def load_exchange_rates(cls):
        from itertools import product
        c = ["USD", "CHF", "CNY"]
        rates = ({"src": src, "dst": dst} for src, dst in product(c, c) if src != dst)
        res = []
        for r in rates:
            r['rate'] = load_exchange_rate(r['src'], r['dst'])
            res.append(r)
        return res


def load_exchange_rate(src, dst):
    from decimal import Decimal
    from urllib.request import urlopen
    from_currency = src
    kwargs = {'from': str(from_currency), 'to': str(dst)}
    url = 'http://quote.yahoo.com/d/quotes.csv?s=%(from)s%(to)s=X&f=l1&e=.csv'
    response = urlopen(url % kwargs).read()
    try:
        # convert bytes to float
        s = float(response.strip())
        # limit floating point
        exchange_rate = Decimal(str(s))
    except ValueError:
        return None

    return exchange_rate
