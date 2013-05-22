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

