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

### .py

