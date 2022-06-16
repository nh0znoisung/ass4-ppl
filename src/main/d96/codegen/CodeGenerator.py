from Utils import *
from StaticCheck import *
from StaticError import *
from Emitter import Emitter
from Frame import Frame
from abc import ABC, abstractmethod
from Visitor import * 
from AST import *
from functools import reduce

from main.d96.utils.AST import IntLiteral
# from pprint import pprint
# from main.d96.utils.AST import VoidType


# TODO: ArrayLit + ArrayCell + +. + ==.

class MType:
    def __init__(self,partype,rettype,skind=Static()):
        self.partype = partype
        self.rettype = rettype
        self.skind  = skind

class Symbol:
    def __init__(self,name,mtype,value = None):
        self.name = name
        self.mtype = mtype
        self.value = value
    def __str__(self):
        return "Symbol("+self.name+","+str(self.mtype)+")"

class CodeGenerator(Utils):
    def __init__(self):
        self.libName = "io" 

    def init(self):
        # Standard: put/get
        # Case: read/write
        return [Symbol("getInt", MType([], IntType()), CName(self.libName)),
                Symbol("putInt", MType([IntType()], VoidType()), CName(self.libName)), 
                Symbol("getFloat", MType([], FloatType()), CName(self.libName)),
                Symbol("putFloat", MType([FloatType()], VoidType()), CName(self.libName)),
                Symbol("getBool", MType([], BoolType()), CName(self.libName)),
                Symbol("putBool", MType([BoolType()],VoidType()), CName(self.libName)),
                Symbol("Str", MType([], StringType()), CName(self.libName)),
                Symbol("putString", MType([StringType()], VoidType()), CName(self.libName))]  

        # return [Symbol("readInt", MType([], IntType()), CName(self.libName)),
        #         Symbol("writeInt", MType([IntType()], VoidType()), CName(self.libName)), 
        #         Symbol("readFloat", MType([], FloatType()), CName(self.libName)),
        #         Symbol("writeFloat", MType([FloatType()], VoidType()), CName(self.libName)),
        #         Symbol("readBool", MType([], BoolType()), CName(self.libName)),
        #         Symbol("writeBool", MType([BoolType()],VoidType()), CName(self.libName)),
        #         Symbol("readStr", MType([], StringType()), CName(self.libName)),
        #         Symbol("writeStr", MType([StringType()], VoidType()), CName(self.libName))]  


    def gen(self, ast, dir_):
        #ast: AST
        #dir_: String

        gl = self.init()
        # gl=GetName().visit(ast,[])+gl
        gc = CodeGenVisitor(ast, gl, dir_)
        gc.visit(ast, None)



# class StringType(Type):
#     def __str__(self):
#         return "StringType"

#     def accept(self, v, param):
#         return None

# class ArrayPointerType(Type):
#     def __init__(self, ctype):
#         #cname: String
#         self.eleType = ctype

#     def __str__(self):
#         return "ArrayPointerType({0})".format(str(self.eleType))

#     def accept(self, v, param):
#         return None
# class ClassType(Type):
#     def __init__(self,cname):
#         self.cname = cname
#     def __str__(self):
#         return "Class({0})".format(str(self.cname))
#     def accept(self, v, param):
#         return None
        
class SubBody():
    def __init__(self, frame, sym):
        #frame: Frame
        #sym: List[Symbol]

        self.frame = frame
        self.sym = sym

class Access():
    def __init__(self, frame, sym, isLeft, isFirst = False):
        #frame: Frame
        #sym: List[Symbol]
        #isLeft: Boolean
        #isFirst: Boolean

        self.frame = frame
        self.sym = sym
        self.isLeft = isLeft
        self.isFirst = isFirst

class Val(ABC):
    pass

class Index(Val):
    def __init__(self, value):
        #value: Int

        self.value = value

class CName(Val):
    def __init__(self, value):
        #value: String

        self.value = value

