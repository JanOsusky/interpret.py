"""
        IPP PROJECT 2 - interpret.py

        Jan Osuský --- xosusk00

        interpret.py for IPPcode23

            BUT FIT / UMA ETSII

                 April 2023
"""

from classes.Error import Error
import classes.Instruction as instruction

# class for storing list of instrution
class InstructionList:
    def __init__(self):
        self.counter = 0 
        self.current = 1
        self.list = {}
        self.callstack = []
        self.labels = {}

    # inserting new instruction
    def insert(self, instr):
        self.counter += 1
        self.list[self.counter] = instr # adding new instr to the list

        if instr.type == 'LABEL' :
            name = instr.arg1['data']
            if name not in self.labels :
                self.labels[name] = self.counter
            else:
                Error.printExit('Label redefinition error', Error.semantic)
    
    # sorting list by order atribute
    @staticmethod
    def sortList(instrList):
        return dict(sorted(instrList.items(), key=lambda x: x[1].order))
    
    # gettin next instruction from the list
    def getNext(self):
        if (self.current <= self.counter) :
            self.current += 1
            return self.list[self.current - 1]
        else:
            return None
    
    # storing instr pos
    def storePosition(self) :
        self.callstack.append(self.current)

    # restoring instr pos
    def restorePosition(self) :
        if len(self.callstack) :
            self.current = self.callstack.pop()
        else :
            Error.printExit('No value in stack', Error.missVal)

    # checking jump instr
    def jump(self, argument) :
        name = argument['data']
        if name in self.labels :
            self.current = self.labels[name]
        else :
            Error.printExit('Jump to not existing labes', Error.semantic)
    # cheking args
    def checkLabel(self, argument) :
        name = argument['data']
        if name not in self.labels :
            Error.printExit('Jump to not existing labes', Error.semantic)
    # fixing strings
    def fixString(self, string):
        index: int = string.find('\\')
        while(index != -1) :
            string = string.replace(string[index:index+4], chr(int(string[index+1:index+4])))
            index = string.find('\\', index + 1)
        return string

    # checking string validity   
    def checkStrings(self):
        for ins in self.list:
            instruction = self.list[ins]
            if hasattr(instruction, 'arg1'):
                if instruction.arg1['type'] == 'string':
                    if 'data' in instruction.arg1:
                        instruction.arg1['data'] = self.fixString(instruction.arg1['data'])
            if hasattr(instruction, 'arg2'):
                if instruction.arg2['type'] == 'string':
                    if 'data' in instruction.arg2:
                        instruction.arg2['data'] = self.fixString(instruction.arg2['data'])
            if hasattr(instruction, 'arg3'):
                if instruction.arg3['type'] == 'string':
                    if 'data' in instruction.arg3:
                        instruction.arg3['data'] = self.fixString(instruction.arg3['data'])
