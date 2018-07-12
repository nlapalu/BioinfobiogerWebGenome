# README
	authors: Antoine Lu
### slidingGC.py

_Description:_
A window of a given size (**length**) slides through a FASTA sequence. The next window **overlaps** the previous on a given number of nucleotides. For each window, is computed a GC % which will be returned as a BED-like file

|Option name | Description|
|------------|------------|
|fastafile|multi FASTA file of the assembled genome. Each sequence correspond to a chromosome|
|length|Length of the slidding window|
|overlap|Number of nucleotides to be overlaped by the next window|
|exportR|HAS TO be **TRUE** if you desire to return a BED file, otherwise nothing will be printed out|

```python
python slidingGC.py Cdestructivum.fasta 5000 500 True
```

The previous output is used in the construction of the Karyoplot for the assembled genome: see [karyoplot section](https://github.com/nlapalu/BioinfobiogerWebGenome/tree/develop/tools/karyoplot)

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

```python
# Extract the Chr lengths in external file: chr \t size
grep "^##sequence-region" arrow.gff | sed s'/ /\t/g' | cut -f2,4 | grep chr > chrLength.txt
python TE_stats.py ../run/Cdestructivum.fasta.out.gff chrLength.txt
```

### stat\_coords\_lc.py

_Description:_
Performs stats on a coord file returned my NUCmer's show-coords output file with -l (length of QUERy and REFerence) and -c (percent coverage information) parameters.
+ Number of matches between REF and QUER
+ % identity between REF and QUER
+ % coverage that the QUER match represents on the REF
+ Longest match

|Option name | Description|
|------------|------------|
|filename| .coords file return after using show-coords -l -c ... |


```python
show-coords -l -c pacbio_assembly.delta > pacbio_assembly.coords
python stat_coords_lc.py pacbio_assembly.coords
```

### searchTelo.py
_Description:_
Look for telomeric motifs at both termini of each assembled contig.
Return for each contig the region (HEAD: 5 prime, TAIL: 3 prime) containing or not a telomeric motif.

|Option name | Description|
|------------|------------|
|input\_file|FASTA file of the assembled genome|

```python
python searchTelo.py file.contigset.fasta
```

### slidingGenCov.py and windowCov.R

_Description:_
#### slidingGenCov.py:

##### Requirements:

+ [matplotlib.pyplot package](https://matplotlib.org/users/installing.html)

##### Description:

This script takes the returned coverage file from _bedtools gencov_. And returns either:

+ a BED file of the coverage for each window parcouring each contig of a given genome
+ a R-formated text file of the coverage for each window parcouring each contig
+ can return one coverage scatter plot for each contig

|Option name | Description|
|------------|------------|
|covfile|Coverage file from _bedtools gencov_|
|length|Length of the sliding window|
|overlap|Number of nucleotides to be overlapped|
|threshold|Threshold which determines whether the current regeion/window is under- or over- covered|

Optional arguments:

|Option name | Description|
|------------|------------|
|-b or --exportBed|Export into a BED-like format|
|-g or --graph|Plot a scatter plot for each contig|
|-r or --exportR|Export into a **R-like** format|

```python
python slidingGenCov.py bedtools.cov 100 20 0.4 (-b example-BED-like.bed OR -r example-R-like.txt) (-g)
```

#### windowCov.R

If **-r** option was selected with the previous script, you can use this script (windowCov.R) to generate a coverage plot for each assembled contig.

|Option name | Description|
|------------|------------|
|-f or --file|R-like file returned from slidingGenCov.py|
|-o or --out|Output BED like file name|
|-t or --threshold|Same threshold value as for _slidingGenCov.py_|
|-w or --windsize|Same window size/length as for _slidingGenCov.py_|
|-g or --graph|if TRUE, output a coverage plot for each contig|
|-m or --merge|if TRUE, merge sliding windows with same state (Min, Default, Max)|

```r
Rscript (--vanilla) windowCov.R -f example-R-like.txt -o example_R_cov.bed -t 0.4 -w 100 --graph=TRUE --merge=TRUE 
```

