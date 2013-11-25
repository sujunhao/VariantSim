def read_ann_chrom(fp):
	sim_pos_list= []
	last_chr = None
	for line in fp:
		if len(line) == 0:#EOF
			break
		words = line.strip().split('\t')
		if last_chr == None or words[0] == last_chr:
			sim_pos_list.append(int(words[7]), int(words[8]))
			last_chr = words[0]
		if words[0] != last_chr:
			fp.seek(-len(line),1)
	return sim_pos_list
class ann:
	def __init__(self, line):
		words = line.strip().split('\t')
		self.ref_chr =words[0]
		self.ref_start = int(words[1])		
		self.ref_end = int(words[2])
		self.var_len = int(words[3])
		self.var_type = words[4]
		self.HOM_HET = words[5]
		self.var_seq = words[6]
		self.sim_start = int(words[7])
		self.sim_end = int(words[8])