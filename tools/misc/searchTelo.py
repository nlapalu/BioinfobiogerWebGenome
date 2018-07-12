#! /usr/bin/python

import re
from Bio import SeqIO
import argparse

def searchTelo(input_file):
    ccctaa = re.compile("(CCCTAA){2,100}", re.I)
    ttaggg = re.compile("(TTAGGG){2,100}", re.I)
    fasta_sequences = SeqIO.parse(open(input_file),'fasta')
    for fasta in fasta_sequences:
        name, sequence = fasta.id, fasta.seq.tostring()
        head = sequence[0:200]
        tail = sequence[-200:]
        h = re.search(ccctaa, head)
        t = re.search(ttaggg, tail)
        if h:
            match_h = h.group()
        else:
            match_h = 'None'
        if t:
            match_t = t.group()
        else:
            match_t = 'None'
        print "{}\nHEAD: {}\nTAIL: {}\n".format(name, match_h, match_t)
    return 0

if __name__ == '__main__':
    program = 'searchTelo - telomeric pattern searcher'
    version = 1.0
    description = 'Search telomeric pattern within each sequence in a FASTA file'
    parser = argparse.ArgumentParser(prog=program)
    parser = argparse.ArgumentParser(description=description, epilog="Author: Antoine Lu, 2018")
    parser.add_argument('--version', action='version', version='{} {}'.format(program, version))
    parser.add_argument("input_file", help="input FASTA file", type=str)

    args = parser.parse_args()
    searchTelo(args.input_file)
