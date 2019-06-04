#!/usr/bin/env python

import re
import sys
import json
from workflow import Json2Str


def ReadJson(file_in):
    with open(file_in, 'r') as in1:
        return Json2Str(json.load(in1))

def main():
    dict1 = ReadJson(sys.argv[1])
    dict2 = ReadJson(sys.argv[2])
    out = open(sys.argv[4], 'w+')
    i = 0
    with open(sys.argv[3], 'r') as in1:
        for line in in1:
            line = line.strip()
            i += 1
            if i%4 == 1:
                maker = re.sub('@', '', re.split('\|', line)[0])
                label = re.split('\=', line)[0]
                out.write(label+'='+str(max(dict1[maker], dict2[maker]))+'\n')
            else:
                out.write(line+'\n')


if __name__ == '__main__':
    main()
