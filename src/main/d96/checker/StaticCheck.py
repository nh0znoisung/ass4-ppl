
"""
 * @author nhphung
"""
from AST import * 
from Visitor import *
from StaticError import *



# Instance_Var=0
# Instance_Const=1
# Static_Var=2
# Static_Const=3 

# sikind * 2 + storedecl
# storedecl = 0 or 1    0: var, 1: const
# sikind = 0 or 1       0: Instance, 1: Static


# Visit all method in AST.py
class StaticChecker(BaseVisitor):

    # global_envi = [
    # Symbol("getInt",MType([],IntType())),
    # Symbol("putIntLn",MType([IntType()],VoidType()))
    # ]
    global_envi = {}
    
    def __init__(self,ast):
        self.ast = ast
        # self.RedeclaredChecker = RedeclaredChecker()
        self.block_number = 0
        # self.o = StaticChecker.global_envi

        self.const_operand = True
        self.const_start = {}
        self.curr_class = "" # For Self.
        self.o = {}

    def check(self):
        return self.visit(self.ast, {})

    ######################## Main
    def visitProgram(self,ast, o): 
        LoopChecker().visit(ast,{})
        EntryChecker().visit(ast,{})
        ConstructorChecker().visit(ast,{})
        DestructorChecker().visit(ast,{})
        self.o = {}
        o = self.o
        for x in ast.decl:
            self.visit(x, o)

        return ""

    def visitClassDecl(self, ast, o):
        par_name = None
        if ast.parentname: # Have parent
            par_name = ast.parentname.name
            # What if paraent declare after child ????
            if par_name not in o:
                raise Undeclared(Class(), par_name)

        name = ast.classname.name
        if name in o:
            raise Redeclared(Class(), name)
        self.curr_class = name
        # -----------
        o[name] = {"attr": {}, "method": {}, "parent": par_name}
        
        for x in ast.memlist:
            if type(x) is MethodDecl:
                self.visit(x, o[name]["method"])
            else:
                self.visit(x, o[name]["attr"])
    

    def visitAttributeDecl(self, ast, o):
        sikind = self.visit(ast.kind, o)
        (name, typ, storedecl) = self.visit(ast.decl, o)
        # (ast.variable.name, ast.varType, ast.varInit, 0)
        # storedecl = 0 or 1    0: var, 1: const
        # ----------
        if name in o:
            # print(o[name]["mem_type"])
            raise Redeclared(Attribute(), name)

        
        o[name] = {
            "sikind": sikind,
            "storedecl": storedecl,
            "type": typ, # str ("int", "float",...)
        }


    def visitMethodDecl(self, ast, o):
        name = ast.name.name
        # ----------
        if name in o:
            raise Redeclared(Method(), name)
        
        sikind = self.visit(ast.kind, o)
        # If recursion allowed, the return type not found => Raise Error
        o[name] = {
            "sikind": sikind,
            "param": [], # [type, ...]
            "retype": "Void", # Check return Expr
            "scope": {
                "global": {},
                "local": {},
            },  # {name: {...}}
        }
    
        for x in ast.param:
            (param_name, typ, storedecl) = self.visit(x, None)
            if param_name in o[name]["scope"]["local"]:
                raise Redeclared(Parameter(), param_name)
            else:
                o[name]["scope"]["local"][param_name] = {
                    "type": typ,
                    "storedecl": storedecl, # 0: Sure Var
                    # auto sikind = instance
                }
                o[name]["param"].append(typ)
        
        newScope = o[name]["scope"].copy()
        # print(newScope)
        # id=158173 -> No return many type in a method
        typ = self.visit(ast.body, newScope)  # Could be None = Void
        o[name]["retype"] = typ

    def visitBlock(self, ast, o):
        re_typ = None
        for x in ast.inst:
            if isinstance(x, StoreDecl):
                # print(o)
                (name, typ, storedecl) = self.visit(x, o)
                if name in o["local"]:
                    if storedecl == 0:
                        raise Redeclared(Variable(), name)
                    else:
                        raise Redeclared(Constant(), name)
                else:
                    o["local"][name]= {
                        "type": typ,
                        "storedecl": storedecl,
                        # auto sikind = instance
                    }
            elif isinstance(x, Return): # Not sure
                typ_ = self.visit(x, o)
                # print(re_typ)
                if re_typ is None:
                    re_typ = typ_
                elif re_typ != typ_:
                    raise TypeMismatchInStatement(x)
            else: #Stmt
                newScope = o.copy()
                newScope["global"].update(newScope["local"])
                newScope["local"] = {}
                self.visit(x, newScope)
        if re_typ is None:
            return "Void"
        return re_typ


    #### Literals
    def visitIntLiteral(self,ast, c): 
        return 'Int'
    
    def visitFloatLiteral(self, ast , o):
        return "Float"
    
    def visitBooleanLiteral(self, ast , o):
        return "Bool"
    
    def visitStringLiteral(self, ast , o):
        return "String"
    
    def visitNullLiteral(self, ast , o):
        return "Null"
    
    def visitSelfLiteral(self, ast , o):
        return "Class:" + self.curr_class

    # Task 2.9
    def visitArrayLiteral(self, ast, o):
        # o: the type of array
        # value: All expr have the same type, size: >0
        typ = None
        size = len(ast.value)
        
        for x in ast.value:
            tmp_typ = self.visit(x,o)
            if typ is None:
                typ = tmp_typ
            elif typ != tmp_typ:
                raise IllegalArrayLiteral(ast)
        return ("Array", typ, size)


    ##### Type
    def visitIntType(self,ast, o):
        return "Int"
    
    def visitFloatType(self, ast , o):
        return "Float"

    def visitBoolType(self, ast , o):
        return "Bool"
    
    def visitStringType(self, ast , o):
        return "String"

    def visitArrayType(self, ast, o):
        # ???
        return ("Array", self.visit(ast.eleType, o), ast.size)
    
    def visitClassType(self, ast, o):
        if ast.classname.name not in self.o:
            raise Undeclared(Class(), ast.classname.name)
        return "Class:" + ast.classname.name
    
    def visitVoidType(self, ast, o):
        return "Void"

    
    # Expression: +,-,*,/,%
    # What o = {} => Visit Id => Type   || Return a str of Type
    def visitBinaryOp(self, ast, o):
        left = self.visit(ast.left, o)
        right = self.visit(ast.right, o)
        op = ast.op # str

        if op in ['-', '+', '*', '/']: # Int/Float => Return int/float
            ### ?? Coerceion ???
            if left not in ["Int", "Float"] or right not in ["Int", "Float"]:
                raise TypeMismatchInExpression(ast)

            if left == "Int" and right == "Int":
                return "Int"
            else:
                return "Float" # Float-point
                
        elif op == "%":
            if left == "Int" and right == "Int":
                return "Int"
            else:
                raise TypeMismatchInExpression(ast)
        elif op in ["&&", "||"]:
            if left == "Bool" and right == "Bool":
                return "Bool"
            else:
                raise TypeMismatchInExpression(ast)
        elif op == "+.":
            if left == "String" and right == "String":
                return "String"
            else:
                raise TypeMismatchInExpression(ast)
        # Compare 2 string
        elif op == "==.":
            if left == "String" and right == "String":
                return "Bool"
            else:
                raise TypeMismatchInExpression(ast)
        # Relation
        elif op in ["==", "!="]:
            # Same type
            if left != right:
                raise TypeMismatchInExpression(ast)
            if left == "Int" or left == "Bool":
                return "Bool"
            else:
                raise TypeMismatchInExpression(ast)
        elif op in [">", "<", "<=", ">="]:
            ### ?? Coerceion ???
            if left not in ["Int", "Float"] or right not in ["Int", "Float"]:
                raise TypeMismatchInExpression(ast)
            else:
                return "Bool"
        
        return None


    # Unary: -, !, a[], New
    def visitUnaryOp(self, ast, o):
        body = self.visit(ast.body, o)
        op = ast.op # str

        if op == "-":
            if body == "Int" or body == "Float":
                return body
            else:
                raise TypeMismatchInExpression(ast)
        elif op == "!":
            if body == "Bool":
                return "Bool"
            else:
                raise TypeMismatchInExpression(ast)
        
        return None

    # what o?
    def visitId(self, ast, o): 
        # if self.const_start:
        #     self.const_operand = False
        # print(o)
        name = ast.name
        if name in o["local"]:
            if o["local"][name]["storedecl"] == 0: # var
                if self.const_start:
                    self.const_operand = False
            return o["local"][name]["type"]
        elif name in o["global"]:
            if o["global"][name]["storedecl"] == 0: # var
                if self.const_start:
                    self.const_operand = False
            return o["global"][name]["type"]
        else:
            raise Undeclared(Identifier(), name)

    def visitArrayCell(self, ast, o):
        # Return array cell type ???
        arr = self.visit(ast.arr, o)
        
        for x in ast.idx:
            idx = self.visit(x, o)
            if type(arr) is tuple and arr[0] == "Array":
                if idx == "Int":
                    arr = arr[1]
                else:
                    raise TypeMismatchInExpression(ast)
            else:
                raise TypeMismatchInExpression(ast)
        return arr

    #### Member accesss
    def visitFieldAccess(self, ast, o):
        # Return type
        # "Class:" + ast.classname.name
        fieldname = ast.fieldname.name
        # classname = None
        flag = True
        if isinstance(ast.obj, Id):
            classname = ast.obj.name
            if classname in self.o:
                flag = False
                # a classname
                # Inside attr
                # pprint(self.o)
                if fieldname in self.o[classname]["attr"]:
                    if fieldname[0] == '$': #static -> True
                        # storedecl = 0 or 1    0: var, 1: const
                        if self.o[classname]["attr"][fieldname]["storedecl"] == 0: # check const
                            if self.const_start:
                                self.const_operand = False
                        return self.o[classname]["attr"][fieldname]["type"]
                    else: #E.a
                        raise IllegalMemberAccess(ast)
                else:
                    if fieldname[0] == '$': #static -> Not found
                        raise Undeclared(Attribute(), fieldname)
                    else: #E.a -> E must be class-type
                        # ????  2-kind of errors
                        raise TypeMismatchInExpression(ast)

        if flag:
            # Real object => Find type
            obj = self.visit(ast.obj, o) # maybe undeclared
            # Must be class-type
            if obj.find("Class:") != -1:
                classname = obj.split(":")[1]
                # Make sure classname is declared: New A()->Undeclared classname

                if fieldname in self.o[classname]["attr"]:
                    if fieldname[0] != '$': #instance -> True
                        # storedecl = 0 or 1    0: var, 1: const
                        if self.o[classname]["attr"][fieldname]["storedecl"] == 0:
                            if self.const_start:
                                self.const_operand = False
                        return self.o[classname]["attr"][fieldname]["type"]
                    else: #e::$a
                        raise IllegalMemberAccess(ast)
                else:
                    if fieldname[0] != '$': #instace -> Not found
                        raise Undeclared(Attribute(), fieldname)
                    else: #e::$a -> E must be class-type
                        ## ???? 2-kind of errors
                        raise TypeMismatchInExpression(ast)
            else: # not class-type
                raise TypeMismatchInExpression(ast)


         
    def visitCallExpr(self, ast, o):
        if self.const_start:
            self.const_operand = False
        # Return type
        params_type = [] #rhs
        for x in ast.param:
            params_type.append(self.visit(x, o))
        
        # Method name == Fieldname
        fieldname = ast.method.name
        # classname = None
        flag = True
        if isinstance(ast.obj, Id):
            classname = ast.obj.name
            if classname in self.o:
                flag = False
                # a classname
                if fieldname in self.o[classname]["method"]:
                    if fieldname[0] == '$': #static -> True
                        augs_type = self.o[classname]["method"][fieldname]["param"] # lhs
                        if self.check_coercionList(augs_type, params_type):
                            if self.o[classname]["method"][fieldname]["retype"] != "Void":
                                return self.o[classname]["method"][fieldname]["retype"]
                        raise TypeMismatchInExpression(ast)
                    else: #E.a
                        raise IllegalMemberAccess(ast)
                else:
                    if fieldname[0] == '$': #static -> Not found
                        raise Undeclared(Method(), fieldname)
                    else: #E.a -> E must be class-type
                        # ????  2-kind of errors
                        raise TypeMismatchInExpression(ast)

        if flag:
            # Real object => Find type
            obj = self.visit(ast.obj, o) # maybe undeclared
            # Must be class-type
            if obj.find("Class:") != -1:
                classname = obj.split(":")[1]
                # Make sure classname is declared: New A()->Undeclared classname

                if fieldname in self.o[classname]["method"]:
                    if fieldname[0] != '$': #instance -> True
                        augs_type = self.o[classname]["method"][fieldname]["param"] # lhs
                        if self.check_coercionList(augs_type, params_type):
                            if self.o[classname]["method"][fieldname]["retype"] != "Void":
                                return self.o[classname]["method"][fieldname]["retype"]
                        raise TypeMismatchInExpression(ast)
                    else: #e::$a
                        raise IllegalMemberAccess(ast)
                else:
                    if fieldname[0] != '$': #instace -> Not found
                        raise Undeclared(Method(), fieldname)
                    else: #e::$a -> E must be class-type
                        ## ???? 2-kind of errors
                        raise TypeMismatchInExpression(ast)
            else: # not class-type
                raise TypeMismatchInExpression(ast)

    
    # Return a stmt, call void, return None
    def visitCallStmt(self, ast, o):
        # Same callexpr, return must be void
        # Return type
        params_type = []
        for x in ast.param:
            params_type.append(self.visit(x, o))
        
        # Method name == Fieldname
        fieldname = ast.method.name
        # classname = None
        flag = True
        if isinstance(ast.obj, Id):
            classname = ast.obj.name
            if classname in self.o:
                flag = False
                # a classname
                if fieldname in self.o[classname]["method"]:
                    if fieldname[0] == '$': #static -> True
                        augs_type = self.o[classname]["method"][fieldname]["param"] # lhs
                        if self.check_coercionList(augs_type, params_type):
                            if self.o[classname]["method"][fieldname]["retype"] == "Void":
                                return None
                        raise TypeMismatchInStatement(ast)
                    else: #E.a
                        raise IllegalMemberAccess(ast)
                else:
                    if fieldname[0] == '$': #static -> Not found
                        raise Undeclared(Method(), fieldname)
                    else: #E.a -> E must be class-type
                        # ????  2-kind of errors
                        raise TypeMismatchInStatement(ast)

        if flag:
            # Real object => Find type
            obj = self.visit(ast.obj, o) # maybe undeclared
            # Must be class-type
            if obj.find("Class:") != -1:
                classname = obj.split(":")[1]
                # Make sure classname is declared: New A()->Undeclared classname

                if fieldname in self.o[classname]["method"]:
                    if fieldname[0] != '$': #instance -> True
                        augs_type = self.o[classname]["method"][fieldname]["param"] # lhs
                        if self.check_coercionList(augs_type, params_type):
                            if self.o[classname]["method"][fieldname]["retype"] == "Void":
                                return None
                        raise TypeMismatchInStatement(ast)
                    else: #e::$a
                        raise IllegalMemberAccess(ast)
                else:
                    if fieldname[0] != '$': #instace -> Not found
                        raise Undeclared(Method(), fieldname)
                    else: #e::$a -> E must be class-type
                        ## ???? 2-kind of errors
                        raise TypeMismatchInStatement(ast)
            else: # not class-type
                raise TypeMismatchInStatement(ast)



    def visitNewExpr(self, ast, o):
        if self.const_start:
            self.const_operand = False

        # Constructor and default constructor
        params_type = []
        for x in ast.param:
            params_type.append(self.visit(x, o))
        classname = ast.classname.name
        augs_type = []
        if classname in self.o:
            # Check params
            if "Constructor" in self.o[classname]["method"]:
                augs_type = self.o[classname]["method"]["Constructor"]["param"]
            if self.check_coercionList(augs_type, params_type):
                return "Class:" + classname
            else:
                raise TypeMismatchInExpression(ast)
        else:
            raise Undeclared(Class(), classname)
        
        

    # Statement: Var + ass, if, for, break, continue, return, block, method invoke.

    def visitIf(self, ast, o):
        if(self.visit(ast.expr, o) != "Bool"):
            raise TypeMismatchInStatement(ast)
        self.visit(ast.thenStmt, o)
        if ast.elseStmt:
            self.visit(ast.elseStmt, o)

    def visitFor(self, ast, o):
        # Check expr1 2 3 must be int 
        # ? Assign or Stmt
        if self.visit(ast.expr1,o)!="Int":
            raise TypeMismatchInStatement(ast)
        if self.visit(ast.expr2,o)!="Int":
            raise TypeMismatchInStatement(ast)
        if ast.expr3:
            if self.visit(ast.expr3,o)!="Int":
                raise TypeMismatchInStatement(ast)
        self.const_start = True
        self.const_operand = True
        
        typ = self.visit(ast.id, o) #type
        if typ not in ["Int", "Float"]:
            raise CannotAssignToConstant(Assign(ast.id,ast.expr1))
        self.const_start = False
        if self.const_operand:
            raise CannotAssignToConstant(Assign(ast.id,ast.expr1))

        # d=158527 => Need declare before use in loop
        # o["local"][ast.id.name] = {"type": "Int", "storedecl": 0}
        self.visit(ast.loop, o)

    # Task 2.7: Break + Continue must in Loop
    def visitContinue(self, ast , o):
        pass
    
    def visitBreak(self, ast , o):
        pass

    #   retu expr as RHS => Return type
    def visitReturn(self, ast, o):
        if ast.expr:
            return self.visit(ast.expr, None) # str: Type of Expr
        else:
            return "Void"

    def check_coercionList(self, l1, l2):
        if len(l1) != len(l2):
            return False
        
        for i in range(len(l1)):
            if self.check_coercion(l1[i], l2[i]) == False:
                return False
        
        return True

    def check_coercion(self, t1, t2):
        if t1 == t2:
            return True
        else:
            if t1 == "Float" and t2 == "Int":
                return True
            # elif inheritance ?????
            elif type(t1) is tuple:
                if type(t2) is tuple and t1[2] == t2[2]:
                    
                    return self.check_coercion(t1[1], t2[1])
                else:
                    return False
            else:
                return False


    def visitAssign(self, ast, o):
        self.const_start = True
        self.const_operand = True
        
        lhs = self.visit(ast.lhs, o) #type
        self.const_start = False
        if self.const_operand:
            raise CannotAssignToConstant(ast)

        rhs = self.visit(ast.exp, o) #type

        # coerce
        if lhs == "Void":
            raise TypeMismatchInStatement(ast)
        
        if self.check_coercion(lhs, rhs) == False:
            raise TypeMismatchInStatement(ast)

    ##############################
    # sikind = 0 or 1       0: Instance, 1: Static
    def visitInstance(self, ast, o):
        return 0
    
    def visitStatic(self, ast, o):
        return 1

    # storedecl = 0 or 1    0: var, 1: const
    def visitVarDecl(self, ast, o):
        typ = self.visit(ast.varType, None)
        # print("Type", typ)
        typ_value = None
        if ast.varInit:
            typ_value = self.visit(ast.varInit, o)

        if typ_value is not None:
            if self.check_coercion(typ, typ_value) == False:
                raise TypeMismatchInStatement(ast)

        return (ast.variable.name, typ, 0)
    
    def visitConstDecl(self, ast, o):
        # Task 2.8
        if ast.value is None:
            raise IllegalConstantExpression(ast.value)
        
        #  IllegalConstantExpression
        # Operands mustbe literal or const + Operator
        

        self.const_start = True
        self.const_operand = True
        # Task 2.6
        typ = self.visit(ast.constType, o) 

        # print(o)
        typ_value = self.visit(ast.value, o) 

        self.const_start = False
        
        if self.const_operand == False:
            raise IllegalConstantExpression(ast.value)

        if self.check_coercion(typ, typ_value) == False:
            raise TypeMismatchInConstant(ast)
        

        return (ast.constant.name, typ, 1)


