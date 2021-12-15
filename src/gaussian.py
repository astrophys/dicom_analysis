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
    """
    return( (-1/(S**3 * np.sqrt(2 * np.pi)) * (X - Mu) * np.exp(-(X-Mu)**2 / (2*S**2))))
    



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


def gaussian_derivative_of_tensor(DataT=None, Axis=None, S=None):
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
        equivalent to gaussian_derivative() in SEGMENT_gsl/parallel/vessels
    DEBUG:
    FUTURE:
    """
    nSig        = 3                     # Number of sigma to use for kernelWidth
    kernelWidth = int(2 * nSig * S + 1) # 3 sigma left of center, 3 sigma right of center
    halfKern    = int(nSig * S)         # Get the 'half kernel width'
    kernelV     = gaussian_derivative_kernel(N=kernelWidth, S=S)
    shape       = DataT.shape
    derivT      = np.zeros(shape)
    ## 3D
    if(len(DataT.shape) == 3):
        for i in range(shape[0]):
            for j in range(shape[1]):
                for k in range(shape[2]):
                    chunkV =np.zeros([kernelWidth])   # Chunk of data to compute deriv on

                    # Handle boundary conditions, basically set to 0 outside of image
                    if(Axis == 'x' or Axis == 0):
                        sliceV = DataT[:,j,k]
                        # Check bounds
                        low = i - halfKern
                        up  = shape[0] - (i + halfKern + 1)
                        idx = i
                    elif(Axis == 'y' or Axis == 1):
                        sliceV = DataT[i,:,k]
                        # Check bounds
                        low = j - halfKern
                        up  = shape[1] - (j + halfKern + 1)
                        idx = j
                    elif(Axis == 'z' or Axis == 2):
                        sliceV = DataT[i,j,:]
                        # Check bounds
                        low = k - halfKern
                        up  = shape[2] - (k + halfKern + 1)
                        idx = k
                    else:
                        exit_with_error("ERROR!!! {} is invalid Axis in 3D".format(Axis))
                    ### Assign data from DataT to chunkV
                    # comfortably w/in DataT bounds
                    if(low >= 0 and up >= 0):
                        chunkV = sliceV[(idx-halfKern):(idx+halfKern+1)]    # Check bounds here
                    elif(low < 0):
                        chunkV[(low-1):] = sliceV[0:(kernelWidth+low)]      # recall low < 0
                    elif(up < 0):
                        chunkV[0:] = sliceV[idx:]
    ## 2D
    if(len(DataT.shape) == 2):
        for i in range(shape[0]):
            for j in range(shape[1]):
                if(Axis == 'x' or Axis == 0):
                    exit_with_error("ERROR!! Not yet implemented")
                elif(Axis == 'y' or Axis == 1):
                    exit_with_error("ERROR!! Not yet implemented")
                else:
                    exit_with_error("ERROR!!! {} is invalid Axis in 2D".format(Axis))
    ## 1D
    if(len(DataT.shape) == 1):
        for i in range(shape[0]):
            if(Axis == 'x' or Axis == 0):
                exit_with_error("ERROR!! Not yet implemented")
            else:
                exit_with_error("ERROR!!! {} is invalid Axis in 1D".format(Axis))
        


def hessian(String):
    """
    ARGS:
    DESCRIPTION:
    RETURN:
    DEBUG:
    FUTURE:
    """
    sys.stderr.write(String)
