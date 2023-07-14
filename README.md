# IPP PROJECT 2 - interpret.py

interpret.py for IPPcode23

BUT FIT / UMA ETSII

April 2023

## Classes
### Args
Represents command-line arguments
Includes methods for argument parsing
Control
Main class for controlling the interpretation process
Handles the interpretation of IPPcode23 instructions
### XML
Class for parsing XML source file
Includes methods for checking the XML structure and extracting instructions
### StatCounter
Class for counting and printing statistics
Handles the printing of required statistics
### InstructionList
Class for storing a list of instructions
Includes methods for inserting, sorting, and retrieving instructions
### Instruction
Class representing IPPcode23 instructions
Includes methods for parsing and manipulating instructions
### Frame
Class representing the frames of the IPPcode23
Includes methods for managing frames, variables, and values
### Error
Class for handling error messages and exiting the program
Includes static methods for printing error messages and error codes
## Usage
The task of the first part of the IPP project was to implement interpret.py, a program that interprets IPPcode23 instructions converted to their XML representation.

## Solution
My solution involved the implementation of an object-oriented design. The final solution consists of 8 classes that are linked to the main file interpret.py. In interpret.py, command-line arguments are loaded using the Args class. This class parses the arguments, checks their validity, and creates an instance of the Stats class if the --stat argument is present, which is used to count statistics. Then, an instance of the Control class is created, which contains the main method interpret() of the program. This method calls other methods for parsing the XML, creating a list of instructions, and performing interpretation.

## Design Patterns
Most of the classes implement the singleton pattern, as they require only one instance. The singleton pattern is applied to all the classes except the Instruction class. It was challenging to implement other design patterns for the interpretation program, as the singleton pattern suited the requirements well. However, there is one instance where the factory pattern could be applied, and that is in the InstructionList class. While the InstructionList class itself implements the singleton pattern, it partially implements the factory pattern for the Instruction class.

