usage = 'filter_variants.py <Var>'

import sys
if __name__ == '__main__':
    fp = open(sys.argv[1], 'r')
    last_chrom = None
    last_pos0 = None
    last_pos1 = None
    for line in fp:
        line = line.strip()
        words = line.split()
        chrom = words[0]
        pos0 = int(words[1])
        pos1 = int(words[2])
        if last_chrom is None:
            last_chrom = chrom
            last_pos0 = pos0
            last_pos1 = pos1
            print line
            continue
        if last_chrom != chrom or pos0 >= last_pos1:
            last_chrom = chrom
            last_pos0 = pos0
            last_pos1 = pos1
            print line
            continue
        else:
            print >>sys.stderr, line
            continue
    fp.close()
