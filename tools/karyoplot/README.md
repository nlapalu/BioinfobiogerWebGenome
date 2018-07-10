# Karyoplot
Karyoplot is an R function based on Bioconductor karyoploteR package to generate karyotype-like figures for chromosome-level assembled (custom) genomes.

	authors: Antoine Lu

**Inputs:**

|Option name | Description|
|------------|------------|
|-f or --fasta|multi FASTA file of the assembled genome. Each sequence correspond to a chromosome|
|-g or --gc\_count|output of slidingGC.py|
|-t or -te| TE annotation file (.gff format), returned by RepeatMasker|

**Running karyoplot:**

```r
Rscript --vanilla karyoplot.R -f [seq_file.fasta] -g [gc_file.out] -t [te_file.gff] (-o [out_figure_name])
```

**Limits/ TODO**

- add a selection: which sequences not to select from FASTA file
- automatic management of the type and name of the returned image file + quality of the figure (the png / jpeg / tiff / pdf functions return a blurry figure)

