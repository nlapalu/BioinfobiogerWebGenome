#!/usr/bin/env Rscript

#' Karyotype like figure from chromosome-level assembled genome
#' Author: Antoine Lu
#' Year: 2018

# LIBRARY
source("https://bioconductor.org/biocLite.R")
#biocLite("VariantAnnotation")
suppressMessages(library("VariantAnnotation"))
suppressMessages(library("karyoploteR"))
suppressMessages(library("optparse"))
suppressMessages(library("seqinr"))
print("Library importation done")

# OPTIONS PARSE
option_list = list(
	make_option(c("-f", "--fasta"), type="character", default=NULL, 
              help="dataset file name", metavar="character"),
	make_option(c("-g", "--gc_count"), type="character", default=NULL, 
              help="dataset file name", metavar="character"),
	make_option(c("-t", "--te"), type="character", default=NULL, 
              help="dataset file name", metavar="character"),
	make_option(c("-o", "--outfig"), type="character", default="karyout", 
              help="output figure name", metavar="character")
);
opt_parser = OptionParser(option_list=option_list);
opt = parse_args(opt_parser);

if (is.null(opt$f)){
  print_help(opt_parser)
  stop("At least one argument must be supplied (input FASTA file)", call.=FALSE)
}

#' for the legend: create vectors that will contain arguments to create the legend box
#' example: if TE and GC files are provided, lgde will contain "Transposable Elements"
#' and "GC %"
#' sign1 and sign2 will contain metadata will be used to determine the shape and size
#' of the data to plot, color will contain a give color name associated to the data type

lgde = c()
sign1 = c()
sign2 = c()
color =  c()

# KARYOPLOT FUNCTION
karyoplot <- function(fasta, gc_count, te, out){

    # Plotting parameters
    pp <- getDefaultPlotParams(plot.type=2)
    pp$leftmargin <- 0.15
    pp$data2inmargin <- 1
    pp$data2outmargin <- 80
    pp$bottommargin <- 150

    ## Main data
    Cdest <- read.fasta(fasta, seqtype = "DNA")
    
    # bigScale: nb of step for the legend scale
    bigScale <- round(max(as.numeric(summary(Cdest)[,1]))/1e6)
    # chr1Name : chr1 name for legend scale
    chr1Name <- row.names(summary(Cdest))[1]

    Cdest <- cbind(data.frame(chr = row.names(summary(Cdest))),
               data.frame(start = rep(1, length(summary(Cdest)[,1]))),
               data.frame(end = as.numeric(summary(Cdest)[,1]))
    )
    row.names(Cdest) = seq(1, dim(Cdest)[1])

    ## Additional data

    # Transposable elements: 
    # te =  ___.fasta.out.TE.gff file from RepeatMasker
    # ex: "Cdestructivum.fasta.out.TE.gff"

    TE <- read.table(te, sep = "\t")
    TE <- TE[grep("chr", TE[,1]),c(1,4,5)]
    
    if(!is.null(TE)){
	lgde = append("Transposable elements", lgde);
	sign1 = append(NA, sign1);
	sign2 = append(15, sign2);
	color = append("aquamarine4", color)}

    # Filter out the TE which length is greater than 100 bp:

    TE[,4]=rep('NA', dim(TE)[1])
    TE[,4] = TE[,3] - TE[,2]
    TE = TE[which(TE[,4] > 100),]
    TE = TE[,-4]
    colnames(TE)=c("chr","start","end")
    TE <- toGRanges(TE)

    # GC content: from the .out file return by 'slidingGC.py'
    GContent <- read.table(gc_count, sep="\t")
    colnames(GContent)=c("middle","gc","chr")
    
	if(!is.null(GContent)){
		lgde = append("GC %", lgde);
		sign1 = append(1, sign1);
		sign2 = append(NA, sign2);
 		color = append("cornflowerblue", color)}
    

    ### PLOT COMMAND LINES ###
	
	
    # karyotype creation
    cd <- plotKaryotype(genome=Cdest,
                plot.type = 2, plot.params = pp, cex = 0.6,
                ideogram.plotter=NULL)
    kpAddCytobandsAsLine(cd, lwd=8, lend=1, color.schema="circos")

    # GC % for each chromosome
    for(chr in unique(GContent$chr)){
        kpArea(cd,
            chr=chr,
            x=GContent[which(GContent[,"chr"]==chr),"middle"],
            y=GContent[which(GContent[,"chr"]==chr),"gc"],
            ymin=0.2, ymax=0.6, base.y =-0.2,
            col=NA, border="cornflowerblue",
            data.panel = 2, lwd=0.05, r0=1.5, r1=0.35)
    }

    # Axis for GC%
    kpAxis(cd, ymin = 0.2,
         ymax = 0.6, labels=c("20%","40%", "60%"),
         numticks = 3, col="#666666",
         r0=1.5, r1=0.35,
         cex=0.4, data.panel = 2)


    # Transposable Elements 
    kpPlotRegions(cd, data=TE,
              data.panel = 1, col="#00b386",
              avoid.overlapping = FALSE, r0=0, r1=0.35)
    

    # Legends
    legend("bottomright",
     lgde,
     lwd=c(1,2,1), col=color,
     lty=sign1, pch=sign2,
     cex=0.8, bty = "o")

    markers <- data.frame(chr=rep("chr1", bigScale), pos=(1:bigScale*1e6), labels=1:bigScale)
    kpAbline(cd, chr = chr1Name, data.panel = 1, h = 1, col="#666666", r0=0.52, r1=1)
    kpPlotMarkers(cd, chr=markers$chr, x=markers$pos, labels=markers$labels,
            r0=0.88, r1=1.2, text.orientation = "horizontal", cex = 0.7,
            line.color = "#666666", label.color = "#666666",
            label.margin=40)
    # add 'Mb' unit to the scale
    mtext(side=3, text="(Mb)", cex = 0.6, outer=TRUE, line = -1.2, at = 0.96)
	
}

# MAIN #
karyo <- karyoplot(opt$fasta, opt$gc_count, opt$te, opt$outfig)
