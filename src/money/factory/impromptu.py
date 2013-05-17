# -*- encoding=utf-8
'''
Immediacte Expression factory
    货币即席运算，跨货币加减运算后，再进行乘/除法分配律算术运算式
    rate:
        CNY:USD = 6:1
        CHF:USD = 2:1

    10 USD + 5 USD => <IMoney 15 USD>
    10 USD * 2     => <IMoney 20 USD>
    60 CNY + 5 USD => <DAdd <IMoney 50 CNY> + <IMoney 5 USD>>
    (12 CNY + 5 USD) * 2 => <DAdd <IMoney 24 CNY> + <IMoney 10 USD>>
    (( 50 CHF - 5 USD ) / 2 + 6 CNY ) * 4 => <DAdd <DSub <Money 100 CHF> - <Money 10 USD>> + <Money 24 CNY>>
'''

from decimal import Decimal
from money.core import Money as BaseMoney
from money.base import Expression, OperatorError
from money.factory.base import FactoryBase
from money import operations
from money.operations import Operation

__all__ = ['ImpromptuOperateMoneyFactory']

class Money(BaseMoney):
    """ Impromptu Operate Money """

    def reduce(self, bank, to):
        if self.amount==0: return Money(0, to)
        rate = bank.rate(self.currency, to)
        return Money(self.amount / rate, to)

    def __mul__(self, y):
        if type(y) not in (int, float, Decimal):
            raise OperatorError("supported operand only in types int,float"
                " for __mul__ Operator of Money")
        y = Decimal(y)
        return  self.__class__(self.amount * y, self.currency)

    def __truediv__(self, y):
        if type(y) not in (int, float, Decimal):
            raise OperatorError("supported operand only in types int,float"
                " for __turediv__ Operator of Money")
        y = Decimal(y)
        return self.__class__(self.amount / y, self.currency)

    def __rtruediv__(self, x):
        raise OperatorError("supported operand only in types int,float"
                " for __rturediv__ Operator of Money")

    def __add__(self, y):
        if not isinstance(y, Expression):
            raise OperatorError("supported operand only Expression instance"
                " for __add__ Operator of Money")
        elif isinstance(y, BaseMoney) and y.currency == self.currency:
            return self.__class__(self.amount + y.amount, self.currency)
        else:
            return super(Money, self).__add__(y)

    def __sub__(self, y):
        if not isinstance(y, Expression):
            raise OperatorError("supported operand only Expression instance"
                " for __sub__ Operator of Money")
        elif isinstance(y, BaseMoney) and y.currency == self.currency:
            return self.__class__(self.amount - y.amount, self.currency)
        else:
            return super(Money, self).__sub__(y)

    def __repr__(self):
        return "<IMoney(%s %s)>" % (self.amount, self.currency)


class DistributionAdd(operations.Add):

    def reduce(self, bank, to):
        return Money(self.left.reduce(bank, to).amount +
                self.right.reduce(bank, to).amount, currency=to)

    def __mul__(self, y):
        if type(y) not in (int, float, Decimal):
            raise OperatorError("supported operand only in types int,float"
                   " for Mul Operator of Money")
        y = Decimal(str(y))
        return DistributionAdd( self.left * y, self.right * y )

    def __truediv__(self, y):
        if type(y) not in (int, float, Decimal):
            raise OperatorError("supported operand only in types int,float"
                   " for Div Operator of Money")
        y = Decimal(str(y))
        return self.__class__( self.left / y, self.right / y)

    def __str__(self):
        return "(%s + %s)" % (self.left, self.right)

    def __repr__(self):
        return "<DAdd(%s + %s)>" % (repr(self.left), repr(self.right))


class DistributionSub(operations.Sub):

    def reduce(self, bank, to):
        return Money(self.left.reduce(bank, to).amount -
                self.right.reduce(bank, to).amount, currency=to)

    def __mul__(self, y):
        if type(y) not in (int, float, Decimal):
            raise OperatorError("supported operand only in types int,float"
                   " for Mul Operator of Money")
        y = Decimal(str(y))
        return self.__class__( self.left * y , self.right * y )

    def __truediv__(self, y):
        if type(y) not in (int, float, Decimal):
            raise OperatorError("supported operand only in types int,float"
                   " for Div Operator of Money")
        y = Decimal(str(y))
        return self.__class__( self.left / y, self.right / y)

    def __str__(self):
        return "(%s - %s)" % (self.left, self.right)

    def __repr__(self):
        return "<DSub(%s - %s)>" % (repr(self.left), repr(self.right))


class ImpromptuOperateMoneyFactory(FactoryBase):

    Money = Money

    @classmethod
    def init(cls):
        Operation.Add = DistributionAdd
        Operation.Sub = DistributionSub
        Operation.Mul = None
        Operation.Div = None
        Expression.operation = Operation

    @classmethod
    def load_exchange_rates(cls):
        #r1 = {"src":"CNY", "dst":"USD", "rate":Decimal(0.1621)}
        #r2 = {"src":"CHF", "dst":"USD", "rate":Decimal(6.1673)}
        #return [r1, r2]
        return []
