# Karyoplot
Karyoplot is an R function based on Bioconductor karyoploteR package to generate karyotype-like figures for chromosome-level assembled (custom) genomes.

**Inputs:**

|Option name | Description|
|------------|------------|
|-f or --fasta|multi FASTA file of the assembled genome. Each sequence correspond to a chromosome|
|-g or --gc\_count|output of slidingGC.py|
|-t or -te| TE annotation file (.gff format), returned by RepeatMasker|
	

	authors: Antoine Lu
