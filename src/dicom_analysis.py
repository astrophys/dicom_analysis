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
import sys
import numpy as np
import time
import glob
from matplotlib import pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib.widgets import Slider
import pydicom
from gaussian import gaussian_derivative_of_tensor
# my code
from error import exit_with_error
from error import warning
    

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
        "\nUSAGE : python src/dicom_analysis.py path [series|single]\n\n"
        "      path            : string, path to either a DICOM file or a directory of DICOMs\n"
        "      [series|single] : string, if 'series', path is a directory with a series of DICOM files\n"
        "                      : string, if 'single', path is a single DICOM file\n"
        "                         \n")
    sys.exit(ExitVal)


def plot_single_dicom(PixelM=None):
    """
    ARGS:
        PixelM  :  2D - Numpy array extacted from Dicom file
    DESCRIPTION:
        Plots PixelM as a heat map
    RETURN:
        N/A
    DEBUG:
    FUTURE:
    """
    fig, ax = plt.subplots(nrows=1, ncols=1)
    im = ax.imshow(X=PixelM, cmap='bone', interpolation='none')
   
    ax.set_title("Plot of Dicom data")
    fig.colorbar(im, ax=ax)

    #plt.tight_layout()
    plt.show()
    #plt.close(fig)


def plot_multiple_dicom(PixelT=None):
    """
    ARGS:
        PixelT  :  3D - Numpy array extacted from Dicom file
    DESCRIPTION:
        Plots PixelT as a heat map with slider to sweep through
        the z-axis
    RETURN:
        N/A
    DEBUG:
    FUTURE:
    """
    fig, ax = plt.subplots(nrows=1, ncols=1)
    im = ax.imshow(X=PixelT[:,:,0], cmap='bone', interpolation='none')
    # Create sliders
    sliderAx = fig.add_axes([0.13, 0.025, 0.56, 0.02])
    slider = Slider(ax=sliderAx, label='z', valmin=0, valmax=PixelT.shape[2]-1, valinit=0)
    ax.set_title("Plot of Dicom data")
    fig.colorbar(im, ax=ax)
    
    # Define how slider behaves
    def update_slider(val):
        z = int(round(slider.val))
        im = ax.imshow(X=PixelT[:,:,z], cmap='bone', interpolation='none')

    #plt.tight_layout()
    slider.on_changed(update_slider)
    plt.show()
    #plt.close(fig)



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
    if(len(sys.argv) != 2 and len(sys.argv) != 3) :
        print_help(1)
    elif(len(sys.argv) == 2 and "-h" in sys.argv[1]):
        print_help(0)
    elif(len(sys.argv) != 3):
        print_help(1)

    path = sys.argv[1]
    if(sys.argv[2].lower() == "series"):
        isSeries = True
    elif(sys.argv[2].lower() == "single"):
        isSeries = False
    else:
        exit_with_error("ERROR!!! Invalid value for [series|single]\n")

    print("Started : %s"%(time.strftime("%D:%H:%M:%S")))
    startTime = time.time()

    # Extract data
    if(isSeries == True):
        # Get list of DICOM files
        fileL = glob.glob("{}/*.dcm".format(path))      # presumably have dcm suffix...
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
        plot_multiple_dicom(PixelT=pixelT)

    else:
        data = pydicom.dcmread(path)
        pixelM = data.pixel_array
        plot_single_dicom(PixelM=pixelM)


    # Test Gaussion derivative
    testT = np.zeros([10,10,10])
    for i in range(testT.shape[0]):
        for j in range(testT.shape[1]):
            for k in range(testT.shape[2]):
                testT[i,j,k] = 2*i + j*j + 3*k*k*k
    gaussian_derivative_of_tensor(DataT=testT, Axis='x', S=1)
    gaussian_derivative_of_tensor(DataT=testT, Axis='y', S=1)
    gaussian_derivative_of_tensor(DataT=testT, Axis='z', S=1, Verbose=True)
    
    print("Ended : %s"%(time.strftime("%D:%H:%M:%S")))
    print("Run Time : {:.4f} h".format((time.time() - startTime)/3600.0))
    sys.exit(0)


if __name__ == "__main__":
    main()

