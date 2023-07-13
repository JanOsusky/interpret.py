"""
        IPP PROJECT 2 - interpret.py

        Jan Osuský --- xosusk00

        interpret.py for IPPcode23

            BUT FIT / UMA ETSII

                 April 2023
"""
import sys
import argparse
import os
from classes.Error import Error
from classes.StatCounter import StatCounter


class Args:

    statCounter = None
    
    def parse(self):
        # create a new ArgumentParser object
        parser = argparse.ArgumentParser(description='interpret.py for IPPcode23', add_help=False)

        # add the arguments we want to parse
        # --help --source=FILE --input=FILE --stats=FILE --insts --vars --hot --print=string --eol --frequent
        parser.add_argument('--help', action='store_true', help='display help message')
        parser.add_argument('--source', type=str, help='specify the source file to use')
        parser.add_argument('--input', type=str, help='specify the input file to use')
        parser.add_argument('--stats', type=str, help='specify the stats file to use')
        parser.add_argument('--insts', action='store_true', help='extension for --stats, stats about all executed instructions')
        parser.add_argument('--vars', action='store_true', help='extension for --stats, stats about all initialized variables')
        parser.add_argument('--hot', action='store_true', help='specify that the program should run in "hot" mode')
        parser.add_argument('--print', type=str, help='specify a string to print')
        parser.add_argument('--eol', action='store_true', help='specify that the program should use the end-of-line character')
        parser.add_argument('--frequent', action='store_true', help='specify that the program should print frequent output')
        # parse the arguments
        args = parser.parse_args()

        # checking the presence of --help arg -> verifing ony its presence in args
        if args.help:
            if len(sys.argv) != 2:
                Error.printExit("--help can only be used alone!\n", Error.parameter)
            else:
                self.printHelp()

        # checking for the use of --source or --input args
        if not args.source and not args.input:
            Error.printExit("One of the --source or --input args must be used!\n", Error.parameter)
        else:
            if args.source and not os.path.isfile(args.source):
                Error.printExit("Cannot open input file set by --source.\n", Error.stdIn)
            if args.input and not os.path.isfile(args.input):
                Error.printExit("Cannot open input file set by --input.\n", Error.stdIn)

        # setting source/input to stdin in case file is not provided
        if not args.source:
            args.source = sys.stdin
        if not args.input:
            args.input = sys.stdin

        # checking --stats options are not used without --stats
        if not args.stats and (args.insts or args.vars or args.hot or args.print or args.eol or args.frequent):
            Error.printExit("ERROR: Use of --stats options without --stats argument!\n", Error.parameter)
        
        # passing statistics requirements to statCounter
        self.statCounter = StatCounter(args)
        
        
        return self.statCounter


    # printing help message and exiting the program with exit code 0
    def printHelp(self):
        print("""
                interpret.py for IPPcode23
                 This program loads XMLfile and executes instructions written in IPPcode23
                Usage:
                --help -> displays help message
                --source=FILE -> this argument stores XMLfile with IPPcode23 (when not stated, it loads from STDIN)
                --input=FILE -> this argument stores data that IPPcode23 needs (when not stated, it loads from STDIN)
                --stats=FILE -> this argument will contain statistics data about the executed XML file
                --insts -> ex stats about all executed instructions
                --vars -> extension for --stats, stats about all initialized variables
                --hot -> writes value of order of the most used instruction with to lowest value of order atribute
                --print=string -> prints a string to stats
                --eol -> prints end of line into the stat file
                --frequent -> prints the most used OP codes
                  """)
        sys.exit(0)
