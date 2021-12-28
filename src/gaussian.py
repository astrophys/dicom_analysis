import sys
import numpy as np
from error import exit_with_error

def gaussian_derivative_1D(X=None, Mu=None, S=None):
    """
    ARGS:
        X       =  (float), location to evaluate derivative
        Mu      =  (float), center of gaussian function
        S       =  (float), sigma, i.e. describes width of gaussian
    DESCRIPTION:
        This takes the analytic form of the derivative w/r/t X of a Gaussian 
        function and returns it's value evaluated at X
    RETURN:
        A float
    NOTES:
        equivalent to derivative_of_gaussian() in SEGMENT_gsl/parallel/vessels
    DEBUG:
    FUTURE:
        1. Figure out why I'm off by a negative here
    """
    return( (1/(S**3 * np.sqrt(2 * np.pi)) * (Mu - X) * np.exp(-(X-Mu)**2 / (2*S**2))))
    



def gaussian_derivative_kernel(N=None, S=None):
    """
    ARGS:
        N       = (int), Number of elements in kernel, MUST BE ODD, so the center is well
                  defined
        S       = (float), Sigma, i.e. describes width of gaussian
    DESCRIPTION:
        This function returns a numpy vector (i.e. the 'kernel') with the values 
        of the gaussian derivative evaluated at the distance from central point in
        the vector (i.e. why N must be ODD). The kernel is used to compute the
        derivative of the image at every point.
    RETURN:
        Numpy vector, the kernel
    NOTES:
        equivalent to derivative_gaussian_kernel() in SEGMENT_gsl/parallel/vessels
    DEBUG:
    FUTURE:
    """
    if(N % 2 == 0):
        exit_with_error("ERROR!!! N ({}) must be ODD\n".format(N))
    kernelV = np.zeros([N])
    c = int(np.floor(N/2))    # Get Center of kernel
    for i in range(N):
        kernelV[i] = gaussian_derivative_1D(X=i, Mu=c, S=S)
    return(kernelV)


