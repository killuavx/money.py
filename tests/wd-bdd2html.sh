#!/usr/bin/env bash
source ~/.profile
workon Pyenv
source wd-base.sh

watch2do "features" "*.feature" 'vim "+TOhtml" "+wqa" features/*.feature 2>/dev/null <<<"
R
R
R
q"'
