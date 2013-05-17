# -*- encoding=utf-8
'''
    货币表达式基础库
'''

_CURRENCY_PROVIDER = None

def currency_provider():
    return _CURRENCY_PROVIDER

def set_currency_provider(provider):
    global _CURRENCY_PROVIDER
    _CURRENCY_PROVIDER = provider

def default_currency():
    return currency_provider().get_default()

def set_default_currency(code):
    global _CURRENCY_PROVIDER
    _CURRENCY_PROVIDER['XXX'] =  _CURRENCY_PROVIDER[code]


class OperatorError(Exception):
    pass

class Expression(object):

    operation = None

    def reduce(self, bank, to):
        raise AttributeError("Not yet implemented")

    def __add__(self, y):
        return self.operation.Add(self, y)

    def __sub__(self, y):
        return self.operation.Sub(self, y)

    def __mul__(self, y):
        return self.operation.Mul(self, y)

    def __truediv__(self, y):
        return self.operation.Div(self, y)

    def __rtruediv__(self, x):
        return self.operation.Div(x, self)

    def __rsub__(self, x):
        return self.operation.Add(x, self)

    def __round__(self, ndigits=False):
        return self.operation.Round(self, ndigits)

    __div__ = __truediv__
    __rdiv__ = __rtruediv__
    __radd__ = __add__

    __iadd__ = __add__
    __isub__ = __sub__
    __imul__ = __mul__
    __itruediv__ = __truediv__

    #__mod__
    #__divmod__
