#!/usr/bin/env python2

import sys
import re
import os
from glob import glob


path = glob(sys.argv[1]+'/analysis/*/*/4.Annotation/*FUNCTIONAL-T_clone-pass.tab')
out = open(os.path.join(sys.argv[2], 'Alakazam.tab'), 'w+')
i = 0
for fl in path:
    with open(fl, 'r') as f:
        lb = re.split('_', os.path.split(fl)[1])[0]
        if not i:
            for line in f:
                line = line.strip()
                if line.startswith('SEQUENCE_ID'):
                    out.write(line+'\t'+'SAMPLE'+'\n')
                else:
                    out.write(line+'\t'+lb+'\n')
        else:
            for line in f.readlines()[1:]:
                line = line.strip()
                out.write(line+'\t'+lb+'\n')
    i += 1

out.close()
