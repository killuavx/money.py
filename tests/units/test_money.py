# -*- encoding=utf-8
'''
File: test_money.py
Author: Killua.VX <killua.vx@gmail.com>
Date: 2013-04-18 21:13
Description:
'''
import sys
from os.path import dirname, abspath
cur_dir = dirname(dirname(dirname(abspath(__file__))))
sys.path.append(cur_dir)
import unittest
from unittest.mock import MagicMock
from decimal import Decimal
from money import operations
from money.base import Expression, OperatorError
from money.factory import MoneyFactory as RawMoneyFactory
from money.core import Bank, Money
from money.currencies import CURRENCY


def MoneyFactory(ftype=1):
    factory = RawMoneyFactory(ftype=ftype)
    # the load_exchange_rates of through webservices or databases
    factory.load_exchange_rates = MagicMock(return_value=[])
    return factory

class TestMoney(unittest.TestCase):

    def setUp(self):
        self.factory = MoneyFactory()
        self.bank = self.factory.bank()
        self.bank.add_rate("CHF", "USD", 2)
        self.bank.add_rate("CNY", "USD", 6)

    def test_bank_load_exchange_rates(self):
        self.assertTrue(self.factory.load_exchange_rates.called)

    def test_money_factory(self):
        factory = self.factory
        five = factory.dollar(5)
        self.assertEqual(factory.dollar(5), five)

    def test_simple_equality(self):
        factory = self.factory

        self.assertEqual(factory.dollar(10), factory.dollar(10))
        self.assertNotEqual(factory.dollar(10), factory.dollar(5))

        self.assertNotEqual(factory.franc(10) , factory.franc(1))
        with self.assertRaisesRegexp(TypeError, "Cannot compare Money with different currencies"):
            factory.franc(10) == factory.dollar(10)

    def test_create_bank(self):
        self.bank.add_rate("CHF", "USD", 2)
        self.bank.add_rate("USD", "CHF", 1/2)
        self.bank.add_rate("USD", "CNY", round(1/6, 2))
        self.assertEqual(2, self.bank.rate("CHF", "USD"))
        self.assertEqual(6, self.bank.rate("CNY", "USD"))
        self.assertEqual(Decimal(.5), self.bank.rate("USD", "CHF"))
        self.assertEqual(Decimal(str(.17)), self.bank.rate("USD", "CNY"))

    def test_money_equality_with_bank(self):
        factory = self.factory
        bank = self.bank
        bank.add_rate("USD", "CHF", 1 / 2)

        self.assertEqual(factory.dollar(10), bank.reduce(factory.dollar(10), "USD"))
        self.assertNotEqual( factory.dollar(11) , bank.reduce(factory.dollar(5), "USD"))
        self.assertEqual(factory.dollar(10), bank.reduce(factory.franc(20), "USD"))
        self.assertNotEqual(factory.dollar(10), bank.reduce(factory.franc(21), "USD"))
        self.assertEqual(factory.franc(10), bank.reduce(factory.franc(10), "CHF"))
        self.assertNotEqual(factory.dollar(10), bank.reduce(factory.yuan(70), "USD"))
        self.assertEqual(factory.dollar(10), bank.reduce(factory.yuan(60), "USD"))
        with self.assertRaisesRegexp(TypeError, "Cannot compare Money with different currencies"):
            factory.dollar(10) != bank.reduce(factory.dollar(10), "CHF")

        with self.assertRaisesRegexp(TypeError, "Cannot compare Money with different currencies"):
            factory.franc(10) != bank.reduce(factory.franc(10), "USD")

        with self.assertRaisesRegexp(TypeError,  "Cannot compare Money with different currencies"):
            factory.dollar(10) != bank.reduce(factory.yuan(60), "CNY")

    def test_sample_multiplication(self):
        factory = self.factory
        bank = self.bank
        five = factory.dollar(5)

        self.assertEqual(factory.dollar(10), bank.reduce(five * 2, "USD"))
        self.assertEqual(factory.dollar(15), bank.reduce(five * 3, "USD"))

    def test_franc_multiplication(self):
        factory = self.factory
        bank = self.bank
        five = factory.franc(5)
        self.assertEqual(factory.franc(10), bank.reduce(five * 2, "CHF"))
        self.assertEqual(factory.franc(15), bank.reduce(five * 3, "CHF"))

    def test_currency(self):
        factory = self.factory
        self.assertEqual("USD", factory.dollar(10).currency)
        self.assertEqual("CHF", factory.franc(10).currency)
        self.assertEqual("CNY", factory.yuan(10).currency)

    def test_plus_return_sum(self):
        factory = self.factory
        five = factory.dollar(5)
        expr = operations.Add(five, five)
        self.assertEqual(expr.left, five)
        self.assertEqual(expr.right, five)
        self.assertIsNot(Money, type(expr))
        self.assertIsInstance(expr, Expression)

    def test_simple_addition(self):
        factory = self.factory
        expr = factory.dollar(5) + factory.dollar(5)
        bank = Bank()
        reduced = bank.reduce(expr, "USD")
        self.assertEqual(factory.dollar(10), reduced)

    def test_mixed_addition(self):
        factory = self.factory
        expr2 = factory.dollar(5) + factory.franc(10)
        bank = Bank()
        reduced2 = bank.reduce(expr2, "USD")
        self.assertEqual(factory.dollar(10), reduced2)

    def test_multiplication_with_expression(self):
        factory = self.factory

        with self.assertRaises(OperatorError):
            factory.dollar(5) * int
        with self.assertRaises(OperatorError):
            factory.dollar(10) * factory.franc(2)
        with self.assertRaises(OperatorError):
            (factory.dollar(3) + factory.franc(2)) * "a"
        with self.assertRaises(OperatorError):
            (factory.dollar(10) - factory.franc(2)) * "a"

        res = factory.dollar(5) * 2
        bank = Bank()
        reduced = bank.reduce(res, "USD")
        self.assertEqual(factory.dollar(10), reduced)

        res = (factory.dollar(2) + factory.franc(8)) * 2
        bank = Bank()
        reduced = bank.reduce(res, "USD")
        self.assertEqual(factory.dollar(12), reduced)

        res = (factory.dollar(10) - factory.franc(4)) * 2
        reduced = bank.reduce(res, "USD")
        self.assertEqual(factory.dollar(16), reduced)

        res2 = factory.dollar(5) * 0
        reduced = bank.reduce(res2, "USD")
        self.assertEqual(factory.dollar(0), reduced)

    def test_divplication_with_expression(self):
        factory = self.factory

        with self.assertRaises(OperatorError):
            factory.dollar(5) / "aadf"
        with self.assertRaises(OperatorError):
            factory.dollar(10) / factory.franc(2)
        with self.assertRaises(OperatorError):
            (factory.dollar(3) + factory.franc(2)) / "a"
        with self.assertRaises(OperatorError):
            (factory.dollar(10) - factory.franc(2)) / "bcd"

        res = factory.dollar(5) - factory.franc(10)
        bank = Bank()
        bank.add_rate("CHF", "USD", 2)
        reduced = bank.reduce(res, "USD")
        self.assertEqual(factory.dollar(0), reduced)

        res2 = factory.dollar(5) - factory.dollar(5)
        reduced = bank.reduce(res2, "USD")
        self.assertEqual(factory.dollar(0), reduced)

    def test_multiplication_with_operations_MulClass(self):
        factory = self.factory

        with self.assertRaises(OperatorError):
            multi = factory.dollar(20) * "a"
        with self.assertRaises(OperatorError):
            multi = factory.dollar(20) * factory.franc(1)

        multi = operations.Mul(factory.dollar(10), 10)
        self.assertEqual(factory.dollar(100), self.bank.reduce(multi, "USD"))

        res = operations.Mul(factory.dollar(10),  2) + factory.franc(10)
        self.assertEqual(factory.dollar(25), self.bank.reduce(res, "USD"))

    def test_divplication_with_operations_DivClass(self):
        factory = self.factory

        with self.assertRaises(OperatorError):
            div = operations.Div(factory.dollar(20), "a")
        with self.assertRaises(OperatorError):
            div = operations.Div(factory.dollar(20), factory.dollar(1))

        div = operations.Div(factory.dollar(20), 10)
        self.assertEqual(factory.dollar(2), self.bank.reduce(div, "USD"))

        d20 = factory.dollar(20)
        div = d20 / 2 - factory.franc(10)
        self.assertEqual(factory.dollar(5), self.bank.reduce(div, "USD"))

    def test_multiplication_with_operations_MulClass_and_Other_Operation(self):
        factory = self.factory

        res = (factory.dollar(10) + factory.franc(10) + factory.yuan(12)) /2
        d = self.bank.reduce( res , "USD" )
        self.assertEqual( factory.dollar(8.5), d)

        # 2.5 + 1.75 = 4.25
        res = (factory.dollar(10) - factory.franc(10) ) /2 + (factory.yuan(12) + factory.dollar(5) ) /4
        d = self.bank.reduce(res, "USD")
        self.assertEqual( factory.dollar(4.25), d)

class TestCurrency(unittest.TestCase):

    def test_strformat(self):
        f = MoneyFactory()
        yuan300 = f.yuan(300)
        self.assertEqual( u"¥300", yuan300.strformat())

        dollar500_1 = f.dollar(500.1)
        self.assertEqual( u"$500.1", dollar500_1.strformat())

    def test_currency_equalto_currencycode(self):
        currencyUSD = CURRENCY["USD"]
        currencyCHF = CURRENCY["CHF"]
        currencyCNY = CURRENCY["CNY"]
        self.assertTrue( currencyUSD == "USD" )
        self.assertTrue( "USD" == currencyUSD)
        self.assertEqual( "USD", currencyUSD)
        self.assertEqual(currencyUSD, "USD")

        self.assertEqual( "CHF", currencyCHF)
        self.assertEqual(currencyCHF, "CHF")

        self.assertEqual( "CNY", currencyCNY)
        self.assertEqual(currencyCNY, "CNY")


from money.factory.base import load_exchange_rate

class TestLoadExchangeRates(unittest.TestCase):

    def test_load_exchange_rate_from_yahoo(self):
        #rate = load_exchange_rate("USD", "CHY")
        #self.assertIsNotNone(rate)
        pass

