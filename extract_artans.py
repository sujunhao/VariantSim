import sys
import itertools
usage = 'extract_artans.py <read1.aln> <read2.aln>'
class header():
	def __init__(self):
		self.readLen = -1
		self.chromMap = {}
	def addChrom(self, chrom, len):
		self.chromMap[chrom] = len
	def setRlen(self, readLen):
		self.readLen = readLen
	def setCmd(self, cmd):
		self.cmd = cmd
def read_header(fp):
	h = header() 
	for line in fp:
		words = line.strip().split()
		if words[0] == '##ART_Illumina':
			h.setRlen(int(words[2]))
		elif words[0] == '##Header':
			return h
		elif words[0] == '@SQ':
			h.addChrom(words[1], int(words[2]))
		elif words[0] == '@CM':
			h.setCmd(words[1])
	print >>sys.stderr, '[Error] func read_header shouldn\'t go here'
	sys.exit(1)


if __name__ == '__main__':
	if len(sys.argv) < 3:
		print >>sys.stderr, usage
		sys.exit(1)
	fp1 = open(sys.argv, 'r')
	fp2 = open(sys.argv, 'r')
	#read header
	h1 = read_header(fp1)
	h2 = read_header(fp2)
	#core loop
	for line1, line2 in itertools.izip(fp1, fp2):
		if line1[0] != '>':
			continue
		line1 = line1.strip()[1:]
		line2 = line2.strip()[1:]
		#print line1.split()
		chrom1, name1, pos1, strand1 = line1.split()
		chrom2, name2, pos2, strand2 = line2.split()
		if chrom1 != chrom2:
			print >>sys.stderr, '[Error] chrom not match'
			sys.exit()
		pos1, pos2 = int(pos1), int(pos2)
		if strand1 =='+' and strand2 =='-':
			pos2 = h2.chromMap[chrom2] - pos2+1+h2.readLen-1
			print '%s\t%d\t%d'%(chrom1, pos1, pos2)
		else:
			pos1 = h1.chromMap[chrom1] - pos1+1+h1.readLen-1
			print '%s\t%s\t%d'%(chrom1, pos2, pos1)

	fp1.close()
	fp2.close()