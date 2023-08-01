from VariableDefinition import VarDef
from intbase import InterpreterBase
from intbase import ErrorType
from MethodDefinition import MethodDef
from StatementDefinition import StateDef

class ObjDef():
    def __init__(self, c):
        self.fields = []
        self.methods = []
        self.c = c

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
    
    def lookUpClass(self,name):
        return self.c.lookUpClass()
    
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
            return self.__execute_print(statement.program, param_names, params)
        if statement.is_return():
            return self.__execute_return(statement.program, param_names, params)
        if statement.is_if():
            return self.__execute_if(statement.program, param_names, params)
        if statement.is_while():
            return self.__execute_while(statement.program, param_names, params)
        if statement.is_set():
            return self.__execute_set(statement.program, param_names, params)
        if statement.is_begin():
            return self.__execute_begin(statement.program, param_names, params)
        if statement.is_inputs():
            return self.__execute_inputs(statement.program, param_names, params)
        if statement.is_inputi():
            return self.__execute_inputi(statement.program, param_names, params)
        if statement.is_call():
            return self.__execute_call(statement.program, param_names, params)
        if statement.is_new():
            return self.__execute_new(statement.program, param_names, params)
        InterpreterBase().error(ErrorType.TYPE_ERROR, f"expression {statement.program} invalid.")

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
    
    def __execute_if(self, statement, param_names, params):
        condition = self.evalName(statement[1], param_names, params)
        
        if (not isinstance(condition, bool)):
            InterpreterBase().error(ErrorType.TYPE_ERROR, f"condition ({statement[1]}) in if statement not a boolean type.")
        
        if (condition):
            result = self.__run_statement(StateDef(None, statement[2]), param_names, params)
        elif (len(statement) == 4):
            result = self.__run_statement(StateDef(None, statement[3]), param_names, params)
        return result
    
    def __execute_while(self, statement, param_names, params):
        condition = self.evalName(statement[1], param_names, params)
        
        if (not isinstance(condition, bool)):
            InterpreterBase().error(ErrorType.TYPE_ERROR, f"condition ({statement[1]}) in while statement not a boolean type.")
        
        result = None
        while (condition and result == None): # if had a "return", result != None and need to stop
            result = self.__run_statement(StateDef(None, statement[2]), param_names, params)
            condition = self.evalName(statement[1], param_names, params)
        return result

    def __execute_set(self, statement, param_names, params):
        val = self.evalName(statement[2], param_names, params)
        name = statement[1]
        if self.lookUpField(name) != None: # a field
            self.lookUpField(name).value = val
        elif name in param_names: # a param
            params[param_names.index(name)] = val
        else :
            InterpreterBase().error(ErrorType.NAME_ERROR, f"'{name}' is not defined.")
        return
    
    def __execute_inputs(self, statement, param_names, params):
        val = InterpreterBase(True, None).get_input()
        name = statement[1]
        if self.lookUpField(name) != None: # a field
            self.lookUpField(name).value = val
        elif name in param_names: # a param
            params[param_names.index(name)] = val
        else :
            InterpreterBase().error(ErrorType.NAME_ERROR, f"'{name}' is not defined.")
        return
    
    def __execute_inputi(self, statement, param_names, params):
        val = int(InterpreterBase().get_input())
        name = statement[1]
        if self.lookUpField(name) != None: # a field
            self.lookUpField(name).value = val
        elif name in param_names: # a param
            params[param_names.index(name)] = val
        else :
            InterpreterBase().error(ErrorType.NAME_ERROR, f"'{name}' is not defined.")
        return

    def __execute_begin(self, statement, param_names, params):
        statement = statement[1:]
        for s in statement:
            result = self.__run_statement(StateDef(None, s), param_names, params)
            if (s[0] == InterpreterBase.RETURN_DEF): return result
        return result
    
    def __execute_call(self, expr, param_names, params):
        c = self
        if (expr[1] != InterpreterBase().ME_DEF):
            c = self.evalName(expr[1])
            if (c == None or not isinstance(c, ObjDef)): 
                InterpreterBase().error(ErrorType.TYPE_ERROR, f"'{expr[1]}' not a valid class for the 'new' keyword.")
        
        res = c.call_method(expr[2], expr[3:]) # temporarily ONLY "me" param-less methods
        if (res == None): res = "None"
        return res
    
    def __execute_new(self, expr, param_names, params):
        c = self.c.lookUpClass(expr[1])
        if (c == None):
            InterpreterBase().error(ErrorType.TYPE_ERROR, f"'{expr[1]}' not a valid classname for the 'new' keyword.")
        return c

    def evaluate_expr(self, expr, param_names=[], params=[]): #param_names=["n", "x"], params=[9,-1]
        #print("evaluating",expr,"with param names",param_names,"and their corresponding values",params)
        op = ''
        if expr[0] == InterpreterBase().CALL_DEF:
            return self.__execute_call(expr, param_names, params)
        elif expr[0] == InterpreterBase().NEW_DEF:
            return self.__execute_new(expr, param_names, params)
        
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
        #print("evalName-", name)
        if name == InterpreterBase.NULL_DEF:
            return None
        if type(name) is list: #sub expr
            name = self.evaluate_expr(name, param_names, params) #recursively process it
        elif type(name) is int: 
            return name
        elif name == InterpreterBase().TRUE_DEF:
            name = True
        elif name == InterpreterBase().FALSE_DEF:
            name = False
        elif (self.isInt(name)):
            name = int(name)
        elif self.isString(name[0]): # a string
            name = name[1:-1] # remove quotes
        elif self.lookUpField(name) != None: # a field
            name = self.lookUpField(name).value # get value
        elif name in param_names: # a param
            params[param_names.index(name)] = self.evalName(params[param_names.index(name)], param_names, params)
            name = params[param_names.index(name)] # get its given value
        else:
            InterpreterBase().error(ErrorType.NAME_ERROR, f"'{name}' is not defined.")
        return name