#!/bin/bash
Ref=~/Desktop/Ref/hg19.fa
#Var=DonorSim_1.2/Demo/venter_sv_chr1_within_6000000bp
Var=NA18507.Variants
VarPrefix=variants
VarPrefixNonOverlap=variantsNonOverlap
SimRefPrefix=SimGenome
art=~/Desktop/NGStools/readSimulator/art/Linux64/art_illumina
echo '===diploid==='
python diploid.py $Var $VarPrefix
python filter_oevrlap_var.py $VarPrefix.A >$VarPrefixNonOverlap.A 2>overlap.A 
python filter_oevrlap_var.py $VarPrefix.a >$VarPrefixNonOverlap.a 2>overlap.a
echo '===diploid end==='
echo '===build sim genome==='
python build_genome.py $Ref $VarPrefixNonOverlap.A $SimRefPrefix.A
python build_genome.py $Ref $VarPrefixNonOverlap.a $SimRefPrefix.a
echo '===build sim genome end==='
echo '===generate reads==='
#./wgsim -N 1000 -1 100 -2 100 -r 0 $SimRefPrefix.sim_genome.fa r1.fq r2.fq
$art --paired --in $SimRefPrefix.A.simGenome.fa --out $SimRefPrefix.A --len 100 --fcov 2 --mflen 500 --sdev 50 -sam -ir 0 -ir2 0 -dr 0 -dr2 0 -qs 10 -qs2 10 
$art --paired --in $SimRefPrefix.a.simGenome.fa --out $SimRefPrefix.a --len 100 --fcov 2 --mflen 500 --sdev 50 -sam -ir 0 -ir2 0 -dr 0 -dr2 0 -qs 10 -qs2 10 
echo '===generate reads end==='



echo '===convert convert coordinates==='
python extract_artans.py $SimRefPrefix.A1.aln $SimRefPrefix.A2.aln >$SimRefPrefix.A.ans 
python extract_artans.py $SimRefPrefix.a1.aln $SimRefPrefix.a2.aln >$SimRefPrefix.a.ans 
python correct_coordinate3.py $SimRefPrefix.A1.fq $SimRefPrefix.A2.fq $SimRefPrefix.A.ans $SimRefPrefix.A.simAnn ReadA
python correct_coordinate3.py $SimRefPrefix.a1.fq $SimRefPrefix.a2.fq $SimRefPrefix.a.ans $SimRefPrefix.a.simAnn Reada
cat ReadA1.fq Reada1.fq >Read1.fq
cat ReadA2.fq Reada2.fq >Read2.fq
echo '===convert convert coordinates end==='

echo '===aln reads==='
#bwa aln $Ref Sim1.fq >Sim1.sai
#bwa aln $Ref Sim2.fq >Sim2.sai
#bwa sampe $Ref Sim1.sai Sim2.sai Sim1.fq Sim2.fq >$SimRefPrefix.sam
echo '===aln reads end==='
