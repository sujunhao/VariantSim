import sys
from readfq import readfq
import read_ann

usage = 'checkAnswer.py <Read.fq> <ann>'
if __name__ == '__main__':
	fp_read = open(sys.argv[1], 'r')
	fp_ann = open(sys.argv[2], 'r')
	
	posRef, posSim = {}, {}
    for line in fp_ann:
        a = read_ann.ann(line)
        createPosMap(posRef, posSim, a)
        #print posRef, pos
	for line in fp_read:
		words = line.strip().split('_')
		chrom = words[0]
		pos0 = int(words[1])
		pos1 = int(words[2])
		

	fp_read.close()
	fp_ann.close()