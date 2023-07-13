"""
        IPP PROJECT 2 - interpret.py

        Jan Osuský --- xosusk00

        interpret.py for IPPcode23

            BUT FIT / UMA ETSII

                 April 2023
"""

class StatCounter:
    
    # --insts --vars --hot --print=string --eol --frequent
    insts = 0
    vars = 0
    hot = 0
    # string form print will be passed directly
    # eol will be passed direcly
    frequent = []
    def __init__(self, args):
        self.args = args

    # opens the --stat=FILE and writes required stats in it
    def printArgs(self):
        pass