import sys
import bisect
import read_ann
from readfq import readfq


def createPosMap(ann, posRefStart, posRefEnd, posSimStart, posSimEnd):
    '''create postion map'''
    posRefStart.setdefault(ann.ref_chr, []).append(ann.ref_start)
    posRefEnd.setdefault(ann.ref_chr, []).append(ann.ref_end)
    posSimStart.setdefault(ann.ref_chr, []).append(ann.sim_start)
    posSimEnd.setdefault(ann.ref_chr, []).append(ann.sim_end)


def simPos2Ref( chrom, posInSim,
                posRefStart, posRefEnd, 
                posSimStart, posSimEnd, 
                fp_answer):
    '''convert pos in simulate genome coord to orignal genome coord'''
    posSimStartVec = posSimStart[chrom]
    posSimEndVec = posSimEnd[chrom]
    posRefStartVec = posRefStart[chrom]
    posRefEndVec = posRefEnd[chrom]
    eventPosInRef, eventPosInRef, ret_pos = 0, 0, 0

    i = bisect.bisect_right(posSimStartVec, posInSim)
    l_posRef = len(posSimStartVec)

    if i > l_posRef:
        print >>sys.stderr, '%d > len(posRef) %d' % (i, l_posRef)
        print >>sys.stderr, i
        sys.exit(1)
    elif i == 0:
        eventPosInRef = posRefStartVec[i]
        eventPosInSim = posSimStartVec[i]
        ret_pos = eventPosInRef - (eventPosInSim - posInSim)
    elif i < l_posRef:
        if posSimEndVec[i-1] <= posInSim:
            eventPosInRef = posRefStartVec[i]
            eventPosInSim = posSimStartVec[i]
            ret_pos = eventPosInRef - (eventPosInSim - posInSim)

        elif posInSim == posSimStartVec[i-1]:
            eventPosInRef = posRefStartVec[i-1]
            eventPosInSim = posInSim
            ret_pos = eventPosInRef - (eventPosInSim - posInSim)
        elif posInSim > posSimStartVec[i-1]:
            #
            if posSimEndVec[i-1] - posSimStartVec[i-1] ==\
               posRefEndVec[i-1] - posRefStartVec[i-1]:
                pass
            # DEL
            elif posSimEndVec[i-1] - posSimStartVec[i-1] == 1 and\
                    posRefEndVec[i-1] - posRefStartVec[i-1] > 2:
                print >>sys.stderr, 'Pos shouldn\'t be in DEL region'
                sys.exit(1)
            # INS
            elif posRefEndVec[i-1] - posRefStartVec[i-1] == 1 and\
                    posSimEndVec[i-1] - posSimStartVec[i-1] > 2:
                eventPosInRef = posRefEndVec[i-1]
                eventPosInSim = posSimEndVec[i-1]
                ret_pos = eventPosInRef - (eventPosInSim - posInSim)
            else:
                print >>sys.stderr, '[Pos Error0]: posInSim = %d' % (posInSim)
                print >>sys.stderr, 'posSimStartVec[i-1] = %d' % \
                                    (posSimStartVec[i-1])
                print >>sys.stderr, 'posSimEndVec[i-1] = %d' % \
                                    (posSimEndVec[i-1])
                print >>sys.stderr, 'posSimStartVec[i] = %d' % \
                                    (posSimStartVec[i])
                print >>sys.stderr, 'posSimEndVec[i] = %d' % \
                                    (posSimEndVec[i])
                sys.exit(1)
        else:
            print >>sys.stderr, '[Pos Convert Error]'
            print >>sys.stderr, posInSim
            sys.exit()
    else:   # i == l_posRef
        if posSimEndVec[i-1] < posInSim:
            ret_pos = posRefEndVec[i-1] + posInSim - posSimEndVec[i-1]
        elif posSimEndVec[i-1] == posInSim:
            ret_pos = posRefEndVec[i-1]
        else:  # posSimEndVec[i-1] > posInSim
            #
            if posSimEndVec[i-1] - posSimStartVec[i-1] ==\
               posRefEndVec[i-1] - posRefStartVec[i-1]:
                pass
            #DEL
            elif posSimEndVec[i-1] - posSimStartVec[i-1] == 1 and\
                    posRefEndVec[i-1] - posRefStartVec[i-1] > 2:
                print >>sys.stderr, 'Pos shouldn\'t be in DEL region'
                sys.exit(1)
            #INS
            elif posRefEndVec[i-1] - posRefStartVec[i-1] == 1 and\
                    posSimEndVec[i-1] - posSimStartVec[i-1] > 2:
                eventPosInRef = posRefEndVec[i-1]
                eventPosInSim = posSimEndVec[i-1]
                ret_pos = eventPosInRef - (eventPosInSim - posInSim)
            else:
                print >>sys.stderr, '[Pos Error1]: posInSim = %d' % (posInSim)
                print >>sys.stderr, 'posSimStartVec[i-1] = %d' % \
                                    (posSimStartVec[i-1])
                print >>sys.stderr, 'posSimEndVec[i-1] = %d' % \
                                    (posSimEndVec[i-1])
                print >>sys.stderr, 'posSimStartVec[i] = %d' % \
                                    (posSimStartVec[i])
                print >>sys.stderr, 'posSimEndVec[i] = %d' % \
                                    (posSimEndVec[i])
                sys.exit(1)
    # if i < l_posRef-1:
    #     if eventPosInSim > posSim and posSimStartVec[i+1] >posSim and\
    #         eventPosInSim - posSim >= posSimStartVec[i+1] -posSim:
    #         print chrom, posInSim, eventPosInSim, eventPosInRef,\
    #                eventPosInRef - (eventPosInSim - posInSim)
    return ret_pos

