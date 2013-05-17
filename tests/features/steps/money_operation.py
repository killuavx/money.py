# -*- encoding=utf-8
from behave import *
from behave.matchers import register_type

from money.factory import MoneyFactory
from money.base import OperatorError
from decimal import Decimal

def str2Decimal(s):
    try:
        return Decimal(s)
    except:
        return None

def str2Money(s, factory_type):
    amount, currency = s.split(" ")
    factory = MoneyFactory(int(factory_type))
    money = None
    if currency == "USD":
       money = factory.dollar(amount)
    elif currency == "CHF":
       money = factory.franc(amount)
    elif currency == "CNY":
       money = factory.yuan(amount)
    else:
        raise Exception( currency + " not in testcase")

    return money

def get_money(s, ft=1):
    i = str2Decimal(s)

    if i == None:
        return str2Money(s, ft)
    return i

@Given('开始准备货币工厂"{factory_type}"')
def step(context, factory_type):
    factory = MoneyFactory(int(factory_type))
    context.response = {}
    context.response['ft'] = factory_type
    context.response['factory'] = factory

@Given('银行录入汇率表')
def step(context):
    bank = context.response['factory'].bank()
    for row in context.table.rows:
        bank.add_rate( row['src'], row['dst'], float(row['rate']))
    context.response['bank'] = bank

@When('有货币"{m1}" 和货币"{m2}"')
def step(context, m1, m2):
    ft = context.response['ft']
    context.response['calc'] = {'x': get_money(m1, ft), 'y': get_money(m2, ft) }

@When('兑换货币"{m}"为"{currency}"')
def step(context, m, currency):
    money = get_money(m, context.response['ft'])
    bank = context.response['bank']
    try:
        context.response['res'] = bank.reduce(money, currency)
    except Exception as e:
        context.response['e'] = e

def operateMoney(m1, op, m2):
    if op == '+':
        res = m1 + m2
    elif op == '-':
        res = m1 - m2
    elif op == '*':
        res = m1 * m2
    elif op == '/':
        res = m1 / m2
    else:
        raise Exception("Not suppport operation: " + op)
    return res


@When('计算货币"{m1}", 操作"{op}"另一操作数"{m2}"')
@When('计算出结果 货币"{m1}", 操作"{op}"另一操作数"{m2}"')
def step(context, m1, op, m2):
    ft = context.response['ft']
    m1, m2 =  get_money(m1, ft),  get_money(m2, ft)
    context.response['calc'] = {'x': m1, 'y': m2}
    try:
        context.response['res'] = operateMoney(m1, op, m2)
    except OperatorError as e:
        context.response['e'] =e

@then('最终结果输出为"{result}"')
def step(context, result):
    assert str(context.response['res']) == result, str(context.response['res'])

@Then('兑换为美元, 最终结果输出为"{result}"')
def step(context, result):
    result = get_money(result, context.response['ft'])
    res = context.response['res']
    bank = context.response['bank']
    money = bank.reduce(res, "USD")
    assert money.currency == result.currency, money.currency
    assert money == result, str(money) + " == " + str(result)


#from math import floor
import math
import builtins
@when('"{money}" 执行函数"{func}"')
def step(context, money, func):
    ft = context.response['ft']
    money = get_money(money, ft)

    try:
        f = getattr(math, func)
    except:
        f = getattr(builtins, func)
    finally:
        pass
    context.response['res'] = f(money)


@Then('得到错误结果"{ename}"')
def step(context, ename):
    e = context.response['e']
    assert type(e).__name__ == ename


def compareMoney(m1, op, m2):
    res = None
    if op == '==':
        res = m1 == m2
    elif op == '!=':
        res = m1 != m2
    elif op == '>':
        res = m1 > m2
    elif op == '>=':
        res = m1 >= m2
    elif op == '<':
        res = m1 < m2
    elif op == '<=':
        res = m1 <= m2
    else:
        raise Exception("Not suppport operation: " + op)
    return res


@Then('"{op}"比较结果正确')
def step(context, op):
    m1, m2 = context.response['calc']['x'], context.response['calc']['y']
    assert compareMoney(m1, op, m2)

@Then('"{op}"比较结果异常')
def step(context, op):
    m1, m2 = context.response['calc']['x'], context.response['calc']['y']
    _e = None
    try:
        res = compareMoney(m1, op, m2)
    except TypeError as e:
        print(e)
        _e = e
    assert _e


import re
@Then('捕获异常错误"{ename}", 信息显示"{msg}"')
def step(context, ename, msg):
    e = context.response['e']
    assert ename == type(e).__name__, e
    assert msg == str(e)

@Then('保留2位小数四舍五入约简')
def step(context):
    res = context.response['res']
    context.response['res'] = round(res, 2)