def gaussian_derivative_of_tensor(DataT=None, Axis=None, S=None, Verbose=False):
    """
    ARGS:
        DataT   = (2D or 3D Numpy array), Input data to differentiate
        Axis    = (int), either 0,1,2 corresponding to x,y,z respectively. It is 
                   the direction along which to differentiate
        S       = (float), Sigma, i.e. describes width of gaussian
    DESCRIPTION:
        This function returns a numpy array (either 2D or 3D) with the values 
        differentiated along the axis of choice.
    RETURN:
        Numpy array, 2D or 3D numpy array
    NOTES:
        equivalent to gaussian_derivative() in
        SEGMENT_gsl/parallel/vessels/src/gaussian_smoothing.c
    DEBUG:
        1. Using testT[i,j,k] = 2*i + j*j + 3*k*k*k, I tested the derivative
           in x,y and z. When fully w/in range of sliceV, it gets the magnitude
           of the derivative correct.
        
           E.g. 
                d(testT)/dx         = -1.9913,  should be 2.0
                d(testT)/dy|_{y=4}  = -7.9651,  should be 8.0
                d(testT)/dz|_{z=4}  = -152.1613 should be 144

           Clearly it does pretty well in the x and y axis b/c the function is
           moderately changing. Clearly it is too low resolution for resolving the 
           fast changing z-axis.
        
    FUTURE:
    """
    nSig        = 3                     # Number of sigma to use for kernelWidth
    kW          = int(2 * nSig * S + 1) # 3 sigma left of center, 3 sigma right of center
    hW          = int(nSig * S)         # Get the 'half kernel width'
    kernelV     = gaussian_derivative_kernel(N=kW, S=S)
    shape       = DataT.shape
    derivT      = np.zeros(shape)
    ## 3D
    if(len(DataT.shape) == 3):
        for i in range(shape[0]):
            for j in range(shape[1]):
                for k in range(shape[2]):
                    chunkV =np.zeros([kW])   # Chunk of data to compute deriv on

                    # Handle boundary conditions, basically set to 0 outside of image
                    if(Axis == 'x' or Axis == 0):
                        sliceV = DataT[:,j,k]
                        # Check bounds
                        low = i - hW
                        up  = shape[0] - (i + hW + 1)
                        idx = i             # 'idx' instead of i to generalize below
                    elif(Axis == 'y' or Axis == 1):
                        sliceV = DataT[i,:,k]
                        # Check bounds
                        low = j - hW
                        up  = shape[1] - (j + hW + 1)
                        idx = j             # 'idx' instead of j to generalize below
                    elif(Axis == 'z' or Axis == 2):
                        sliceV = DataT[i,j,:]
                        # Check bounds
                        low = k - hW
                        up  = shape[2] - (k + hW + 1)
                        idx = k             # 'idx' instead of k to generalize below
                    else:
                        exit_with_error("ERROR!!! {} is invalid Axis in 3D".format(Axis))
                    ###### Assign data from DataT to chunkV ######
                    #### Conditions :
                    #### 1. chunkV[] should be 'centered' on sliceV[idx]
                    #### 2. if chunkV[] overruns bounds of sliceV[], leave the 'hanging'
                    ####    ends of chunkV[] as '0'
                    #### 3. Using testT from dicom_analysis.py
                    # comfortably w/in DataT bounds, e.g. 
                    # E.g. idx = 5, low=2, up=1
                    #
                    #                   low=2                idx == 5              up=1
                    #                   ___|___                 ||                  _|_
                    #                  |       |                \/                 |   |
                    #  chunkV = array(          [ 4.,  6.,  8., 10., 12., 14., 16.])
                    #  sliceV = array([ 0.,  2.,  4.,  6.,  8., 10., 12., 14., 16., 18.])
                    if(low >= 0 and up >= 0):
                        chunkV = sliceV[(idx-hW):(idx+hW+1)]    # Check bounds here
                    # E.g. idx = 2, low=-1, up=4
                    # 
                    #                 low=-1    idx == 2
                    #                  _|_         ||
                    #                 |   |        \/
                    #  chunkV = array([ 0,  0,  2,  4,  6,  8,  10 ])
                    #  sliceV = array(    [ 0,  2,  4,  6,  8,  10,  12,  14,  16,  18])
                    elif(low < 0):
                        chunkV[abs(low):] = sliceV[0:(kW+low)]      # recall low < 0
                    # E.g. idx = 8        
                    #
                    #                                                 idx == 2     up == -2
                    #                                                     ||        __|__
                    #                                                     \/       |     |
                    #  chunkV = array(                     [10,  12,  14, 16,  18,  0,  0 ])
                    #  sliceV = array([ 0,  2,  4,  6,  8,  10,  12,  14, 16,  18])
                    elif(up < 0):
                        chunkV[:up] = sliceV[idx-hW:]
                    if(Verbose == True):
                        print("({:<2d} {:<2d} {:<2d}) : d/dx = {:<.4f}".format(i,j,k,
                              np.dot(chunkV, kernelV)))
    ## 2D
    if(len(DataT.shape) == 2):
        for i in range(shape[0]):
            for j in range(shape[1]):
                chunkV =np.zeros([kW])   # Chunk of data to compute deriv on
                # Handle boundary conditions, basically set to 0 outside of image
                if(Axis == 'x' or Axis == 0):
                    sliceV = DataT[:,j]
                    # Check bounds
                    low = i - hW
                    up  = shape[0] - (i + hW + 1)
                    idx = i             # 'idx' instead of i to generalize below
                elif(Axis == 'y' or Axis == 1):
                    sliceV = DataT[i,:]
                    # Check bounds
                    low = j - hW
                    up  = shape[1] - (j + hW + 1)
                    idx = j             # 'idx' instead of j to generalize below
                else:
                    exit_with_error("ERROR!!! {} is invalid Axis in 3D".format(Axis))
                #
                # See comments above in 3D conditional for relevant debugging details
                #
                if(low >= 0 and up >= 0):
                    chunkV = sliceV[(idx-hW):(idx+hW+1)]    # Check bounds here
                elif(low < 0):
                    chunkV[abs(low):] = sliceV[0:(kW+low)]      # recall low < 0
                elif(up < 0):
                    chunkV[:up] = sliceV[idx-hW:]
                if(Verbose == True):
                    print("({:<2d} {:<2d} : d/dx = {:<.4f}".format(i,j,
                          np.dot(chunkV, kernelV)))
    ## 1D
    if(len(DataT.shape) == 1):
        for i in range(shape[0]):
            chunkV =np.zeros([kW])   # Chunk of data to compute deriv on
            # Handle boundary conditions, basically set to 0 outside of image
            if(Axis == 'x' or Axis == 0):
                sliceV = DataT[:]
                # Check bounds
                low = i - hW
                up  = shape[0] - (i + hW + 1)
                idx = i             # 'idx' instead of i to generalize below
            else:
                exit_with_error("ERROR!!! {} is invalid Axis in 1D".format(Axis))
            #
            # See comments above in 3D conditional for relevant debugging details
            #
            if(low >= 0 and up >= 0):
                chunkV = sliceV[(idx-hW):(idx+hW+1)]    # Check bounds here
            elif(low < 0):
                chunkV[abs(low):] = sliceV[0:(kW+low)]      # recall low < 0
            elif(up < 0):
                chunkV[:up] = sliceV[idx-hW:]
            if(Verbose == True):
                print("({:<2d} : d/dx = {:<.4f}".format(i, np.dot(chunkV, kernelV)))
        


def hessian(String):
    """
    ARGS:
    DESCRIPTION:
    RETURN:
    DEBUG:
    FUTURE:
    """
    sys.stderr.write(String)
