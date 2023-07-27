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
        field.value = self.evalName(field.value)
        self.fields.append(field)
    
    def lookUpMethod(self,name):
        for m in self.methods:
            if (m.name == name):
                return m
        return None
    
    def lookUpField(self,name):
        for f in self.fields:
            if (f.name == name):
                return f
        return None
    
    # Interpret the specified method using the provided parameters    
    def call_method(self, method_name, params=[]): 
        method = self.lookUpMethod(method_name)
        if (method == None):
            InterpreterBase().error(ErrorType.NAME_ERROR, f"Method '{method_name}' is not defined.")
        statement = method.body
        if (len(params) != len(method.params)): #if call w/ args 1,2  then n=1 and m=2, so [1,2] for m.params=["n", "m"]
            InterpreterBase().error(ErrorType.NAME_ERROR, f"Method '{method_name}' given wrong number of parameters.")
        result = self.__run_statement(statement, method.params, params)
        return result

    # runs/interprets the passed-in statement until completion and 
    # gets the result, if any
    def __run_statement(self, statement, param_names, params):
        if statement.is_print():
            result = self.__execute_print(statement.program, param_names, params)
        elif statement.is_return():
            result = self.__execute_return(statement.program, param_names, params)
        return result

    def __execute_print(self, statement, param_names, params):
        converted_list = [str(elem) for elem in self.evaluate_expr(statement[1:], param_names, params)]
        output = "".join(converted_list)

        ib = InterpreterBase()
        ib.output(output)
        return None

    def __execute_return(self, statement, param_names, params):
        if (len(statement) <= 1): # just "(return)"
            return None
        converted_list = [str(elem) for elem in self.evaluate_expr(statement[1:], param_names, params)]
        output = "".join(converted_list)
        return output

    def evaluate_expr(self, expr, param_names=[], params=[]): #param_names=["n", "x"], params=[9,-1]
        print("evaluating",expr,"with param names",param_names,"and their corresponding values",params)
        op = ''
        if expr[0] == 'call':
            res = self.call_method(expr[2], expr[3:]) # temporarily ONLY "me" param-less methods
            if (res == None): 
                res = "None"
            return res
        elif expr[0] == '+' or expr[0] == '-' or expr[0] == '*' or expr[0] == '/' or expr[0] == '%' or expr[0] == '<' or expr[0] == '>' or expr[0] == '<=' or expr[0] == '>=' or expr[0] == '==' or expr[0] == '!=' or expr[0] == '!' or expr[0] == '&' or expr[0] == '|':
            op = expr[0]
            expr = expr[1:3]

        for i in range(len(expr)):
            expr[i] = self.evalName(expr[i], param_names, params)

        if op == '':
            return expr
        
        if op == '!' and isinstance(expr[0],bool):
            return not expr[0]
        
        if not ((isinstance(expr[0], bool) and isinstance(expr[1], bool)) or (isinstance(expr[0], int) and isinstance(expr[1], int)) or (isinstance(expr[0], str) and isinstance(expr[1], str))):
            InterpreterBase().error(ErrorType.TYPE_ERROR, f"'{expr[0]}' and {expr[1]} not of same type to perform operation.")
        
        if op == '==':
            return expr[0] == expr[1]
        if op == '!=':
            return expr[0] != expr[1]
            
        if (isinstance(expr[0], int)) or (isinstance(expr[0], str)):
            if op == '+':
                return expr[0] + expr[1]
            if op == '>':
                return expr[0] > expr[1]
            if op == '<':
                return expr[0] < expr[1]
            if op == '<=':
                return expr[0] <= expr[1]
            if op == '>=':
                return expr[0] >= expr[1]

        if(isinstance(expr[0], bool)):
            if (op == '&'):
                return expr[0] and expr[1]
            if (op == '|'):
                return expr[0] or expr[1]
        
        if (isinstance(expr[0], int)):
            if op == '-':
                return expr[0] - expr[1]
            if op == '*':
                return expr[0] * expr[1]
            if op == '/':
                return expr[0] // expr[1]
            if op == '%':
                return expr[0] % expr[1]
            InterpreterBase().error(ErrorType.TYPE_ERROR, f"'{expr[0]}' and {expr[1]} cannot use operation {op}.")
    
    def isString(self, input):
        return input[0] == '"' and input[-1] == '"'
    
    def isInt(self,input):
        return input.isdigit() or (input[0] == '-' and input[1:].isdigit())
    
    def evalName(self, name, param_names=[], params=[]):
        if type(name) is list: #sub expr
            name = self.evaluate_expr(name, param_names, params) #recursively process it
        elif name == 'true':
            name = True
        elif name == 'false':
            name = False
        elif self.isString(name[0]): # a string
            name = name[1:-1] # remove quotes
        elif self.lookUpField(name) != None: # a field
            name = self.lookUpField(name).value # get value
        elif name in param_names: # a param
            params[param_names.index(name)] = self.evalName(params[param_names.index(name)], param_names, params)
            name = params[param_names.index(name)] # get its given value
        elif (self.isInt(name)):
            name = int(name)
        else:
            InterpreterBase().error(ErrorType.NAME_ERROR, f"'{name}' is not defined.")
        return name