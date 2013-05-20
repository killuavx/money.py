# vim: set noet nolist:
DIR=$(shell pwd)
VIRTUAL_ENV=/Users/me/Devel/VirtualEnvs/Pyenv
PYLIBDIR=${VIRTUAL_ENV}/lib
ctags=/usr/local/bin/ctags
SRC=${DIR}/src
PKGNAME=money.py
EGGINFO=${PKGNAME}.egg-info

.PHONY: readme
readme:
	@echo "# Money.py" > README.md
	@cat OVERVIEW.md \
	 AUTHORS.md \
	 INSTALL.md \
	 USAGE.md \
	 FAQ.md \
	 THANKS.md \
	 TODO.md \
	 ChangeLog.md >> README.md

.PHONY: install
install:
	python3 setup.py install --record install.files

.PHONY: uninstall
uninstall:
	cat install.files | xargs rm -rf
	rm install.files

.PHONY: buildproject
buildproject: listlibs listfiles ctagsfile cscopefile

.PHONY: listlibs
listlibs:
	@find ${PYLIBDIR} -type f -name "*.py" >> ${DIR}/cscope.files

.PHONY: listfiles
listfiles:
	@find ${DIR} -type f -name "*.py" > ${DIR}/cscope.files

.PHONY: ctagsfile
ctagsfile:
	@cat ${DIR}/cscope.files | xargs ${ctags} --c++-kinds=+px --fields=+iaS --extra=+q -o tags ${DIR}

.PHONY: cscopefile
cscopefile:
	@cscope -bkq -i ${DIR}/cscope.files -f ${DIR}/cscope.out

.PHONY: fntags
fntags:
	@echo -e "!_TAG_FILE_SORTED\t2\t2/2=foldcase/" > ${DIR}/fntags
	@find ${DIR} -not -regex '.*\.\(png\|gif\|jpg\)' -type f -printf "%f\t%p\t0\n" | sort -f >> fntags

.PHONY: clean
clean:
	@rm -rf tags cscope* 
	@rm -rf build dist
	@rm -rf ${SRC}/${EGGINFO}
	@find ${SRC} -name "*.pyc" -type f | xargs rm -rf
	@find ${SRC} -name __pycache__ -type d | xargs rm -rf
