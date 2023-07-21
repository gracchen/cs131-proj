import os
os.system("cls")

from intbase import InterpreterBase
from bparser import BParser

from VariableDefinition import VarDef
from ClassDefinition import ClassDef

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
        for i in range(len(parsed_program)): #parsed_program[i] = a new defined class
            if (parsed_program[i][0] != "class"):
                continue
            fields = []
            methods = []
            for j in range(len(parsed_program[i])): # number of fields and methods in that class
                if (parsed_program[i][j][0] == "field"):
                    #print(f'field of name "{parsed_program[i][j][1]}" with init val = {parsed_program[i][j][2]}')
                    fields.append(VarDef(parsed_program[i][j][1],parsed_program[i][j][2]))
                    f = fields[len(fields)-1]
                    #print(f'\tfield "{f.name}" = {f.value}')
                #if (parsed_program[i][j][0] == "method"):
                    #print(f'method of name "{parsed_program[i][j][1]}"')
            classes.append(ClassDef(parsed_program[i][1], fields, methods))
            classes[0].printAll()
            #(self, name, fields, methods):
            print("ddd\n")


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