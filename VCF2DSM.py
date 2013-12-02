usage ='%VCF2DSM.py <file.vcf>'
import sys
if __name__ == '__main__':
	if len(sys.argv) < 2:
		print >>sys.stderr, 'CMD ERROR!'
		print >>sys.stderr, usage
		sys.exit(1)
	fp = open(sys.argv[1])
	for line in fp:
		line = line.strip()
		#skip meta-info and header
		if line[0] =='#':
			continue
		words = line.split('\t')
		VT_start = words[7].find('VT=')+len('VT=')
		if words[7][VT_start:].find(';') == -1:
			VT_length = len(words[7][VT_start:])
		else:
			VT_length = words[7][VT_start:].find(';')
		VT = words[7][VT_start:VT_start+VT_length]#variant type
		chrom, pos_start, pos_end, VT_size, VT_name, hom_het, ALT = None, None, None,None,None,None,None 
		if VT == 'SNP':
			chrom = words[0]
			pos_start= int(words[1])-1
			pos_end = int(words[1])+1
			VT_size = 1
			VT_name = 'SNV'
			GT=words[9].split(':')[0]
			if len(GT) ==1 or GT == '1|1': #haploid or homozygous diploid
				hom_het = 'HOM' #fix me 
			elif GT == '0|1' or GT == '1|0':#heterozygous diploid 
				hom_het = 'HET'
			else:
				print >>sys.stderr, '>>genotype Error'
				print >>sys.stderr, line
				continue
			ALT = words[4]
			print '%s\t%d\t%d\t%d\t%s\t%s\t%s'%(chrom, pos_start, pos_end, VT_size, VT_name, hom_het, ALT) 
		elif VT == 'INDEL':
			chrom = words[0]
			if len(words[3]) > len(words[4]):#DEL
				pos_start = int(words[1])
				pos_end = pos_start+len(words[3])
				VT_size =len(words[3]) -1
				VT_name = 'DEL'
				if len(GT) ==1 or GT == '1|1': #haploid or homozygous diploid
					hom_het = 'HOM' #fix me 
				elif GT == '0|1' or GT == '1|0':#heterozygous diploid 
					hom_het = 'HET'
				else:
					print >>sys.stderr, '>>genotype Error'
					print >>sys.stderr, line
					continue
				ALT = '*'
			else:#INS
				pos_start = int(words[1])
				pos_end = pos_start+1
				VT_size =len(words[4]) -1
				VT_name = 'INS'
				if len(GT) ==1 or GT == '1|1': #haploid or homozygous diploid
					hom_het = 'HOM' #fix me 
				elif GT == '0|1' or GT == '1|0':#heterozygous diploid
					hom_het = 'HET'
				else:
					print >>sys.stderr, '>>genotype Error'
					print >>sys.stderr, line
					continue
				ALT = words[4][1:]#strip the first char
			print '%s\t%d\t%d\t%d\t%s\t%s\t%s'%(chrom, pos_start, pos_end, VT_size, VT_name, hom_het, ALT) 
		elif VT == 'SV':
			pass
		else:
			print >>sys.stderr, '>>variant type Error', VT
			print >>sys.stderr, line
	fp.close()
