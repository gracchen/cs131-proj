from VariableDefinition import VarDef
from intbase import InterpreterBase
from intbase import ErrorType
from MethodDefinition import MethodDef

class ObjDef():
    def __init__(self):
        self.fields = []
        self.methods = []

    def printAll(self):
        print(f'class():')
        for f in self.fields:
            print(f'\tfield "{f.name}" = {f.value}')
        for m in self.methods:
            print(f'\tmethod {m.name}({m.params}) = ({m.body.program})')

    def add_method(self, method):
        self.methods.append(method)

    def add_field(self, field):
        self.fields.append(field)
    
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
    
    # Interpret the specified method using the provided parameters    
    def call_method(self, method_name):
        method = self.lookUpMethod(method_name)
        statement = method.body
        result = self.__run_statement(statement)
        return result

    # runs/interprets the passed-in statement until completion and 
    # gets the result, if any
    def __run_statement(self, statement):
        if statement.is_print():
            result = self.__execute_print(statement.program)
        return result

    def __execute_print(self, statement):
        #print(statement)
        #if len(statement.program) too small ERROR
        statement = statement[1:]
        for i in range(len(statement)):
            if statement[i][0] == '"' and statement[i][-1] == '"':
                statement[i] = statement[i][1:-1] #remove quotes
            else :
                statement[i] = self.lookUpField(statement[i]).value

        output = "".join(statement)

        ib = InterpreterBase()
        ib.output(output)