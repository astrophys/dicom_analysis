# Author : Ali Snedden
# Date   : 1/1/22
# License: MIT
# Notes  : 
#
# Background : 
#       
# Purpose :
#   This code interactively generates a test data set to test dicom_analysis.py 
#
# How to Run :
#   python 
#
import sys
import numpy as np
import time
import pydicom
import os
import tempfile
import datetime
from pydicom.dataset import FileDataset, FileMetaDataset
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
        "\nUSAGE : python src/generate_test_data.py \n\n"
        "                         \n")
    sys.exit(ExitVal)



def parse_polynomial(String=None, Var='x'):
    """
    ARGS:
        String : expects a polynomial (using 'x') like '2x + 3x**2'
        Var    : Variable / character to split on
    DESCRIPTION:
        Parses text from String and returns the coefficients and exponents of each
        term. This function does not handle dependencies on variables other than 'x'
        or exponential terms

        Currently only works with simple combinations of operators and spacing. 
        It is best to have spaces between '+' and '-' operators between terms
             Works : 
                 -> 2x**2 - 4
             Fails :
                 -> 2x**2-4
                 -> 2x**-1
                 -> 2x**(2)
    RETURN:
        coeffV  : numpy vector of coefficients for each term
        powerV  : numpy vector of powers for each term
    DEBUG:
    FUTURE:
        1. Make more robust to handle all combinations of operators and spacing OR add
           properly error handling for incorrect formatting
    """
    String = String.strip("\n")
    strL = String.split(' ')
    coeffV = np.zeros(len(strL))
    powerV = np.zeros(len(strL))
    signV  = np.ones(len(strL))     # Use to control sign change
    v = Var                         # Better to use one char variable here
    print(strL)
    for idx in range(len(strL)):
        ## Handle non-'x' or numeric characters
        if(strL[idx] == "+"):
            continue
        if(strL[idx] == "-"):
            signV[idx+1] = -1*signV[idx+1]
            continue
        term = strL[idx].split(v)
        # No dependency on 'x', e.g. 4
        if(len(term) == 1 and v not in term[0]):
            powerV[idx] = 0
            coeffV[idx] = float(term[0])
        # 
        elif(len(term) == 2):
            if(term[0] == ''):
                coeffV[idx] = 1.0
            else:
                coeffV[idx] = float(term[0])
            if(term[1] == ''):
                powerV[idx] = 1.0
            else:
                powerV[idx] = float(term[1].split("**")[1])
        else:
            exit_with_error("ERROR!!! Unexpected case has occurred = {}".format(term))
    # flip signs for '-'s
    coeffV = coeffV*signV
    print(coeffV, powerV)
    return(coeffV, powerV)


