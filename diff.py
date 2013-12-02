from readfq import readfq
def diffSeq(line, fnRef, fnSim):
    MaxPrintChars = 100
    
    fpRef = open(fnRef, 'r')
    fpSim = open(fnSim, 'r')
    words = line.strip().split()

    chrom = words[0]
    refPos0 = int(words[1])
    refPos1 = int(words[2])
    simPos0 = int(words[7])
    simPos1 = int(words[8])

    print line.strip()
    print '---------'
    if refPos1 - refPos0 +1 < MaxPrintChars and simPos1 - simPos0+1 < MaxPrintChars:
        for name, seq, qual in readfq(fpRef):
            if name == chrom:
                print seq[refPos0-1: refPos1]
                break
        for name, seq, qual in readfq(fpSim):
            if name == chrom:
                print seq[simPos0-1: simPos1]
                break
    fpRef.close()
    fpSim.close()

fnRef = './DonorSim_1.2/Demo/chr1_hg18_100000_lines.fa'
fnSim = 'test.sim_genome.fa'

usage = 'diff <sim_ann>'
import sys 
if __name__ == '__main__':
    #print variant region seq in original genome and simulate geenome
    #
    if len(sys.argv) <2 :
        print usage
        sys.exit(1)
    
    fp = open(sys.argv[1])
    for line in  fp:
        print '=================================='
        diffSeq(line, fnRef, fnSim)
    fp.close()
