# Author : Ali Snedden
# Date   : 12/2/21
# License: MIT
# Notes  : 
#
# Background : 
#       
# Purpose :
#
# How to Run :
#   python src/dicom_analysis.py path [series|single|pickle] stem
import sys
import numpy as np
import time
import pydicom
import pickle
# my code
from gaussian import gaussian_derivative_of_tensor
from hessian import extract_local_shape
from error import exit_with_error
from error import warning
from file_io import read_data
    

def print_help(ExitVal=None):
    """
    ARGS:
        ExitVal : int, exit value
    DESCRIPTION:
        Print Help. Exit with value arg
    RETURN:
        N/A
    DEBUG:
        1. Tested, it worked
    FUTURE:
    """
    sys.stdout.write(
        "\nUSAGE : python src/dicom_analysis.py path [series|single|pickle] stem s1,s2,...,sN\n\n"
        "      path            : string, path to either a DICOM file or a directory of DICOMs\n"
        "      [series|single|pickle] : string\n"
        "                               if 'series' : path is a directory with a series of DICOM files\n"
        "                               if 'single' : path is a single DICOM file\n"
        "                               if 'pickle' : path is a single pickle file generated by generate_test_data.py\n"
        "      stem            : The output filename stem\n"
        "      s1,s2,...,sN    : int (comma seperated). The list of sigmas controlling size of \n"
        "                        guassian kernel in derivative calculation\n"
        "                         \n")
    sys.exit(ExitVal)


def main():
    """
    ARGS:
        None.
    DESCRIPTION:
        Driver function.  Does all the analysis
    RETURN:
    DEBUG:
    FUTURE:
        1. Check suffixes for correct file types
    """
    ###### Check python version ######
    if(sys.version_info[0] != 3):
        exit_with_error("ERROR!!! Wrong python version ({}), version 3 "
                        "expected\n".format(sys.version_info[0]))

    ###### Get Command Line Options ######
    if(len(sys.argv) != 2 and len(sys.argv) != 5) :
        print_help(1)
    elif(len(sys.argv) == 2 and "-h" in sys.argv[1]):
        print_help(0)
    elif(len(sys.argv) != 5):
        print_help(1)

    path = sys.argv[1]
    if(sys.argv[2].lower() == "series"):
        inputFmt = "series"
    elif(sys.argv[2].lower() == "single"):
        inputFmt = "single"
    elif(sys.argv[2].lower() == "pickle"):
        inputFmt = "pickle"
    else:
        exit_with_error("ERROR!!! {} is invalid value for "
                        "[series|single|pickle]\n".format(inputFmt))
    stem = sys.argv[3]
    string = sys.argv[4]
    strL   = string.split(",")
    sL     = [int(s) for s in strL]
    print("kernel widths (sigma) used : {}".format(sL))
    pixelT = read_data(Path=path, NFiles=inputFmt)

    print("Started : %s"%(time.strftime("%D:%H:%M:%S")))
    startTime = time.time()


    #### Test Gaussion derivative
    ## 3D
    #testT = np.zeros([10,10,10])
    #for i in range(testT.shape[0]):
    #    for j in range(testT.shape[1]):
    #        for k in range(testT.shape[2]):
    #            testT[i,j,k] = 2*i + j*j + 3*k*k*k
    #gaussian_derivative_of_tensor(DataT=testT, Axis='x', S=1, Verbose=True)
    #gaussian_derivative_of_tensor(DataT=testT, Axis='y', S=1)
    #gaussian_derivative_of_tensor(DataT=testT, Axis='z', S=1, Verbose=True)
    ## 2D
    #testT = np.zeros([10,10])
    #for i in range(testT.shape[0]):
    #    for j in range(testT.shape[1]):
    #        testT[i,j] = 2*i + j*j
    ##gaussian_derivative_of_tensor(DataT=testT, Axis='x', S=1, Verbose=True)
    #gaussian_derivative_of_tensor(DataT=testT, Axis='y', S=1, Verbose=True)
    ## 1D
    #testT = np.zeros([10])
    #for i in range(testT.shape[0]):
    #    testT[i] = 2*i
    #gaussian_derivative_of_tensor(DataT=testT, Axis='x', S=1, Verbose=True)
    ####

    (vesselT, vSigmaT, clustT, cSigmaT) = extract_local_shape(SigmaL=sL, DataT=pixelT)

    ### Output analysis ###
    # Vesselness
    outFile = open("{}_vessel.pkl".format(stem), "wb")
    pickle.dump(vesselT, outFile, protocol=4)
    outFile.close()
    # Vessel Sigma
    outFile = open("{}_vSigma.pkl".format(stem), "wb")
    pickle.dump(vSigmaT, outFile, protocol=4)
    outFile.close()
    # Clumpiness
    outFile = open("{}_clust.pkl".format(stem), "wb")
    pickle.dump(clustT, outFile, protocol=4)
    outFile.close()
    # Clumpiness
    outFile = open("{}_cSigma.pkl".format(stem), "wb")
    pickle.dump(cSigmaT, outFile, protocol=4)
    outFile.close()

    ### Add visualization of vesselT and clustT


    print("Ended : %s"%(time.strftime("%D:%H:%M:%S")))
    print("Run Time : {:.4f} h".format((time.time() - startTime)/3600.0))
    sys.exit(0)


if __name__ == "__main__":
    main()

