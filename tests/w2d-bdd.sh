#!/usr/bin/env bash
source ~/.profile
workon Pyenv
source w2d-base.sh
watch2do "$FEATURE_DIRS $SRC_DIRS" '*.py;*.feature' 'make bdd' 
