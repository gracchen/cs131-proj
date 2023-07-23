from VariableDefinition import VarDef
from intbase import InterpreterBase
from intbase import ErrorType

class ClassDef():
    def __init__(self, name, fields, methods):
        self.name = name
        self.fields = fields
        self.methods = methods
    
    def printAll(self):
        print(f'class {self.name}():')
        for f in self.fields:
            print(f'\tfield "{f.name}" = {f.value}')
        for m in self.methods:
            print(f'\tmethod {m.name}({m.params}) = ({m.body.program})')

    def lookUpMethod(self,name):
        for m in self.methods:
            if (m.name == name):
                return m
        return None  #interpreter = InterpreterBase()
        #interpreter.error(ErrorType.NAME_ERROR, f"Name '{name}' is not defined.", line_num=2)
    
    def lookUpField(self,name):
        for f in self.fields:
            if (f.name == name):
                return f
        return None  #interpreter = InterpreterBase()
        #interpreter.error(ErrorType.NAME_ERROR, f"Name '{name}' is not defined.", line_num=2)
    
        