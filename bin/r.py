#!/usr/bin/env python

import sys
import re

a = []
with open(sys.argv[1], 'r') as f:
    for i in f:
        a += re.split('\s+', i.strip())

print '\n'.join([str(m) for m in a])

