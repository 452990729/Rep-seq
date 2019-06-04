#!/usr/bin/env python2


from scipy import stats
import numpy as np
from copy import deepcopy
from statsmodels.sandbox.stats.multicomp import multipletests
from qvalue import estimate


def TwoSampleKSTest(np1_in, np2_in, FDR=True):
    assert np1_in.shape[0] == np2_in.shape[0]
    ary = np1_in.shape[0]
    pvalue = np.zeros(ary)
    for i in range(ary):
        a,p = stats.ks_2samp(np1_in[i], np2_in[i])
        pvalue[i] = p
    if FDR:
        qv = multipletests(pvalue, method='fdr_bh')[1]
#        qv = estimate(pvalue)
        return pvalue, qv
    else:
        return pvalue


def TwoSampleTTest(np1_in, np2_in, FDR=True):
    assert np1_in.shape[0] == np2_in.shape[0]
    ary = np1_in.shape[0]
    pvalue = np.zeros(ary)
    for i in range(ary):
        a,p = stats.ttest_ind(np1_in[i], np2_in[i])
        pvalue[i] = p
    if FDR:
#        qv = multipletests(pvalue, method='fdr_bh')[1]
        sl = deepcopy(pvalue)
        for i in range(len(sl)):
            if not (sl[i] >= 0 and sl[i] <= 1):
                print sl[i]
                sl[i] = 1.0
        qv = estimate(sl)
        return pvalue, qv
    else:
        return pvalue
