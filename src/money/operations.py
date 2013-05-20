# -*- encoding=utf-8
'''
    货币四则运算表达式
'''


from decimal import Decimal
from money.base import Expression, OperatorError
from money.core import Money

__all__ = ['Operation']


class Add(Expression):
    """
        Add(x, y) ==> x * y
    """

    x = None
    y = None

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.y

    def __init__(self, augend, addend):
        """
         @param Expression x
         @param Expression y
        """
        if not isinstance(addend, Expression) or not isinstance(augend, Expression):
            raise OperatorError("supported operand only instance of Expression"
                    " for Sum Operator of Money")
        self.x, self.y = augend, addend

    def reduce(self, bank, to):
        return Money(self.left.reduce(bank, to).amount +
                self.right.reduce(bank, to).amount, currency=to)

    def __str__(self):
        return "(%s + %s)" % (self.x, self.y)

    def __repr__(self):
        return "<Sum(%s + %s)>" % (repr(self.x), repr(self.y))


class Sub(Expression):
    """
        Sub(x, y) ==> x - y
    """

    x = None
    y = None

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.y

    def __init__(self, x, y):
        """
         @param Expression x
         @param Expression y
        """
        if not isinstance(x, Expression) or not isinstance(y, Expression):
            raise OperatorError("supported operand only instance of Expression"
                   " for Minus Operator of Money")
        self.x, self.y = x, y

    def reduce(self, bank, to):
        return Money(self.left.reduce(bank, to).amount -
                self.right.reduce(bank, to).amount, currency=to)

    def __str__(self):
        return "(%s - %s)" % (self.x, self.y)

    def __repr__(self):
        return "<Minus(%s - %s)>" % (repr(self.x), repr(self.y))


class Mul(Expression):
    """
        Mul(x, y) ==> x * y
    """

    x = None
    y = None

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.y

    def __init__(self, x, y):
        """
         @param Expression x
         @param int,float y
        """
        if type(y) not in (int, float, Decimal):
            raise OperatorError("supported operand only in types int,float"
                   " for Multi Operator of Money")
        y = Decimal(y)
        self.x, self.y = x, y

    def reduce(self, bank, to):
        return Money(self.left.reduce(bank, to).amount * self.right, to)

    def __str__(self):
        return "(%s * %s)" % (self.x, self.y)

    def __repr__(self):
        return "<Multi(%s * %s)>" % (repr(self.x), repr(self.y))


class Div(Expression):
    """
        Div(x, y) ==> x / y
    """

    x = None
    y = None

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.y

    def __init__(self, x, y):
        """
         @param Expression x
         @param int,float y
        """
        if type(y) not in (int, float, Decimal):
            raise OperatorError("supported operand only in types int,float"
                   " for Div Operator of Money")
        y = Decimal(y)
        self.x, self.y = x, y

    def reduce(self, bank, to):
        return Money(self.left.reduce(bank, to).amount / self.right, to)

    def __str__(self):
        return "(%s / %s)" % (self.x, self.y)

    def __repr__(self):
        return "<Div(%s / %s)>" % (repr(self.x), repr(self.y))


class Round(Expression):
    """
        Round(x, y) ==> round(x, y)
    """

    def __init__(self, expr, ndigits=False):
        super(Round, self).__init__()
        self.expr = expr
        self.ndigits = ndigits

    def reduce(self, bank, to):
        money = self.expr.reduce(bank, to)
        return money.__class__(round(money.amount, self.ndigits), money.currency)


class Operation(object):

    Add = Add

    Sub = Sub

    Mul = Mul

    Div = Div

    Round = Round


Expression.operation = Operation
