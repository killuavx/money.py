## Usage 使用

### 开始

```
>>> import money.factory import MoneyFactory
>>> factory = MoneyFactory()
>>> dollar10 = factory.dollar(10)
>>> repr(dollar10)
<Money 10 USD>
```

其实更有效地了解项目的技巧是通过该项目的单元测试代码来熟悉, 
详情可以参考tests/test_money，里面提供使用money.py的不同方式。

### 高级应用

money.py 采用工厂模式来实例化货币、以及bank进行货币计算、汇率转换的操作。
相关源码目录如下:

```
money/
	feactory/
		__init__.py
		base.py
		default.py
		impromptu.py
```

`money.factory.base`是作为货币工厂的基类，实现了具体货币类型(USD/CNY)方法。
money.factory.default/impromptu 是具体的工厂模块，default.py是默认货币计算方式，
impromptu.py是即席计算方式，具体说明可见对应模块的说明。

使用`money.factory.MoneyFactory`函数，指定ftype参数1.default，2.improptu使用某
一个工厂。如果你需要自定义自己的计算方式，可以通过新建module，继承重写
money.factory.base.FactoryBase类的方法，来实现诸如Bank装载获取汇率方式、
继承重写money.core.Money类并作为自定义工厂上类的内部类，达到格式化输出货币样式
等操作。

示例如下:

```
class Money(money.core.Money):

	def __str__():
		return "%s%s%s" % (self.currency.prefix, self.amount, self.currency.suffix)

class MyMoneyFactory(FactoryBase):
	Money = Money
	
	@classmethod
	def init(cls):
		# TODO overwrite init
		pass
	
	@classmethod
	def load_exchange_rates(self):
		# TODO load exchange rates from database
		return []
```

不要忘了要在`money.factory.MoneyFactory`函数里为新的工厂类型增加ftype的选项，
这里为MyMoneyFactory选定ftype=3。最后你就可以像这样使用新的工厂整理:

```
>>> import money.factory import MoneyFactory
>>> factory = MoneyFactory(ftype=3)
>>> dollar30 = factory.dollar(30)
>>> print(dollar30)
$30
```

