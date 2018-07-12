# /usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
import re
import logging

class Chr(object):
    #
    def __init__(self, name, TE, SSR, size):
        """constructeur"""
        self.name = name
        self.TE = TE # liste de longueur des TE/SSR
        self.SSR = SSR
        self.size = size
    #
    def statChr(self):
        """chrLengthFile: external file with chr length:  chrName \t size in bp
        grep "^##sequence-region" /work/nlapalu/colleto/arrow/test/arrow.gff | sed s'/ /\t/g' | cut -f2,4 | grep "chr" > chrLength.txt
        """
        # SSR
        totalSSR = float(len(self.SSR)) # nombre de SSR dans le chr
        basesSSR = sum(self.SSR)
        # TE
        totalTE = float(len(self.TE))
        basesTE = sum(self.TE) # somme des longueurs des TE dans le chr
        #
        repetPercent = (basesTE+basesSSR)/float(self.size) * 100
        tePercent = basesTE/float(self.size) * 100
        ssrPercent = basesSSR/float(self.size) * 100
        #
        print("|{}|{}|{}|{}|{}|{}|{}|{}|".format(self.name, int(totalTE), int(basesTE), round(tePercent, 2),
                                            int(totalSSR), int(basesSSR), round(ssrPercent, 2),
                                            round(repetPercent, 2)))
#
class readRepeatMasker(object):
    #
    def __init__(self, gff, chrLengthFile):
        """constructeur"""
        self.gff = gff
        self.chrLengthFile = chrLengthFile
    #
    def getLlength(self):
        with open(self.gff, 'r') as f:
            currentChr = ''
            for line in f:
                m = re.match("chr*", line) # on ne prend ni mito, ni rdna
                if m:       
                    if line.split('\t')[0] == currentChr:
                        start = float(line.split('\t')[3])
                        end = float(line.split('\t')[4])
                        length = (end - start) + 1
                        #if length < 5: # Montre que les SSR s'insère dans les TE, donc fragmentation des TE (1-5bp)
                        #    print line
                        te = re.match("^(Target \"Motif:[a-zA-Z]+)" ,line.split('\t')[8])
                        ssr = re.match("^(Target \"Motif:\(*)", line.split('\t')[8])
                        if te:
                            TE.append(length)
                        elif ssr:
                            SSR.append(length)
                    elif line.split('\t')[0] != currentChr or currentChr == '':
                        if currentChr:
                            with open(self.chrLengthFile, 'r') as chrLength:
                                for chrline in chrLength:
                                    if currentChr == chrline.split('\t')[0]:
                                        yield Chr(currentChr, TE, SSR, chrline.split('\t')[1])
                        TE = []
                        SSR = []
                        currentChr = line.split('\t')[0]
                        start = float(line.split('\t')[3])
                        end = float(line.split('\t')[4])
                        length = (end - start) + 1
                        TE.append(length)
                        SSR.append(length)
            if currentChr:
                with open(self.chrLengthFile, 'r') as chrLength:
                    for chrline in chrLength:
                        if currentChr == chrline.split('\t')[0]:
                            yield Chr(currentChr, TE, SSR, chrline.split('\t')[1])

    def run(self):
        repeatMasker = readRepeatMasker(self.gff, self.chrLengthFile)
        #
        print "|/2. chr|\\3. TE|\\3. SSR|/2. TOTAL % REPEAT|"
        print "|# TE|Nb Bases TE|% TE|# SSR|Nb Bases SSR|% SSR|"
        #
        for chromosome in repeatMasker.getLlength():
            chromosome.statChr()

if __name__ == '__main__':
    program = 'stat TE'
    version = 1.0
    description = 'Performs simple stats on a repeat motifs annotation file (.gff)'
    parser = argparse.ArgumentParser(prog=program)
    parser = argparse.ArgumentParser(description=description, epilog="Author: Antoine Lu, 2018")
    parser.add_argument('--version', action='version', version='{} {}'.format(program, version))
    parser.add_argument("gff", help="input GFF file", type=str)
    parser.add_argument("chrLengthFile", help="input chromosome length file", type=str)
    parser.add_argument("-v", "--verbosity", type=int, choices=[1, 2, 3],
                        help="increase output verbosity 1=error, 2=info, 3=debug")

    args = parser.parse_args()

    rMasker = readRepeatMasker(args.gff, args.chrLengthFile)
    rMasker.run()


