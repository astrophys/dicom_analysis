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
    DEBUG:
    FUTURE:
    """
    return( (-1/(S**3 * np.sqrt(2 * np.pi)) * (X - Mu) * np.exp(-(X-Mu)**2 / (2*S**2))
    



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
    DEBUG:
    FUTURE:
    """
    nSig        = 3                     # Number of sigma to use for kernelWidth
    kernelWidth = int(2 * nSig * S + 1) # 3 sigma left of center, 3 sigma right of center
    kernelV     = gaussian_derivative_kernel(N=kernelWidth, S=S)
    shape = DataT.shape
    for i in range(shape[0]):
        


def hessian(String):
    """
    ARGS:
    DESCRIPTION:
    RETURN:
    DEBUG:
    FUTURE:
    """
    sys.stderr.write(String)
