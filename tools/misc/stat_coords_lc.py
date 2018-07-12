#!/usr/bin/env python

import re
import argparse

def statOnCoords(filename):
    dictChrCtg = {}
    dictChrLen = {}
    dictCtgLen = {}
    regex = re.compile("^\s+([0-9]+)")
    with open("toto.coords", "r") as coords:
        for line in coords:
            if regex.search(line):
                lRecord = line.rstrip().split()
                if lRecord[17] not in dictChrCtg:
                    dictChrCtg[lRecord[17]] = {}
                    dictChrLen[lRecord[17]] = int(lRecord[11])
                    dictCtgLen[lRecord[18]] = int(lRecord[12])
                    dictChrCtg[lRecord[17]][lRecord[18]] = []
                    dictChrCtg[lRecord[17]][lRecord[18]].append((float(lRecord[9]),int(lRecord[6]),int(lRecord[7]),int(lRecord[0]),int(lRecord[1]),int(lRecord[3]),int(lRecord[4])))
                else:
                    if lRecord[18] not in dictChrCtg[lRecord[17]]:
                        dictCtgLen[lRecord[18]] = int(lRecord[12])
                        dictChrCtg[lRecord[17]][lRecord[18]] = []
                        dictChrCtg[lRecord[17]][lRecord[18]].append((float(lRecord[9]),int(lRecord[6]),int(lRecord[7]),int(lRecord[0]),int(lRecord[1]),int(lRecord[3]),int(lRecord[4])))
                    else:
                        dictChrCtg[lRecord[17]][lRecord[18]].append((float(lRecord[9]),int(lRecord[6]),int(lRecord[7]),int(lRecord[0]),int(lRecord[1]),int(lRecord[3]),int(lRecord[4])))

    for k in dictChrCtg:
        for i in dictChrCtg[k]:
            lLenChr = [0] * dictChrLen[k]
            lIdent = [] 
            for t in dictChrCtg[k][i]:
                #compute identity
                lIdent.append(t[0])
                #compute coverage
                for b in range(min(t[3],t[4])-1,max(t[3],t[4])):
                    #print  range(min(t[1],t[2])-1,max(t[1],t[2]))
                    lLenChr[b] = 1

            print "{} -- {} ::: nb matchs: {}\tid: {}%\tcov: {}%".format(k, i, sum(lLenChr), sum(lIdent)/len(lIdent), (sum(lLenChr)/float(dictChrLen[k]))*100)

if __name__ == '__main__':
    program = 'Stas on show-coords -l -c file'
    version = 0.1
    description = 'Calculates stats on "show-coords -l -c file.delta" file'
    parser = argparse.ArgumentParser(prog=program)
    parser = argparse.ArgumentParser(description=description, epilog="Author: Antoine Lu, 2018")
    parser.add_argument('--version', action='version', version='{} {}'.format(program, version))
    parser.add_argument("filename", help="input .coords file", type=str)

    args = parser.parse_args()

    statOnCoords(args.filename)
