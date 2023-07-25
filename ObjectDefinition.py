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
        if (method == None):
            InterpreterBase().error(ErrorType.NAME_ERROR, f"Method '{method_name}' is not defined.")
        statement = method.body
        result = self.__run_statement(statement)
        return result

    # runs/interprets the passed-in statement until completion and 
    # gets the result, if any
    def __run_statement(self, statement):
        if statement.is_print():
            result = self.__execute_print(statement.program)
        elif statement.is_return():
            result = self.__execute_return(statement.program)
        return result

    def __execute_print(self, statement):
        output = "".join(self.evaluate_expr(statement[1:]))

        ib = InterpreterBase()
        ib.output(output)
        return None

    def __execute_return(self, statement):
        if (len(statement) <= 1): # just "(return)"
            return None
        output = "".join(self.evaluate_expr(statement[1:]))
        return output

    def evaluate_expr(self, expr):
        if expr[0] == 'call':
            res = self.call_method(expr[2]) # temporarily ONLY "me" param-less methods
            if (res == None): 
                res = "None"
            return res
        
        for i in range(len(expr)):
            if type(expr[i]) is list:
                expr[i] = self.evaluate_expr(expr[i]) #recursively process sublists
                continue
            name = expr[i]
            if name[0] == '"' and name[-1] == '"': # a string
                expr[i] = expr[i][1:-1] # remove quotes
                continue
            if self.lookUpField(name) != None: # a field
                expr[i] = self.lookUpField(expr[i]).value # get value
                continue

        return expr