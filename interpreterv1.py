import os
os.system("cls")

from intbase import InterpreterBase
from bparser import BParser

from VariableDefinition import VarDef
from ClassDefinition import ClassDef
from StatementDefinition import StateDef
from MethodDefinition import MethodDef

class Interpreter(InterpreterBase): 
    def __init__(self, console_output=True, inp=None, trace_output=True):
        super().__init__(console_output, inp)   # call InterpreterBase’s constructor

    def run(self, program):
        #parse program
        result, parsed_program = BParser.parse(program)
       
        if result == False:
            print('Parsing failed. There must have been a mismatched parenthesis.')
            return
        classes = []
        mainClass = None
        for i in range(len(parsed_program)): #parsed_program[i] = a new defined class
            if (parsed_program[i][0] != "class"):
                continue
            fields = []
            methods = []
            for j in range(len(parsed_program[i])): # number of fields and methods in that class
                if (parsed_program[i][j][0] == "field"):
                    fields.append(VarDef(parsed_program[i][j][1],parsed_program[i][j][2]))
                if (parsed_program[i][j][0] == "method"):
                    methods.append(MethodDef(parsed_program[i][j]))
            
            c = ClassDef(parsed_program[i][1], fields, methods)
            classes.append(c)

            if (c.name == "main"):
                mainClass = c
            classes[0].printAll()
            print("---------------------------\n")
        
        if (mainClass != None): #runs main method's main.
            m = mainClass.lookUpMethod("main")
            if (m != None):
                m.run()

program = [
    '(class main',
    ' (field num1 0)',
    ' (field num2 1)',
    ' (method main ()',
    '   (print "hello world!")',
    ' ) # end of method',
    ') # end of class']

interpreter = Interpreter()
interpreter.run(program)