class CodeGenVisitor(BaseVisitor, Utils):
    def __init__(self, astTree, env, dir_):
        #astTree: AST
        #env: List[Symbol]
        #dir_: File

        self.astTree = astTree
        self.env = env
        self.path = dir_
        self.isProgram = False
        self.isMain = False
        # self.className = "D96Class"
        # self.emit = Emitter(self.path + "/" + self.className + ".j")

    def visitProgram(self, ast, o):
        #ast: Program
        #c: Any

        o = StaticChecker(ast).visit(ast, {})
        for class_decl in ast.decl:
            self.visit(class_decl, o[class_decl.classname.name])
        return o

    # o: [attr, method]
    def visitClassDecl(self, ast, o):
        self.className = "D96Class" if ast.classname.name == "Program" else ast.classname.name #Entry point
        self.emit = Emitter(self.path + "/" + self.className+'.j')
        self.emit.printout(self.emit.emitPROLOG(self.className, ast.parentname.name if (ast.parentname) else "java.lang.Object"))

        # Attribute visitor
        for x in ast.memlist:
            if type(x) is AttributeDecl:
                self.visit(x, o)
        
        # Constructor
        if "Constructor" not in o['method']:
            self.genINIT(MethodDecl(Instance(),Id("<init>"), [], Block([])) , self.env, Frame("<init>", VoidType()) )

        self.isProgram = True if ast.classname.name == "Program" else False

        # Simple method
        for x in ast.memlist:
            if type(x) is MethodDecl:
                self.visit(x, SubBody(Frame(x.name.name, self.convertType(o['method'][x.name.name]['retype'])), self.env))

        self.isProgram = False

        self.genCLINITMETHOD(ast, o, Frame("<clinit>", VoidType() ))
        self.emit.emitEPILOG()
        return o
    
    def convertType(self, s):
        if s == "Int":
            return IntType()
        elif s == "Float":
            return FloatType()
        elif s == "Bool":
            return BoolType()
        elif s == "String":
            return StringType()
        elif s == "Void":
            return VoidType()
        else:
            return ClassType(s.spilt(':')[-1])
    
    # Visit Method: Init + Simple Method 
    def visitMethodDecl(self, ast, o):
        if self.isProgram and ast.name.name == "main":
            self.isMain = True
            self.genMETHOD(ast, o.sym, o.frame)
            self.isMain = False
        else:
            self.genMETHOD(ast, o.sym, o.frame)

    def genINIT(self, ast, sym, frame): 
        intype = []
        mtype = MType(intype, VoidType(), ast.kind)
        self.emit.printout(self.emit.emitMETHOD(ast.name.name, mtype, False,frame))
        
        frame.enterScope(True)

        self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "this", ClassType(self.className), frame.getStartLabel(), frame.getEndLabel(),frame))

        global_env = sym
        local = []
        for x in ast.param:
            local.append(self.visit(x,SubBody(frame,global_env)))

        global_env = local + global_env
        
        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))
        self.emit.printout(self.emit.emitREADVAR("this", ClassType(Id(self.className)), 0, frame))
        self.emit.printout(self.emit.emitINVOKESPECIAL(frame))

        body = ast.body
        local = []
        for x in body.inst:
            if isinstance(x, StoreDecl):
                local.append(self.visit(x, SubBody(frame, global_env)))

        global_env = local + global_env

        for x in body.inst:
            if isinstance(x, Stmt):
                self.visit(x, SubBody(frame, global_env))

        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        self.emit.printout(self.emit.emitRETURN(VoidType(), frame))
        self.emit.printout(self.emit.emitENDMETHOD(frame))
        frame.exitScope()

    def genMETHOD(self, ast, sym, frame): # entry point + Simple
        returnType = frame.returnType
        name = "<init>" if ast.name.name == "Constructor" else ast.name.name
        intype = [ArrayType(0,StringType())] if self.isMain else list(map(lambda x: x.varType, ast.param))

        mtype = MType(intype, returnType, ast.kind)

        isStatic = True if self.isMain else type(ast.kind) is Static

        # Constructor -> Init
        self.emit.printout(self.emit.emitMETHOD(name, mtype, isStatic, frame))
        
        frame.enterScope(True)

        global_env = sym

        if self.isMain:
            self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "args", ArrayType(0,StringType()), frame.getStartLabel(), frame.getEndLabel(),frame))

        local = []
        for x in ast.param:
            local.append(self.visit(x,SubBody(frame,global_env)))

        global_env = local + global_env
        

        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))

        
        body = ast.body
        # local = []
        for x in body.inst:
            if isinstance(x, StoreDecl):
                temp = self.visit(x, SubBody(frame, global_env))
                global_env = [temp] + global_env

                # local.append()

        # global_env = local + global_env

        for x in body.inst:
            if isinstance(x, Stmt):
                self.visit(x, SubBody(frame, global_env))

        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        if type(returnType) is VoidType:
            self.emit.printout(self.emit.emitRETURN(VoidType(), frame))
        self.emit.printout(self.emit.emitENDMETHOD(frame))
        frame.exitScope()


    def genCLINITMETHOD(self, consdecl, o, frame):
        #included default init and init
        self.emit.printout(self.emit.emitMETHOD("<clinit>", MType([], VoidType()), True,frame))
        frame.enterScope(True)
        att=list(filter(lambda x:type(x)is AttributeDecl and type(x.kind)is Static,consdecl.memlist))
        list(map(lambda x: self.visit(Assign(x.decl.variable,x.decl.varInit),SubBody(frame,o)) if type(x.decl) is VarDecl else\
            self.visit(Assign(x.decl.constant,x.decl.value),SubBody(frame,o)),att))

        self.emit.printout(self.emit.emitRETURN(VoidType(), frame))
        self.emit.printout(self.emit.emitENDMETHOD(frame))
        frame.exitScope()


    # Visit Attr + Var + Const
    def visitAttributeDecl(self,ast,o):
        # kind: SIKind #Instance or Static
        # decl: StoreDecl # VarDecl for mutable or ConstDecl for immutable
        field = ast.decl
        if type(field) is VarDecl:
            self.emit.emitATTRIBUTE(field.variable.name,field.varType,False, None)
        else:
            self.emit.emitATTRIBUTE(field.constant.name,field.constType,True, None)

    def visitVarDecl(self,ast,o):
        frame = o.frame
        mtype = ast.varType
        name = ast.variable.name
        idx = frame.getNewIndex()

        self.emit.printout(self.emit.emitVAR(idx, name, mtype, frame.getStartLabel(), frame.getEndLabel(), frame))

        # Assign if have init value
        if ast.varInit:
            self.visit(Assign(ast.variable, ast.varInit), SubBody(o.frame, [Symbol(name, mtype, Index(idx))] + o.sym))
        
        return Symbol(name, mtype, Index(idx))

    def visitConstDecl(self,ast,o): 
        frame = o.frame
        mtype = ast.constType
        name = ast.constant.name
        idx = frame.getNewIndex()

        # Same with VarDecl
        self.emit.printout(self.emit.emitVAR(idx, name, mtype, frame.getStartLabel(), frame.getEndLabel(), frame))

        val = ast.value # Make sure have init  
        self.visit(Assign(ast.constant, val), SubBody(o.frame, [Symbol(name, mtype, Index(idx))] + o.sym))

        return Symbol(name, mtype, Index(idx))



    # # io: put/get => write/read 
    def visitCallExpr(self, ast, o):
        frame = o.frame
        sym = o.sym
        name = ast.method.name
        
        # Convert problem -> io.java
        if isinstance(ast.obj, Id) and ast.obj.name == "io":
            if name == "readInt":
                name = "getInt"
            elif name == "writeInt":
                name = "putInt"
            elif name == "readFloat":
                name = "getFloat"
            elif name == "writeFloat":
                name = "putFloat"
            elif name == "readBool":
                name = "getBool"
            elif name == "writeBool":
                name = "putBool"
            elif name == "readStr":
                name = "Str"
            elif name == "writeStr":
                name = "putString"

        _sym = self.lookup(name, sym, lambda x: x.name)
        cname = _sym.value.value    
        ctype = _sym.mtype
        in_ = ("", list())

        for x in ast.param:
            str1, typ1 = self.visit(x, Access(frame, sym, False, True))
            in_ = (in_[0] + str1, in_[1].append(typ1))

        code = in_[0] + self.emit.emitINVOKESTATIC(cname + "/" + name, ctype, frame)
        return code, ctype.rettype

    # Field access, method call, array access....
    def visitBlock(self,ast,o):    
        # inst: List[Inst] -> StoreDecl, Stmt
        frame = o.frame
        sym = o.sym
        frame.enterScope(False)
        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))
        local = SubBody(frame, [])
        for x in ast.inst:
            if type(x) is StoreDecl:
                local = SubBody(frame, [self.visit(x, local)])

        sym = local.sym + sym
        for x in ast.inst:
            if type(x) is Stmt:
                self.visit(x,sym)
        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        frame.exitScope()    

    # io: put/get => read/write 
    def visitCallStmt(self, ast, o):
        frame = o.frame
        sym = o.sym
        name = ast.method.name
        # Convert problem -> io.java
        if isinstance(ast.obj, Id) and ast.obj.name == "io":
            if name == "readInt":
                name = "getInt"
            elif name == "writeInt":
                name = "putInt"
            elif name == "readFloat":
                name = "getFloat"
            elif name == "writeFloat":
                name = "putFloat"
            elif name == "readBool":
                name = "getBool"
            elif name == "writeBool":
                name = "putBool"
            elif name == "readStr":
                name = "Str"
            elif name == "writeStr":
                name = "putString"

        sym_ = next(filter(lambda x: name == x.name, sym), None)
        cname = sym_.value.value    
        ctype = sym_.mtype
        in_ = ("", list())

        for x in ast.param:
            str1, typ1 = self.visit(x, Access(frame, sym, False, True))
            in_ = (in_[0] + str1, in_[1].append(typ1))
        
        if type(ctype.skind) is Static:
            self.emit.printout(in_[0])
            self.emit.printout(self.emit.emitINVOKESTATIC(cname + "/" + name, ctype, frame))
        else:            
            self.emit.printout(in_[0])
            self.emit.printout(self.emit.emitINVOKEVIRTUAL(cname + "/" + name, ctype, frame))


    def visitFieldAccess(self,ast,o):
        frame = o.frame
        sym = o.sym

        sym_ = self.lookup(ast.fieldname.name, sym, lambda x: x.name)
        cname = sym_.value.value    
        ctype = sym_.mtype #Mtype -> rettype, skind

        c, _ = self.visit(ast.obj, Access(frame, sym, False))
        _code = c
        typ = ctype.rettype
        if not o.isLeft:
            if type(ctype.skind) is Static:
                _code += self.emit.emitGETSTATIC(cname + "/" + ast.fieldname.name ,ctype, frame)
            else:
                _code += self.emit.emitGETFIELD(cname + "/" + ast.fieldname.name  ,ctype, frame)
        else:            
            if type(ctype.skind) is Static:
                _code += self.emit.emitPUTSTATIC(cname + "/" + ast.fieldname.name ,ctype, frame)
            else:
                _code += self.emit.emitPUTFIELD(cname + "/" + ast.fieldname.name ,ctype, frame)

        return _code, typ

    # Call stmt
    def visitIf(self, ast, o): 
        # expr:Expr, thenStmt:Stmt, elseStmt:Stmt = None 
        c1,_=self.visit(ast.expr,Access(o.frame,o.sym,False))
        self.emit.printout(c1)
        falseLabel=o.frame.getNewLabel()
        self.emit.printout(self.emit.emitIFFALSE(falseLabel,o.frame))
        self.visit(ast.tstmt,o)
        
        if not ast.estmt:
            self.emit.printout(self.emit.emitLABEL(falseLabel,o.frame))
        else:
            endElse=o.frame.getNewLabel()
            self.emit.printout(self.emit.emitGOTO(endElse,o.frame))
            self.emit.printout(self.emit.emitLABEL(falseLabel,o.frame))
            self.visit(ast.estmt,o)
            self.emit.printout(self.emit.emitLABEL(endElse,o.frame))

    ### ??? Not sure
    def visitFor(self, ast, o): 
        # Use con and break
        # id:Id, expr1:Expr, expr2:Expr
        # up: bool #True => increase; False => decrease ??
        # loop:Stmt, expr3: Expr = None => 1

        # Setup
        frame = o.frame
        sym = o.sym

        labelInit = frame.getNewLabel()

        frame.enterLoop()

        # Left: True (LHS: id, arraycell, fieldaccess), Right: False (expr)
        accessT = Access(frame, sym, True, True)
        accessF = Access(frame, sym, False, True)

        labelContinue = frame.getContinueLabel()
        labelBreak = frame.getBreakLabel()
    
        # Plan: assign e1 -> label init -> (2 cases e1 <= e2 ?) -> id compare e2 (can go to break) -> Stmt -> label continue -> x += e3 -> go init -> label break 

        # Assign id to expr1
        # expr1, _ = self.visit(ast.expr1, accessF)
        # id1, _ = self.visit(ast.id, accessT)
        # self.emit.printout(expr1)
        # self.emit.printout(id1)
        self.visit(Assign(ast.id, ast.expr1), o)
        self.emit.printout(self.emit.emitLABEL(labelInit, frame)) # init label

        # Protected: expr2 + expr3 (Eval at the first time) -> assign it to the virtual variable(not avail -> $) -> Id('$e2', '$e3')
        self.visit(Assign(Id('$e1'), ast.expr1), o)
        self.visit(Assign(Id('$e2'), ast.expr2), o)
        if ast.expr3:
            self.visit(Assign(Id('$e3'), ast.expr3), o)
        else:
            self.visit(Assign(Id('$e3'), IntLiteral(1)), o)


        # Compare the id vs expr2 in 2 cases
        labelIf_1 = frame.getNewLabel()
        labelIf_2 = frame.getNewLabel()
        id1, _ = self.visit(Id('$e1'), accessF)
        id2, _ = self.visit(Id('$e2'), accessF)
        self.emit.printout(id1)
        self.emit.printout(expr2)
        self.emit.printout(self.emit.emitIFICMPGT(labelIf_1, frame)) # if greater than -> If_1
        # if less than or equal: Compare when id > exp2
        id1, _ = self.visit(ast.id, accessF)
        expr2, _ = self.visit(ast.expr2, accessF)
        self.emit.printout(id1)
        self.emit.printout(expr2)
        self.emit.printout(self.emit.emitIFICMPGT(labelBreak, frame))
        self.emit.printout(self.emit.emitGOTO(labelIf_2, frame))
        self.emit.printout(self.emit.emitLabel(labelIf_1, frame))
        # if greater: Compare when id < exp2
        id1, _ = self.visit(ast.id, accessF)
        expr2, _ = self.visit(ast.expr2, accessF)
        self.emit.printout(id1)
        self.emit.printout(expr2)
        self.emit.printout(self.emit.emitIFICMPLT(labelBreak, frame))
        self.emit.printout(self.emit.emitLabel(labelIf_2, frame))


        # Visit inside block
        self.visit(ast.loop,o)

        self.emit.printout(self.emit.emitLABEL(labelContinue, frame))

        # Add expr3 in 2 cases
        labelIf_3 = frame.getNewLabel()
        labelIf_4 = frame.getNewLabel()
        id1, _ = self.visit(Id('$e1'), accessF)
        id2, _ = self.visit(Id('$e2'), accessF)
        self.emit.printout(id1)
        self.emit.printout(expr2)
        self.emit.printout(self.emit.emitIFICMPGT(labelIf_3, frame)) # if greater than -> If_1
        # if less than or equal: Compare when id > exp2
        expr, _ = self.visit(BinaryOp('+', ast.id, Id('$e3')), accessF)
        id2, _ = self.visit(ast.id, accessT)
        self.emit.printout(expr)
        self.emit.printout(id2)

        self.emit.printout(self.emit.emitGOTO(labelIf_4, frame))
        self.emit.printout(self.emit.emitLabel(labelIf_3, frame))
        # if greater: Compare when id < exp2
        expr, _ = self.visit(BinaryOp('-', ast.id, Id('$e3')), accessF)
        id2, _ = self.visit(ast.id, accessT)
        self.emit.printout(expr)
        self.emit.printout(id2)

        self.emit.printout(self.emit.emitLabel(labelIf_4, frame))
        
        self.emit.printout(self.emit.emitGOTO(labelInit, frame))
        self.emit.printout(self.emit.emitLABEL(labelBreak, frame))
        frame.exitLoop()



    def visitContinue(self,ast,o):
        self.emit.printout(self.emit.emitGOTO(o.frame.getContinueLabel(), o.frame))
    
    def visitBreak(self,ast,o):
        self.emit.printout(self.emit.emitGOTO(o.frame.getBreakLabel(), o.frame))

    def visitReturn(self, ast, o):
        frame = o.frame
        sym = o.sym

        t = VoidType()
        if ast.expr:
            c, t = self.visit(ast.expr, Access(frame, sym, False))

            if type(t) is IntType and type(frame.returnType) is FloatType:
                c += self.emit.emitI2F(frame)
            self.emit.printout(c)

        self.emit.printout(self.emit.emitRETURN(t, frame))        
        self.emit.printout(self.emit.emitGOTO(frame.getEndLabel(), frame))


    def visitAssign(self, ast, o):
        # Type is the same or Float = Int
        # 
        e2, t2 = self.visit(ast.exp, Access(o.frame, o.sym, False, True)) 
        e1, t1 = self.visit(ast.lhs, Access(o.frame, o.sym, True, True))
        
        if type(t2) is IntType and type(t1) is FloatType:
            e2 += self.emit.emitI2F(o.frame)

        self.emit.printout(e2+e1)

    # Una, Bin op: Done
    def visitBinaryOp(self, ast, o):
        # op:str, left:Expr, right:Expr
        frame = o.frame

        lc, lt = self.visit(ast.left, o)
        rc, rt = self.visit(ast.right, o)

        reType = None # return type
        _code = ""

        if ast.op in ['+','-', '*' ,'/' ,'<' ,'<=' ,'>', '>=']: #Coerceion
            # Covert to the same type
            if type(lt) is type(rt):
                reType = lt
            else: 
                code = self.emit.emitI2F(frame)
                if type(lt) is IntType:
                    lc += code
                else:
                    rc += code
                reType = FloatType()

            if ast.op == '/':
                reType = FloatType()

            if ast.op in ['+','-']:
                _code = lc + rc + self.emit.emitADDOP(ast.op, reType, frame)

            elif ast.op in ['*','/']:
                _code = lc + rc + self.emit.emitMULOP(ast.op, reType, frame)


            elif ast.op in ['<' ,'<=' ,'>', '>=']:
                _code = lc + rc + self.emit.emitREOP(ast.op, rt, frame)
                reType = BoolType()

        elif ast.op in ["==", "!="]: # Same type
            _code = lc + rc + self.emit.emitREOP(ast.op, rt, frame)
            rt = BoolType()
        
        elif ast.op == "&&":
            _code = lc + rc + self.emit.emitANDOP(frame)
            reType = BoolType()
        elif ast.op == "||":
            _code = lc + rc + self.emit.emitOROP(frame)
            reType = BoolType()        
        # elif ast.op in ["&&", "||"]:
        #     if ast.op=='&&':
        #         labelFalse = frame.getNewLabel()
        #         labelTrue = frame.getNewLabel()
        #         lc += self.emit.emitIFFALSE(labelFalse,frame)
        #         rc += self.emit.emitIFFALSE(labelFalse,frame)
        #         con = self.emit.emitPUSHICONST("true", frame)+self.emit.emitGOTO(labelTrue,frame) + self.emit.emitLABEL(labelFalse,frame)
        #         brk = self.emit.emitPUSHICONST("false", frame)+self.emit.emitLABEL(labelTrue,frame)

        #         _code = lc + rc + con + brk
        #         rt = BoolType()
        #     else:
        #         labelFalse = frame.getNewLabel()
        #         labelTrue = frame.getNewLabel()
        #         lc += self.emit.emitIFTRUE(labelFalse,frame)
        #         rc += self.emit.emitIFTRUE(labelFalse,frame)
        #         con = self.emit.emitPUSHICONST("false", frame)+self.emit.emitGOTO(labelFalse,frame) + self.emit.emitLABEL(labelTrue,frame)
        #         brk = self.emit.emitPUSHICONST("true", frame)+self.emit.emitLABEL(labelFalse,frame)

        #         _code = lc + rc + con + brk
        #         rt = BoolType()

        return _code, reType

    def visitUnaryOp(self, ast, o):
        # op: str, body: Expr
        frame = o.frame
        sym = o.sym
        body, typ = self.visit(ast.body, Access(frame, sym, False, True))
        if ast.op == '!' and type(typ) is BoolType:
            return body + self.emit.emitNOT(IntType(), frame), BoolType()
        elif ast.op == '-' and type(typ) is IntType:
            return body + self.emit.emitNEGOP(IntType(), frame), IntType()
        elif ast.op == '-' and type(typ) is FloatType:
            return body + self.emit.emitNEGOP(FloatType(), frame), FloatType()

    # Visit ID
    def visitId(self, ast, o):
        sym = self.lookup(ast.name, o.sym, lambda x: x.name)
        # for x in o.sym:
        #     print(x)
        # print(ast.name)
        # print("Hello World", sym)
        typ = sym.mtype

        if o.isLeft:
            if type(sym.value) is CName:
                return self.emit.emitPUTSTATIC(sym.value.value+'/'+sym.name, typ, o.frame), typ
            else:
                return self.emit.emitWRITEVAR(sym.name, typ, sym.value.value, o.frame), typ
        else:
            if type(sym.value) is CName:
                return self.emit.emitGETSTATIC(sym.value.value+'/'+sym.name, typ, o.frame), typ
            else:
                return self.emit.emitREADVAR(sym.name, typ, sym.value.value, o.frame), typ


    # Literal: value:(type)
    # ????
    # def visitArrayLiteral(self, ast, o): pass

    def visitIntLiteral(self, ast, o):
        return self.emit.emitPUSHICONST(ast.value, o.frame), IntType()
    
    def visitFloatLiteral(self, ast, o):
        return self.emit.emitPUSHFCONST(ast.value, o.frame), FloatType()
    
    def visitBooleanLiteral(self, ast, o):
        return self.emit.emitPUSHICONST(str(ast.value).lower(), o.frame), BoolType()

    def visitStringLiteral(self, ast, o):
        return self.emit.emitPUSHCONST(ast.value, StringType(), o.frame), StringType()

    def lookup(self, name, lst, func):
        if type(lst) is not list:
            lst = [lst]
        for x in lst:
            if name == func(x):
                return x
        return None
    
