#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
#import time
import logging

class Contig(object):
    """"Initiate a instance of Contig class"""
    def __init__(self, name, lcov):
        """Constructor"""
        self.name = name
        self.lcov = lcov


class covReader(object):
    """Read a cov.genome file (file return by bedtools genomecov)"""
    def __init__(self, covFile):
        """Constructor"""
        self.covFile = covFile
        self.listename = []

    def createContig2(self):
        lCov = []
        currentCtg = ''
        with open(self.covFile, 'r') as f:
            for line in f:
                lValues = line.rstrip().split('\t')
                if currentCtg != lValues[0]:
                    if currentCtg:
                        yield Contig(currentCtg, lCov)
                    currentCtg = lValues[0]   
                    lCov = []
                else:
                    lCov.append(int(lValues[2]))
            yield Contig(currentCtg, lCov)


class SlidingWindow(object):
    """Get position from covFile to construct sliding window"""

    def __init__(self, covFile, length, overlap, threshold, exportBed, graph, exportR, logLevel='ERROR'):
        """Constructor"""
        self.covFile = covFile
        self.length = length
        self.overlap = overlap
        self.threshold = threshold
        self.exportBed = exportBed
        self.exportR = exportR
        self.graph = graph
        self.logLevel = logLevel
        logging.basicConfig(level=self.logLevel)
    #
    def slidingWindow(self, lcov):
        """Sliding window"""
        lvalues = []
        for i in range(0, len(lcov), (self.length - self.overlap)):
            if(i + self.length) <= (len(lcov)):
                lvalues.append(sum(lcov[i:(i + self.length)]) / float(self.length))
        return lvalues

    def run(self):
        dExport = {}
        lmax = 0
        g = covReader(self.covFile)
        for contig in g.createContig2():
            lvalues = self.slidingWindow(contig.lcov)
            if self.exportBed:
                self.exportToBedFile(contig, lvalues)
            dExport[contig.name] = lvalues
            if len(lvalues) > lmax:
                lmax = len(lvalues)
        # export dictionary in R-like format
        for key in sorted(dExport):
            while len(dExport[key]) < lmax:
                dExport[key].append('NA')
        if self.exportR:
            print '{}\t{}'.format('pos', '\t'.join(sorted(dExport)))
            for i in range(0, lmax):
                print '{}\t{}'.format(self.indexToWindowPos(i) - (self.length / 2),
                                      '\t'.join([str(dExport[key][i]) for key in sorted(dExport)]))
        #else:
            #for key in sorted(dExport):
                #print key, dExport[key]

    def exportToBedFile(self, contig, lvalues):
        """Export coverage score to BED format for Genome Browser visualization
        If -g argument is specified, draw one coverage scatter plot for each contig"""

        logging.info('Reading contig: {}'.format(contig.name))

        mean = sum(lvalues) / len(lvalues)
        minT = mean - (mean * self.threshold)
        maxT = mean + (mean * self.threshold)

        currentState = None
        lVals = []
        lPos = []

        lstart = []
        lend = []
        lmiddle = []
        lscore = []

        for i in range(0,len(lvalues)):
            
            state = None
            if lvalues[i] <= minT:
                state = -1
            elif lvalues[i] >= maxT:
                state = 1
            else:
                state = 0

            #print "{}-{}-{}-{}-{}".format(i,state,lvalues[i],minT,maxT)
            if state == currentState or currentState == None:
                currentState = state
                lVals.append(lvalues[i])
                lPos.append(i)
            else:
                start = self.indexToWindowPos(min(lPos)) - self.length
                lstart.append(start)
                end = self.indexToWindowPos(max(lPos))
                lend.append(end)
                lmiddle.append(end - ((end - start) / 2))
                name = "{}-{}".format(currentState, end - (end - start))
                score = sum(lVals)/len(lVals)
                lscore.append(score)
                print "{}\t{}\t{}\t{}\t{}".format(contig.name, start, end, name, score)
                currentState = state
                lVals = [lvalues[i]]
                lPos = [i]

        start = self.indexToWindowPos(min(lPos)) - self.length
        lstart.append(start)
        end = self.indexToWindowPos(max(lPos))
        lend.append(end)
        lmiddle.append(end - ((end - start) / 2))
        name = "{}-{}".format(currentState, end - (end - start))
        score = sum(lVals) / len(lVals)
        lscore.append(score)
        print "{}\t{}\t{}\t{}\t{}".format(contig.name, start, end, name, score)
        if self.graph:
            #print contig.name
            #print lstart
            #print lmiddle
            #print lend
            Graphics.drawContigCovplot(contig, lstart, lend, lmiddle, lscore, minT, maxT)

    def indexToWindowPos(self, index):
        """convert index value into position of the window"""
        windpos = ((index + 1) * self.length - (index + 1 - 1) * self.overlap)
        return windpos

