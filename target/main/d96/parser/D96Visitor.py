# Generated from main/d96/parser/D96.g4 by ANTLR 4.10.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .D96Parser import D96Parser
else:
    from D96Parser import D96Parser

# This class defines a complete generic visitor for a parse tree produced by D96Parser.

class D96Visitor(ParseTreeVisitor):

    # Visit a parse tree produced by D96Parser#program.
    def visitProgram(self, ctx:D96Parser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#class_decls.
    def visitClass_decls(self, ctx:D96Parser.Class_declsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#class_decl.
    def visitClass_decl(self, ctx:D96Parser.Class_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#parent.
    def visitParent(self, ctx:D96Parser.ParentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#class_body.
    def visitClass_body(self, ctx:D96Parser.Class_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#class_member.
    def visitClass_member(self, ctx:D96Parser.Class_memberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#member.
    def visitMember(self, ctx:D96Parser.MemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#attribute_decl.
    def visitAttribute_decl(self, ctx:D96Parser.Attribute_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#attr_equal.
    def visitAttr_equal(self, ctx:D96Parser.Attr_equalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#attr_list.
    def visitAttr_list(self, ctx:D96Parser.Attr_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#expr_list.
    def visitExpr_list(self, ctx:D96Parser.Expr_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#method_decl.
    def visitMethod_decl(self, ctx:D96Parser.Method_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#normal.
    def visitNormal(self, ctx:D96Parser.NormalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#method_params.
    def visitMethod_params(self, ctx:D96Parser.Method_paramsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#param_decl.
    def visitParam_decl(self, ctx:D96Parser.Param_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#id_list.
    def visitId_list(self, ctx:D96Parser.Id_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#block_statement.
    def visitBlock_statement(self, ctx:D96Parser.Block_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#state_list.
    def visitState_list(self, ctx:D96Parser.State_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#special.
    def visitSpecial(self, ctx:D96Parser.SpecialContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#constructor.
    def visitConstructor(self, ctx:D96Parser.ConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#block_constructor.
    def visitBlock_constructor(self, ctx:D96Parser.Block_constructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#destructor.
    def visitDestructor(self, ctx:D96Parser.DestructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#block_destructor.
    def visitBlock_destructor(self, ctx:D96Parser.Block_destructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#typedecl.
    def visitTypedecl(self, ctx:D96Parser.TypedeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#array_type.
    def visitArray_type(self, ctx:D96Parser.Array_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#primitive_type.
    def visitPrimitive_type(self, ctx:D96Parser.Primitive_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#intlitlowerbound.
    def visitIntlitlowerbound(self, ctx:D96Parser.IntlitlowerboundContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#class_type.
    def visitClass_type(self, ctx:D96Parser.Class_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#bool_value.
    def visitBool_value(self, ctx:D96Parser.Bool_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#int_value.
    def visitInt_value(self, ctx:D96Parser.Int_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#float_value.
    def visitFloat_value(self, ctx:D96Parser.Float_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#string_value.
    def visitString_value(self, ctx:D96Parser.String_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#class_value.
    def visitClass_value(self, ctx:D96Parser.Class_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#array_value.
    def visitArray_value(self, ctx:D96Parser.Array_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#muldim_array.
    def visitMuldim_array(self, ctx:D96Parser.Muldim_arrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#operand.
    def visitOperand(self, ctx:D96Parser.OperandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#instance_attr_access.
    def visitInstance_attr_access(self, ctx:D96Parser.Instance_attr_accessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#static_attr_access.
    def visitStatic_attr_access(self, ctx:D96Parser.Static_attr_accessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#instance_method_access.
    def visitInstance_method_access(self, ctx:D96Parser.Instance_method_accessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#static_method_access.
    def visitStatic_method_access(self, ctx:D96Parser.Static_method_accessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#object_creation.
    def visitObject_creation(self, ctx:D96Parser.Object_creationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#expr.
    def visitExpr(self, ctx:D96Parser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#scalar_type.
    def visitScalar_type(self, ctx:D96Parser.Scalar_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#statement.
    def visitStatement(self, ctx:D96Parser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#varconst_decl.
    def visitVarconst_decl(self, ctx:D96Parser.Varconst_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#attrId_equal.
    def visitAttrId_equal(self, ctx:D96Parser.AttrId_equalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#attrId_list.
    def visitAttrId_list(self, ctx:D96Parser.AttrId_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#ass.
    def visitAss(self, ctx:D96Parser.AssContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#ifstmt.
    def visitIfstmt(self, ctx:D96Parser.IfstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#if_stmt.
    def visitIf_stmt(self, ctx:D96Parser.If_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#elseif_stmt.
    def visitElseif_stmt(self, ctx:D96Parser.Elseif_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#else_stmt.
    def visitElse_stmt(self, ctx:D96Parser.Else_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#forstmt.
    def visitForstmt(self, ctx:D96Parser.ForstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#breakstmt.
    def visitBreakstmt(self, ctx:D96Parser.BreakstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#continuestmt.
    def visitContinuestmt(self, ctx:D96Parser.ContinuestmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#retu.
    def visitRetu(self, ctx:D96Parser.RetuContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by D96Parser#method_invoke.
    def visitMethod_invoke(self, ctx:D96Parser.Method_invokeContext):
        return self.visitChildren(ctx)



del D96Parser