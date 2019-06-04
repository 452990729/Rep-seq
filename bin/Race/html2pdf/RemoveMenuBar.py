#!/usr/bin/env python2
#encoding=utf-8

import sys
import re

out = open(sys.argv[2], 'w')

m = 1
with open(sys.argv[1], 'r') as f:
    for line in f:
        if re.search('MenuBar', line):
            m = 0
        if re.search('EndBar', line):
            m = 1
            out.write('<div id="main">')
        if m:
            if re.search('p class\=\"head\"', line) or re.search('\"\>广州华银医学检验中心', line):
                pass
            else:
                out.write(line)
