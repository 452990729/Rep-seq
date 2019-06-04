#!/usr/bin/env R

library(ggplot2)
library(alakazam)

Args <- commandArgs()
datain <- read.delim(Args[6], header = TRUE)
pdf(Args[7], width=10, height=10)
clones <- estimateAbundance(datain, group="SAMPLE", ci=0.95,
                            nboot=200, copy="DUPCOUNT")
#sample_colors <- c("PB7"="red", "SB7"="blue")
plotAbundance(clones, legend_title="Samples", plot.title = element_text(hjust = 0.5, size=22, face="bold"),
              legend.text=element_text(size=12), legend.title=element_text(size=15), axis.title=element_text(size=18), 
              axis.text.x = element_text(size = 12), axis.text.y = element_text(size = 12))
dev.off()
pdf(Args[8], width=10, height=10)
sample_div <- rarefyDiversity(datain, "SAMPLE", min_q=0, max_q=32, step_q=0.05, 
                              ci=0.95, nboot=200, copy="DUPCOUNT")

sample_main <- paste0("Sample diversity (n=", sample_div@n, ")")

plotDiversityCurve(sample_div, main_title=sample_main, 
                   legend_title="Sample", log_q=TRUE, log_d=TRUE, plot.title = element_text(hjust = 0.5, size=22, face="bold"),
                   legend.text=element_text(size=12), legend.title=element_text(size=15), axis.title=element_text(size=18), 
                   axis.text.x = element_text(size = 12), axis.text.y = element_text(size = 12))
dev.off()
