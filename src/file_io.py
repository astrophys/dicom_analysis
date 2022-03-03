# Author : Ali Snedden
# Date   : 1/9/22
# License: MIT
# Notes  : 
#
# Background : 
#       
# Purpose :
#
# How to Run :
#   Isn't run directly
import time
import glob
import pydicom
import numpy as np
import pickle
from error import exit_with_error

def read_data(Path=None, NFiles=None):
    """
    ARGS:
        Path     : string, Path to file or (if series) directory containing the data
        NFiles   : string, Number of files, i.e. 'series' or 'single' 
    DESCRIPTION:
        This function solely reads in data from either a directory or single file
        (pickle or dcm)
    RETURN:
        A tensor, either 2D or 3D
    DEBUG:
    FUTURE:
    """
    print("Reading data : ")
    print("\tStarted : %s"%(time.strftime("%D:%H:%M:%S")))
    startTime = time.time()
    # Extract data
    if(NFiles == "series"):
        # Get list of DICOM files
        fileL = glob.glob("{}/*.*".format(Path))      # presumably have dcm suffix...
        # Get suffixes, ensure that it is dicom
        suffixL = []
        for f in fileL:
            suffix = f.split('.')[-1]
            if(suffix.lower() != "dcm"):
                exit_with_error("ERROR!!! suffix {} NOT handled. Expecting dcm "
                                "instead".format(suffix))
        dim = None
        # Assume all files should have the same dimension...
        # --> allocate 3D array
        data = pydicom.dcmread(fileL[0])
        shape = data.pixel_array.shape
        pixelT = np.zeros([shape[0], shape[1], len(fileL)])      # 3D matrix, or Tensor
        idx=0                   # File index
        # Assume that files are sanely named AND have z-pos embeded in filename
        fileL = sorted(fileL)
        for fPath in fileL:
            data = pydicom.dcmread(fPath)
            pixelM = data.pixel_array
            if(shape != pixelM.shape):
                exit_with_error("ERROR!!! {} contains DICOM files of different "
                                "dimensions! {} != {}\n".format(fPath,shape,data.shape))
            pixelT[:,:,idx] = pixelM
            idx+=1

    elif(NFiles == "single"):
        suffix = Path.split('.')[-1]
        if(suffix == "dcm"):
            data = pydicom.dcmread(Path)
            pixelT = data.pixel_array
        elif(suffix == "pkl" or suffix == "pickle"):
            inFile = open(Path, "rb")
            pixelT = pickle.load(inFile)
        else:
            exit_with_error("ERROR!!! suffix = {} is unhandled, pkl or dcm expected".format(suffix))
    else:
        exit_with_error("ERROR!!! {} is invalid value for "
                        "[series|single|pickle]\n".format(inputFmt))
    print("\tEnded : %s"%(time.strftime("%D:%H:%M:%S")))
    print("\tTime : {:.4f} h".format((time.time() - startTime)/3600.0))
    return(pixelT)

