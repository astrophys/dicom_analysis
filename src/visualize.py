# Author : Ali Snedden
# Date   : 1/9/22
# License: MIT
# Notes  : 
#
# Background : 
#       
# Purpose :
#   This code is for the sole purpose of visualizing either dicom data (single file OR
#   series of files) and pickle'd numpy arrays. It is used to visualize both input and
#   output data products
#
# How to Run :
#   python src/visualize.py path [series|single|pickle]
import sys
import numpy as np
import time
import glob
from matplotlib import pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib.widgets import Slider
import pydicom
import pickle
# my code
from file_io import read_data
from error import exit_with_error
    

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
        "\nUSAGE : python src/visualize.py path [series|single] [matplotlib|vtk]\n\n"
        "      path            : string \n"
        "                           path to pkl file,  DICOM file or a directory of DICOMs\n"
        "      [series|single] : string\n"
        "                           if 'series' : path is a directory with a series of DICOM files\n"
        "                           if 'single' : path is a single DICOM or pkl file\n"
        "      [2D|3D]:        : string, \n"
        "                           visualize in 2D (using matplotlib)\n"
        "                           visualize in 3D (using vtk)\n"
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


def plot_3D(PixelT=None):
    """
    ARGS:
        PixelT  :  3D - Numpy array extacted from Dicom file
    DESCRIPTION:
        Plots PixelT in '3D' using vtk
    RETURN:
        N/A
    DEBUG:
    FUTURE:
    """
    import vtk
    from vtk.util import numpy_support
    from vtk.util.misc import vtkGetDataRoot



def main():
    """
    ARGS:
        None.
    DESCRIPTION:
        Reads in data and visualizes it.
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
    if(len(sys.argv) != 2 and len(sys.argv) != 4) :
        print_help(1)
    elif(len(sys.argv) == 2 and "-h" in sys.argv[1]):
        print_help(0)
    elif(len(sys.argv) != 4):
        print_help(1)
    ## argv[1]
    path = sys.argv[1]
    ## argv[2]
    if(sys.argv[2].lower() == "series"):
        nFiles = "series"
    elif(sys.argv[2].lower() == "single"):
        nFiles = "single"
    else:
        exit_with_error("ERROR!!! {} is invalid value for "
                        "[series|single]\n".format(inputFmt))
    ## argv[3]
    if(sys.argv[3].upper() == "2D"):
        visType = "2D"
    elif(sys.argv[3].upper() == "3D"):
        visType = "3D"
    else:
        exit_with_error("ERROR!!! {} is invalid value for "
                        "[2D|3D]\n".format(inputFmt))
    pixelT = read_data(Path=path, NFiles=nFiles)
    if(visType == "2D"):
        if(len(pixelT.shape) == 2):
            plot_single_dicom(PixelM=pixelT)
        elif(len(pixelT.shape)==3):
            plot_multiple_dicom(PixelT=pixelT)
        else:
            exit_with_error("ERROR!!! Code can't handle matrices of "
                            "dim = {}\n".format(len(pixelT.shape)))
    if(visType == "3D"):
        if(nFiles == "series"):
            exit_with_error("ERROR!!! 'series' with '3D' not yet implemented!\n")
        plot_3D(PixelT=pixelT)

    sys.exit(0)

if __name__ == "__main__":
    main()
