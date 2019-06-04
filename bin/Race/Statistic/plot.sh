#!/bin/bash

/huayin/project/HUAYIN/lixuefei/Pipeline/RepSeq/bin/Race/Statistic/QcPlot.py\
    $1 $3 $2
/huayin/project/HUAYIN/lixuefei/Pipeline/RepSeq/bin/Race/Statistic/StatPlotRace.py\
    PlotVDJ $2 $3

/huayin/project/HUAYIN/lixuefei/Pipeline/RepSeq/bin/Race/Statistic/StatPlotRace.py\
    PlotVJComb $2 $3
/huayin/project/HUAYIN/lixuefei/Pipeline/RepSeq/bin/Race/Statistic/MakeFinalRace.py\
    $1 read1,read2
