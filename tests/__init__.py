# -*- encoding=utf-8
'''
File: __init__.py
Author: Killua.VX <killua.vx@gmail.com>
Date: 2013-04-18 21:12
Description:
'''
import sys
from os.path import dirname, abspath
cur_dir = dirname(dirname(abspath(__file__)))
sys.path.append(cur_dir)
