# python3
import sys
from copy import deepcopy
def InverseBWT(bwt):
    # write your code here

    M = [[] for i in range(len(bwt))]
    bwt = [[bwt[i]] for i in range(len(bwt))]

    for i in range(len(bwt)):
        
        bwt_copy = deepcopy(bwt)      

        for j in range(len(bwt)):

            bwt_copy[j].extend(M[j])
        
        
        M = bwt_copy
        print(M)

        M.sort()  
           
    return ''.join(M[0][1:]) + '$'

def InverseBWT_fast(bwt):
    # write your code here

    
    last = range(len(bwt))
    first = sorted(range(len(bwt)), key=lambda i: bwt[i])

    first_to_last = {first[i] : last[i] for i in range(len(bwt))}

    index = first[0]
    res = ''
    
    for i in range(len(bwt)):
        index = first_to_last[index]
        res += bwt[index]

    return res[-2::-1] + '$'




if __name__ == '__main__':
    bwt = sys.stdin.readline().strip()
    print(InverseBWT_fast(bwt))