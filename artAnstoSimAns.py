import sys
import itertools
usage = 'artAns2SimAns.py <read1.aln> <read2.aln>'
ReadLen = 100
if __name__ == '__main__':
	if len(sys.argv) < 3:
		print usage
		sys.exit(1)
	fp1 = open(sys.argv[1])
	fp2 = open(sys.argv[2])
	for line1, line2 in itertools.izip(fp1, fp2):
		if line1[0] != '>':
			continue
		line1 = line1.strip()[1:]
		line2 = line2.strip()[1:]
		#print line1.split()
		chrom1, name1, pos1, strand1 = line1.split()
		chrom2, name2, pos2, strand2 = line2.split()
		if chrom1 != chrom2:
			print >>sys.stderr, '[ERROR]chrom not match!'
			sys.exit(1)
		if int(pos1) < int(pos2):
			print '%s\t%s\t%d'%(chrom1, pos1+1, int(pos2)+ReadLen-1+1)
		else:
			print '%s\t%s\t%d'%(chrom1, pos1+1, int(pos2)+ReadLen-1+1)

	fp1.close()
	fp2.close()