# -*- encoding=utf-8
'''
Default factory
    完全OO的货币四则运算，运算结果返回Composite模式的算术运算式对象
    rate:
        CNY:USD = 6:1
        CHF:USD = 2:1

    10 USD + 5 USD => <Money 15 USD>
    10 USD * 2     => <Money 20 USD>
    60 CNY + 5 USD => <Sum <Money 50 CNY> + <Money 5 USD>>
    (12 CNY + 5 USD) * 2 => <Multi <Sum <Money 12 CNY> + <IMoney 5 USD>> * 2>
    (( 50 CHF - 5 USD ) / 2 + 6 CNY ) * 4 => <Multi <Sum <Div
                                                        <Minus <Money 50 CHF> - <Money 5 USD>> / 2
                                                      > + <Money 6 CNY>
                                                    > * 4
                                                  >
'''

from decimal import Decimal
from money.base import Expression
from money.factory.base import FactoryBase
from money import operations
from money.operations import Operation


class NormalMoneyFactory(FactoryBase):

    @classmethod
    def init(cls):
        Operation.Add = operations.Add
        Operation.Sub = operations.Sub
        Operation.Mul = operations.Mul
        Operation.Div = operations.Div
        Operation.Round = operations.Round
        Expression.operation = Operation

    @classmethod
    def load_exchange_rates(self):
        return []
