import numpy as np
from error import exit_with_error
from gaussian import gaussian_derivative_of_tensor

def extract_local_shape(SigmaL=None, DataT=None):
    """
    ARGS:
        ScaleL = List of gaussian scales to test, translates to a list of sigma's 
        DataT  = Intput data tensor (can be 1D, 2D, 3D)
    DESCRIPTION:
        Steps : 
            1. Compute maximum Frobenius norm
            2. Compute hessian matrix using a variety of different sized
               gaussian kernels at each voxel
            3. Compute eigenvalues and vectors at each voxel
            4. 
    RETURN:
    DEBUG:
    FUTURE:
        1. Handle 2D and 1D cases...
    """
    frobL = []          # Frobenius Norm, maps to each SigmaL
    shape = DataT.shape
    # Keeping notation in line with from eqn 5 in dx.doi.org/10.1016/j.jcp.2015.07.004
    e1L   = []
    e2L   = []
    e3L   = []
    # Compute maximum Frobenius norm
    for s in SigmaL:
        e1T = np.zeros(shape)
        e2T = np.zeros(shape)
        e3T = np.zeros(shape)
        maxFrob = 0             # Maximum frobenius norm
        # Compute 2nd derivatives
        dxT  = gaussian_derivative_of_tensor(DataT=DataT, Axis='x', S=s)
        dyT  = gaussian_derivative_of_tensor(DataT=DataT, Axis='y', S=s)
        dzT  = gaussian_derivative_of_tensor(DataT=DataT, Axis='z', S=s)
        # Dxx
        dxxT = gaussian_derivative_of_tensor(DataT=dxT, Axis='x', S=s)
        # Dxy
        dxyT = gaussian_derivative_of_tensor(DataT=dxT, Axis='y', S=s)
        # Dxz
        dxzT = gaussian_derivative_of_tensor(DataT=dxT, Axis='z', S=s)
        # Dyy
        dyyT = gaussian_derivative_of_tensor(DataT=dyT, Axis='y', S=s)
        # Dyz
        dyzT = gaussian_derivative_of_tensor(DataT=dyT, Axis='z', S=s)
        # Dzz
        dzzT = gaussian_derivative_of_tensor(DataT=dzT, Axis='z', S=s)
           
        # 3D 
        if(len(shape) == 3):
            for i in range(shape[0]):
                for j in range(shape[1]):
                    for k in range(shape[2]):
                        # Compute hessian matrix using different gaussian kernels
                        hessianM = np.asarray([[dxxT[i,j,k], dxyT[i,j,k], dxzT[i,j,k]],
                                               [dxyT[i,j,k], dyyT[i,j,k], dyzT[i,j,k]],
                                               [dxzT[i,j,k], dyzT[i,j,k], dzzT[i,j,k]]])
                        # Compute eigenvalues / vectors at each voxel
                        [e1,e2,e3],[e1V,e2V,e3V]= np.linalg.eig(hessianM)
                        maxFrob = np.max(maxFrob, np.sqrt(e1**2 + e2**2 + e3**2))
                        e1T[i,j,k] = e1
                        e2T[i,j,k] = e2
                        e3T[i,j,k] = e3
        else:
            exit_with_error("ERROR!!! len(shape) = {} not yet "
                            "implemented\n".format(len(shape)))
        e1L.append(e1T)
        e2L.append(e2T)
        e3L.append(e3T)
        frobL.append(maxFrob)

    # Compute vessel measure 
    vesselL = []                    # Spans different sigma
    vSigmaT = np.zeros(shape)       # Save sigma with max vessel value...
    avgRho  = np.mean(DataT)
    if(len(shape) == 3):
        for sIdx in len(SigmaL):
            vesselT = np.zeros(shape)
            # Get e-values associated w/ sigma
            s = SigmaL[sIdx]
            e1T = e1L[sIdx]
            e2T = e2L[sIdx]
            e3T = e3L[sIdx]
            for i in range(shape[0]):
                for j in range(shape[1]):
                    for k in range(shape[2]):
                        # See EGMENT_gsl/parallel/vessels/src/hessian.c : compute_vesselness()
                        F = np.sqrt(e1T[i,j,k]**2 + e2T[i,j,k]**2 + e3T[i,j,k]**2)   # Frobenius Norm
                        Fnorm = F / FrobL[sIdx]
                        # This ratio distinguishes ribbons/tubes from sheets/blobs
                        if(e3T[i,j,k] == 0 or DataT[i,j,k] < avgRho):
                            vesselT[i,j,k] = 0
                        else:
                            Rc = np.abs(e1T[i,j,k] / e2T[i,j,k])
                        alpha = 2   # Constants from Frangi's paper
                        beta  = 2   # Constants from Frangi's paper
                        vesselT[i,j,k] = (1 - exp(-alpha*Rc*Rc))*(1.0 - exp(-beta*Fnorm*Fnorm))
            vesselL.append(vesselT)


    # Compute cluster measure 
    clustT  = np.zeros(shape)
    cSigmaT = np.zeros(shape)       # Save sigma with max cluster value...





