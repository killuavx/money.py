# -*- encoding=utf-8
'''
    货币Factory入口
    >>> factory = MoneyFactory(ftype=1)
    >>> bank = factory.bank()
    >>> factory.dollar(10)
    10 USD
'''
def MoneyFactory(ftype=1):
    if ftype is 1:
        from money.factory.default import NormalMoneyFactory
        NormalMoneyFactory.init()
        return NormalMoneyFactory
    else:
        from money.factory.impromptu import ImpromptuOperateMoneyFactory
        ImpromptuOperateMoneyFactory.init()
        return ImpromptuOperateMoneyFactory
