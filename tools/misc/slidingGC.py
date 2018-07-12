#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
import re
import logging

class FastaReader(object):
    # Read Fasta input sequence, store each seq in a generator
    def __init__(self, fastaFile):
        """Constructor"""
        self.fastaFile = fastaFile
    #
    def readSeqs(self):
        mySeq = []
        currentSeq = ''
        with open(self.fastaFile, 'r') as f:
            for line in f:
                if line == '\n':
                    next
                m = re.match('>(.*)',line)
                if m:
                    if currentSeq:
                        yield Seq(currentSeq, ''.join(mySeq))
                    #
                    currentSeq = re.split('[\s\|]+',m.group(1))[0]
                    mySeq = []
                else:
                    mySeq.append(line.replace('\n',''))
            yield Seq(currentSeq, ''.join(mySeq))


class Seq(object):
    # Sequence define by its name and its bases sequence
    def __init__(self, name, bases):
        """Constructor"""
        self.name = name
        self.bases = bases


class SlidingWindow(object):
    #
    def __init__(self, fastaFile, length, overlap, exportR=True, cytobands=True, logLevel='ERROR'):
        self.fastaFile = fastaFile
        self.length = length
        self.overlap = overlap
        self.exportR = exportR
        self.logLevel = logLevel
        logging.basicConfig(level=self.logLevel)
    #
    def countGC(self, sequence):
        """calculates the GC percentage for a given sequence, 
        will be used to calculate de % in each window"""
        gc = 0
        for nucl in list(sequence):
            if(nucl == "C") or (nucl == "G") or (nucl == "c") or (nucl == "g"):
                gc += 1
        gcContent = float(gc)/float(len(sequence))
        return gcContent
    #
    def slidingWindow(self, seqObj):
        """Sliding window"""
	lStart = []
	lEnd = []
        lGC = []
        lSeqName = []
        for i in range(0, len(seqObj.bases), (self.length - self.overlap)):
            if(i + self.length) <= len(seqObj.bases):
                # If the window is in the sequence, calculates GC% and the window middle
		lStart.append(i)
		lEnd.append(i + self.length)
                windSeq = seqObj.bases[i:i + self.length]
                lGC.append(self.countGC(windSeq))
        return lStart, lEnd, lGC
    #
    def run(self):
        # main actions of the script: exportR has to be TRUE
        flag = -1
        ff = FastaReader(self.fastaFile)
        for seq in ff.readSeqs():
            start, end, gc = self.slidingWindow(seq)
            if self.exportR:
                fout = self.fastaFile.split('/')[-1].split(".fasta")[:-1][0] + '_' + str(self.length) + '_' + str(self.overlap) + ".bed"
                with open(fout, 'a') as filout:
                    for i in range(len(start)):
                        new_gc = round(float(gc[i]), 2)
                        filout.write("{}\t{}\t{}\t{}\n".format(seq.name, start[i], end[i], new_gc))


if __name__ == '__main__':

    program = 'SlidingGC'
    version = 0.1
    description = 'Get GC content (%) from each chromosome using a sliding window of a given size from a fasta file'
    parser = argparse.ArgumentParser(prog=program)
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--version', action='version', version='{} {}'.format(program, version))
    parser.add_argument("fastaFile", help="input fasta file", type=str)
    parser.add_argument("length", help="length of window", type=int)
    parser.add_argument("overlap", help="overlap between window", type=int)
    parser.add_argument("exportR", help="To export data in formated R text", type=bool, choices=[True, False])
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

    gc = SlidingWindow(args.fastaFile, args.length, args.overlap, args.exportR, logLevel)
    gc.run()
