"""
        IPP PROJECT 2 - interpret.py

        Jan Osuský --- xosusk00

        interpret.py for IPPcode23

            BUT FIT / UMA ETSII

                 April 2023
"""

from classes.Error import Error
import classes.Instruction as instr

# representing the frames of the IPPcode23
class Frame :
    def __init__(self):
        self.GF = {}
        self.TF = {}
        self.TFDef = False
        self.frameStack = []
    #
    # returning the frame specified in parameter
    def getFrame(self, frame):
        if frame == 'GF':
            return self.GF
        elif frame == 'LF':
            return (self.frameStack[-1] if len(self.frameStack) > 0 else None)
        elif frame == 'TF':
            return (self.TF if self.TFDef else None)
        else:
            return None
        
    # implementations of instruction:
    def createFrame(self):
        self.TF = {}
        self.TFDef = True

    # implementations of instruction:
    def pushFrame(self):
        if self.TFDef :
            self.frameStack.append(self.TF) # adding Tempororary frame
            self.TFDef = False
        else :
            Error.printExit('Pushframe with non exisint frame', Error.missFrame)

    # poping frame 
    def popFrame(self):
        if len(self.frameStack) :
            self.TF = self.frameStack.pop() # poping
            self.TFdef = True
        else :
            Error.printExit('Poprframe with empty stack', Error.missFrame)

     # definng new variable 
    def defVar(self, argument) :
        frame, name = instr.Instruction.splitVar(argument) # spliting with @
        frameD = self.getFrame(frame)
        if frameD is None :
            Error.printExit('Non existing frame', Error.missFrame)
        else :
            if name in frameD :
                Error.printExit('Already existing var', Error.semantic)
            else :
                frameD[name] = {'data': None, 'type': None}

    # seting value of a variable
    def setVar(self, argument, typ, value) :
        frame, name = instr.Instruction.splitVar(argument) # spliting with @
        frameD = self.getFrame(frame)
        if frameD is None :
            Error.printExit('Non exiting var', Error.missFrame)
        if name not in frameD :
            Error.printExit('Non exiting var', Error.missVar)
        frameD[name]['type'] = typ
        frameD[name]['data'] = value

   