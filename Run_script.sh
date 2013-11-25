#!/bin/bash
Ref=DonorSim_1.2/Demo/chr1_hg18_100000_lines.fa
#Var=DonorSim_1.2/Demo/venter_sv_chr1_within_6000000bp
Var=venter_filter
SimRefPrefix=test
echo '===build sim genome==='
python src/build_genome.py $Ref $Var $SimRefPrefix
echo '===build sim genome end==='
echo '===generate reads==='
./wgsim -N 1000 -1 100 -2 100 -r 0 $SimRefPrefix.sim_genome.fa r1.fq r2.fq
echo '===generate reads end==='
echo '===convert convert coordinates==='
python src/simPos2Ref.py r1.fq r2.fq $SimRefPrefix.sim_ann Sim
echo '===convert convert coordinates end==='

echo '===aln reads==='
bwa aln $Ref Sim1.fq >Sim1.sai
bwa aln $Ref Sim2.fq >Sim2.sai
bwa sampe $Ref Sim1.sai Sim2.sai Sim1.fq Sim2.fq >$SimRefPrefix.sam
echo '===aln reads end==='
