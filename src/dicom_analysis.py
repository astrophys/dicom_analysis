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
from matplotlib import pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import pydicom
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
        "\nUSAGE : python src/dicom_analysis.py some_file.dcm\n\n"
        "      some_file.dcm : A DICOM file\n"
        "                         \n")
    sys.exit(ExitVal)


def plot_dicom(PixelM=None):
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
    if(len(sys.argv) != 2) :
        print_help(1)
    elif(len(sys.argv) == 2 and "-h" in sys.argv[1]):
        print_help(0)
    path = sys.argv[1]

    print("Started : %s"%(time.strftime("%D:%H:%M:%S")))
    startTime = time.time()

    # Extract data
    data = pydicom.dcmread(path)
    pixelM = data.pixel_array

    plot_dicom(PixelM=pixelM)

    
    print("Ended : %s"%(time.strftime("%D:%H:%M:%S")))
    print("Run Time : {:.4f} h".format((time.time() - startTime)/3600.0))
    sys.exit(0)


if __name__ == "__main__":
    main()

