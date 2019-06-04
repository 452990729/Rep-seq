#!/usr/bin/env python

import re
import sys
import os
from glob import glob

path = glob(sys.argv[1]+'/analysis/*/*/out/*.alakazam.out')
alakazam = open(os.path.join(sys.argv[2], 'alakazam.out'), 'w+')
with open(path[0], 'r') as f:
    for line in f:
        alakazam.write(line.strip()+'\n')
for path_s in path[1:]:
    with open(path_s, 'r') as f:
        for line in f.readlines()[1:]:
            alakazam.write(line.strip()+'\n')

alakazam.close()
