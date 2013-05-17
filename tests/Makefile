# vim: set noet nolist:
DIR=$(shell pwd)
lang=zh-CN

.PHONY: test
test: bdd unit

.PHONY: bdd
bdd:
	@behave ${args} --lang=${lang} features/*.${lang}.feature

.PHONY: unit
unit:
	@nosetests ${args} --config=setup.cfg units/${files}

echo:
	@echo ${VIRTUAL_ENV}

.PHONY: clean
clean:
	@-rm -rf reports/*
	@-rm -rf units/.ropeproject
