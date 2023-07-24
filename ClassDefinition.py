from VariableDefinition import VarDef
from intbase import InterpreterBase
from intbase import ErrorType
from MethodDefinition import MethodDef
from ObjectDefinition import ObjDef

class ClassDef():
    def __init__(self, program):
        self.name = program[1]
        self.fields = []
        self.methods = []
        for j in range(len(program)): # number of fields and methods in that class
            if (program[j][0] == "field"):
                self.fields.append(VarDef(program[j][1],program[j][2]))
            if (program[j][0] == "method"):
                self.methods.append(MethodDef(self, program[j]))
    
    def instantiate_object(self):
        obj = ObjDef()
        for m in self.methods:
            obj.add_method(m)
        for f in self.fields:
            obj.add_field(f)
        return obj