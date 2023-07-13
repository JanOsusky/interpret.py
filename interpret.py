"""
        IPP PROJECT 2 - interpret.py

        Jan Osuský --- xosusk00

        interpret.py for IPPcode23

            BUT FIT / UMA ETSII

                 April 2023
"""
import sys
from classes.Args import Args
from classes.Control import Control


# instance of Args for argument parsing

args = Args()

statcounter = args.parse()

control = Control(statcounter.args.source, statcounter.args.input)

control.interpret()
exit(0) # succces



