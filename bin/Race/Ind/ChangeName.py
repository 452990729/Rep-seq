#!/usr/bin/env python2

import sys
import re
import os


lb = re.split('/', sys.argv[1])[-1]
root, dirs, files = next(os.walk(os.path.join(sys.argv[1], '5.stats')))
outpath = os.path.join(sys.argv[2], sys.argv[3])
if not os.path.exists(outpath):
    os.mkdir(outpath)
for fl in files:
    ol = re.sub(lb, sys.argv[3], fl)
    os.system('ln -s {} {}'.format(os.path.join(root, fl),\
                                  os.path.join(outpath, ol)))
