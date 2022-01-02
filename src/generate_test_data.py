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



def parse_polynomial(String=None):
    """
    ARGS:
        String : expects a polynomial (using 'x') like '2x + 3x**2'
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
    print(strL)
    for idx in range(len(strL)):
        ## Handle non-'x' or numeric characters
        if(strL[idx] == "+"):
            continue
        if(strL[idx] == "-"):
            signV[idx+1] = -1*signV[idx+1]
            continue
        term = strL[idx].split('x')
        # No dependency on 'x', e.g. 4
        if(len(term) == 1 and 'x' not in term[0]):
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
            exit_with_error("ERROR!!! Unexpected case has occurred")
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

    print("Welcome to genearte_test_data.py!\nLet's get started by answering some"
          "questions.")
    
    ##### Base name
    print("Enter stem for output files:")
    stem = input().strip("\n")

    ##### Dimensions
    print("\tData size (e.g. x,y,z):")
    string = input().strip("\n")
    sizeS = string.split(',')
    sizeV = np.zeros([3])
    for idx in range(len(sizeS)):
        if '.' in sizeS[idx]:
            exit_with_error("ERROR!!! dimensions CANNOT be floats\n")
        sizeV[idx] = int(sizeS[idx])
    data = np.zeros(sizeV)
    
    ##### Get underlying gradients
    # X 
    print("\tEnter x gradient (e.g. 2, x**2, n/a: ")
    string = input().strip("\n")
    xCoeffV,xPowerV = parse_polynomial(string)
    # Y 
    print("\tEnter y gradient (e.g. 2, y**2, n/a: ")
    string = input().strip("\n")
    yCoeffV,yPowerV = parse_polynomial(string)
    # Z 
    print("\tEnter z gradient (e.g. 2, z**2, n/a: ")
    string = input().strip("\n")
    zCoeffV,zPowerV = parse_polynomial(string)
    # Modify 'data'
    for i in range(len(data.shape[0])):
        for j in range(len(data.shape[1])):
            for k in range(len(data.shape[2])):
                data[i,j,k] = (xCoeffV * (i**xPowerV)) + (yCoeffV * (j**yPowerV)) +
                              (zCoeffV * (k**zPowerV))

    ##### Get clumps to insert
    moreClump = True
    while moreClump :
        print("\tDo you want to add a clump? [Y/N]")
        string = input().strip("\n")
        if(string.lower() == "y" or string.lower() == "yes"):
            moreClump = True
            # Center
            print("\tEnter center for clump")
            string = input().strip("\n")
            centerV= string.split(',')
            centerV= [float(c) for c in centerV]
            # Size
            print("\tEnter radius of clump")
        else :
            moreClump = False
        
        

    print("Started : %s"%(time.strftime("%D:%H:%M:%S")))
    startTime = time.time()

    print("Ended : %s"%(time.strftime("%D:%H:%M:%S")))
    print("Run Time : {:.4f} h".format((time.time() - startTime)/3600.0))
    sys.exit(0)


if __name__ == "__main__":
    main()

