import sys
from readfq import readfq
import read_ann

usage = 'map <Ref> <sim_genome> <sim_ann>'

if __name__ == '__main__':
	if len(sys.argv) < 4:
		print >>sys.stderr, usage
		sys.exit(1)
	fp_ref = open(sys.argv[1], 'r')
	fp_sim_genome = open(sys.argv[2], 'r')
	fp_ann = open(sys.argv[3], 'r')
	last = None
	for chrom_ref, seq_ref, qual_ref in readfq(fp_ref):
		chrom_sim, seq_sim, qual_sim = readfq(fp_sim_genome).next()
		if chrom_ref != chrom_sim:
			print >>sys.stderr, '[Error]: Diff chromosome!'
			sys.exit(1)
		last = ann(fp_ann.readline())




	fp_ref.close()
	fp_sim_genome.close()
	fp_ann.close()

