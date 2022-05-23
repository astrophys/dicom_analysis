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
#   python src/visualize.py ~/Downloads/APOLLO-5-LUAD\:/manifest-1637691614015//APOLLO-5-LUAD/AP-78LL/07-27-1977-NA-CT_CHEST_W-O_CON-49429/2.000000-CT\ CHEST-28012 series 3D
import sys
import numpy as np
import time
import glob
from matplotlib import pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib.widgets import Slider
from functions import otsu_threshold
from hessian import extract_local_shape
import pydicom
import pickle
# my code
from file_io import read_data
from error import exit_with_error
from random import random
    

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
        "      [2D|2Dseg|3D|hist]: string, \n"
        "                           2D     - visualize in 2D (using matplotlib)\n"
        "                           2D-seg - visualize in 2D (using matplotlib) and segmentation\n"
        "                           3D     - visualize in 3D (using vtk)\n"
        "                           hist   - histogram of the pixel values\n"
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


def plot_histogram(Array=None):
    """
    ARGS:
        Array :  Numpy array of any dimension
    DESCRIPTION:
        Plots histogram of values
    RETURN:
        N/A
    DEBUG:
    FUTURE:
    """
    fig, ax = plt.subplots(nrows=1, ncols=1)
    uniqV,countV = np.unique(Array, return_counts=True)
    ax.bar(uniqV, np.log10(countV), align='center', width=1)
    ax.set_title("Distribution of pixel values")
    plt.show()


def plot_multiple_dicom(PixelT=None, SegT=None):
    """
    ARGS:
        PixelT :  3D Numpy array extacted from Dicom file
        SegT   :  (optional) 3D Numpy array of segmented volume to plot side-by-side 
    DESCRIPTION:
        Plots PixelT as a heat map with slider to sweep through
        the z-axis
    RETURN:
        N/A
    DEBUG:
    FUTURE:
    """
    # Decide whether 1 or 2 plots are showed
    if(SegT is not None):
        fig = plt.figure()
        #plt.subplots_adjust(hspace=0.4,wspace=0.4)
        gs  = fig.add_gridspec(1,2)
        # MRI / CT image
        ax = fig.add_subplot(gs[0,0])
        im = ax.imshow(X=PixelT[:,:,0], cmap='bone', interpolation='none')
        # Segmented image
        ax2 = fig.add_subplot(gs[0,1])
        im2 = ax2.imshow(X=SegT[:,:,0], cmap='bone', interpolation='none')
    else:
        fig, ax = plt.subplots(nrows=1, ncols=1)
        im = ax.imshow(X=PixelT[:,:,0], cmap='bone', interpolation='none')
        fig.colorbar(im, ax=ax)

    # Create sliders
    sliderAx = fig.add_axes([0.13, 0.025, 0.56, 0.02])
    slider = Slider(ax=sliderAx, label='z', valmin=0, valmax=PixelT.shape[2]-1, valinit=0)
    ax.set_title("Plot of Dicom data")
    
    # Define how slider behaves
    def update_slider(val):
        z = int(round(slider.val))
        im = ax.imshow(X=PixelT[:,:,z], cmap='bone', interpolation='none')
        if(SegT is not None):
            im2 = ax2.imshow(X=SegT[:,:,z], cmap='bone', interpolation='none')

    #plt.tight_layout()
    slider.on_changed(update_slider)
    plt.show()
    #plt.close(fig)


