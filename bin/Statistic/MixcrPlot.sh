#!/usr/bin/env bash

/huayin/project/HUAYIN/lixuefei/Pipeline/RepSeq/bin/Statistic/QcPlot.py\
    ../ $1
/huayin/project/HUAYIN/lixuefei/Pipeline/RepSeq/bin/Statistic/StatPlotMixcr.py\
    PlotVDJ ./ $1
/huayin/project/HUAYIN/lixuefei/Pipeline/RepSeq/bin/Statistic/StatPlotMixcr.py\
    PlotVJComb ./ $1
