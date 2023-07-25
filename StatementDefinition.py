
class StateDef():
    def __init__(self, c, program):
        self.c = c
        self.program = program

    def is_print(self):
        return self.program[0] == "print"

    def is_return(self):
        return self.program[0] == "return"

