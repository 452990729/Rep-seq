#!/usr/bin/env python2

import os
import sys
import re
import xlwt
from glob import glob
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
#from Test import TwoSampleKSTest
from Test import TwoSampleTTest
from UsefulFunc import ExcelStyle


def GetGroup(path_in):
    path_base = path_in+'/analysis'
    root, dirs, files = next(os.walk(path_base))
    root1, dirs1, files1 = next(os.walk(os.path.join(root, dirs[0])))
    return len(dirs1)

def CalP(np_in, group_len):
    np_new = np_in[0, :]
    for ary in np_in[1:, :]:
        if len(filter(lambda x:x>0, [float(i) for i in ary[1:]])) > 0:
            np_new = np.vstack([np_new, ary])
    np1 = np_new[1:, 1:group_len+1].astype('float')
    np2 = np_new[1:, group_len+1:].astype('float')
#    pv, qv = TwoSampleKSTest(np1, np2)
    pv, qv = TwoSampleTTest(np1, np2)
    npv = np.array(['Pvalue']+list(pv), dtype='S50')
    nqv = np.array(['Qvalue']+list(qv), dtype='S50')
    return np.hstack([np_new, np.vstack([npv, nqv]).T])

def WriteExcelSheet(sheet, np_in):
    default = ExcelStyle('Times New Roman',220,True)
    m = 1
    for ary in np_in:
        if m==1 or float(ary[-2]) <=0.05:
            m += 1
            for i in range(0, len(ary)):
                sheet.write(m-2, i, ary[i], default)

def ValueTest(path_in):
    path_base = path_in+'/Compare'
    np_v = np.loadtxt(os.path.join(path_base, 'VFraction.txt'), dtype='S50')
    np_vj = np.loadtxt(os.path.join(path_base, 'VJFraction.txt'), dtype='S50')
    np_vdj = np.loadtxt(os.path.join(path_base, 'VDJFraction.txt'), dtype='S50')
    np_clone = np.loadtxt(os.path.join(path_base, \
                                       'ClonetypeFraction.txt'), dtype='S50')
    group_len = GetGroup(path_in)
    out_v = CalP(np_v, group_len)
    out_vj = CalP(np_vj, group_len)
    out_vdj = CalP(np_vdj, group_len)
    out_clone = CalP(np_clone, group_len)
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(u'VFraction',cell_overwrite_ok=True)
    WriteExcelSheet(sheet1, out_v)
    sheet2 = f.add_sheet(u'VJFraction',cell_overwrite_ok=True)
    WriteExcelSheet(sheet2, out_vj)
    sheet3 = f.add_sheet(u'VDJFraction',cell_overwrite_ok=True)
    WriteExcelSheet(sheet3, out_vdj)
    sheet4 = f.add_sheet(u'ClonetypeFraction',cell_overwrite_ok=True)
    WriteExcelSheet(sheet4, out_clone)
    f.save(os.path.join(path_base, 'MixDiffAnalysis.xls'))

def PCAAnalysis(path_in):
    path_base = path_in+'/Compare'
    np_v = np.loadtxt(os.path.join(path_base, 'VFraction.txt'), dtype='S50')
    np_vj = np.loadtxt(os.path.join(path_base, 'VJFraction.txt'), dtype='S50')
    np_vdj = np.loadtxt(os.path.join(path_base, 'VDJFraction.txt'),\
                        dtype='S50')
    np_clone = np.loadtxt(os.path.join(path_base, \
                                       'ClonetypeFraction.txt'), dtype='S50')
    group_len = GetGroup(path_in)
    pca=PCA(n_components=2)
    colors = ['red',]*group_len+['blue']*(np_v.shape[1]-group_len)
    label = np_v[0, 1:]
    fig, axes = plt.subplots(2,2,  figsize=(12, 12))
    vdata = pca.fit_transform(np_v[1:, 1:].T)
    axes[0,0].scatter(vdata[:,0], vdata[:,1], c=colors, alpha=0.5)
    for i, txt in enumerate(label):
        axes[0,0].annotate(txt, (vdata[i,0], vdata[i,1]))
    axes[0,0].set_xlabel('PCA1')
    axes[0,0].set_ylabel('PCA2')
    axes[0,0].set_title('V gene')
    vjdata = pca.fit_transform(np_vj[1:, 1:].T)
    axes[0,1].scatter(vjdata[:,0], vjdata[:,1], c=colors, alpha=0.5)
    for i, txt in enumerate(label):
        axes[0,1].annotate(txt, (vjdata[i,0], vjdata[i,1]))
    axes[0,1].set_xlabel('PCA1')
    axes[0,1].set_ylabel('PCA2')
    axes[0,1].set_title('VJ gene')
    vdjdata = pca.fit_transform(np_vdj[1:, 1:].T)
    axes[1,0].scatter(vdjdata[:,0], vdjdata[:,1], c=colors, alpha=0.5)
    for i, txt in enumerate(label):
        axes[1,0].annotate(txt, (vdjdata[i,0], vdjdata[i,1]))
    axes[1,0].set_xlabel('PCA1')
    axes[1,0].set_ylabel('PCA2')
    axes[1,0].set_title('VDJ gene')
    clonedata = pca.fit_transform(np_clone[1:, 1:].T)
    axes[1,1].scatter(clonedata[:,0], clonedata[:,1], c=colors, alpha=0.5)
    for i, txt in enumerate(label):
        axes[1,1].annotate(txt, (clonedata[i,0], clonedata[i,1]))
    axes[1,1].set_xlabel('PCA1')
    axes[1,1].set_ylabel('PCA2')
    axes[1,1].set_title('Clonetype')
    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    plt.savefig(os.path.join(path_base, 'PCA.png'),dpi=100)

def main():
    ValueTest(sys.argv[1])
    PCAAnalysis(sys.argv[1])


if __name__ == '__main__':
    main()