def main():
    """
    ARGS:
        None.
    DESCRIPTION:
        Interactively creates sample data sets for tesing dicom_analysis.py
    RETURN:
    DEBUG:
    FUTURE:
        1. Add an option to pass a config file
    """
    ###### Check python version ######
    if(sys.version_info[0] != 3):
        exit_with_error("ERROR!!! Wrong python version ({}), version 3 "
                        "expected\n".format(sys.version_info[0]))

    ###### Get Command Line Options ######
    if(len(sys.argv) != 2 and len(sys.argv) != 1) :
        print_help(1)
    elif(len(sys.argv) == 2 and "-h" in sys.argv[1]):
        print_help(0)

    print("\n\n##########################################\n"
              "Welcome to genearte_test_data.py!\n"
              "##########################################\n"
            "\nLet's get started by answering some questions.")
    
    ##### Base name
    print("Enter stem for output files:")
    stem = input().strip("\n")

    ##### Dimensions
    print("\nData size (e.g. x,y,z):")
    string = input().strip("\n")
    sizeS = string.split(',')
    sizeV = np.zeros([3],dtype=np.int32)
    for idx in range(len(sizeS)):
        if '.' in sizeS[idx]:
            exit_with_error("ERROR!!! dimensions CANNOT be floats\n")
        sizeV[idx] = np.int(sizeS[idx])
    print("--> Entered sizeV = {}".format(sizeV))
    data = np.zeros(sizeV)
    
    ##### Get underlying gradients
    # X 
    print("\nEnter x gradient (e.g. 2, x**2, n/a: ")
    string = input().strip("\n")
    xCoeffV,xPowerV = parse_polynomial(String=string, Var='x')
    # Y 
    print("\nEnter y gradient (e.g. 2, y**2, n/a: ")
    string = input().strip("\n")
    yCoeffV,yPowerV = parse_polynomial(String=string, Var='y')
    # Z 
    print("\nEnter z gradient (e.g. 2, z**2, n/a: ")
    string = input().strip("\n")
    zCoeffV,zPowerV = parse_polynomial(String=string, Var='z')
    # Modify 'data'
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            for k in range(data.shape[2]):
                data[i,j,k] = ((xCoeffV * (i**xPowerV)) + (yCoeffV * (j**yPowerV)) +
                              (zCoeffV * (k**zPowerV)))

    ##### Get clumps to insert
    moreClump = True
    while moreClump :
        print("\nDo you want to add a clump? [Y/N]")
        string = input().strip("\n")
        if(string.lower() == "y" or string.lower() == "yes"):
            moreClump = True
            # Center
            print("\nEnter center for clump (e.g. x,y,z)")
            string = input().strip("\n")
            centerV= string.split(',')
            cV = [float(c) for c in centerV]
            # Size
            print("\nEnter radius of clump (e.g. float)")
            string = input().strip("\n")
            r      = float(string)
            print("\nEnter value of clump (e.g. float)")
            string = input().strip("\n")
            v      = float(string)
            # Create clump
            for i in range(data.shape[0]):
                for j in range(data.shape[1]):
                    for k in range(data.shape[2]):
                        # displacement
                        d = ((i - cV[0])**2 + (j - cV[1])**2 + (k - cV[2])**2)
                        if(d < r):
                            data[i,j,k] = v
        else :
            moreClump = False
        
    print("Starting to write files : %s"%(time.strftime("%D:%H:%M:%S")))
    startTime = time.time()

    ##### Write data
    # Follow example : https://pydicom.github.io/pydicom/stable/auto_examples/input_output/plot_write_dicom.html
    outName="{}.dcm".format(stem)
    #filename_little_endian = tempfile.NamedTemporaryFile(suffix=suffix).name
    #filename_big_endian = tempfile.NamedTemporaryFile(suffix=suffix).name
    
    print("Setting file meta information...")
    # Populate required values for file meta information
    meta = FileMetaDataset()
    meta.MediaStorageSOPClassUID = "CT Image Storage"
    meta.MediaStorageSOPInstanceUID = "1.3.6.1.4.1.14519.5.2.1.101692030094434533703823936384802321461"
    meta.ImplementationClassUID = "1.3.6.1.4.1.22213.1.143"
    meta.TransferSyntaxUID      = "Implicit VR Little Endian"
    meta.ImplementationVersionName = "0.5"
    meta.SourceApplicationEntityTitle = "POSDA"
    
    print("Setting dataset values...")
    # Create the FileDataset instance (initially no data elements, but meta
    # supplied)
    ds = FileDataset(outName, {},
                     file_meta=meta, preamble=b"\0" * 128)
    
    # Add the data elements -- not trying to set all required here. Check DICOM
    # standard
    ds.PatientName = "Test^Firstname"
    ds.PatientID = "123456"
    
    # Set the transfer syntax
    ds.is_little_endian = True
    ds.is_implicit_VR = True
    
    # Set creation date/time
    dt = datetime.datetime.now()
    ds.ContentDate = dt.strftime('%Y%m%d')
    timeStr = dt.strftime('%H%M%S.%f')  # long format with micro seconds
    ds.ContentTime = timeStr
    
    print("Writing test file {}", outName)
    ds.save_as("{}".format(outName))
    print("File saved.")
    
    # Write as a different transfer syntax XXX shouldn't need this but pydicom
    # 0.9.5 bug not recognizing transfer syntax
    #ds.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRBigEndian
    #ds.is_little_endian = False
    #ds.is_implicit_VR = False
    
    #print("Writing test file as Big Endian Explicit VR", filename_big_endian)
    #ds.save_as(filename_big_endian)

    print("Ended : %s"%(time.strftime("%D:%H:%M:%S")))
    print("Run Time : {:.4f} h".format((time.time() - startTime)/3600.0))
    sys.exit(0)


if __name__ == "__main__":
    main()

