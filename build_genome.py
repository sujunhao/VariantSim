import sys
from readfq import readfq


class var():
    def __init__(self, line):
        if len(line) == 0:
            return (None, None, None, None, None, None, None)
        words = line.strip().split('\t')
        self.chr, self.type, self.HOM_HET, self.seq = words[0], words[4], words[5], words[6]
        self.pos_start, self.pos_end, self.len = int(words[1]), int(words[2]),\
                                                 int(words[3])
# Variants.txt and Ref should be sorted by chrom
# Note Variatnts.txt
# chrom  pos_start pos_end variant_len variant_type HOM/HET seq

usage = 'build_genome <Ref> <Variants.txt> <Prefix.out>'
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print usage
        sys.exit(1)

    fp_ref = open(sys.argv[1], 'r')
    fp_var = open(sys.argv[2], 'r')
    fp_sim_genome = open(sys.argv[3]+".simGenome.fa", 'w')
    fp_sim_ann = open(sys.argv[3]+".simAnn", 'w')
    sim_genome = ''

    cur_var = None
    line = fp_var.readline().strip()
    if len(line) == 0:
        print >>sys.stderr, "File %s is empty" % (sys.argv[2])
        sys.exit(1)
    cur_var = var(line)
    for chrom, seq, qual in readfq(fp_ref):
        sim_genome_len = 0
        sim_genome = ''
        non_variant_region_start = 1
        non_variant_region_end = 1
        sim_start = -1
        sim_end = -1
        while cur_var.chr == chrom:
            non_variant_region_end = cur_var.pos_start

            if cur_var.type == 'SNV' or cur_var.type == 'SNP':
                sim_genome += seq[non_variant_region_start-1:non_variant_region_end] + cur_var.seq
                sim_genome_len += non_variant_region_end - non_variant_region_start +1 +1
                #print >>sys.stderr, '>Ref_%d_%d\n%s'%(non_variant_region_start-1, non_variant_region_end+1, seq[non_variant_region_start-1:non_variant_region_end+1])
                #print >>sys.stderr, '@Sim SNP\n%s'%(seq[non_variant_region_start-1:non_variant_region_end]+cur_var.seq)

                #print >>fp_sim_ann, "%s\t%d\t%d"%(line, sim_genome_len - 1, sim_genome_len+1)
            elif cur_var.type == 'INS':
                sim_genome += seq[non_variant_region_start-1:non_variant_region_end]+cur_var.seq
                sim_genome_len += non_variant_region_end - non_variant_region_start +1+cur_var.len
                #print >>sys.stderr, '>Ref_%d_%d\n%s'%(non_variant_region_start-1, non_variant_region_end,seq[non_variant_region_start-1:non_variant_region_end])
                #print >>sys.stderr, '@Sim INS%d\n%s'%(cur_var.len,seq[non_variant_region_start-1:non_variant_region_end]+cur_var.seq)
                print >>fp_sim_ann, "%s\t%d\t%d"%(line, sim_genome_len - cur_var.len, sim_genome_len+1)
            elif cur_var.type == 'DEL':
                sim_genome += seq[non_variant_region_start-1:non_variant_region_end]
                sim_genome_len += non_variant_region_end - non_variant_region_start+1
                #print >>sys.stderr, '>Ref_%d_%d\n%s'%(non_variant_region_start-1, non_variant_region_end+cur_var.len, seq[non_variant_region_start-1:non_variant_region_end]+seq[cur_var.pos_start:cur_var.pos_end])
                #print >>sys.stderr, '@Sim DEL%d\n%s'%(cur_var.len, seq[non_variant_region_start-1:non_variant_region_end])
                print >>fp_sim_ann, "%s\t%d\t%d"%(line, sim_genome_len, sim_genome_len+1)
            elif cur_var.type == 'MERGE_INDEL':
                pass
            else:
                print >>sys.stderr, 'unknown variant type %s' % (cur_var.type)
            non_variant_region_start = cur_var.pos_end

            line = fp_var.readline().strip()
            if len(line) == 0:
                break
            cur_var = var(line)
        sim_genome += seq[non_variant_region_start-1:]
        sim_genome_len = len(sim_genome)
        #output sim genome 70 chars per line
        print >>fp_sim_genome, '>'+chrom
        i = 0
        while i < sim_genome_len:
            print >>fp_sim_genome, sim_genome[i:i+70]
            i += 70
        if i != sim_genome_len:
            print >>fp_sim_genome, sim_genome[i:]

    fp_sim_genome.close()
    fp_sim_ann.close()
    fp_ref.close()
    fp_var.close()
