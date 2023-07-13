"""
        IPP PROJECT 2 - interpret.py

        Jan Osuský --- xosusk00

        interpret.py for IPPcode23

            BUT FIT / UMA ETSII

                 April 2023
"""

from classes.Error import Error

# class for representing instructions
class Instruction:
    def __init__(self, order, type, arg1=None, arg2=None, arg3=None):
        self.order = order # order of the instruction in the XML file can not be sorted correctly
        self.type = type
        self.counter = 0 # number of args
        # read of args if presenet 
        if arg1 is not None: # structure from the XML parser class
            self.arg1 = {'type' : arg1.attrib['type'] , 'data' :  (arg1.text if arg1.text is not None else '')}
            self.counter += 1
        if arg2 is not None:
            self.arg2 = {'type' : arg2.attrib['type'] , 'data' :  (arg2.text if arg2.text is not None else '')}
            self.counter += 1
        if arg3 is not None:
            self.arg3 = {'type' : arg3.attrib['type'] , 'data' :  (arg3.text if arg3.text is not None else '')}
            self.counter += 1

    # spliting 2 parts or a variable
    @staticmethod
    def splitVar(var):
        return var['data'].split('@', 1)
    
    # getting argument timpe and value 
    def getArgTypeAndData(self, argument, frameClassObj):
        if argument['type'] in ['int', 'bool', 'string', 'type', 'label', 'nil'] :
            return(argument['type'], argument['data'])
        else :
            frame, data = self.splitVar(argument)
            frameObj = frameClassObj.getFrame(frame)
            if frameObj is None :
                Error.printExit('Not defined frame', Error.missFrame)
            if data not in frameObj :
                Error.printExit('not defined var in frame', Error.missVar)
            else :
                if (frameObj[data]['type'] is None or frameObj[data]['data'] is None) :
                    Error.printExit('Not defined var', Error.missVal)
                    
                return(frameObj[data]['type'], frameObj[data]['data'])
            
    # getting type of the instr
    def getType(self, argument, frameObj):
        if argument['type'] in ['int', 'bool', 'string', 'type', 'label', 'nil'] :
            return argument['type']
        else :
            frame, data = self.splitVar(argument)
            frameObj = frameObj.getFrame(frame)
            if frameObj is None :
                Error.printExit('Var error', Error.missFrame)
            if data not in frameObj :
                Error.printExit('Var error', Error.missVar)
            else :
                if frameObj[data]['type'] is None :
                    return None
                return frameObj[data]['type']