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

