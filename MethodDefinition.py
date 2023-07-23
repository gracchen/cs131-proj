from VariableDefinition import VarDef
from StatementDefinition import StateDef
from ClassDefinition import ClassDef

class MethodDef():
    def __init__(self, program):
        self.name = program[1]
        self.params = program[2]
        self.body = StateDef(program[3])
    
    def run(self):
        self.body.run()