# Task 2.7| Break, Continue must in Loop
class LoopChecker(BaseVisitor): 
    # Must be in Loop
    # o = 1 if visit through at least a loop else o = 0
    def visitProgram(self, ast, o):
        for x in ast.decl:
            self.visit(x, 0)
    
    def visitClassDecl(self, ast, o):
        for x in ast.memlist:
            if type(x) is MethodDecl:
                self.visit(x, 0)

    def visitMethodDecl(self, ast, o):
        # body: Block
        self.visit(ast.body, 0)

    def visitBlock(self, ast, o):
        for x in ast.inst:
            if isinstance(x, Stmt):
                # if, for, break, continue: Have Stmt inside it
                if isinstance(x, If) or isinstance(x, For) or isinstance(x, Break) or isinstance(x, Continue):
                    self.visit(x, o)

    def visitIf(self, ast, o):
        self.visit(ast.thenStmt, o)
        if ast.elseStmt:
            self.visit(ast.elseStmt, o)

    def visitFor(self, ast, o):
        self.visit(ast.loop, 1)
    
    def visitContinue(self, ast, o):
        # Raise MustInLoop(<Stmt>)
        if o == 0:
            raise MustInLoop(ast)
    
    def visitBreak(self, ast, o):
        if o == 0:
            raise MustInLoop(ast)

