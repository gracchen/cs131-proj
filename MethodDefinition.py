from VariableDefinition import VarDef
from StatementDefinition import StateDef

class MethodDef():
    def __init__(self, c, program):
        self.c = c #class
        self.name = program[1]
        self.params = program[2]
        self.body = StateDef(c, program[3])
