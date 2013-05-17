功能: 货币运算
	为了 跨货币的运算
	作为 业务开发者, 我需要对货币进行基本的上/下取整,四舍五入,货币比较,货币兑换,四则运算

	@simplify
	场景大纲: 化简
		假如 开始准备货币工厂"1"
		当 "<money>" 执行函数"<function>"
		那么 最终结果输出为"<result>"

		例子: 向上取整
			| money    | function | result | 
			| 12.1 USD | ceil     | 13 USD | 
			| 10.5 CNY | ceil     | 11 CNY | 
			| 2.7 CHF  | ceil     | 3 CHF  | 

		例子: 向下取整
			| money    | function | result | 
			| 12.1 USD | floor    | 12 USD | 
			| 10.5 CNY | floor    | 10 CNY | 
			| 2.7 CHF  | floor    | 2 CHF  | 

		例子: 四舍五入
			| money    | function | result | 
			| 12.2 USD | round    | 12 USD | 
			| 2.7 CHF  | round    | 3 CHF  | 

		@fixme
		例子: 异常例子
			| money | function | result |
			| 10.5 CNY | round    | 11 CNY | 
			| 0.5 CNY | round    | 1 CNY | 
	
	@compare
	场景大纲: 货币比较
		假如 开始准备货币工厂"1"
		当 有货币"<money>" 和货币"<to>"
		那么 "<compare>"比较结果正确

		例子: 等于
			| money  | compare | to     | 
			| 12 USD | ==      | 12 USD | 
			| 11 CNY | ==      | 11 CNY | 
			| 3 CHF  | ==      | 3 CHF  | 

		例子: 不等于
			| money  | compare | to     | 
			| 56 USD | !=      | 12 USD | 
			| 10 CNY | !=      | 11 CNY | 
			| 31 CHF | !=      | 3 CHF  | 
			| 56 USD | !=      | 12 USD | 
			| 10 CNY | !=      | 11 CNY | 
			| 31 CHF | !=      | 3 CHF  | 

		例子: 大于
			| money  | compare | to     | 
			| 2 USD  | >       | 1 USD  | 
			| 21 CNY | >       | 11 CNY | 
			| 12 CHF | >       | 3 CHF  | 

		例子: 小于
			| money   | compare | to      | 
			| 0.5 USD | <       | 1 USD   | 
			| 123 CNY | <       | 321 CNY | 
			| 77 CHF  | <       | 99 CHF  | 

		例子: 大于等于
			| money    | compare | to      | 
			| 82.1 USD | >=      | 82 USD  | 
			| 101 CNY  | >=      | 101 CNY | 
			| 137 CHF  | >=      | 123 CHF | 

		例子: 小于等于
			| money    | compare | to       | 
			| 12.2 USD | <=      | 12.5 USD | 
			| 10.5 CNY | <=      | 11 CNY   | 
			| 2.7 CHF  | <=      | 3 CHF    | 

	@compare
	@exception
	场景大纲: 非法货币比较
		假如 开始准备货币工厂"1"
		当 有货币"<money>" 和货币"<to>"
		那么 "<compare>"比较结果异常

		例子: 等于
			| money  | compare | to     | 
			| 2 USD  | ==      | 1      | 
			| 21 CNY | ==      | 11.1   | 
			| 12 CHF | ==      | 3      | 
			| 2 CNY  | ==      | 2 USD  | 
			| 21 CHF | ==      | 21 CNY | 
			| 100    | ==      | 12 CHF | 

		例子: 不等于
			| money  | compare | to     | 
			| 2 USD  | !=      | 1      | 
			| 21 CNY | !=      | 11.1   | 
			| 12 CHF | !=      | 3      | 
			| 2 CNY  | !=      | 2 USD  | 
			| 21 CHF | !=      | 21 CNY | 
			| 100    | !=      | 12 CHF | 

		例子: 大于
			| money  | compare | to     | 
			| 2 USD  | >       | 1      | 
			| 21 CNY | >       | 11.1   | 
			| 12 CHF | >       | 3      | 
			| 100    | >       | 2 USD  | 
			| 100    | >       | 21 CNY | 
			| 100    | >       | 12 CHF | 

		例子: 小于
			| money   | compare | to      | 
			| 0.5 USD | <       | 1       | 
			| 123 CNY | <       | 321     | 
			| 77 CHF  | <       | 99      | 
			| 0.5     | <       | 1 USD   | 
			| 123     | <       | 321 CNY | 
			| 77      | <       | 99 CHF  | 

		例子: 大于等于
			| money    | compare | to      | 
			| 82.1     | >=      | 82 USD  | 
			| 101      | >=      | 101 CNY | 
			| 137      | >=      | 123 CHF | 
			| 82.1 USD | >=      | 82      | 
			| 101 CNY  | >=      | 101     | 
			| 137 CHF  | >=      | 123     | 


		例子: 小于等于
			| money    | compare| to     | 
			| 12.2     | <=     | 12 USD | 
			| 10.5     | <=     | 11 CNY | 
			| 2.7      | <=     | 3 CHF  | 
			| 12.2 USD | <=     | 12     | 
			| 10.5 CNY | <=     | 11     | 
			| 2.7 CHF  | <=     | 3      | 
	
	@exchange
	场景大纲: 货币兑换
		假如 开始准备货币工厂"1"
		而且 银行录入汇率表
			| src | dst | rate |
			| CNY | USD |  6   |
			| CHF | USD |  2   |
		当 兑换货币"<money>"为"USD"
		那么 最终结果输出为"<reduce>"

		例子:
			| money  | reduce |
			| 23 USD | 23 USD |
			| 12 CHF | 6 USD |
			| 18 CNY | 3 USD |

	@exchange
	@simplify
	场景大纲: 货币兑换后约简
		假如 开始准备货币工厂"1"
		而且 银行录入汇率表
			| src | dst | rate |
			| CNY | USD |  6   |
			| CHF | USD |  2   |
		当 兑换货币"<money>"为"USD"
		那么 保留2位小数四舍五入约简
		而且 最终结果输出为"<to>"

		例子:
			| money     | to        | 
			| 23.13 USD | 23.13 USD | 
			| 50.27 CHF | 25.14 USD |
			| 20 CNY    | 3.33 USD  |

	@exchange
	@exception
	场景大纲: 异常货币兑换
		假如 开始准备货币工厂"1"
		而且 银行录入汇率表
			| src | dst | rate |
			| CNY | USD |  6   |
			| CHF | USD |  2   |
		当 兑换货币"<money>"为"<to>"
		那么 捕获异常错误"ExchangeRateNotExist", 信息显示"missing exchanged rate from <message>"

		例子:
			| money  | to  | message    | 
			| 12 USD | CNY | USD to CNY | 
			| 18 USD | CNF | USD to CNF | 
			| 18 CNY | CNF | CNY to CNF | 

	@dual
	场景大纲: 二元运算
		假如 开始准备货币工厂"1"
		而且 银行录入汇率表
			| src | dst | rate |
			| CNY | USD |  6   |
			| CHF | USD |  2   |
		当 计算出结果 货币"<money>", 操作"<operation>"另一操作数"<other>"
		那么 最终结果输出为"<result>"
		而且 兑换为美元, 最终结果输出为"<reduce>"

		例子: 加法
			| money  | operation | other | result           | reduce  | 
			| 2 USD  | +         | 1 USD | (2 USD + 1 USD)  | 3 USD   | 
			| 4 USD  | +         | 2 CHF | (4 USD + 2 CHF)  | 5 USD   | 
			| 6 USD  | +         | 3 CNY | (6 USD + 3 CNY)  | 6.5 USD | 
			| 8 CHF  | +         | 4 USD | (8 CHF + 4 USD)  | 8 USD   | 
			| 10 CHF | +         | 5 CHF | (10 CHF + 5 CHF) | 7.5 USD | 
			| 12 CHF | +         | 6 CNY | (12 CHF + 6 CNY) | 7 USD   | 
			| 12 CNY | +         | 7 USD | (12 CNY + 7 USD) | 9 USD   | 
			| 18 CNY | +         | 8 CHF | (18 CNY + 8 CHF) | 7 USD   | 
			| 18 CNY | +         | 9 CNY | (18 CNY + 9 CNY) | 4.5 USD | 

		例子: 减法
			| money  | operation | other | result           | reduce   | 
			| 2 USD  | -         | 1 USD | (2 USD - 1 USD)  | 1 USD    | 
			| 7 USD  | -         | 2 CHF | (7 USD - 2 CHF)  | 6 USD    | 
			| 12 USD | -         | 3 CNY | (12 USD - 3 CNY) | 11.5 USD | 
			| 17 CHF | -         | 4 USD | (17 CHF - 4 USD) | 4.5 USD  | 
			| 22 CHF | -         | 5 CHF | (22 CHF - 5 CHF) | 8.5 USD  | 
			| 27 CHF | -         | 6 CNY | (27 CHF - 6 CNY) | 12.5 USD | 
			| 36 CNY | -         | 7 USD | (36 CNY - 7 USD) | -1 USD   | 
			| 36 CNY | -         | 8 CHF | (36 CNY - 8 CHF) | 2 USD    | 
			| 42 CNY | -         | 9 CNY | (42 CNY - 9 CNY) | 5.5 USD  | 

		例子: 乘法
			| money  | operation | other | result       | reduce | 
			| 3 USD  | *         | 2     | (3 USD * 2)  | 6 USD  | 
			| 14 CHF | *         | 5     | (14 CHF * 5) | 35 USD | 
			| 30 CNY | *         | 3     | (30 CNY * 3) | 15 USD | 

		例子: 除法二元运算
			| money  | operation | other | result       | reduce  | 
			| 4 USD  | /         | 2     | (4 USD / 2)  | 2 USD   | 
			| 9 CHF  | /         | 3     | (9 CHF / 3)  | 1.5 USD | 
			| 12 CNY | /         | 2     | (12 CNY / 2) | 1 USD   | 

	@dual
	场景大纲: 二元运算(即席运算,乘/除法分配律)
		假如 开始准备货币工厂"2"
		而且 银行录入汇率表
			| src | dst | rate |
			| CNY | USD |  6   |
			| CHF | USD |  2   |
		当 计算出结果 货币"<money>", 操作"<operation>"另一操作数"<other>"
		那么 最终结果输出为"<result>"
		而且 兑换为美元, 最终结果输出为"<reduce>"

		例子: 加法
			| money  | operation | other | result           | reduce  | 
			| 2 USD  | +         | 1 USD | 3 USD            | 3 USD   | 
			| 4 USD  | +         | 2 CHF | (4 USD + 2 CHF)  | 5 USD   | 
			| 6 USD  | +         | 3 CNY | (6 USD + 3 CNY)  | 6.5 USD | 
			| 8 CHF  | +         | 4 USD | (8 CHF + 4 USD)  | 8 USD   | 
			| 10 CHF | +         | 5 CHF | 15 CHF           | 7.5 USD | 
			| 12 CHF | +         | 6 CNY | (12 CHF + 6 CNY) | 7 USD   | 
			| 12 CNY | +         | 7 USD | (12 CNY + 7 USD) | 9 USD   | 
			| 18 CNY | +         | 8 CHF | (18 CNY + 8 CHF) | 7 USD   | 
			| 24 CNY | +         | 6 CNY | 30 CNY           | 5 USD   | 

		例子: 减法
			| money  | operation | other | result           | reduce   | 
			| 2 USD  | -         | 1 USD | 1 USD            | 1 USD    | 
			| 7 USD  | -         | 2 CHF | (7 USD - 2 CHF)  | 6 USD    | 
			| 12 USD | -         | 3 CNY | (12 USD - 3 CNY) | 11.5 USD | 
			| 17 CHF | -         | 4 USD | (17 CHF - 4 USD) | 4.5 USD  | 
			| 22 CHF | -         | 5 CHF | 17 CHF           | 8.5 USD  | 
			| 27 CHF | -         | 6 CNY | (27 CHF - 6 CNY) | 12.5 USD | 
			| 36 CNY | -         | 7 USD | (36 CNY - 7 USD) | -1 USD   | 
			| 36 CNY | -         | 8 CHF | (36 CNY - 8 CHF) | 2 USD    | 
			| 42 CNY | -         | 9 CNY | 33 CNY           | 5.5 USD  | 

		例子: 乘法
			| money  | operation | other | result | reduce | 
			| 3 USD  | *         | 2     | 6 USD  | 6 USD  | 
			| 14 CHF | *         | 5     | 70 CHF | 35 USD | 
			| 30 CNY | *         | 3     | 90 CNY | 15 USD | 

		例子: 除法二元运算
			| money  | operation | other | result | reduce  | 
			| 4 USD  | /         | 2     | 2 USD  | 2 USD   | 
			| 9 CHF  | /         | 3     | 3 CHF  | 1.5 USD | 
			| 12 CNY | /         | 2     | 6 CNY  | 1 USD   | 


	@dual
	@exception
	场景大纲: 错误二元运算
		假如 开始准备货币工厂"<type>"
		当 计算货币"<money>", 操作"<operation>"另一操作数"<other>"
		那么 得到错误结果"OperatorError"

		例子: 错误二元运算
			| type | money  | operation | other  | 
			| 1    | 11     | +         | 12 USD | 
			| 1    | 8 CNY  | -         | 1      | 
			| 1    | 5 USD  | *         | 3 USD  | 
			| 1    | 3 CHF  | /         | 1 CNY  | 
			| 1    | 1      | /         | 1 USD  | 
			| 2    | 2 CNY  | -         | 1      | 
			| 2    | 7 USD  | +         | 2      | 
			| 2    | 12 CHF | *         | 11 USD | 
			| 2    | 3      | /         | 4 USD  | 

