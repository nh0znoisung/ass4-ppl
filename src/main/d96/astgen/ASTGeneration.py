from D96Visitor import D96Visitor
from D96Parser import D96Parser
from AST import *
# from main.d96.utils.AST import IntLiteral, NullLiteral, SelfLiteral
from functools import reduce


class ASTGeneration(D96Visitor):
    def visitProgram(self, ctx: D96Parser.ProgramContext):
        return Program(self.visit(ctx.class_decls()))

    def visitClass_decls(self, ctx: D96Parser.Class_declsContext):        
        return reduce(lambda x,y: x + [self.visit(y)], ctx.class_decl(), [])

    def visitClass_decl(self, ctx: D96Parser.Class_declContext):
        # class_decl: 'Class' ID (':' ID)? '{' class_body '}';
        body = self.visit(ctx.class_body())
        if(ctx.ID().getText() == 'Program'):
            for x in body:
                if isinstance(x, MethodDecl) and x.name == Id('main') and x.param == []:
                    x.kind = Static()
        if ctx.parent():
            return ClassDecl(Id(ctx.ID().getText()),body,self.visit(ctx.parent()))
        return ClassDecl(Id(ctx.ID().getText()), body)

    def visitParent(self, ctx: D96Parser.ParentContext):
        return Id(ctx.ID().getText())

    def visitClass_body(self, ctx: D96Parser.Class_bodyContext):
        # class_body: class_member *;
        return reduce(lambda x,y: x + self.visit(y), ctx.class_member(), [])

    # ?????
    def visitClass_member(self, ctx: D96Parser.Class_memberContext):
        # class_member: attribute_decl | method_decl;
        # array of MemDecl
        return self.visit(ctx.getChild(0))

    def visitMember(self, ctx: D96Parser.MemberContext):
        # member: ID | DOLLARID;        
        tmp = 0 if ctx.ID() else 1
        return (Id(ctx.getChild(0).getText()),tmp)

    # Type
    def visitTypedecl(self, ctx: D96Parser.TypedeclContext):
        if ctx.BOOLTYPE():
            return BoolType()
        elif ctx.INTTYPE():
            return IntType()
        elif ctx.FLOATTYPE():
            return FloatType()
        elif ctx.STRINGTYPE():
            return StringType()
        elif ctx.array_type():
            return self.visit(ctx.array_type())
        return self.visit(ctx.class_type())

    def visitArray_type(self, ctx: D96Parser.Array_typeContext):
        # 'Array' '[' primitive_type ',' intlitlowerbound ']' ;
        # size: int
        return ArrayType(self.visit(ctx.intlitlowerbound()),  self.visit(ctx.primitive_type()))
    
    def visitClass_type(self, ctx: D96Parser.Class_typeContext):
        # class_type: ID;
        return ClassType(Id(ctx.ID().getText()))

    def visitIntlitlowerbound(self, ctx: D96Parser.IntlitlowerboundContext):
        # intlitlowerbound: INTLIT;
        txt = ctx.getChild(0).getText()
        num = 0
        if len(txt) == 0:
            # Not happen
            num = 0
        else:
            if txt[0] == '0':
                if len(txt) == 1:
                    # Just 0 (Decimal)
                    num = 0
                elif txt[1] in ['x', 'X']:
                    # Start with 0x, 0X
                    num = int(txt[2:], 16)
                elif txt[1] in ['b', 'B']:
                    # Start with 0b, 0B
                    num = int(txt[2:], 2)
                else:
                    # Start with 0
                    num = int(txt[1:], 8)
            else:
                # Decimal
                num = int(txt)
        return num  

    def visitPrimitive_type(self, ctx: D96Parser.Primitive_typeContext):
        # primitive_type: BOOLTYPE | INTTYPE | FLOATTYPE | STRINGTYPE | array_type;
        if ctx.BOOLTYPE():
            return BoolType()
        elif ctx.INTTYPE():
            return IntType()
        elif ctx.FLOATTYPE():
            return FloatType()
        elif ctx.STRINGTYPE():
            return StringType()
        elif ctx.array_type():
            return self.visit(ctx.array_type())
        return None

    # Value
    def visitBool_value(self, ctx: D96Parser.Bool_valueContext):
        if ctx.TRUE():
            return BooleanLiteral(True)
        else:
            return BooleanLiteral(False)
    
    def visitInt_value(self, ctx: D96Parser.Int_valueContext):
        # int_value: INTLIT;
        # Hex, oct, bin, base 10
        txt = ctx.getChild(0).getText()
        num = 0
        if len(txt) == 0:
            # Not happen
            num = 0
        else:
            if txt[0] == '0':
                if len(txt) == 1:
                    # Just 0 (Decimal)
                    num = 0
                elif txt[1] in ['x', 'X']:
                    # Start with 0x, 0X
                    num = int(txt[2:], 16)
                elif txt[1] in ['b', 'B']:
                    # Start with 0b, 0B
                    num = int(txt[2:], 2)
                else:
                    # Start with 0
                    num = int(txt[1:], 8)
            else:
                # Decimal
                num = int(txt)
        return IntLiteral(num)
    
    def visitFloat_value(self, ctx: D96Parser.Float_valueContext):
        # float_value: FLOATLIT;
        return FloatLiteral(float(ctx.getChild(0).getText()))

    def visitString_value(self, ctx: D96Parser.String_valueContext):
        # string_value: STRINGLIT;
        return StringLiteral(ctx.getChild(0).getText())

    # expr_list ????
    def visitArray_value(self, ctx: D96Parser.Array_valueContext):
        # array_value: '[' value_list ']' ;
        return ArrayLiteral(self.visit(ctx.expr_list()))

    # Not multi-array ????
    def visitClass_value(self, ctx: D96Parser.Class_valueContext):
        # class_value: NULL | NEW class_type '(' ')';
        if ctx.NULL():
            return NullLiteral()
        else:
            # NewExpr: T or F????
            return NewExpr(Id(ctx.class_type().getText()),[])

    def visitOperand(self, ctx: D96Parser.OperandContext):
        # operand: bool_value | int_value | float_value | string_value | class_value | array_value;
        if ctx.bool_value():
            return self.visit(ctx.bool_value())
        elif ctx.int_value():
            return self.visit(ctx.int_value())
        elif ctx.float_value():
            return self.visit(ctx.float_value())
        elif ctx.string_value():
            return self.visit(ctx.string_value())
        elif ctx.class_value():
            return self.visit(ctx.class_value())
        elif ctx.array_value():
            return self.visit(ctx.array_value())
        return None


    # Statement
    def visitScalar_type(self, ctx: D96Parser.Scalar_typeContext):
        return Id(ctx.getChild(0).getText())
    
    def visitStatement(self, ctx: D96Parser.StatementContext):
        if ctx.varconst_decl():
            return self.visit(ctx.varconst_decl()) #List
        elif ctx.ass():
            return [self.visit(ctx.ass())]
        elif ctx.ifstmt():
            return [self.visit(ctx.ifstmt())]
        elif ctx.forstmt():
            return [self.visit(ctx.forstmt())]
        elif ctx.breakstmt():
            return [self.visit(ctx.breakstmt())]
        elif ctx.continuestmt():
            return [self.visit(ctx.continuestmt())]
        elif ctx.retu():
            return [self.visit(ctx.retu())]
        elif ctx.method_invoke():
            return [self.visit(ctx.method_invoke())]
        elif ctx.block_statement():
            return [self.visit(ctx.block_statement())]

    # ????????
    def visitVarconst_decl(self, ctx: D96Parser.Varconst_declContext):
        res = []
        m = 0 if ctx.IMMUTABLE() else 1 # 0: Val, 1: Var
        if ctx.attrId_list():
            # Case 1: Not initialized
            arr_attr = self.visit(ctx.attrId_list())
            typedecl = self.visit(ctx.typedecl())
            init = NullLiteral() if isinstance(typedecl,ClassType) else None
            if m == 0:
                # Val
                for (name, tmp) in arr_attr:
                    res.append(ConstDecl(name, typedecl, init))
            else:
                # Var
                for (name, tmp) in arr_attr:
                    res.append(VarDecl(name, typedecl, init))
            return res
        else:
            # Case 2: Symmetric
            (lst_member, lst_expr, typedecl) = self.visit(ctx.attrId_equal())
            n = len(lst_member)
            if m == 0:
                # Val
                for i in range(n):
                    res.append(ConstDecl(lst_member[i][0], typedecl, lst_expr[i]))
            else:
                # Var
                for i in range(n):
                    res.append(VarDecl(lst_member[i][0], typedecl, lst_expr[i]))
            return res

    def visitAttrId_equal(self, ctx: D96Parser.Attr_equalContext):
        # attr_equal: member COMMA attr_equal COMMA expr| member (':' typedecl '=') expr;
        if ctx.typedecl():
            return ([(Id(ctx.ID().getText()),0)], [self.visit(ctx.expr())], self.visit(ctx.typedecl()) )
        else:
            (lst_member, lst_expr, kind)  = self.visit(ctx.attr_equal())
            return ([(Id(ctx.ID().getText()),0)] + lst_member, lst_expr + [self.visit(ctx.expr())], kind)

    def visitAttrId_list(self, ctx: D96Parser.Attr_listContext):
        return [(Id(x.getText()),0) for x in ctx.ID()]

    def visitAss(self, ctx: D96Parser.AssContext):
        return Assign(self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))

    def visitIfstmt(self, ctx: D96Parser.IfstmtContext):
        # ifstmt: if_stmt (elseif_stmt)* (else_stmt)?
        n = ctx.getChildCount() 
        # maybe None
        curr_stmt = self.visit(ctx.else_stmt()) if ctx.else_stmt() else None
        k = n-2 if ctx.else_stmt() else n-1
        for i in range(k,-1,-1):
            (expr, if_stmt) = self.visit(ctx.getChild(i))
            curr_stmt = If(expr, if_stmt, curr_stmt)

        return curr_stmt



    def visitIf_stmt(self, ctx: D96Parser.If_stmtContext):
        # if_stmt: IF '(' expr ')' statement;
        return (self.visit(ctx.expr()), self.visit(ctx.block_statement()))

    def visitElseif_stmt(self, ctx: D96Parser.Elseif_stmtContext):
        # elseif_stmt: ELSEIF expr ':' statement;
        return (self.visit(ctx.expr()), self.visit(ctx.block_statement()))
        # ElseIfStmt(self.visit(ctx.expr()), self.visit(ctx.statement(0)))

    def visitElse_stmt(self, ctx: D96Parser.Else_stmtContext):
        # else_stmt: ELSE ':' statement;
        return self.visit(ctx.block_statement())

        

    def visitForstmt(self, ctx: D96Parser.ForstmtContext):
        # forstmt: 'Foreach' '(' scalar_type 'In' expr '..' expr ('By' expr)? ')' 
        if ctx.expr(2):
            return For(self.visit(ctx.scalar_type()), self.visit(ctx.expr(0)), self.visit(ctx.expr(1)), self.visit(ctx.block_statement()), self.visit(ctx.expr(2)))

        return For(self.visit(ctx.scalar_type()), self.visit(ctx.expr(0)), self.visit(ctx.expr(1)), self.visit(ctx.block_statement()), IntLiteral(1))
    
    def visitBreakstmt(self, ctx: D96Parser.BreakstmtContext):
        # breakstmt: 'Break' ';';
        return Break()

    def visitContinuestmt(self, ctx: D96Parser.ContinuestmtContext):
        # continuestmt: 'Continue' ';';
        return Continue()

    def visitRetu(self, ctx: D96Parser.RetuContext):
        # retu: 'Return' expr ';';
        if ctx.expr():
            return Return(self.visit(ctx.expr()))
        return Return()

    def visitMethod_invoke(self, ctx: D96Parser.Method_invokeContext):
        # (static_method_access | instance_method_access)
        return self.visit(ctx.getChild(0))[1]

    
    def visitBlock_statement(self, ctx: D96Parser.Block_statementContext):
        # block_statement: '{' statement* '}';
        return Block(self.visit(ctx.state_list()))
    
    def visitState_list(self, ctx: D96Parser.State_listContext):
        # state_list: statement*;
        if ctx.statement():
            return reduce(lambda x,y: x+self.visit(y), ctx.statement(), [])
        return []
    

    # Expression
    # def visitElement_expr(self, ctx: D96Parser.Element_exprContext):
    #     # element_expr: expr '[' expr ']';
    #     return ArrayCell(self.visit(ctx.expr()), self.visit(ctx.index_operator()))

    # def visitIndex_operator(self, ctx: D96Parser.Index_operatorContext):
    #     # index_operator: expr (',' expr)*;
    #     if ctx.index_operator():
    #         return [self.visit(ctx.expr())] + self.visit(ctx.index_operator())
    #     return [self.visit(ctx.expr())]


    def visitInstance_attr_access(self, ctx: D96Parser.Instance_attr_accessContext):
        # instance_attr_access: expr '.' ID;
        return FieldAccess(self.visit(ctx.expr()), Id(ctx.ID().getText()))

    def visitStatic_attr_access(self, ctx: D96Parser.Static_attr_accessContext):
        # static_attr_access: ID '.' ID;
        return FieldAccess(Id(ctx.ID().getText()), Id(ctx.DOLLARID().getText()))

    def visitInstance_method_access(self, ctx: D96Parser.Instance_method_accessContext):
        # instance_method_access: expr '.' ID;
        tail = self.visit(ctx.expr_list()) if ctx.expr_list() else []

        return [CallExpr(self.visit(ctx.expr()), Id(ctx.ID().getText()), tail),CallStmt(self.visit(ctx.expr()), Id(ctx.ID().getText()), tail)]
    
    def visitStatic_method_access(self, ctx: D96Parser.Static_method_accessContext):
        # static_method_access: ID '(' expr_list? ')';
        tail = self.visit(ctx.expr_list()) if ctx.expr_list() else []

        return [CallExpr(Id(ctx.ID().getText()), Id(ctx.DOLLARID().getText()), tail),CallStmt(Id(ctx.ID().getText()), Id(ctx.DOLLARID().getText()), tail)]


    def visitObject_creation(self, ctx: D96Parser.Object_creationContext):
        # object_creation: NEW ID '(' expr_list? ')';
        return NewExpr(Id(ctx.class_type().getText()), self.visit(ctx.expr_list()))

    # ????
    def visitExpr(self, ctx: D96Parser.ExprContext):
        # expr: Using bina, una, lit
        if ctx.LB() and ctx.getChildCount() == 3:
            return self.visit(ctx.expr(0))
        elif ctx.NEW():
            tail = self.visit(ctx.expr_list()) if ctx.expr_list() else []
            return NewExpr(Id(ctx.ID().getText()), tail)
        
        elif ctx.static_attr_access():
            return self.visit(ctx.static_attr_access())
        elif ctx.static_method_access():
            return self.visit(ctx.static_method_access())[0]

        elif ctx.DOT():
            if ctx.LB():
                # Method call
                tail = self.visit(ctx.expr_list()) if ctx.expr_list() else []
                return CallExpr(self.visit(ctx.expr(0)), Id(ctx.ID().getText()), tail)
            else:
                # Attribute access
                return FieldAccess(self.visit(ctx.expr(0)), Id(ctx.ID().getText()))
        elif ctx.LC():
            # Index []
            arr = []
            for i in range(1,len(ctx.expr())):
                arr.append(self.visit(ctx.expr(i)))
            return ArrayCell(self.visit(ctx.expr(0)), arr)

        elif len(ctx.expr()) == 1:
            return UnaryOp(ctx.getChild(0).getText(), self.visit(ctx.expr(0)))
        elif len(ctx.expr()) == 2:
            return BinaryOp(ctx.getChild(1).getText(), self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))
        elif ctx.operand():
            # ????
            return self.visit(ctx.operand())
        elif ctx.ID():
            return Id(ctx.ID().getText())
        elif ctx.DOLLARID():
            return Id(ctx.DOLLARID().getText())
        elif ctx.SELF():
            return SelfLiteral()
        elif ctx.NULL():
            return NullLiteral()
        return None

    # Expression list
    def visitExpr_list(self, ctx: D96Parser.Expr_listContext):
        # expr_list: expr (',' expr)*;
        return [self.visit(x) for x in ctx.expr()]





    # visitMember returns a ID, tmp(0 if ID, 1 if Dollar)
    # Attribute Declaration
    def visitAttribute_decl(self, ctx: D96Parser.Attribute_declContext):
        # attribute_decl: 'Attribute' (Instance | Static) StoreDecl;
        # Return a list of AttributeDecl
        # Kind: (Instance: ID or Static: Dollar), Decl: StoreDecl (Var or Const)
        res = []
        m = 0 if ctx.IMMUTABLE() else 1 # 0: Val, 1: Var
        if ctx.attr_list():
            # Case 1: Not initialized
            arr_attr = self.visit(ctx.attr_list())
            typedecl = self.visit(ctx.typedecl())
            init = NullLiteral() if isinstance(typedecl,ClassType) else None
            if m == 0:
                # Val
                for (name, tmp) in arr_attr:
                    kind = Instance() if tmp == 0 else Static()
                    res.append(AttributeDecl(kind, ConstDecl(name, typedecl, init)))
            else:
                # Var
                for (name, tmp) in arr_attr:
                    kind = Instance() if tmp == 0 else Static()
                    res.append(AttributeDecl(kind, VarDecl(name, typedecl, init)))
            return res
        else:
            # Case 2: Symmetric
            (lst_member, lst_expr, typedecl) = self.visit(ctx.attr_equal())
            n = len(lst_member)
            if m == 0:
                # Val
                for i in range(n):
                    kind = Instance() if lst_member[i][1] == 0 else Static()
                    res.append(AttributeDecl(kind, ConstDecl(lst_member[i][0], typedecl, lst_expr[i])))
            else:
                # Var
                for i in range(n):
                    kind = Instance() if lst_member[i][1] == 0 else Static()
                    res.append(AttributeDecl(kind, VarDecl(lst_member[i][0], typedecl, lst_expr[i])))
            return res

    def visitAttr_equal(self, ctx: D96Parser.Attr_equalContext):
        # attr_equal: member COMMA attr_equal COMMA expr| member (':' typedecl '=') expr;
        if ctx.typedecl():
            return ([self.visit(ctx.member())], [self.visit(ctx.expr())], self.visit(ctx.typedecl()) )
        else:
            (lst_member, lst_expr, kind)  = self.visit(ctx.attr_equal())
            return ([self.visit(ctx.member())] + lst_member, lst_expr + [self.visit(ctx.expr())], kind)

    def visitAttr_list(self, ctx: D96Parser.Attr_listContext):
        # attr_list: member (COMMA member)*;
        # list of tuple (name, tmp = 0 if ID, 1 if Dollar)
        return [self.visit(x) for x in ctx.member()]


    # Method Declearation
    def visitMethod_decl(self, ctx: D96Parser.Method_declContext):
        # method_decl: special | normal;
        # return a list just only an element
        if ctx.special():
            return self.visit(ctx.special())
        return self.visit(ctx.normal())
    
    def visitSpecial(self, ctx: D96Parser.SpecialContext):
        # special: 'Constructor' param_list block;
        if ctx.constructor():
            return self.visit(ctx.constructor())
        return self.visit(ctx.destructor())
    
    def visitConstructor(self, ctx: D96Parser.ConstructorContext):
        # constructor: 'Constructor' '(' method_params ')' block_constructor;
        return [MethodDecl(Instance(), Id('Constructor'), self.visit(ctx.method_params()), self.visit(ctx.block_constructor()))]

    def visitBlock_constructor(self, ctx: D96Parser.Block_constructorContext):
        # Return nothing
        return Block(self.visit(ctx.state_list()))

    # No params
    def visitDestructor(self, ctx: D96Parser.DestructorContext):
        # destructor: 'Destructor' block;
        return [MethodDecl(Instance(), Id('Destructor'), [], self.visit(ctx.block_destructor()))]

    def visitBlock_destructor(self, ctx: D96Parser.Block_destructorContext):
        # No return statement
        return Block(self.visit(ctx.state_list()))

    def visitNormal(self, ctx: D96Parser.NormalContext):
        # normal: member'(' method_params ')'  block_statement
        name, tmp = self.visit(ctx.member())
        kind = Instance() if tmp == 0 else Static()
        return [MethodDecl(kind, name, self.visit(ctx.method_params()), self.visit(ctx.block_statement()))]

    def visitMethod_params(self, ctx: D96Parser.Method_paramsContext):
        # method_params: (param_decl (SEMI param_decl)*)?;
        # method_params = List[VarDecl]
        if ctx.getChildCount() == 0:
            return []
        return reduce(lambda x,y: x+self.visit(y), ctx.param_decl(), [])

    def visitParam_decl(self, ctx: D96Parser.Param_declContext):
        # param_decl: id_list ':' typedecl;
        return list(map(lambda x: VarDecl(x, self.visit(ctx.typedecl())), self.visit(ctx.id_list())))
    
    def visitId_list(self, ctx: D96Parser.Id_listContext):
        # id_list: ID (COMMA ID)*;
        return [Id(x.getText()) for x in ctx.ID()]