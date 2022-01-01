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



def parse_polynomial(String=None)
    """
    ARGS:
        String : expects a polynomial (using 'x') like '2x + 3x**2'
    DESCRIPTION:
        Parses text from String and returns the coefficients and exponents of each
        term. This function does not handle dependencies on variables other than 'x'
        or exponential terms
    RETURN:
        coeffV  : numpy vector of coefficients for each term
        powerV  : numpy vector of powers for each term
    DEBUG:
    FUTURE:
    """
    String = String.strip("\n")
    strL = String.split(' ')
    coeffV = np.zeros(len(strL))
    powerV = np.zeros(len(strL))
    for idx in range(len(strL)):
        term = s.split('x')
        # No dependency on 'x', e.g. 4
        if(len(term) == 1 and 'x' not in term[0]):
            powerV[idx] = 0
            coeffV[idx] = float(term[0])
        elif(len(term) == 1):


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
    if(len(sys.argv) != 2) :
        print_help(1)
    elif(len(sys.argv) == 2 and "-h" in sys.argv[1]):
        print_help(0)

    print("Welcome to genearte_test_data.py!\nLet's get started by answering some"
          "questions.")
    
    ##### Base name
    print("Enter stem for output files:")
    stem = input().strip("\n")

    ##### Dimensions
    print("\tData size (e.g. x,y,z):")
    sizeS = input().strip("\n")
    sizeS = sizeS.split(',')
    sizeV = np.zeros([3])
    for idx in range(len(sizeS)):
        if '.' in sizeS[idx]:
            exit_with_error("ERROR!!! dimensions CANNOT be floats\n")
        sizeV[idx] = int(sizeS[idx])
    data = np.zeros(sizeV)
    
    ##### Get underlying gradients
    # X 
    print("\tEnter x gradient (e.g. 2, x**2, n/a: ")
    gradX = input().strip("\n")
    
    try :
        
    except ValueError :



    print("Started : %s"%(time.strftime("%D:%H:%M:%S")))
    startTime = time.time()

    print("Ended : %s"%(time.strftime("%D:%H:%M:%S")))
    print("Run Time : {:.4f} h".format((time.time() - startTime)/3600.0))
    sys.exit(0)


if __name__ == "__main__":
    main()

