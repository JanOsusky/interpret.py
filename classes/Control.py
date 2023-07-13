"""
        IPP PROJECT 2 - interpret.py

        Jan Osuský --- xosusk00

        interpret.py for IPPcode23

            BUT FIT / UMA ETSII

                 April 2023
"""

from classes.Frame import Frame
from classes.InstructionList import InstructionList
from classes.XML import XML
from classes.Error import Error

import sys




# main class interpreting the entire program
#
class Control:
    def __init__(self, source, input):
        self.source = source
        self.input = input
        self.frame = Frame()
        self.instructionList = InstructionList()
        self.parser = XML(source)
        self.dataStack = []

    # main method performing all the interpretation
    def interpret(self):
        self.parser.parse(self.instructionList) # parsing xml
        
        self.instructionList.checkStrings() # removing backslashes

        lineCounter = 0
        
        while True :
            # get next instruction
            instruction = self.instructionList.getNext()

            # end of file 
            if (instruction == None) :
                break

            # looking for the right instr
            if instruction.type == 'WRITE' or instruction.type == 'DPRINT':
                aType, aData = instruction.getArgTypeAndData(instruction.arg1, self.frame)
                if aData == None:
                    Error.printExit('Error', Error.missVal)
                else :
                    if (aType == 'nil' and aData == 'nil') :
                        aData = ''

                    if instruction.type == 'WRITE' :
                        print(aData, end='')
                    else:
                        pass

            elif instruction.type == 'BREAK' :
                pass

            elif instruction.type == 'CREATEFRAME' :
                self.frame.createFrame()

            elif instruction.type == 'PUSHFRAME' :
                self.frame.pushFrame()

            elif instruction.type == 'POPFRAME' :
                self.frame.popFrame()

            elif instruction.type == 'DEFVAR' :
                self.frame.defVar(instruction.arg1)

            elif instruction.type == 'PUSHS' :
                typee, data = instruction.getArgTypeAndData(instruction.arg1, self.frame)
                self.dataStack.append((typee, data))

            elif instruction.type == 'POPS' :
                try:
                    typee, data = self.dataStack.pop()
                except IndexError :
                    Error.printExit('Error', Error.missVal)
                self.frame.setVar(instruction.arg1, typee, data)

            elif instruction.type == 'MOVE' :
                typee, data = instruction.getArgTypeAndData(instruction.arg2, self.frame)
                self.frame.setVar(instruction.arg1, typee, data)

            elif instruction.type == 'CALL' :
                self.instructionList.storePosition()
                self.instructionList.jump(instruction.arg1)

            elif instruction.type == 'RETURN' :
                self.instructionList.restorePosition()

            elif instruction.type in ['ADD', 'SUB', 'MUL', 'IDIV'] :
                type1, data1 = instruction.getArgTypeAndData(instruction.arg2, self.frame)
                type2, data2 = instruction.getArgTypeAndData(instruction.arg3, self.frame)
                if type1 == type2 == 'int' :
                    if instruction.type == 'ADD':
                        self.frame.setVar(instruction.arg1, 'int', str(int(data1)+int(data2)))
                    elif instruction.type == 'SUB':
                        self.frame.setVar(instruction.arg1, 'int', str(int(data1) - int(data2)))
                    elif instruction.type == 'MUL':
                        self.frame.setVar(instruction.arg1, 'int', str(int(data1) * int(data2)))
                    else:
                        if int(data2) == 0:
                            Error.printExit('Error', Error.wrongOpVal)
                        else:
                            self.frame.setVar(instruction.arg1, 'int', str(int(data1) // int(data2)))
                else :
                    Error.printExit('Error', Error.wrongOp)

            elif instruction.type in ['LT', 'GT', 'EQ'] :
                type1, data1 = instruction.getArgTypeAndData(instruction.arg2, self.frame)
                type2, data2 = instruction.getArgTypeAndData(instruction.arg3, self.frame)

                if type1 == type2 :
                    if instruction.type == 'EQ' :
                        self.frame.setVar(instruction.arg1, 'bool', 'true' if data1 == data2 else 'false')
                    elif (instruction.type in ['GT', 'LT'] and (type1 == 'nil' and type2 == 'nil')) :
                        Error.printExit('Error', Error.wrongOp)
                    elif instruction.type == 'LT' :
                        if type1 == 'string' :
                            self.frame.setVar(instruction.arg1, 'bool', 'true' if data1 < data2 else 'false')
                        elif type1 == 'nil' :
                            self.frame.setVar(instruction.arg1, 'bool', 'false')
                        elif type1 == 'bool':
                            self.frame.setVar(instruction.arg1, 'bool', 'true' if data1 == 'false' and data2 == 'true' else 'false')
                        else :
                            self.frame.setVar(instruction.arg1, 'bool', 'true' if int(data1) < int(data2) else 'false')
                    else :
                        if type1 == 'string' :
                            self.frame.setVar(instruction.arg1, 'bool', 'true' if data1 > data2 else 'false')
                        elif type1 == 'nil' :
                            self.frame.setVar(instruction.arg1, 'bool', 'false')
                        elif type1 == 'bool':
                            self.frame.setVar(instruction.arg1, 'bool', 'true' if data1 == 'true' and data2 == 'false' else 'false')
                        else :
                            self.frame.setVar(instruction.arg1, 'bool', 'true' if int(data1) > int(data2) else 'false')

                elif instruction.type == 'EQ' and (type1 == 'nil' or type2 == 'nil') :
                    self.frame.setVar(instruction.arg1, 'bool', 'false')
                else :
                    Error.printExit('Error', Error.wrongOp)

            elif instruction.type in ['AND', 'OR'] :
                type1, data1 = instruction.getArgTypeAndData(instruction.arg2, self.frame)
                type2, data2 = instruction.getArgTypeAndData(instruction.arg3, self.frame)

                if type1 == type2 == 'bool' :
                    if instruction.type == 'AND' :
                        self.frame.setVar(instruction.arg1, 'bool', 'true' if data1 == data2 == 'true' else 'false')
                    else :
                        self.frame.setVar(instruction.arg1, 'bool', 'true' if data1 == 'true' or data2 == 'true' else 'false')
                else :
                    Error.printExit('Error ' + type1 + ' a ' + type2 + '.', Error.wrongOp)

            elif instruction.type == 'NOT' :
                type1, data1 = instruction.getArgTypeAndData(instruction.arg2, self.frame)
                if type1 == 'bool':
                    self.frame.setVar(instruction.arg1, 'bool', 'true' if data1 == 'false' else 'false')
                else :
                    Error.printExit('Error' + type1 + '.', Error.wrongOp)

            elif instruction.type == 'INT2CHAR' :
                type1, data1 = instruction.getArgTypeAndData(instruction.arg2, self.frame)
                if type1 == 'int' :
                    try:
                        char = chr(int(data1))
                    except ValueError:
                        Error.printExit('Error', Error.string)
                    self.frame.setVar(instruction.arg1, 'string', char)
                else :
                    Error.printExit('Error' + type1 + '.', Error.wrongOp)

            elif instruction.type == 'STRI2INT' :
                type1, data1 = instruction.getArgTypeAndData(instruction.arg2, self.frame)
                type2, data2 = instruction.getArgTypeAndData(instruction.arg3, self.frame)

                if type1 == 'string' and type2 == 'int' :
                    i = int(data2)
                    if i >= 0 and i <= len(data1) - 1 :
                        ordd = ord(data1[i])
                        self.frame.setVar(instruction.arg1, 'int', ordd)
                    else :
                        Error.printExit('Error', Error.string)
                else :
                    Error.printExit('Error' + type1 + ' a ' + type2 + '.', Error.wrongOp)

            elif instruction.type == 'READ' :
                type1, data1 = instruction.getArgTypeAndData(instruction.arg2, self.frame)

                if len(self.input) :
                    try :
                        with open(self.input) as file :
                            uis = file.read().splitlines()
                    except FileNotFoundError :
                        Error.printExit('Error', Error.stdIn)

                    try:
                        userInput = uis[lineCounter]
                    except IndexError:
                        sys.stderr.write('Error')
                        self.frame.setVar(instruction.arg1, 'nil', '')
                        continue
                    finally :
                        lineCounter += 1
                else :
                    try :
                        userInput = input()
                    except Exception :
                        Error.printExit('Error', Error.stdIn)

                if data1 == 'int' :
                    try:
                        number = str(int(userInput))
                    except :
                        sys.stderr.write('Error')
                        self.frame.setVar(instruction.arg1, 'nil', '')
                    else :
                        self.frame.setVar(instruction.arg1, 'int', number)
                elif data1 == 'bool' :
                    if userInput.lower() == 'true' :
                        self.frame.setVar(instruction.arg1, 'bool', 'true')
                    elif userInput.lower() == 'false' :
                        self.frame.setVar(instruction.arg1, 'bool', 'false')
                    else :
                        sys.stderr.write('Error')
                        self.frame.setVar(instruction.arg1, 'bool', 'false')
                else :
                    self.frame.setVar(instruction.arg1, 'string', userInput)

            elif instruction.type == 'CONCAT' :
                type1, data1 = instruction.getArgTypeAndData(instruction.arg2, self.frame)
                type2, data2 = instruction.getArgTypeAndData(instruction.arg3, self.frame)

                if type1 == type2 == 'string' :
                    data1 = '' if data1 is None else data1
                    data2 = '' if data2 is None else data2
                    self.frame.setVar(instruction.arg1, 'string', data1 + data2)
                else :
                    Error.printExit('Error', Error.wrongOp) 

            elif instruction.type == 'STRLEN' :
                type1, data1 = instruction.getArgTypeAndData(instruction.arg2, self.frame)

                if type1 == 'string' :
                    self.frame.setVar(instruction.arg1, 'int', len(data1))
                else :
                    Error.printExit('Error', Error.wrongOp)

            elif instruction.type == 'GETCHAR' :
                type1, data1 = instruction.getArgTypeAndData(instruction.arg2, self.frame)
                type2, data2 = instruction.getArgTypeAndData(instruction.arg3, self.frame)

                if type1 == 'string' and type2 == 'int' :
                    number = int(data2)
                    if number >= 0 and number < len(data1) :
                        self.frame.setVar(instruction.arg1, 'string', data1[number])
                    else :
                        Error.printExit('Error', Error.string)
                else :
                    Error.printExit('Error', Error.wrongOp)

            elif instruction.type == 'SETCHAR' :
                type1, data1 = instruction.getArgTypeAndData(instruction.arg2, self.frame)
                type2, data2 = instruction.getArgTypeAndData(instruction.arg3, self.frame)
                dataV: str
                typeV, dataV = instruction.getArgTypeAndData(instruction.arg1, self.frame)

                if type1 == 'int' and type2 == 'string' and typeV == 'string':
                    number = int(data1)
                    if number < 0 or number >= len(dataV) or dataV == '' :
                        Error.printExit('Error', Error.string)
                    if data2 == '' :
                        Error.printExit('Error', Error.string)
                    else :
                        data_list = list(dataV)
                        data_list[number] = data2[0]
                        dataV = "".join(data_list)
                        self.frame.setVar(instruction.arg1, 'string', dataV)
                else :
                    Error.printExit('Error', Error.wrongOp)

            elif instruction.type == 'TYPE' :
                type1 = instruction.getType(instruction.arg2, self.frame)
                if type1 is None :
                    type1 = ''
                self.frame.setVar(instruction.arg1, 'string', type1)

            elif instruction.type == 'LABEL' :
                continue
            
            elif instruction.type in ['JUMPIFEQ', 'JUMPIFNEQ'] :
                type1, data1 = instruction.getArgTypeAndData(instruction.arg2, self.frame)
                type2, data2 = instruction.getArgTypeAndData(instruction.arg3, self.frame)

                self.instructionList.checkLabel(instruction.arg1)

                if (type1 == type2 or type1 == 'nil' or type2 == 'nil') :
                    if instruction.type == 'JUMPIFEQ' and data1 == data2 :
                        self.instructionList.jump(instruction.arg1)
                    elif instruction.type == 'JUMPIFNEQ' and data1 != data2 :
                        self.instructionList.jump(instruction.arg1)
                    else :
                        pass
                else :
                    Error.printExit('Error', Error.wrongOp)

            elif instruction.type == 'JUMP' :
                self.instructionList.jump(instruction.arg1)

            elif instruction.type == 'EXIT' :
                type1, data1 = instruction.getArgTypeAndData(instruction.arg1, self.frame)

                if type1 != 'int' :
                    Error.printExit('Error', Error.wrongOp)
                else :
                    number = int(data1)
                    if number < 0 or number > 49 :
                        Error.printExit('Error', Error.wrongOpVal)
                    else :
                        #Error.printExit('Error',)
                        pass