def plot_3D(PixelT=None, Thresh=1080):
    """
    ARGS:
        PixelT  : 3D - Numpy array extacted from Dicom file
        Thresh  : float/int, threshold above which to plot
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
    reader  = vtk.vtkStructuredPointsReader()
    dim     = PixelT.shape
    scaling   = (1.0, 1.0, 1.0)
    # Create the standard renderer, render window and interactor
    ren = vtk.vtkRenderer()         # control geom, camera view, light, coords, etc.
    renWin = vtk.vtkRenderWindow()  # place where renderers draw their images.
    renWin.AddRenderer(ren)         # Add renderer to window
    iren = vtk.vtkRenderWindowInteractor()  # control mech of mouse/key/time
    iren.SetRenderWindow(renWin)    # set window to be controlled by interactor
    # Create the reader for the data
    # Create transfer mapping scalar value to opacity
    opacityTransferFunction = vtk.vtkPiecewiseFunction()
    opacityTransferFunction.AddPoint(0, 0.0)
    opacityTransferFunction.AddPoint(1, .01)
    opacityTransferFunction.AddPoint(5, .1)
    opacityTransferFunction.AddPoint(50, .4)
    opacityTransferFunction.AddPoint(100, 1.0)
    # Create transfer mapping scalar value to color
    colorTransferFunction = vtk.vtkColorTransferFunction()
    colorTransferFunction.AddRGBPoint(0.0,0.0,0.0,0.0)
    colorTransferFunction.AddRGBPoint(5.0,0.0,0.0,1.0)
    colorTransferFunction.AddRGBPoint(50.0,1.0,0.0,0.0)
    colorTransferFunction.AddRGBPoint(100.0,0.0,1.0,0.0)
    # The property describes how the data will look
    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetColor(colorTransferFunction)
    volumeProperty.SetScalarOpacity(opacityTransferFunction)
    volumeProperty.ShadeOn()
    volumeProperty.SetInterpolationTypeToLinear()
    # The mapper / ray cast function know how to render the data
    volumeMapper = vtk.vtkFixedPointVolumeRayCastMapper()
    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)      # volume.GetBounds() to see bounds
    volume.SetProperty(volumeProperty)
    outline = vtk.vtkOutlineFilter()
    outline.SetInputConnection(reader.GetOutputPort())
    mapOutline = vtk.vtkPolyDataMapper()
    mapOutline.SetInputConnection(outline.GetOutputPort())
    outlineActor = vtk.vtkActor()
    outlineActor.SetMapper(mapOutline)
    outlineActor.GetProperty().SetColor(0,0,0)
    tprop = vtk.vtkTextProperty()
    tprop.SetColor(.1,.1,.1)
    tprop.ShadowOn()
    whichcluster = 1 # zero is the void
    countActors = 0
    contActors = []
    tmpT = np.zeros(PixelT.shape)
    tmpT = (PixelT > Thresh)*255
    # Flatten to convert to vtk data array
    pyDataV = tmpT.transpose(2,1,0).flatten()
    vtkDataArray = numpy_support.numpy_to_vtk(pyDataV)
    cellcentereddata = vtk.vtkImageData()
    cellcentereddata.SetSpacing(scaling)
    # shift origina so it is centerd in middle of image
    cellcentereddata.SetOrigin((-1.0*(dim[0]+1))/2.0,(-1.0*(dim[1]+1))/2.0,(-1.0*(dim[2]+1))/2.0)
    cellcentereddata.SetDimensions(dim[0]+1,dim[1]+1,dim[2]+1)
    cellcentereddata.GetCellData().SetScalars(vtkDataArray)
    vtkThreshold = vtk.vtkThreshold()
    vtkThreshold.SetInputArrayToProcess(0,0,0,1,0)
    vtkThreshold.SetInputDataObject(cellcentereddata)
    vtkThreshold.ThresholdBetween(1,100000)
    vtkThreshold.Update()
    geometry = vtk.vtkGeometryFilter()
    geometry.SetInputConnection(vtkThreshold.GetOutputPort())
    contMapper = vtk.vtkPolyDataMapper()
    contMapper.SetInputConnection(geometry.GetOutputPort())
    contMapper.SetScalarRange(1,100000)
    contMapper.SetScalarModeToUseCellData()
    # Enabling this line, and commenting out next two, disables use of
    #   color LUT defined above.
    contMapper.ScalarVisibilityOff()
    # Triangles
    triangles = vtk.vtkTriangleFilter()
    triangles.SetInputConnection(geometry.GetOutputPort())
    masscalcs = vtk.vtkMassProperties()
    masscalcs.SetInputConnection(triangles.GetOutputPort())
    theVolume = masscalcs.GetVolume()
    theArea = masscalcs.GetSurfaceArea()
    theNSI = masscalcs.GetNormalizedShapeIndex()
    contActors.append(vtk.vtkActor())
    contActors[countActors].SetMapper(contMapper)
    contActors[countActors].GetProperty().SetOpacity(1)
    contActors[countActors].GetProperty().SetColor(random(),random(),random())
    countActors = countActors + 1
    print("Ended : {}".format((time.strftime("%H:%M:%S"))))
    print("Press E to exit")
    ### Render image ###
    contActor = vtk.vtkActor()
    contActor.SetMapper(contMapper)
    contActor.GetProperty().SetOpacity(1)
    contActor.GetProperty().SetColor(0,.9,0)
    camera = vtk.vtkCamera()
    camera.SetClippingRange(1,500)
    camera.SetFocalPoint(0,0,0)
    #camera.SetPosition(256,256,128)
    camera.SetPosition(10,10,10)
    camera.SetViewUp(0,0,1)

    for aCont in contActors:
        ren.AddActor(aCont)
    ren.SetBackground(1, 1, 1)
    ren.SetActiveCamera(camera)
    ren.AddActor(outlineActor)
    renWin.SetSize(600, 600)
    axes = vtk.vtkCubeAxesActor2D()
    axes.SetInputData(reader.GetOutput())
    axes.SetCamera(ren.GetActiveCamera())
    axes.SetLabelFormat("%6.4g")
    axes.SetFlyModeToOuterEdges()
    axes.SetFontFactor(5.8)
    axes.SetAxisTitleTextProperty(tprop)
    axes.SetAxisLabelTextProperty(tprop)
    # Axis order is Dx=Drows, Dy=D(dim[2])columns, Dz=Dcolumns
    axes.SetRanges(0,dim[0]-1,0,dim[1]-1,0,dim[2]-1)  # Changes Range!
    axes.SetUseRanges(1)
    ren.AddViewProp(axes)
    renWin.Render()                         # Throws supposed error here
    # Change inline function later...
    def CheckAbort(obj, event):
        if obj.GetEventPending() != 0:
            obj.SetAbortRender(1)

    renWin.AddObserver("AbortCheckEvent", CheckAbort)
    iren.Initialize()
    renWin.Render()
    iren.Start()




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
        2. Add some arxiving so I don't have to rerun the image segmentation each time
           I change some of the plotting
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
    elif(sys.argv[3].upper() == "2DSEG"):
        visType = "2DSEG"
    elif(sys.argv[3].upper() == "3D"):
        visType = "3D"
    elif(sys.argv[3].upper() == "HIST"):
        visType = "HIST"
    else:
        exit_with_error("ERROR!!! {} is invalid value for "
                        "[2D|3D]\n".format(inputFmt))
    pixelT = read_data(Path=path, NFiles=nFiles)
    if(visType == "2D"):
        if(len(pixelT.shape) == 2):
            exit_with_error("ERROR!! This is yet to be implemented")
            plot_single_dicom(PixelM=pixelT)
        elif(len(pixelT.shape)==3):
            plot_multiple_dicom(PixelT=pixelT)
        else:
            exit_with_error("ERROR!!! Code can't handle matrices of "
                            "dim = {}\n".format(len(pixelT.shape)))
    elif(visType == "2DSEG"):
        tmpT = np.copy(pixelT)              # Temporary array to massage before segmenting
        tmpT[tmpT < 0] = 0                  # Remove bias from scanner bounds
        # Should I do thresholding? - maybe it creates artifacts.
        thresh,discard = otsu_threshold(tmpT) # Remove image noise 
        tmpT[tmpT < thresh] = 0
        sigmaL = [1]
        (vesselT, vSigmaT, clustT, cSigmaT) = extract_local_shape(SigmaL=sigmaL, DataT=pixelT)
        if(len(pixelT.shape) == 2):
            plot_single_dicom(PixelM=pixelT)
        elif(len(pixelT.shape)==3):
            plot_multiple_dicom(PixelT=pixelT, SegT=clustT)
        else:
            exit_with_error("ERROR!!! Code can't handle matrices of "
                            "dim = {}\n".format(len(pixelT.shape)))
    elif(visType == "3D"):
        #plot_histogram(pixelT)
        pixelT[pixelT < 0] = 0                  # Remove bias from scanner bounds
        # Add conditional here
        #thresh,discard = otsu_threshold(pixelT) # Remove image noise 
        plot_3D(PixelT=pixelT, Thresh=180)
    elif(visType == "HIST"):
        plot_histogram(pixelT)
    else:
        exit_with_error("ERROR!!! plot type {} is not a valid option".format(visType))

    sys.exit(0)

if __name__ == "__main__":
    main()
