# README

### slidingGC.py

|Input|FASTA file|
|Script description|A window of a given size (**length**) slides through a FASTA sequence. The next window **overlaps** the previous on a given number of nucleotides. For each window, is computed a GC % which will be returned as a BED-like file|
|Output|BED file of the GC % for each window and for each provided sequence|

|Option name | Description|
|------------|------------|
|-f or --fasta|multi FASTA file of the assembled genome. Each sequence correspond to a chromosome|
|-g or --gc\_count|BED-like output file of slidingGC.py|
|-t or -te| TE annotation file (.gff format), returned by RepeatMasker|
|-o or --outfig|Output figure name|

