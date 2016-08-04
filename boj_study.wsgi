#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/scsc_2016_summer/")
print sys.path

from boj_study import app as application
