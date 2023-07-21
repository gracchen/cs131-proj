from VariableDefinition import VarDef
class ClassDef():
    def __init__(self, name, fields, methods):
        self.name = name
        self.fields = fields
        self.methods = methods
    
    def printAll(self):
        print(f'class {self.name}():')
        for f in self.fields:
            print(f'\tfield "{f.name}" = {f.value}')
        #for m in self.methods:
            #print(f'\tmethod {m.name}({m.params}) = {m.body}')
        