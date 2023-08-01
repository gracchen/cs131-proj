
from intbase import InterpreterBase

class StateDef():
    def __init__(self, c, program):
        self.c = c
        self.program = program

    def is_print(self):
        return self.program[0] == InterpreterBase().PRINT_DEF

    def is_return(self):
        return self.program[0] == InterpreterBase().RETURN_DEF

    def is_if(self):
        return self.program[0] == InterpreterBase().IF_DEF
    
    def is_set(self):
        return self.program[0] == InterpreterBase().SET_DEF
    
    def is_begin(self):
        return self.program[0] == InterpreterBase().BEGIN_DEF
    
    def is_while(self):
        return self.program[0] == InterpreterBase().WHILE_DEF

    def is_inputs(self):
        return self.program[0] == InterpreterBase().INPUT_STRING_DEF

    def is_inputi(self):
        return self.program[0] == InterpreterBase().INPUT_INT_DEF

    def is_call(self):
        return self.program[0] == InterpreterBase().CALL_DEF

    def is_new(self):
        return self.program[0] == InterpreterBase().NEW_DEF
    
