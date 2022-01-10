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
def read_data(Path=None, InputFmt=None):
    """
    ARGS:
        Path     : string, Path to file or (if series) directory containing the data
        InputFmt : string, 'series', 'single' or 'pickel' valid options
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
    if(InputFmt == "series"):
        # Get list of DICOM files
        fileL = glob.glob("{}/*.dcm".format(Path))      # presumably have dcm suffix...
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
        #plot_multiple_dicom(PixelT=pixelT)

    elif(InputFmt == "single"):
        data = pydicom.dcmread(Path)
        pixelM = data.pixel_array
        #plot_single_dicom(PixelM=pixelM)
    elif(InputFmt == "pickle"):
        inFile = open(Path, "rb")
        pixelT = pickle.load(inFile)
        #plot_multiple_dicom(PixelT=pixelT)
    else:
        exit_with_error("ERROR!!! {} is invalid value for "
                        "[series|single|pickle]\n".format(inputFmt))
    print("\tEnded : %s"%(time.strftime("%D:%H:%M:%S")))
    print("\tTime : {:.4f} h".format((time.time() - startTime)/3600.0))
    return(pixelT)

