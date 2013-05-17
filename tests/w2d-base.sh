#!/usr/bin/env bash

function find_dirs(){
	find "$1" -not -name "__*" -not -name ".*" -type d | xargs
	return
}

function watch2do(){
	directories=$1
	patterns=$2
	todo=$3
	watchmedo shell-command --recursive --ignore-directories \
		--patterns="$patterns" --wait --command="$todo" \
		$directories
}

SRC_DIRS=../src/money
UNIT_DIRS=units
FEATURE_DIRS=features
