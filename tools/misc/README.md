# README

### slidingGC.py

_Description:_
A window of a given size (**length**) slides through a FASTA sequence. The next window **overlaps** the previous on a given number of nucleotides. For each window, is computed a GC % which will be returned as a BED-like file

|Option name | Description|
|------------|------------|
|fastafile|multi FASTA file of the assembled genome. Each sequence correspond to a chromosome|
|length|Length of the slidding window|
|overlap|Number of nucleotides to be overlaped by the next window|
|exportR|HAS TO be **TRUE** if you desire to return a BED file, otherwise nothing will be printed out|

### TE\_stats.py

_Description:_
Performs simple stats on a .gff annotation file returned by RepeatMasker (for example):
+ Number of TE/SSR per chromosomes
+ Total TE/SSR percentage across each chromosome
+ Sum of the TE+SSR percentage for each chromosome

|Option name | Description|
|------------|------------|
|gff|Annotation file of the TEs and SSRs|
|chrLengthFile|File containing the size of each chromosome: chr '\t' length|

### searchTelo.py

_Description:_

