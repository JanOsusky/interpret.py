"""
        IPP PROJECT 2 - interpret.py

        Jan Osuský --- xosusk00

        interpret.py for IPPcode23

            BUT FIT / UMA ETSII

                 April 2023
"""

import sys


class Error:
    # error codes
    parameter = 10
    stdIn = 11
    stdOut = 12
    xmlFormat = 31
    xmlStruct = 32
    semantic = 52
    wrongOp = 53
    missVar = 54
    missFrame = 55
    missVal = 56
    wrongOpVal = 57
    string = 58
    intern = 99

    # printing error messages and exiting the program
    @staticmethod
    def printExit( msg, errorCode):
        print(msg, file=sys.stderr)
        sys.exit(errorCode)
