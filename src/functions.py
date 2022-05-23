import numpy as np
import time
import sys
from error import exit_with_error

def otsu_threshold(Array = None, Verbose=False):
    """
    ARGS:
        Array   : numpy array to compute threshold on
        Verbose : boolean, if True print diagnostics
    RETURN:
        kopt    : Otsu threshold
        s2_b_max: 
    DESCRIPTION:
        Computes Otsu threshold on a numpy array. See "A Threshold Selection
        Method from Gray-Level Histograms" by Nobuyuki Otsu 
        DOI : 10.1109/TSMC.1979.4310076
    DEBUG:
        1. Checked that cntPerVal, probPerVal, w0, w1 are correctly computed
        2. Checked w0 + w1 = 1
        3. Checked that equation 5 holds, i.e. that we did compute w0,w1,u0,u1
           correctly. So...
                Sum_{k+1}^{L} i*p_{i}/w1 == (uT - u0*w0)/(1 - w0)
        4. Checked that w0*u0 + w1*u1 == uT (equation 9)
        5. Checked that s2_w + s2_b = s2_t holds for each value of k (eqn 16).
           This wouldn't  work if s2_0, s2_1, s2_w, s2_b and s2_t weren't
           correct.
        6. Spot checked with my init_test_array(), and it correctly selects the
           optimal k value
        7. Previously, if valMin was not 0, cntPerVal and propPerVal would overstep
           their bounds
        8. Tested with data read from matlab_int files and vtk files, both
           types work correctly.
        9. Added ability to handle instance where voxels can only one of two values

    FUTURE:
        1. Print out min,max,probPerVal and cntPerVal details
    """
    print("     Computing Otsu Thresholding...")
    print("          Start : %s"%(time.strftime("%D:%H:%M:%S")))
    array   = Array if Array is not None else exit_with_error("ERROR in Array!\n")
    array   = array.astype(np.int64)       # Cast as int so this works
    dim     = array.shape
    minVal  = np.min(array)
    #array   = array + np.abs(minVal)
    #minVal  = minVal+ np.abs(minVal)    # Reset zero so it works w/ legacy code
    maxVal  = np.max(array)             # Max value in array
    uT      = np.mean(array)            # Total mean
    nBin    = maxVal - minVal + 1
    valA    = np.full(nBin, range(minVal, maxVal+1))
    cntPerVal = np.zeros(nBin, dtype=np.int)   # Each int maps to range [Min,Max]
    probPerVal= np.zeros(nBin, dtype=np.float) # Each int maps to range [Min,Max]
    if(len(dim) == 3):
        N = dim[0] * dim[1] * dim[2]
    elif(len(dim) == 2):
        N = dim[0] * dim[1]
    kopt = 0                            # Optimal value of k
    s2_b_max = 0

    ### Bin counts -
    #   NOTE : that the arrays uValA,uCountA returned by np.unique() aren't
    #          necessarily the same length as cntPerVal, probPerVal or valA.
    #          This is why we have the nested loops to map them correctly
    uValA,uCountA = np.unique(array, return_counts=True)# returns (valuesA,counts)
    for idx in range(len(valA)):
        for uIdx in range(len(uValA)):
            if(valA[idx] == uValA[uIdx]):
                cntPerVal[idx]  = uCountA[uIdx]        # 
                # Compute probabilities (eqn 1)
                ### NOTE : 
                # probPerVal[0]      maps to minVal
                # probPerVal[nBin-1] maps to maxVal
                probPerVal[idx] = cntPerVal[idx] / float(N)     # (eqn 1)            

    ### Error Check 
    # Check data type
    if(array.dtype != np.int64 and array.dtype != np.uint8):
        exit_with_error("ERROR!! data is of incorrect type. np.int64 wanted {}"
                   " given!\n".format(array.dtype))
    # Confirm that uT makes sense w/r/t probPerVal
    iV = np.full(nBin, range(minVal,maxVal+1))
    if(np.isclose(np.dot(iV,probPerVal), uT, rtol=10**-6, atol=10**-8) == False):
        exit_with_error("ERROR!!! iV*probPerVal ({}) != uT ({})".format(
                        np.dot(iV,probPerVal), uT))

    # Stdev for ALL data
    iV  = np.full(nBin, range(minVal,maxVal+1))
    iV = (iV - uT)**2
    s2_t = np.dot(iV,probPerVal)                  # (eqn 15)

    # Loop through thresholds, k....avoid k=0,valMax
    for idx in range(0, nBin):
        k = valA[idx]
    
        # Skip boundary
        if(k==maxVal):
            continue

        # Group 0 is at or below threshold
        p0V = probPerVal[0:idx+1]                 # Prob of values at or below thresh
        w0 = sum(p0V)                             # (eqn 2)
        iV = np.full(k+1, range(0,k+1))           # i'th vector for values <= k
        u0 = np.dot(iV, p0V) / w0                 # (eqn 4)
        s2_0 = np.dot((iV - u0)**2, p0V) / w0     # (eqn 10)

        # Group 1 is at or below threshold
        p1V = probPerVal[idx+1:nBin]
        w1  = sum(p1V)                            # (eqn 3)
        iV = np.full(maxVal-k, range(k+1,maxVal+1)) # i'th vector for values > k
        u1 = np.dot(iV, p1V) / w1                 # (eqn 5)
        s2_1 = np.dot((iV - u1)**2, p1V) / w1     # (eqn 11)

        s2_w = w0 * s2_0 + w1 * s2_1              # (eqn 13)
        #s2_b = w0 * (u0 - uT)**2 + w1 * (u1 - uT)**2
        s2_b = w0 * w1 * (u1 - u0)**2             # (eqn 14)

        # (eqn 19)
        if(s2_b > s2_b_max):
            s2_b_max = s2_b
            kopt = k

        ##### Error / Sanity Check
        #if(k>=255):
        #    exit_with_error("ERROR!!! k ({}) > 255\n".format(k))
        # (eqn 9a)
        if(np.isclose(w0*u0 + w1*u1, uT, rtol=10**-6, atol=10**-8) == False):
            exit_with_error("ERROR!!! w0*u0+w1*u1 ({}) != uT ({})\n".format(
                            w0*u0 + w1*u1,uT))
        # (eqn 9b)
        if(np.isclose(w0 + w1, 1.0, rtol=10**-6, atol=10**-8) == False):
            exit_with_error("ERROR!!! w0+w1 ({}) != 1\n".format(w0*w1))

        # (eqn 16)
        if(np.isclose(s2_w + s2_b, s2_t, rtol=10**-6, atol=10**-8) == False):
            exit_with_error("ERROR!!! s2_w + s2_b ({}) != s2_t ({})\n".format(
                            s2_w+s2_b, s2_t))

        if(Verbose == True):
            print("{:<}  w0: {:<5.3f}  w1: {:<5.3f}  u0: {:<5.3f}  "
                  "u1: {:<5.3f}  s2_0: {:<5.3f}  s2_1: {:<5.3f}  "
                  "s2_w: {:<5.3f}  s2_b: {:<5.3f}  sum: {:<5.3f}".format(k,w0,w1,u0,
                   u1,s2_0,s2_1,s2_w,s2_b, s2_w + s2_b))
    # Diagnostics
    #print(cntPerVal)
    #print(probPerVal)
    #print(s2_t)
    #print(kopt)
    if(kopt == 0):
        sys.stderr.write("\n"
                         "     ****************************************************\n"
                         "     WARNING!!! kopt = 0, probably b/c there aren't many\n"
                         "                values > 0?\n"
                         "     ***************************************************\n\n")
        #kopt = 1    # <---- NEED to FIX

    print("          End : %s"%(time.strftime("%D:%H:%M:%S")))
    print("          kopt = {}, s2_b_max = {}\n".format(kopt,s2_b_max))
    return(kopt, s2_b_max)