# Assignment 3 => Get method return type
class StaticChecker(BaseVisitor):    
    def __init__(self,ast):
        self.ast = ast
        self.block_number = 0

        self.const_operand = True
        self.const_start = {}
        self.curr_class = "" # For Self.
        self.o = {}

    def check(self):
        return self.visit(self.ast, {})

    ######################## Main
    def visitProgram(self,ast, o): 
        self.o = {}
        o = self.o
        for x in ast.decl:
            self.visit(x, o)

        return self.o

    def visitClassDecl(self, ast, o):
        par_name = None
        if ast.parentname: # Have parent
            par_name = ast.parentname.name

        name = ast.classname.name
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
        
        o[name] = {
            "sikind": sikind,
            "storedecl": storedecl,
            "type": typ, # str ("int", "float",...)
        }


    def visitMethodDecl(self, ast, o):
        name = ast.name.name
        sikind = self.visit(ast.kind, o)

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

            o[name]["scope"]["local"][param_name] = {
                "type": typ,
                "storedecl": storedecl, # 0: Sure Var
                # auto sikind = instance
            }
            o[name]["param"].append(typ)
        
        newScope = o[name]["scope"].copy()

        typ = self.visit(ast.body, newScope)
        o[name]["retype"] = typ

    def visitBlock(self, ast, o):
        re_typ = None
        for x in ast.inst:
            if isinstance(x, StoreDecl):
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
                    }
            elif isinstance(x, Return): # Not sure
                newScope = o.copy()
                newScope["global"].update(newScope["local"])
                newScope["local"] = {}
                typ_ = self.visit(x, newScope)
                if re_typ is None:
                    re_typ = typ_
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
        return ("Array", self.visit(ast.eleType, o), ast.size)
    
    def visitClassType(self, ast, o):
        return "Class:" + ast.classname.name
    
    def visitVoidType(self, ast, o):
        return "Void"

    
    def visitBinaryOp(self, ast, o):
        left = self.visit(ast.left, o)
        right = self.visit(ast.right, o)
        op = ast.op # str

        if op in ['-', '+', '*', '/']: # Int/Float => Return int/float
            if left == "Int" and right == "Int":
                return "Int"
            else:
                return "Float" # Float-point
        elif op == "%":
            return "Int"
        elif op in ["&&", "||"]:
            return "Bool"

        elif op == "+.":
            return "String"
        elif op == "==.":
            return "Bool"

        elif op in ["==", "!="]:
            return "Bool"

        elif op in [">", "<", "<=", ">="]:
            return "Bool"
        


    def visitUnaryOp(self, ast, o):
        body = self.visit(ast.body, o)
        return body

        
        return None

    def visitId(self, ast, o): 
        name = ast.name
        if name in o["local"]:
            return o["local"][name]["type"]
        elif name in o["global"]:
            return o["global"][name]["type"]


    def visitArrayCell(self, ast, o):
        arr = self.visit(ast.arr, o)
        
        for x in ast.idx:
            idx = self.visit(x, o)
            if type(arr) is tuple and arr[0] == "Array":
                if idx == "Int":
                    arr = arr[1]

        return arr

    #### Member accesss
    def visitFieldAccess(self, ast, o):
        fieldname = ast.fieldname.name
        if isinstance(ast.obj, Id):
            classname = ast.obj.name
            if classname in self.o:
                return self.o[classname]["attr"][fieldname]["type"]

        obj = self.visit(ast.obj, o)
        if obj.find("Class:") != -1:
            classname = obj.split(":")[1]

        return self.o[classname]["attr"][fieldname]["type"]

         
    def visitCallExpr(self, ast, o):        
        fieldname = ast.method.name
        if isinstance(ast.obj, Id):
            classname = ast.obj.name
            if classname in self.o:
                return self.o[classname]["method"][fieldname]["retype"]


        obj = self.visit(ast.obj, o)
        if obj.find("Class:") != -1:
            classname = obj.split(":")[1]
        return self.o[classname]["method"][fieldname]["retype"]


    def visitNewExpr(self, ast, o):
        classname = ast.classname.name
        return "Class:" + classname


    # Task 2.7: Break + Continue must in Loop
    def visitContinue(self, ast , o):
        pass
    
    def visitBreak(self, ast , o):
        pass

    def visitReturn(self, ast, o):
        if ast.expr:
            return self.visit(ast.expr, o)
        else:
            return "Void"


    ##############################
    # sikind = 0 or 1       0: Instance, 1: Static
    def visitInstance(self, ast, o):
        return 0
    
    def visitStatic(self, ast, o):
        return 1

    # storedecl = 0 or 1    0: var, 1: const
    def visitVarDecl(self, ast, o):
        typ = self.visit(ast.varType, None)
        return (ast.variable.name, typ, 0)
    
    def visitConstDecl(self, ast, o):
        typ = self.visit(ast.constType, o) 
        return (ast.constant.name, typ, 1)

