from VariableDefinition import VarDef
from intbase import InterpreterBase
from intbase import ErrorType
from MethodDefinition import MethodDef
from ObjectDefinition import ObjDef

class ClassDef():
    classes = []

    def __init__(self, program):
        self.name = program[1]
        self.fields = []
        self.methods = []
        for j in range(len(program)): # number of fields and methods in that class
            if (program[j][0] == InterpreterBase().FIELD_DEF):
                self.fields.append(VarDef(program[j][1],program[j][2]))
            if (program[j][0] == InterpreterBase().METHOD_DEF):
                self.methods.append(MethodDef(self, program[j]))
    
    def printAll(self):
        print(f'class():')
        for f in self.fields:
            print(f'\tfield "{f.name}" = {f.value}')
        for m in self.methods:
            print(f'\tmethod {m.name}({m.params}) = ({m.body.program})')

    def instantiate_object(self):
        obj = ObjDef(self)
        for m in self.methods:
            obj.add_method(m)
        for f in self.fields:
            obj.add_field(f)
        return obj
    
    def lookUpClass(self,name):
        for c in ClassDef.classes:
            if (c.name == name):
                return c.instantiate_object()
        return None    