#INPUT: read.fq ann
usage = \
    'simPos2Ref.py <Read1.fq> <Read2.fq> <Ann> <ConvertCoordinateNamePrefix>'
if __name__ == '__main__':
    if len(sys.argv) < 4:
        print >>sys.stderr, usage
        sys.exit(1)
    fp_in_r1 = open(sys.argv[1], 'r')
    fp_in_r2 = open(sys.argv[2], 'r')
    fp_ann = open(sys.argv[3], 'r')
    fp_out_r1 = open(sys.argv[4] + '1.fq', 'w')
    fp_out_r2 = open(sys.argv[4] + '2.fq', 'w')
    fp_ans = open(sys.argv[4] + '.ans', 'w')
    #Read Ann
    posRefStart, posSimStart, posRefEnd, posSimEnd = {}, {}, {}, {}
    for line in fp_ann:
        a = read_ann.ann(line)
        createPosMap(a, posRefStart, posRefEnd, posSimStart, posSimEnd)
        #print posRefEnd, posSimEnd
    #convert read1
    tot_num = 0
    for name, seq, qual in readfq(fp_in_r1):
        words = name.split('_')
        chrom = words[0]
        simPos0 = int(words[1])
        simPos1 = int(words[2])
        refPos0 = simPos2Ref(chrom, simPos0,
                             posRefStart, posRefEnd,
                             posSimStart, posSimEnd, fp_ans)
        refPos1 = simPos2Ref(chrom, simPos1,
                             posRefStart, posRefEnd,
                             posSimStart, posSimEnd, fp_ans)
        words[1], words[2] = str(refPos0), str(refPos1)
        name = ''
        for i in words:
            name += i + '_'
        name = name.rstrip('_')

        if qual is not None:
            print >>fp_out_r1, '@'+name
            print >>fp_out_r1, seq
            print >>fp_out_r1, '+'
            print >>fp_out_r1, qual
        else:
            print >>fp_out_r1, '>'+name
            print >>fp_out_r1, seq
        tot_num += 1
        if tot_num % 10000 == 0:
            print >>sys.stderr, '%d reads has been converted' % (tot_num)
    print >>sys.stderr, '%d reads has been converted in file %s' %\
                        (tot_num, sys.argv[1])
    tot_num = 0
    for name, seq, qual in readfq(fp_in_r2):
        words = name.split('_')
        chrom = words[0]
        simPos0 = int(words[1])
        simPos1 = int(words[2])
        refPos0 = simPos2Ref(chrom, simPos0,
                             posRefStart, posRefEnd,
                             posSimStart, posSimEnd, fp_ans)
        refPos1 = simPos2Ref(chrom, simPos1,
                             posRefStart, posRefEnd,
                             posSimStart, posSimEnd, fp_ans)
        words[1], words[2] = str(refPos0), str(refPos1)
        name = ''
        for i in words:
            name += i + '_'
        name = name.rstrip('_')
        if qual is not None:
            print >>fp_out_r2, '@'+name
            print >>fp_out_r2, seq
            print >>fp_out_r2, '+'
            print >>fp_out_r2, qual
        else:
            print >>fp_out_r2, '>'+name
            print >>fp_out_r2, seq
        tot_num += 1
        if tot_num % 10000 == 0:
            print >>sys.stderr, '%d reads has been converted' % (tot_num)
    print >>sys.stderr, '%d reads has been converted in file %s' %\
                        (tot_num, sys.argv[2])

    fp_in_r1.close()
    fp_in_r2.close()
    fp_ann.close()
    fp_out_r1.close()
    fp_out_r2.close()
    fp_ans.close()
