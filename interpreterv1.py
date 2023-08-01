from intbase import InterpreterBase
from bparser import BParser

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
        
        mainClass = None

        for i in range(len(parsed_program)): #parsed_program[i] = a new defined class
            if (parsed_program[i][0] != InterpreterBase().CLASS_DEF):
                continue

            c = ClassDef(parsed_program[i])
            ClassDef.classes.append(c)

            if (c.name == InterpreterBase().MAIN_CLASS_DEF):
                mainClass = c
            #classes[0].printAll()
            #print("---------------------------\n")
        
        if (mainClass != None): #runs main method's main.
            #main = mainClass.lookUpMethod("main")
            #if (main != None):
            m = mainClass.instantiate_object()
            #m.printAll()
            m.call_method(InterpreterBase().MAIN_FUNC_DEF)

        #for c in mainClass.classes:
        #    c.printAll()

        #print(len(ClassDef.classes))
        #print(len(mainClass.classes))

#    NULL_DEF = "null"
#    NEW_DEF = "new"
#    ME_DEF = "me"


program = ['	 (class main',
'         (field other null)',
'         (field result 0)',
'         (method main ()',
'           (begin',
'             (call me foo 10 20)   # call foo method in same object',
'             (set other (new other_class))',
'             (call other foo 5 6)  # call foo method in other object',
'             (print "square: " (call other square 10)) # call expression',
'           )',
'         )',
'         (method foo (a b)',
'          (print a " " b)',
'         )',
'       )',
'',
' (class other_class',
'         (method foo (q r) (print q " " r))',
'         (method square (q) (return (* q q)))',
'       )',
'',]





'''
program = [
'(class person',
'   (field name "")',
'   (field age 0)',
'   (method init (n a) (begin (set name n) (set age a)))',
'   (method talk (to_whom) (print name " says hello to " to_whom))',
'   (method get_age () (return age))',
')',
'',
'(class main',
' (field p null)',
' (method tell_joke (to_whom) (print "Hey " to_whom ", knock knock!"))',
' (method main ()',
'   (begin',
'      (call me tell_joke "Leia")  # calling method in the current obj',
'      (set p (new person))    ',
'      (call p init "Siddarth" 25)  # calling method in other object',
'      (call p talk "Boyan")        # calling method in other object',
'      (print "Siddarths age is " (call p get_age))',
'   )',
' )',
')',
]


program = [
    '(class main',
    ' (field num1 1)',
    ' (field num2 2)',
    ' (field tr true)',
    ' (field fa false)',
    ' (method main ()',
    '   (begin'
    '     (inputs num2)'
    '     (set fa (new other_class))',
    '     (print "hello world! " (call fa foo) num1 num2)',
    '     (call me retnum1)',
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
    ') # end of class',
    '(class other_class (field a 10) (method foo () (print "ayooooo foo here " a ))) '
    
    
    ]





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