# Task 2.11| No entry point
class EntryChecker(BaseVisitor): 
    # Must have class Program, main(), return nothing.
    check_main = False
    def visitProgram(self, ast, o):
        o = {}
        for x in ast.decl:
            self.visit(x, o)
        if "Program" not in o:
            raise NoEntryPoint()
        
    
    def visitClassDecl(self, ast, o):
        o[ast.classname.name] = 1
        if ast.classname.name == "Program":
            for x in ast.memlist:
                if type(x) is MethodDecl:
                    self.visit(x, o)
            
            if self.check_main == False:
                raise NoEntryPoint()
            

    def visitMethodDecl(self, ast, o):
        if ast.name.name == "main":
            self.check_main = True
            if len(ast.param) == 0:
                # Check return nothing
                self.visit(ast.body, o)
            else:
                raise NoEntryPoint()
            

    def visitBlock(self, ast, o):
        for x in ast.inst:
            if isinstance(x, Return):
                self.visit(x, o)
    
    def visitReturn(self, ast, o):
        if ast.expr:
            # Return a value => Fourm 157987
            # self.visit(ast.expr, o)
            raise TypeMismatchInStatement(ast)
            


# Constructor 
class ConstructorChecker(BaseVisitor): 
    # If exists, Return Nothing
    def visitProgram(self, ast, o):
        o = {}
        for x in ast.decl:
            self.visit(x, o)
    
    def visitClassDecl(self, ast, o):
        for x in ast.memlist:
            if type(x) is MethodDecl:
                self.visit(x, o)

    def visitMethodDecl(self, ast, o):
        if ast.name.name == "Constructor":
            self.visit(ast.body, o)
        
    def visitBlock(self, ast, o):
        for x in ast.inst:
            if isinstance(x, Return): # in it
                self.visit(x, o)
    
    def visitReturn(self, ast, o):
        if ast.expr:
            raise TypeMismatchInStatement(ast)

# Destructor
class DestructorChecker(BaseVisitor):
    # If exists, No Return (Have -> Wrong), Empty Params (Ast checker)
    def visitProgram(self, ast, o):
        o = {}
        for x in ast.decl:
            self.visit(x, o)
    
    def visitClassDecl(self, ast, o):
        for x in ast.memlist:
            if type(x) is MethodDecl:
                self.visit(x, o)
            
    def visitMethodDecl(self, ast, o):
        if ast.name.name == "Destructor":
            if len(ast.param) != 0:
                raise TypeMismatchInStatement(ast)
            else:
                self.visit(ast.body, o)
        
    def visitBlock(self, ast, o):
        for x in ast.inst:
            if isinstance(x, Return): # in it
                raise TypeMismatchInStatement(x)
    
