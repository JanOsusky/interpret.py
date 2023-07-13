"""
        IPP PROJECT 2 - interpret.py

        Jan Osuský --- xosusk00

        interpret.py for IPPcode23

            BUT FIT / UMA ETSII

                 April 2023
"""
import xml.etree.ElementTree as ET
import sys

from classes.Error import Error
from classes.Instruction import Instruction
from classes.InstructionList import InstructionList

# class for parsing XML source file
class XML: 
    def __init__(self, source):
        self.source = source 
        
    
    # calls all the parsing methods
    def parse(self, instructionList):
        self.checkXML()
        return self.getInstrList(instructionList)

    # helping method 
    def checkNumOfArgs(self, instr, num):
        if (len(list(instr))) != num :
            Error.printExit("Number of args is not correct", Error.xmlStruct)

    
    # opens XML file and catches errors
    def checkXML(self):
        try:
            if self.source == 'sys.stdin':
                tree = ET.parse(sys.stdin) 
            else:
                tree = ET.parse(self.source) # --source was used
        except FileNotFoundError as e: # errors handling
            Error.printExit("File could not be open", Error.stdIn)
        except Exception as e:
            Error.printExit("XML is not correct", Error.xmlFormat)

        try:
            self.root = tree.getroot()
        except Exception as e:
            Error.printExit("Unable to get XML root", Error.xmlFormat)

        if self.root.tag != 'program' : # program check
            Error.printExit('XML root misses program atr', Error.xmlFormat)

        for atr in self.root.attrib : 
            if atr not in ['language', 'name', 'description'] : # allowed atr
                Error.printExit('Use of forbidden atribute', Error.xmlStructs)

        if 'language' not in self.root.attrib : # language check
            Error.printExit('XML root misses language atr', Error.xmlFormat)

        if self.root.attrib['language'].upper() != 'IPPCODE23': # check of the mandatory ippcode23
            Error.printExit('Value of languange atr is not IppCode23', Error.xmlFormat)

    # checks the instructions and creates list of instructions
    def getInstrList(self, instructionList):
        opcodeList = [] # storing opcode values
        for instruction in self.root :
            if instruction.tag != 'instruction': # checking xlm structure instruction
                Error.printExit('Wrong element name', Error.xmlStruct)
            if 'order' not in instruction.attrib : # checking xlm structure
                Error.printExit('Missing atr order', Error.xmlStruct)
            if 'opcode' not in instruction.attrib : # checking xlm structure
                Error.printExit('Missing atr opcode', Error.xmlStruct)
            try:
                instrNumber = int(instruction.attrib['order']) # parsing order value
            except ValueError:
                Error.printExit('Opcode wasnt read', Error.xmlStruct) 
            if instrNumber <= 0 : # greater than 0
                Error.printExit('Opcode must be a positive number', Error.xmlStruct)
            if  instrNumber in opcodeList: # checking its uniqueness
                Error.printExit('Duplicit use of opcode', Error.xmlStruct)
            else:
                opcodeList.append(instrNumber) # adding new order to the list
            
            # checking the instruction arguments
            counter = 0
            for argument in instruction :
                counter += 1
                if argument.tag != 'arg'+str(counter) :
                    Error.printExit('Args order error', Error.xmlStruct) # wrong args order
                if 'type' not in argument.attrib :
                    Error.printExit('Missing atribute type', Error.xmlStruct)
                if argument.attrib['type'] not in ['string', 'int', 'bool', 'label', 'type', 'nil', 'var'] : # wrong type of instruction
                    Error.printExit('Wrong instruction type', Error.xmlStruct)
            
            # checking number of arguments that are supposed to be present at 
            if instruction.attrib['opcode'].upper() in ['CREATEFRAME', 'PUSHFRAME', 'POPFRAME', 'BREAK', 'RETURN'] :
                self.checkNumOfArgs(instruction, 0)
                i = Instruction(int(instruction.attrib['order']),instruction.attrib['opcode'].upper()) # 0 args
                instructionList.insert(i)
            elif instruction.attrib['opcode'].upper() in ['DPRINT', 'DEFVAR', 'CALL', 'PUSHS', 'POPS', 'LABEL', 'JUMP', 'WRITE', 'EXIT'] :
                self.checkNumOfArgs(instruction, 1)
                i = Instruction(int(instruction.attrib['order']), instruction.attrib['opcode'].upper(), instruction[0]) # 1 args
                instructionList.insert(i)
            elif instruction.attrib['opcode'].upper() in ['MOVE', 'INT2CHAR', 'READ', 'STRLEN', 'TYPE', 'NOT'] :
                self.checkNumOfArgs(instruction, 2)
                i = Instruction(int(instruction.attrib['order']),instruction.attrib['opcode'].upper(), instruction[0], instruction[1]) # 2 args
                instructionList.insert(i)
            elif instruction.attrib['opcode'].upper() in ['ADD', 'SUB', 'MUL', 'IDIV', 'LT', 'GT', 'EQ', 'AND', 'OR', 'JUMPIFEQ', 'JUMPIFNEQ', 'STRI2INT', 'CONCAT', 'GETCHAR', 'SETCHAR'] :
                self.checkNumOfArgs(instruction, 3)
                i = Instruction(int(instruction.attrib['order']),instruction.attrib['opcode'].upper(), instruction[0], instruction[1], instruction[2])  # 3 args
                instructionList.insert(i)
            else :
                Error.printExit("Other xml error", Error.xmlStruct)

        return InstructionList.sortList(instructionList.list) # returnning sorted instruction list


       
    
