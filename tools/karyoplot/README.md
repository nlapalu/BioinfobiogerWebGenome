# Karyoplot
Karyoplot is an R function based on Bioconductor karyoploteR package to generate karyotype-like figures for chromosome-level assembled (custom) genomes. Karyoplot has been developed by Antoine Lu at [INRA-BIOGER](https://www6.versailles-grignon.inra.fr/bioger).

	authors: Antoine Lu

### Install
The actual version of Bioconductor's karyoploteR package runs under R version 3.4.1 or latter.
You will need the following packages to run our tool:
+ [variantAnnotation](https://bioconductor.org/packages/release/bioc/html/VariantAnnotation.html)
+ [karyoploteR](http://bioconductor.org/packages/release/bioc/html/karyoploteR.html)
+ [seqinr](https://cran.r-project.org/web/packages/seqinr/index.html)
+ [optparse](https://cran.r-project.org/web/packages/optparse/index.html)



### Running karyoplot:

**Inputs:**

|Option name | Description|
|------------|------------|
|-f or --fasta|multi FASTA file of the assembled genome. Each sequence correspond to a chromosome|
|-g or --gc\_count|BED-like output file of slidingGC.py|
|-t or -te| TE annotation file (.gff format), returned by RepeatMasker|
|-o or --outfig|Output figure name|

```r
Rscript --vanilla karyoplot.R -f [seq_file.fasta] -g [gc_file.out] -t [te_file.gff] (-o [out_figure_name])
```
**Output:**

One Rplot.pdf file corresponding to the constructed karyoplot

**Limits/ TODO**

- add a selection: which sequences not to select from FASTA file
- automatic management of the type and name of the returned image file + quality of the figure (the png / jpeg / tiff / pdf functions return a blurry figure)

