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

            c = ClassDef(parsed_program[i])
            classes.append(c)

            if (c.name == "main"):
                mainClass = c
            #classes[0].printAll()
            #print("---------------------------\n")
        
        if (mainClass != None): #runs main method's main.
            #main = mainClass.lookUpMethod("main")
            #if (main != None):
            m = mainClass.instantiate_object()
            #m.printAll()
            m.call_method("main")

program = [
    '(class main',
    ' (field num1 1)',
    ' (field num2 2)',
    ' (field tr true)',
    ' (field fa false)',
    ' (method main ()',
    '   (begin'
    '     (inputs num2)'
    '     (print "hello world! " (call me countDown 4) num1 num2)',
    '   )',
    ' )',
    ' (method retnum1 ()',
    '  (begin',
    '   (set tr false)',
    '   (if tr (return ":D") (print ":("))',
    '   (print "hi")',
    '  )',
    ' )' ,
    ' (method countDown (n)',
    '  (begin',
    '   (inputi n)',
    '   (while (> n 0)',
    '    (begin',
    '      (print "n is " n)',
    '      (set n (- n 1))',
    '    )',
    '   )' ,
    '   (return n)'
    '  )',
    ' )' ,
    ') # end of class']

'''
program = [
    '(class main',
    ' (field num1 1)',
    ' (field num2 2)',
    ' (field tr true)',
    ' (field fa false)',
    ' (method main ()',
    '   (print "hello world! " (call me retnum1) " " num2 " " -2 " " (call me retinput 2 num2))',
    ' )' ,
    ' (method retnum1 ()',
    '   (return (! tr))',
    ' )' ,
    ' (method retinput (n m)',
    '   (if true (return ":D") (return ":("))',
    ' )' ,
    ') # end of class']

program = [
    '(class main',
    ' (field num1 1)',
    ' (field num2 2)',
    ' (field tr true)',
    ' (field fa false)',
    ' (method main ()',
    '   (print "hello world! " (call me retnum1) " " num2 " " -2 " " (call me retinput 2 num2))',
    ' )' ,
    ' (method retnum1 ()',
    '   (set tr false)',
    ' )' ,
    ' (method retinput (n m)',
    '   (if tr (return ":D") (return ":("))',
    ' )' ,
    ') # end of class']
'''

import os
os.system("cls")
interpreter = Interpreter()
interpreter.run(program)