#!/usr/bin/env bash
source ~/.profile
workon Pyenv
source w2d-base.sh
watch2do "$UNIT_DIRS $SRC_DIRS" '*.py' 'make unit' 
