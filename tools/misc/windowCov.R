#!/usr/bin/Rscript


if(require(optparse) == FALSE){
  install.packages("optparse")
}
require(ggplot2)
require(reshape2)

option_list <- list(
  make_option(c("-f", "--file"), type="character", default=NULL, 
              help="tabulated coverage per contig file name (obtained from slidingGenCov.py)", metavar="character"),
  make_option(c("-o", "--out"), type="character", default="out.bed", 
              help="output BED format file name [default= %default]", metavar="character"),
  make_option(c("-t", "--threshold"), type = "double", default = 0.4,
              help = "Threshold (double < 1) to determine Min and Max cutoff coverage", metavar = "number"),
  make_option(c("-w", "--windsize"), type = "integer", default = 100,
              help = "Sliding window size, same value as for the python script", metavar = "number"),
  make_option(c("-g", "--graph"), type = "logical", default = FALSE,
              help = "if TRUE, output a coverage plot for each contig", metavar = "logical"),
  make_option(c("-m", "--merge"), type = "logical", default = FALSE,
              help = "if TRUE, merge sliding windows with same state (Min, Default, Max)", metavar = "logical")
)

opt_parser = OptionParser(usage = "usage: Rscript %prog -f input.txt -o output.bed -t 0.4 -w 100 [options <--graph=TRUE --merge=TRUE>]", option_list=option_list)
opt = parse_args(opt_parser)

if (is.null(opt$file)){
  print_help(opt_parser)
  stop("At least three arguments must be supplied (input file, threshold, window size).n", call.=FALSE)
}

if(opt$threshold >= 1){
  print_help(opt_parser)
  stop("Threshold must be a DOUBLE lower than 1.", call. = FALSE)
}


alldata <- read.table(opt$file, header=TRUE, sep="\t")
colnames(alldata)[-1] = substring(colnames(alldata)[-1], 2)

tMin = apply(alldata, 2, mean, na.rm=T) * opt$threshold
tMin = tMin[-1]
tMax = apply(alldata, 2, mean, na.rm=T) * (1 + opt$threshold)
tMax = tMax[-1]

alldata <-melt(alldata, id.vars='pos', variable.name='series')

# Coverage plot 

# For a given window on a contig, attribuate a state: either Min or Max
# Min if value < tMin
# Max if value > tMax
for(x in seq(length(levels(alldata$series)))){
  tmpDF = alldata[which(alldata$series == levels(alldata$series)[x]),]
  tmpDF[which(tmpDF$value < tMin[x]), 'state']<-"Min" 
  tmpDF[which(tmpDF$value > tMax[x]), 'state']<-"Max" 
  tmpDF[which(is.na(tmpDF$state)),'state'] <- "Default"
  tmp = na.omit(tmpDF)
  rm(tmpDF)
  tmp$start <- NA
  tmp$end <- NA
  tmp[,'start'] = tmp[,'pos'] - (opt$windsize/2)
  tmp[,'end'] = tmp[,'pos'] + (opt$windsize/2)
  
  # if TRUE, create one plot per contig
  if(opt$graph == TRUE){
    png(paste0("covplot_",levels(alldata$series)[x],".png"))
    print(ggplot(tmp, aes(pos, value)) + geom_line() + geom_point(aes(colour = state)) + 
            ggtitle(paste0(levels(alldata$series)[x]," coverage fluctuations")) +
            xlab("Window position") + ylab("Coverage"))
    dev.off()
  }
  if(x == 1){
    towrite = tmp
  }
  else{
    towrite = rbind(towrite, tmp)
  }
  rm(tmp)
}

if(opt$merge == TRUE){
  currentstate = NULL
  for(i in seq(dim(towrite)[1])){
    if(is.null(currentstate)){
      fstart = i
      currentstate = towrite[fstart, 'state']
    }
    if(!is.null(currentstate)){
      if(towrite[i, 'state'] == currentstate){
        fend = i
      }
      if(towrite[i, 'state'] != currentstate || i == dim(towrite)[1]){
        towrite.value = mean(towrite[fstart:fend, 'value'])
        towrite.start = as.numeric(towrite[fstart, 'start'])
        towrite.end = as.numeric(towrite[fend, 'end'])
        write(paste(as.character(towrite[fstart, 'series']), towrite.start, towrite.end,
                    paste(currentstate, as.character(towrite[fstart, 'series']), mean(c(towrite.start, towrite.end)), sep = '_'),
                    towrite.value, sep = "\t"), file = paste0('merged', opt$out), sep = '\n', append = TRUE)
        fstart = i
        currentstate = towrite[fstart, 'state']
      }
    }
  }
}


# dataframe containing only state of interest (Min and Max)
towrite2 = towrite[which(towrite$state != 'Default'),]

# write a BED file of the extreme (Max or Min) value positions 
for(ligne in seq(dim(towrite2)[1])){
  write(paste(towrite2[ligne, 'series'], towrite2[ligne, 'start'], towrite2[ligne, 'end'],
              paste(towrite2[ligne,'state'], towrite2[ligne,'series'], towrite2[ligne,'pos'], sep = "_"),
              towrite2[ligne, 'value'], sep = "\t"), file = opt$out, sep = '\n', append = TRUE)
}
