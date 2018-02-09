def ebf(nNodes, depth, precision=0.01):
    # note the high estimates. Wonder if we can use some n-ary tree semantics to arrive at better estimates.
    endEstimate = nNodes
    return ebfHelper(1, endEstimate, nNodes, depth, precision)

def ebfHelper(start, end, nNodes, depth, precision=0.01):
    if end == 0 :
        return 0
    mid = (start + end)/2
    if ( end - start < precision ):
        return mid
    #nEstimate = ((mid**(depth+1)-1))/(mid -1)
    nEstimate = ebfSummer(mid, depth)
    if (nEstimate < nNodes):
        return ebfHelper(mid, end, nNodes, depth, precision)
    else:
        return ebfHelper(start, mid, nNodes, depth, precision)
    
def ebfSummer(b, d):
    total=1
    term=1
    for i in  range(d):
        term = term*b
        total += term        
    return total
