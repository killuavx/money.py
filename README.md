# Money.py
## Overview 概览

**Money.py**是一个国际货币包。 你可以用在自己的项目中方便地进行
相同货币间的比较, 不同货币转换以及的四则运算进而将运算表达式转换最终的货币。

## Install 安装

###安装之前的测试

项目使用 *unittest* 做单元测试, 配合 *nose* + *coverage* 做集成测试, 
功能测试使用 *behave* .

*nix系统下采用以下方式完成单元测试和功能测试:

```
$ cd tests
$ make test
```

你也可以只做单元测试或只做功能测试:

```
$ cd tests
$ # for unitttest
$ make unit

$ # for feature test
$ make bdd
```

如果你在windows下开发, 首先你得把已经安装的behave和nosetests添加到PATH上,
然后执行以下命令来做单元测试, 以及功能测试

```
$ cd tests
$ nosetests units/*

$ behave --lang=zh-CN features/*.zh-CN.feature
```

测试并不是必须的, 不过我强烈建议你在使用之前完整地执行一遍单元测试和功能测试, 
以确保在你的环境下能够正常使用.

###正式安装

```
$ python setup.py build
$ python setup.py install
```

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

## Thanks 致谢

Thanks to s3x3y1 <s3x3y1@gmail.com>  [python-money][21] for the class Currnecy and currencies.py.
    
[21]: https://code.google.com/p/python-money/ "python-money"

## TODO 代办列表

####2013-05-01

#####新增项目文档

在下一个版本中，将增加项目文档，位于docs目录下，包含以下类型文档：

1. *design.model.md* 详细设计文档，解析代码整体结构、算法流程
2. *maintain.md* 维护文档，记录开发过程中的备忘，测试信息，项目指标项
3. *anlysis.model.md* 概要设计文档，整体概述项目功能、模块
4. *money.vpp* UML设计图，Visual Paradigm for UML

#####已知缺陷:

1. `money.core.Money.__round__`, [Floating Point Arithmetic: Issues and Limitations](http://docs.python.org/3.3/tutorial/floatingpoint.html)

	计算机的浮点数运算一直存在精度误差问题, 在python3.3中你可以看到如下结果

	```
	>>> sum(0.1 for i in range(0,8))
	0.7999999999999999
	```
	
	与之相关的问题, 四舍五入的处理同样存在不可预知的误差,
	以下情况在python3.3出现, 在python2.7.2则没有这个问题
	
	```
	>>> round(0.5)
	0
	>>> round(1.5)
	2
	>>> round(2.5)
	2
	>>> round(3.5)
	4
	```

	针对这种问题, 通常我的做法是在各项运算过程中,
	将运算两方浮点向右移位若干位, 再计算操作, 最后结果向左移位若干位,
	维持原来精度无误
	
	```
	>>> sum( 0.1*10 for i in range(0,8)) / 10
	0.8
	```

	或者是将浮点抽象成含有整数、小数属性的类形式表示, 两数均以整数形式存储在该类里，
	小数点左右两则数值分别与另外的操作数运算, 过程中的进退位, 分别反映在整数和小数属性上,
	最终输出的结果再将整数和小数属性合并显示.
	
	不过这两种方式都不怎么优雅.

2. `money.operations.Round`, 货币间转换的四舍五入处理问题
	
	在以下汇率背景情况下
			
	```
	>>> from money.factory import MoneyFactory
	>>> factory = MoneyFactory()
	>>> bank = factory.bank()
	>>> bank.add_rate('USD', 'CHF', '0.9424')
	>>> bank.add_rate('USD', 'CNY', '6.1673')
	```

	*场景1*: 如美元和人民币等其他第三方货币进行交易, 最终以美元结算,
	但除美元以外的货币结算, 会出现中间转换过程出现小数点后多于2位的情况:
	
	``` 
	10 USD + 10 CHF + 150 RMB ==> 10 USD + 9.424 USD + 24.321826407017657 USD 
	==> 43.748826407017657 USD 
	==> 43.75 USD
	```

	*场景2*: 现实交易过程中, 货币间转换都会做小数点后2位的四舍五入取舍:
	
	```
	10 USD + 10 CHF + 150 RMB ==> 10 USD + 9.424 USD + 24.321826407017657 USD 
	==> 10 USD + 9.42 USD + 24.32 USD 
	==> 43.74 USD
	```
	
	因此我们会看到以下两种处理方式，两次计算的结果不同

	```
	>>> # 场景1
	>>> d10 = factory.dollar(10)
	>>> f10 = factory.franc(10)
	>>> y150 = factory.yuan(150)
	>>> round(bank.reduce(d10 + f10 + y150, 'USD'), 2)
	>>> 43.75 USD
	>>>
	>>> # 场景2 
	>>> bank.reduce( round(d10 + f10 + y150, 2), 'USD'))
	>>> 43.74 USD
	```
	
	问题就是应不应该把现实场景的"货币兑换中间结果将取舍后再汇总"业务带进来?
	 
	如果不带进来, 保留那么高的精度没有实际的意义, 反而造成业务人员的误解;
	
	如果带进来, 就会产生设计上的问题, 货币计算受业务场景影响,与业务场景耦合起来, 违反SRP.

##Change Log 变更日志

### `0.8.0` 2013-05-05 

完成基本货币操作:
 
1. 创建多种货币, 格式化输出货币 
2. 不同货币间的兑换 
3. 不同货币的四则运算, 最终兑换成指定货币
 
#### News

1. 完善README.md文档, 通过`make readme`合并文档
2. 增加[DEVELOPMENT.md](DEVELOPMENT.md)文档，记录开发笔记

#### Fixes

1. `money.factory.base.FactoryBase`方法bank内，使用错误的拼写调用Bank.add_rate
 
#### Important Notes

Money.py目前只支持`python3`或以上版本，尚在*开发阶段*

