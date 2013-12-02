#1. Introduction

It's a read simulate tookit.
The basic idea comes from [donorsim](https://code.google.com/p/donorsim/).

	Input:	original genome and VCF.
	Output:	simulate reads.

	1. add variants(SNP/Indel) from variants.txt(converted from VCF) to original genome in order to get a simulate genome
	2. split simulate genome into simulate reads by simulator (wgsim or art)  
	3. convert simulate position coordinate to original position coordinate

#2. Tools

Tools provided in this tookit.

##2.1 Main tools

ID |  Description										|  Src
:----------------|:-------------------------------------|  :---------------
1  |  VCF to variants format  							|  [VCF2DSM.py]
2  |  ref + variants ===> sim_genome + sim_ann  		|  [build_genome.py]
3  |  split sim_genome into reads  						|  [wgsim]
4  |  replace sim_genome pos in read name with ref pos  |  [correct_coordinate.py]
5  |  divide variants doc into two files and each file respents one copy |  [diploid.py]
6  |  move chrom and pos in read.aln(for art only) to ans file|  [extract_artans.py]

##2.2 Extra Tools

ID |  Description  										 |	Src
:----------------|:----------------|:---------------
1  |  show the variants region seq in Ref and SimGenome  |  [diff.py]
2  |  filter overlap variants  							 |  [filter_variants.py]
