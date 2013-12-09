
import random
import sys


def diploid(variantsFileName, diploidFilePrefix):
	fpVariants = open(variantsFileName, 'r')
	fpDiploid0 = open(diploidFilePrefix+'.A', 'w')
	fpDiploid1 = open(diploidFilePrefix+'.a', 'w')
	for line in fpVariants:
		line = line.strip()
		words = line.split('\t')
		if words[5] == 'HOM':
			print >>fpDiploid0, line
			print >>fpDiploid1, line
		elif words[5] == 'HET':
			if random.random() < 0.5:
				print >>fpDiploid0, line
			else:
				print >>fpDiploid1, line

	fpDiploid0.close()
	fpDiploid1.close()
	fpVariants.close() 

if __name__ == '__main__':
	usage = 'diploid <variants.txt> <diploidPrefix>'
	if len(sys.argv) < 3:
		print >>sys.stderr, usage
		sys.exit(1)
	diploid(sys.argv[1], sys.argv[2])