class Graphics(object):

    def __init__(self):
        pass

    @staticmethod 
    def drawContigCovplot(contig, lstart, lend, lmiddle, lscore, minT, maxT):

        try:
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_agg import FigureCanvasAgg
            from matplotlib import gridspec

            fig = plt.Figure(figsize=(20,20))
            fig.suptitle("Coverage plot of {}".format(contig.name), fontsize=15)
            ax = fig.add_subplot(111)


            for i in range(len(lscore)):
                if lscore[i] <= minT:
                    col = 'red'
                elif lscore[i] >= maxT:
                    col = 'blue'
                else:
                    col = 'green'
                #ax.plot(lstart[i], lscore[i], c=col, marker='+')
                ax.hlines(y=lscore[i], xmin=lstart[i], xmax=lend[i], color=col)
                ax.vlines(x=lmiddle[i], ymin=lscore[i] - 1, ymax=lscore[i] + 1, color=col)

            #ax.title("Coverage plot of {}".format(contig.name))
            ax.set_xlabel('Window position', fontsize=10)
            ax.set_ylabel('Coverage score', fontsize=10)
            canvas = FigureCanvasAgg(fig)
            canvas.print_figure("covplot_{}".format(contig.name), dpi=80)

        except ImportError:
            print "Module matplotlib.pyplot not installed"


if __name__ == '__main__':
    #start = time.time()

    program = 'GenomeCov_SlidingWindow'
    version = 1.7
    description = 'Perform sliding window computation over a given genome coverage file\
                    obtain after using "bedtools genomecov".'
    parser = argparse.ArgumentParser(prog=program)
    parser = argparse.ArgumentParser(description=description, epilog="Author: Antoine Lu, 2018")
    parser.add_argument('--version', action='version', version='{} {}'.format(program, version))
    parser.add_argument("covFile", help="input coverage file", type=str)
    parser.add_argument("length", help="length of window", type=int)
    parser.add_argument("overlap", help="overlap between window", type=int)
    parser.add_argument("threshold",
                        help="threshold to determine whether region is under or over covered",
                        type=float, default=0.4)
    parser.add_argument("-b", "--exportBed", help="export results in bed format",
                        action="store_true", default=False)
    parser.add_argument("-g", "--graph", help="draw contig coverage scatter plot",
                        action="store_true", default=False)
    parser.add_argument("-r", "--exportR", help="print result in R-like column",
                        action="store_true", default=False)
    parser.add_argument("-v", "--verbosity", type=int, choices=[1, 2, 3],
                        help="increase output verbosity 1=error, 2=info, 3=debug")

    args = parser.parse_args()

    logLevel='ERROR'
    if args.verbosity == 1:
        logLevel = 'ERROR'
    if args.verbosity == 2:
        logLevel = 'INFO'
    if args.verbosity == 3:
        logLevel = 'DEBUG'
    logging.getLogger().setLevel(logLevel)



    if args.overlap >= args.length:
        raise Exception('window size must be at least one base longer than overlap')

    if args.graph:
        if args.exportBed == False:
            raise Exception('Argument needed: -b')

    sw = SlidingWindow(args.covFile, args.length, args.overlap, args.threshold, args.exportBed, args.graph, args.exportR, logLevel)
    sw.run()
    #end = time.time()
    #print(end - start)








