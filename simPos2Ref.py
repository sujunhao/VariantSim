import sys
import bisect
import read_ann
from readfq import readfq
def createPosMap(posRef,posSim, ann):
    if ann.ref_chr in posRef:
        posRef[ann.ref_chr].append(ann.ref_start)
        posSim[ann.ref_chr].append(ann.sim_start)
    else:
        posRef[ann.ref_chr] = []
        posSim[ann.ref_chr] = []
        posRef[ann.ref_chr].append(ann.ref_start)
        posSim[ann.ref_chr].append(ann.sim_start)

def simPos2Ref(chrom, posInSim, posRef, posSim):
    posSimList = posSim[chrom]
    i = bisect.bisect_right(posSimList, posInSim)
    if i >= len(posRef[chrom]):
        print >>sys.stderr, 'len of posRef '+str(len(posRef[chrom])) 
        print >>sys.stderr, i
        #sys.exit(1)
        return 0  
    eventPosInRef = posRef[chrom][i]
    eventPosInSim = posSim[chrom][i]
    print chrom, posInSim, eventPosInSim, eventPosInRef, eventPosInRef - (eventPosInSim - posInSim)


    return  eventPosInRef - (eventPosInSim - posInSim)

#INPUT: read.fq ann
usage = 'simPos2Ref.py <Read1.fq> <Read2.fq> <Ann> <ConvertCoordinateNamePrefix>'
if __name__ == '__main__':
    if len(sys.argv) <4:
        print >>sys.stderr, usage
        sys.exit(1)
    fp_in_r1 = open(sys.argv[1], 'r')
    fp_in_r2 = open(sys.argv[2], 'r')
    fp_ann = open(sys.argv[3], 'r')
    fp_out_r1 = open(sys.argv[4]+'1.fq', 'w') 
    fp_out_r2 = open(sys.argv[4]+'2.fq', 'w') 
    #Read Ann
    posRef, posSim = {}, {}
    for line in fp_ann:
        a = read_ann.ann(line)
        createPosMap(posRef, posSim, a)
        #print posRef, posSim
    #convert read1
    tot_num = 0
    for name, seq, qual in readfq(fp_in_r1):
        words = name.split('_')
        chrom = words[0]
        simPos0 = int(words[1])
        simPos1 = int(words[2])

        refPos0 = simPos2Ref(chrom, simPos0, posRef, posSim)
        
        refPos1 = simPos2Ref(chrom, simPos1, posRef, posSim)

        words[1], words[2] = str(refPos0), str(refPos1)
        name = ''
        for i in words:
            name += i +'_'
        name = name.rstrip('_')

        if qual != None:
            print >>fp_out_r1, '@'+name
            print >>fp_out_r1, seq
            print >>fp_out_r1, '+'
            print >>fp_out_r1, qual
        else:
            print >>fp_out_r1, '>'+name
            print >>fp_out_r1, seq
        tot_num +=1
        if tot_num %10000 ==0:
            print>>sys.stderr, '%d reads has been converted'%(tot_num)
    print>>sys.stderr, '%d reads has been converted in file %s'%(tot_num, sys.argv[1])
    tot_num = 0
    for name, seq, qual in readfq(fp_in_r2):
        words = name.split('_')
        chrom = words[0]
        simPos0 = int(words[1])
        simPos1 = int(words[2])
        refPos0 = simPos2Ref(chrom, simPos0, posRef, posSim)
        refPos1 = simPos2Ref(chrom, simPos1, posRef, posSim)
        words[1], words[2] = str(refPos0), str(refPos1)
        name = ''
        for i in words:
            name += i +'_'
        name = name.rstrip('_')
        if qual != None:
            print >>fp_out_r2, '@'+name
            print >>fp_out_r2, seq
            print >>fp_out_r2, '+'
            print >>fp_out_r2, qual
        else:
            print >>fp_out_r2, '>'+name
            print >>fp_out_r2, seq
        tot_num +=1
        if tot_num %10000 ==0:
            print>>sys.stderr, '%d reads has been converted'%(tot_num)
    print>>sys.stderr, '%d reads has been converted in file %s'%(tot_num, sys.argv[2])


    fp_in_r1.close()
    fp_in_r2.close()    
    fp_ann.close()
    fp_out_r1.close()
    fp_out_r2.close()
        