import unittest
from TestUtils import TestChecker
from AST import *

class CheckerSuite(unittest.TestCase):
    # Basic 1
    def test_0(self):
        input = Program(
                    [
                        ClassDecl(
                            Id("Program"),
                            [
                                MethodDecl(
                                    Static(),
                                    Id("main"),
                                    [],
                                    Block([Return()])
                                ),
                                AttributeDecl(
                                    Instance(),
                                    VarDecl(Id("myVar"),
                                    StringType(),
                                    StringLiteral("Hello World"))
                                ),
                                AttributeDecl(
                                    Instance(),
                                    VarDecl(Id("myVar"),
                                    IntType())
                                )
                            ]
                        )
                    ]
                )
        expect = "Redeclared Attribute: myVar"
        self.assertTrue(TestChecker.test(input,expect,400))

    # Basic 2
    def test_1(self):
        """More complex program"""
        input = Program([ClassDecl(Id("Program"),[MethodDecl(Static(),Id("main"),[],Block([Return()]))])])
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,401))
    
    ####### Single Error ########
    def test_2(self):
        input = """Class Program {
                        main(){
                            Var x: Int;
                            Foreach(x In 5 .. 2 By 12){
                                {
                                    {
                                        {
                                            
                                        }
                                        {
                                            Break;
                                        }
                                    }
                                    If("Hello" ==. "World"){
                                        Break;
                                        {
                                            Continue;
                                        }
                                    }
                                }
                                Continue;
                            }
                            Return;
                        }
                    }"""
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,402))

    # Break standard
    def test_3(self):
        input = """Class Program {
                        main(){
                            Var x : Int = 13-45+12;
                            Foreach(x In 5 .. 2){
                                Break;
                            }
                            Return;
                        }
                    }"""
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,403))

    # Continue standard
    def test_4(self):
        input = """Class Program {
                        main(){
                            Var x : Float = 12.423;
                            Foreach(x In 5 .. 2){
                                Continue;
                            }
                            Return;
                        }
                    }"""
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,404))

    # Break not in loop
    def test_5(self):
        input = """Class Program {
                        main(){
                            Break;
                            Return;
                        }
                    }"""
        expect = "Break Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,405))

    # Continue not in loop
    def test_6(self):
        input = """Class Program {
                        main(){
                            Continue;
                        }
                    }"""
        expect = "Continue Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,406))

    # Break-Continue complex
    def test_7(self):
        input = """Class Program {
                main(){
                    Var x : Int = 124%31/21;
                    If(True){
                        Foreach(x In 2 .. 5 By 10){
                            Break;
                        }
                    }
                    Return;
                }
            }"""
        expect = "Continue Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,407))

    # Scope
    def test_7(self):
        input = """Class Program {
                main(){
                    If(True){
                        {
                            Var x : Int = 124%31/21;
                        }
                        Foreach(x In 2 .. 5 By 1){
                            {
                                {
                                    Break;
                                }
                            }
                        }
                    }
                }
            }"""
        expect = "Undeclared Identifier: x"
        self.assertTrue(TestChecker.test(input,expect,407))





    # Break-Continue complex
    def test_8(self):
        input = """Class Program {
                main(){
                    If(True){
                        Foreach(x In 2 .. 5 By 1){
                            Break;
                        }
                    }
                    Return;
                }
            }"""
        expect = "Undeclared Identifier: x"
        self.assertTrue(TestChecker.test(input,expect,408))

    # Break-Continue complex
    def test_9(self):
        input = """Class Program {
                main(){
                    Val x : Int = 124%31/21;
                    If(True){
                        Foreach(x In 2 .. 5 By 1){
                            Return;
                        }
                        Foreach(x In 2 .. 5 By 1){
                            Foreach(y In 2 .. 5 By 1){
                                Break;
                            }
                        }
                    }
                    Return;
                }
            }"""
        expect = "Cannot Assign To Constant: AssignStmt(Id(x),IntLit(2))"
        self.assertTrue(TestChecker.test(input,expect,409))


    # Break-Continue complex
    def test_10(self):
        input = """Class Program {
                main(){
                    Var x,y,z: Float;
                    If(True){
                        Foreach(x In 2 .. 5 By 1){
                            Foreach(y In 2 .. 5 By 1){
                                Foreach(z In 2 .. 5 By 1){
                                    Foreach(z In 2 .. 5 By 1){
                                        Continue;
                                    }
                                }
                            }
                        }
                    }
                    Return;
                }
            }"""
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,410))

    # Break-Continue complex
    def test_11(self):
        input = """Class Program {
                main(){
                    If(True){
                        Foreach(x In 2 .. 5 By 1){
                            If(False){
                                Break;
                            }
                            Continue;
                        }
                        Foreach(x In 2 .. 5 By 1){
                            Foreach(y In 2 .. 5 By 1){
                                Foreach(z In 2 .. 5 By 1){
                                    Foreach(z In 2 .. 5 By 1){
                                        Continue;
                                    }
                                }
                            }
                        }
                    }
                    Return;
                }
            }"""
        expect = "Undeclared Identifier: x"
        self.assertTrue(TestChecker.test(input,expect,411))

    # Break-Continue complex
    def test_12(self):
        input = """Class Program {
                main(){
                    If(True){
                        Foreach(x In 2 .. 5 By 1){
                            If(False){
                                Break;
                            }
                            Continue;
                        }
                        If(False){
                            Break;
                        }Else{
                            Continue;
                        }
                        Foreach(x In 2 .. 5 By 1){
                            Foreach(y In 2 .. 5 By 1){
                                Foreach(z In 2 .. 5 By 1){
                                    Foreach(z In 2 .. 5 By 1){
                                        Continue;
                                    }
                                }
                            }
                        }
                    }
                    Return;
                }
            }"""
        expect = "Break Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,412))

    # Break-Continue complex
    def test_13(self):
        input = """Class Program {
                main(){
                    Var x,y,z: Int;
                    If(True){
                        Foreach(x In 2 .. 5 By 1){
                            If(False){
                                Foreach(y In 2 .. 5 By 1){
                                    Foreach(z In 2 .. 5 By 1){
                                        Break;
                                    }
                                }
                                Continue;
                            }
                        }
                    }
                    Return;
                }
            }"""
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,413))

    ## Have multi-scope block
    # Break-Continue complex
    def test_14(self):
        input = """Class Program {
                main(){
                    Var x,y,z: Int;
                    Foreach(x In 2 .. 5 By 1){
                        If(False){
                            Foreach(y In 2 .. 5 By 1){
                                If(False){
                                    Return;
                                }Else{
                                    Continue;
                                }
                            }
                            If(True){
                                Break;
                            }
                        }
                    }
                    Return;
                }
            }"""
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,414))

    # No entry point
    def test_15(self):
        input = """Class Rectangle {
                main(){
                    Return;
                }
            }"""
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input,expect,415))
    
    def test_15(self):
        input = """Class Program {
                main(a,b,c: Int; d,e: Float; f: String){}
            }"""
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input,expect,415))

    def test_16(self):
        input = """Class Program {
                main1(){
                    Return;
                }
                main(a,b,c: Int; d,e: Float; f: String){
                    Return;
                }
            }"""
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input,expect,416))

    def test_17(self):
        input = """Class Program {
                main(){
                    Return 12+12;
                }
            }"""
        expect = "Type Mismatch In Statement: Return(BinaryOp(+,IntLit(12),IntLit(12)))"
        self.assertTrue(TestChecker.test(input,expect,417))
    
    # Redeclared name main
    def test_18(self):
        input = """Class Program {
                main(){
                    Var x: Int = 12;
                    Return;
                }
                main(){
                    Return;
                }
            }"""
        expect = "Redeclared Method: main"
        self.assertTrue(TestChecker.test(input,expect,418))

    # Name checking
    def test_19(self):
        input = """Class Program {
                Var a, $b: Float;
                Val c,d,e: Int = 1,5,6;

                main(){
                    Return;
                }

                calc(a,c: Int; b,d: Float){
                    Var m,n: Float;
                    Return;
                }
                $getArea(e,b: String){
                    Val x,a,c: Boolean;
                    Return;
                }
            }
            Class Shape{}
            Class Reactangle: Shape{}
            """
        expect = "Illegal Constant Expression: None"
        self.assertTrue(TestChecker.test(input,expect,419))

    # Duplicate classname
    def test_20(self):
        input = """Class Program {
                        main(){
                                Return;
                            }
                    }
            Class Shape{}
            Class Reactangle: Shape{}
            Class Shape{}
            """
        expect = "Redeclared Class: Shape"
        self.assertTrue(TestChecker.test(input,expect,420))

    # Duplicate classname
    def test_21(self):
        input = """Class Program {
                        main(){
                                Return;
                            }
                    }
            Class B{}
            Class A{}
            Class A: B{}
            """
        expect = "Redeclared Class: A"
        self.assertTrue(TestChecker.test(input,expect,421))

    # Undeclare parent classname
    def test_22(self):
        input = """Class Program {
                        main(){
                                Return;
                            }
                    }
            Class A: B{}
            """
        expect = "Undeclared Class: B"
        self.assertTrue(TestChecker.test(input,expect,422))

    # Name checking
    def test_23(self):
        input = """Class Program {
                Var a, $b: Float;
                Val c,d,e: Int = 1,5,6;

                main(){
                    Return;
                }

                calc(a,c: Int; b,d: Float){
                    Var m,n: Float;
                    Return 12;
                }
            }
            Class Shape{}
            Class Reactangle: Shape{}
            """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,423))

    # Name checking
    def test_24(self):
        input = """Class Program {
                Var a, $a: Float;
                main(){
                    Return;
                }
            }
            Class Shape{}
            Class Reactangle: Shape{}
            """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,424))

    # Task 2.8
    def test_25(self):
        input = """Class Program {
                Var a, $a: Float;
                Val b: Int = 1 + Program::$a;
                Var a: Boolean;
                main(){
                    Return;
                }
            }
            Class Shape{}
            Class Reactangle: Shape{}
            """
        expect = "Illegal Constant Expression: BinaryOp(+,IntLit(1),FieldAccess(Id(Program),Id($a)))"
        self.assertTrue(TestChecker.test(input,expect,425))

    def test_26(self):
        input = """Class Program {
                Val a, $a: Float;
                Val b: Int = 1 + Program::$a;
                Var a: Boolean;
                main(){
                    Return;
                }
            }
            Class Shape{}
            Class Reactangle: Shape{}
            """
        expect = "Illegal Constant Expression: None"
        self.assertTrue(TestChecker.test(input,expect,426))

    # Type Int + Float
    def test_27(self):
        input = """Class Program {
                Val a, $a: Float = 1.34, 124.e-2;
                Val b: Int = 1 + Program::$a;
                Var a: Boolean;
                main(){
                    Return;
                }
            }
            Class Shape{}
            Class Reactangle: Shape{}
            """
        expect = "Type Mismatch In Constant Declaration: ConstDecl(Id(b),IntType,BinaryOp(+,IntLit(1),FieldAccess(Id(Program),Id($a))))"
        self.assertTrue(TestChecker.test(input,expect,427))

            

    # Redeclare
    def test_28(self):
        input = """Class Program {
                Val a, $a: Int = 3*2+1-21/3, 124-32-122;
                Val b: Int = 1 + Program::$a;
                Var a: Boolean;
                main(){
                    Return;
                }
            }
            Class Shape{}
            Class Reactangle: Shape{}
            """
        expect = "Redeclared Attribute: a"
        self.assertTrue(TestChecker.test(input,expect,428))

    def test_29(self):
        input = """Class Program {
                Var a, $a: Int = 3*2+1-21/3, 124-32-122;
                Val b: Int = 1 + Program::$a;
                Var d: Boolean;
                main(){
                    Return;
                }
            }
            Class Shape{}
            Class Reactangle: Shape{}
            """
        expect = "Illegal Constant Expression: BinaryOp(+,IntLit(1),FieldAccess(Id(Program),Id($a)))"
        self.assertTrue(TestChecker.test(input,expect,429))

    # Array Literal
    def test_30(self):
        input = """Class Program {
                Val a, $a: Int = 3*2+1-21/3, 124-32-122;
                Val b: Int = 1 + Program::$a;
                Var d: Array[Int, 5] = Array(1,2,3,4,5);
                main(){
                    Return;
                }
            }
            Class Shape{}
            Class Reactangle: Shape{}
            """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,430))

    # Out of index
    def test_31(self):
        input = """Class Program {
                Val a, $a: Int = 3*2+1-21/3, 124-32-122;
                Val b: Int = 1 + Program::$a;
                Var d: Array[Int, 5] = Array(1,2,3,4,5,6);
                main(){
                    Return;
                }
            }
            Class Shape{}
            Class Reactangle: Shape{}
            """
        expect = "Type Mismatch In Statement: VarDecl(Id(d),ArrayType(5,IntType),[IntLit(1),IntLit(2),IntLit(3),IntLit(4),IntLit(5),IntLit(6)])"
        self.assertTrue(TestChecker.test(input,expect,431))

    # Task 2.9: Type mustbe the same
    def test_32(self):
        input = """Class Program {
                Val a, $a: Int = 3*2+1-21/3, 124-32-122;
                Val b: Int = 1 + Program::$a;
                Var d: Array[Int, 5] = Array(1,2,3,4,5.6);
                main(){
                    Return;
                }
            }
            Class Shape{}
            Class Reactangle: Shape{}
            """
        expect = "Illegal Array Literal: [IntLit(1),IntLit(2),IntLit(3),IntLit(4),FloatLit(5.6)]"
        self.assertTrue(TestChecker.test(input,expect,432))

    # Need to pass the whole array (Diff)
    def test_33(self):
        input = """Class Program {
                Var $myArray: Array[Array[Array[Int,4],2],2] = Array(
                    Array(
                        Array(1,2,3,4),
                        Array(5,6,7,8)
                    ),
                    Array(
                        Array(-1,-2,-3,-4),
                        Array(-5,-6,-7, False)
                    )
                );
                main(){
                    Return;
                }
            }
            Class Shape{}
            Class Reactangle: Shape{}
            """
        expect = "Illegal Array Literal: [UnaryOp(-,IntLit(5)),UnaryOp(-,IntLit(6)),UnaryOp(-,IntLit(7)),BooleanLit(False)]"
        self.assertTrue(TestChecker.test(input,expect,433))

    def test_34(self):
        input = """Class Program {
                main(){
                    Var a: Array[Int, 3] = Array(1,2,3);
                    a[4] = 5; 
                    
                    Return;
                }
            }
            Class Shape{}
            Class Reactangle: Shape{}
            """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,434))

    def test_35(self):
        input = """Class Program {
                main(){
                    Var a: Array[Int, 3] = Array(1,2,3);
                    a[1][2] = 4;
                    Return;
                }
            }
            Class Shape{}
            Class Reactangle: Shape{}
            """
        expect = "Type Mismatch In Expression: ArrayCell(Id(a),[IntLit(1),IntLit(2)])"
        self.assertTrue(TestChecker.test(input,expect,435))

    # Int/Int = Int (not change type)
    def test_36(self):
        input = """Class Program {
                Var a: Array[Array[Float, 2], 2] = Array(
                    Array(1.1, 2.2),
                    Array(3.3, 4.4-21/3)
                );
                main(){    
                    Self.a[1][2] = 4;
                    Return;
                }
            }
            Class Shape{}
            Class Reactangle: Shape{}
            """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,436))


    # Float = Int (coerce)
    def test_37(self):
        input = """Class Program {
                Var a: Array[Array[Float, 2], 3] = Array(
                    Array(1.1, 2.2),
                    Array(3.3, 4.4-21.1/3.7),
                    Array(3.3, 4.4-21.1/3.7)
                );
                main(){    
                    Self.a[1][2] = 4;
                    Return;
                }
            }
            Class Shape{}
            Class Reactangle: Shape{}
            """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,437))

    # Array Cell and Type
    def test_38(self):
        input = """Class Program {
                Var a: Array[Array[Float, 2], 3] = Array(
                    Array(1.1, 2.2),
                    Array(3.3, 4.4-21.1/3.7),
                    Array(3.3, 4.4-21.1/3.7)
                );
                main(){    
                    Self.a[101+1.2][2] = 4;
                    Return;
                }
            }
            Class Shape{}
            Class Reactangle: Shape{}
            """
        expect = "Type Mismatch In Expression: ArrayCell(FieldAccess(Self(),Id(a)),[BinaryOp(+,IntLit(101),FloatLit(1.2)),IntLit(2)])"
        self.assertTrue(TestChecker.test(input,expect,438))

    def test_39(self):
        input = """Class Program {
                Var a: Array[Array[Float, 2], 3] = Array(
                    Array(1.1, 2.2),
                    Array(3.3, 4.4-21.1/3.7),
                    Array(3.3, 4.4-21.1/3.7)
                );
                main(){    
                    Self.aaaaaa[101][2] = 4;
                    Return;
                }
            }
            Class Shape{}
            Class Reactangle: Shape{}
            """
        expect = "Undeclared Attribute: aaaaaa"
        self.assertTrue(TestChecker.test(input,expect,439))

    def test_40(self):
        input = """Class Program {
                Var a: Array[Array[Float, 2], 3] = Array(
                    Array(1.1, 2.2),
                    Array(3.3, 4.4-21.1/3.7),
                    Array(3.3, 4.4-21.1/3.7)
                );
                Val aaaaaa: Array[Boolean, 3] = Array(True, False, True);
                main(){    
                    Self.aaaaaa[101][2] = 4;
                    Return;
                }
            }
            Class Shape{}
            Class Reactangle: Shape{}
            """
        expect = "Type Mismatch In Expression: ArrayCell(FieldAccess(Self(),Id(aaaaaa)),[IntLit(101),IntLit(2)])"
        self.assertTrue(TestChecker.test(input,expect,440))

    # Bool not type
    def test_41(self):
        input = """Class Program {
                Var a: Array[Array[Float, 2], 3] = Array(
                    Array(1.1, 2.2),
                    Array(3.3, 4.4-21.1/3.7),
                    Array(3.3, 4.4-21.1/3.7)
                );
                Val aaaaaa: Array[Boolean, 3] = Array(True, False, True);
                main(){    
                    Self.aaaaaa[101] = 4;
                    Return;
                }
            }
            Class Shape{}
            Class Reactangle: Shape{}
            """
        expect = "Cannot Assign To Constant: AssignStmt(ArrayCell(FieldAccess(Self(),Id(aaaaaa)),[IntLit(101)]),IntLit(4))"
        self.assertTrue(TestChecker.test(input,expect,441))

    def test_42(self):
        input = """Class Program {
                Var a: Array[Array[Float, 2], 3] = Array(
                    Array(1.1, 2.2),
                    Array(3.3, 4.4-21.1/3.7),
                    Array(3.3, 4.4-21.1/3.7)
                );
                Val aaaaaa: String = "Hello World, my name is Quach Minh Tuan. Glad to see you";
                main(){    
                    Self.aaaaaa[101] = 4;
                    Return;
                }
            }
            Class Shape{}
            Class Reactangle: Shape{}
            """
        expect = "Type Mismatch In Expression: ArrayCell(FieldAccess(Self(),Id(aaaaaa)),[IntLit(101)])"
        self.assertTrue(TestChecker.test(input,expect,442))

    # Type match Type
    def test_43(self):
        input = """Class Program {
                Var a: Array[Array[Float, 2], 3] = Array(
                    Array(1.1, 2.2),
                    Array(3.3, 4.4-21.1/3.7),
                    Array(3.3, 4.4-21.1/3.7)
                );
                main(){    
                    Self.a[101] = 4;
                    Return;
                }
            }
            Class Shape{}
            Class Reactangle: Shape{}
            """
        expect = "Type Mismatch In Statement: AssignStmt(ArrayCell(FieldAccess(Self(),Id(a)),[IntLit(101)]),IntLit(4))"
        self.assertTrue(TestChecker.test(input,expect,443))

    def test_44(self):
        input = """Class Program {
                Var a: Array[Array[Float, 2], 3] = Array(
                    Array(1.1, 2.2),
                    Array(3.3, 4.4-21.1/3.7),
                    Array(3.3, 4.4-21.1/3.7)
                );
                main(){    
                    Self.a[101] = Array(1,2,3);
                    Return;
                }
            }
            Class Shape{}
            Class Reactangle: Shape{}
            """
        expect = "Type Mismatch In Statement: AssignStmt(ArrayCell(FieldAccess(Self(),Id(a)),[IntLit(101)]),[IntLit(1),IntLit(2),IntLit(3)])"
        self.assertTrue(TestChecker.test(input,expect,444))

    # True case
    def test_45(self):
        input = """Class Program {
                Var a: Array[Array[Float, 2], 3] = Array(
                    Array(1.1, 2.2),
                    Array(3.3, 4.4-21.1/3.7),
                    Array(3.3, 4.4-21.1/3.7)
                );
                main(){    
                    Self.a[101] = Array(1.,2e-12);
                    Return;
                }
            }
            Class Shape{}
            Class Reactangle: Shape{}
            """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,445))

########********* Do in another class
    def test_46(self):
        input = """
            Class Shape{}
            Class Rectangle: Shape{
                Var $a,$b,$c: Int = 5/31+43,6,6+23;
                Val d: Float = 12;
            }    
            Class Program {
                Var a: Array[Array[Float, 2], 3] = Array(
                    Array(1.1, 2.2),
                    Array(3.3, 4.4-21.1/3.7),
                    Array(3.3, 4.4-21.1/3.7)
                );
                main(){    
                    Self.a[12][Rectangle::$b] = 12*12*12%7128;
                    
                    Return;
                }
            }
            
            """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,446))

    def test_47(self):
        input = """
            Class Shape{}
            Class Rectangle: Shape{
                Var $a,$b,$c: Int = 5/31+43,6,6+23;
                Val d: Float = 12;
            }    
            Class Program {
                Var a: Array[Array[Float, 2], 3] = Array(
                    Array(1.1, 2.2),
                    Array(3.3, 4.4-21.1/3.7),
                    Array(3.3, 4.4-21.1/3.7)
                );
                main(){    
                    Self.a[Rectangle::$c][Rectangle::$b] = New Rectangle().d;
                    
                    Return;
                }
            }
            
            """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,447))

    def test_48(self):
        input = """
            Class Shape{}
            Class Rectangle: Shape{
                Var $a,$b,$c: Int = 5/31+43,6,6+23;
                Val d: Float = 12;
            }    
            Class Program {
                Var $a: Array[Array[Float, 2], 3] = Array(
                    Array(1.1, 2.2),
                    Array(3.3, 4.4-21.1/3.7),
                    Array(3.3, 4.4-21.1/3.7)
                );
                main(){    
                    Program::$a[Rectangle::$c][Rectangle::$b] = New Rectangle() .d;
                    
                    Return;
                }
            }
            
            """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,448))
    
    # Already have parent class
    def test_49(self):
        input = """
            Class Program : Program {
                main(){    
                    Return;
                }
            }
            """
        expect = "Undeclared Class: Program"
        self.assertTrue(TestChecker.test(input,expect,449))

    def test_50(self):
        input = """
            Class Program{
                Constructor(a,c,edf: Int; b: Float){
                    Return;
                }
                Destructor(){}
                main(){    
                    Return;
                }
            }
            """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,450))

    # Constructor Checker
    def test_51(self):
        input = """
            Class Program{
                Constructor(a,c,edf: Int; b: Float){
                    Return 121*12+131-12;
                }
                Destructor(){}
                main(){    
                    Return;
                }
            }
            """
        expect = "Type Mismatch In Statement: Return(BinaryOp(-,BinaryOp(+,BinaryOp(*,IntLit(121),IntLit(12)),IntLit(131)),IntLit(12)))"
        self.assertTrue(TestChecker.test(input,expect,451))
    
    # Destructor Checker
    def test_52(self):
        input = """
            Class Program{
                Constructor(a,c,edf: Int; b: Float){
                    Return;
                }
                Destructor(){
                    Return 1231.32/21.3678;
                }
                main(){    
                    Return;
                }
            }
            """
        expect = "Type Mismatch In Statement: Return(BinaryOp(/,FloatLit(1231.32),FloatLit(21.3678)))"
        self.assertTrue(TestChecker.test(input,expect,452))

    def test_53(self):
        input = """
            Class Program{
                Constructor(a,c,edf: Int; b: Float){
                    Return;
                }
                Destructor(){
                    Return;
                }
                main(){    
                    Return;
                }
            }
            """
        expect = "Type Mismatch In Statement: Return()"
        self.assertTrue(TestChecker.test(input,expect,453))

    def test_54(self):
        input = """
            Class Program{
                Constructor(a,c,edf: Int; b: Float){
                    Return;
                }
                Destructor(){
                    Return;
                }
                main(){    
                    Return 1231.32/21.3678;
                }
            }
            """
        expect = "Type Mismatch In Statement: Return(BinaryOp(/,FloatLit(1231.32),FloatLit(21.3678)))"
        self.assertTrue(TestChecker.test(input,expect,454))

    # Task 2.6
    def test_55(self):
        input = """
            Class Program{
                Val a : Int = 1.2;
                main(){    
                    Return;
                }
            }
            """
        expect = "Type Mismatch In Constant Declaration: ConstDecl(Id(a),IntType,FloatLit(1.2))"
        self.assertTrue(TestChecker.test(input,expect,455))

    def test_56(self):
        input = """
            Class Program{
                Val a : Int = 1*2;
                Val $a : Int = 1/2;
                main(){    
                    Return;
                }
            }
            """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,456))

    # Assign rule
    def test_57(self):
        input = """
            Class Program{
                Val a : Int = 1*2;
                Val $a : Float = 1/2;
                main(){    
                    Return;
                }
            }
            """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,457))

    def test_58(self):
        input = """
            Class Program{
                Val a,$a,b,$c : Float = 1.2, 1e-3,   1*2, "Hello World";
                main(){    
                    Return;
                }
            }
            """
        expect = "Type Mismatch In Constant Declaration: ConstDecl(Id($c),FloatType,StringLit(Hello World))"
        self.assertTrue(TestChecker.test(input,expect,458))

    # Attr + Method can be same name in class
    def test_57(self):
        input = """
            Class Program{
                Val a, $a: Float = 12, 1e-3;
                a(){
                    Return;
                }
                $a(){
                    Return;
                }
                main(){    
                    Return;
                }
            }
            """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,457))

    # Declare overlap, behind
    def test_58(self):
        input = """
            Class Program{
                Val a, $a: Float = 12, 1e-3;
                a(){
                    Return;
                }
                $a(){
                    Return;
                }
                main(){    
                    Return;
                }
                Val a: Boolean = True;
            }
            """
        expect = "Redeclared Attribute: a"
        self.assertTrue(TestChecker.test(input,expect,458))

    def test_59(self):
        input = """Class Program {
                Var a: Array[Array[Float, 2], 3] = Array(
                    Array(1.1, 2.2),
                    Array(3.3, 4.4-21.1/3.7),
                    Array(3.3, 4.4-21.1/3.7)
                );
                Var aaaaaa: Array[Boolean, 3] = Array(True, False, True);
                main(){    
                    Self.aaaaaa[101] = 4;
                    Return;
                }
            }
            Class Shape{}
            Class Reactangle: Shape{}
            """
        expect = "Type Mismatch In Statement: AssignStmt(ArrayCell(FieldAccess(Self(),Id(aaaaaa)),[IntLit(101)]),IntLit(4))"
        self.assertTrue(TestChecker.test(input,expect,459))

    # Try to access + Invoke method (params of inside its)
    def test_60(self):
        input = """
            Class Shape{}
            Class Rectangle: Shape{
                Var $b,$c: Int = 6,6+23;
                Val d: Float = 12;
                $a(){Return 5/31+43;}
            }    
            Class Program {
                Var $a: Array[Array[Float, 2], 3] = Array(
                    Array(1.1, 2.2),
                    Array(3.3, 4.4-21.1/3.7),
                    Array(3.3, 4.4-21.1/3.7)
                );
                main(){    
                    Program::$a[Rectangle::$c][Rectangle::$a()] = New Rectangle() .d;
                    Return;
                }
            }
            
            """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,460))

    def test_61(self):
        input = """
            Class Shape{}
            Class Rectangle: Shape{
                Var $b,$c: Int = 6,6+23;
                Val d: Float = 12;
                $a(){Return 5/31+43;}
                $b(){Return 5/31+43;}
                d(){Return 5/31+43;}
            }    
            Class Program {
                Var $a: Array[Array[Float, 2], 3] = Array(
                    Array(1.1, 2.2),
                    Array(3.3, 4.4-21.1/3.7),
                    Array(3.3, 4.4-21.1/3.7)
                );
                main(){    
                    Program::$a[Rectangle::$b][Rectangle::$b()] = New Rectangle() .d();
                    Return;
                }
            }
            
            """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,461))

    def test_62(self):
        input = """
            Class Shape{}
            Class Rectangle: Shape{
                Var $b,$c: Int = 6,6+23;
                Val d: Float = 12;
                $a(){Return 5/31+43;}
                $b(){Return 5/31+43;}
                d(){Return 5/31+43;}
            }    
            Class Program {
                Var $a: Array[Array[Float, 2], 3] = Array(
                    Array(1.1, 2.2),
                    Array(3.3, 4.4-21.1/3.7)
                );
                main(){    
                    Program::$a[Rectangle::$b][Rectangle::$b()] = New Rectangle() .d();
                    Return;
                }
            }
            
            """
        expect = "Type Mismatch In Statement: VarDecl(Id($a),ArrayType(3,ArrayType(2,FloatType)),[[FloatLit(1.1),FloatLit(2.2)],[FloatLit(3.3),BinaryOp(-,FloatLit(4.4),BinaryOp(/,FloatLit(21.1),FloatLit(3.7)))]])"
        self.assertTrue(TestChecker.test(input,expect,462))
    
    # Pass augument to method
    def test_63(self):
        input = """
            Class Shape{}
            Class Rectangle: Shape{
                Var $b,$c: Int = 6,6+23;
                Val d: Float = 12;
                $a(){Return 5/31+43;}
                $b(){Return 5/31+43;}
                d(a: Float; b,e,f: Float){Return 5/31+43;}
            }    
            Class Program {
                Var $a: Array[Array[Float, 2], 3] = Array(
                    Array(1.1, 2.2),
                    Array(3.3, 4.4-21.1/3.7),
                    Array(3.3, 4.4-21.1/3.7)
                );
                main(){    
                    Program::$a[Rectangle::$b][Rectangle::$b()] = New Rectangle() .d(Rectangle::$b, Rectangle::$c, Rectangle::$b, Rectangle::$b, Rectangle::$b);
                    Return;
                }
            }
            
            """
        expect = "Type Mismatch In Expression: CallExpr(NewExpr(Id(Rectangle),[]),Id(d),[FieldAccess(Id(Rectangle),Id($b)),FieldAccess(Id(Rectangle),Id($c)),FieldAccess(Id(Rectangle),Id($b)),FieldAccess(Id(Rectangle),Id($b)),FieldAccess(Id(Rectangle),Id($b))])"
        self.assertTrue(TestChecker.test(input,expect,463))
    
    def test_64(self):
        input = """
            Class Shape{}
            Class Rectangle: Shape{
                Var $b,$c: Int = 6,6+23;
                Val d: Float = 12;
                $a(){Return 5/31+43;}
                $b(){Return 5/31+43;}
                d(a: Float; b,e,f: Float){Return 5/31+43;}
            }    
            Class Program {
                Var $a: Array[Array[Float, 2], 3] = Array(
                    Array(1.1, 2.2),
                    Array(3.3, 4.4-21.1/3.7),
                    Array(3.3, 4.4-21.1/3.7)
                );
                main(){    
                    Program::$a[Rectangle::$b][Rectangle::$b()] = New Rectangle() .d(Rectangle::$b, Rectangle::$c, Rectangle::$b);
                    Return;
                }
            }
            
            """
        expect = "Type Mismatch In Expression: CallExpr(NewExpr(Id(Rectangle),[]),Id(d),[FieldAccess(Id(Rectangle),Id($b)),FieldAccess(Id(Rectangle),Id($c)),FieldAccess(Id(Rectangle),Id($b))])"
        self.assertTrue(TestChecker.test(input,expect,464))
    
    def test_65(self):
        input = """
            Class Shape{}
            Class Rectangle: Shape{
                Var $b,$c: Int = 6,6+23;
                Val d: Float = 12;
                $a(){Return 5/31+43;}
                $b(){Return 5/31+43.0;}
                d(a: Int; b,e,f: Float){Return 5/31+43;}
            }    
            Class Program {
                Var $a: Array[Array[Float, 2], 3] = Array(
                    Array(1.1, 2.2),
                    Array(3.3, 4.4-21.1/3.7),
                    Array(3.3, 4.4-21.1/3.7)
                );
                main(){    
                    Program::$a[Rectangle::$b][Rectangle::$b()] = New Rectangle() .d(Rectangle::$b(), Rectangle::$c, Rectangle::$b);
                    Return;
                }
            }
            
            """
        expect = "Type Mismatch In Expression: ArrayCell(FieldAccess(Id(Program),Id($a)),[FieldAccess(Id(Rectangle),Id($b)),CallExpr(Id(Rectangle),Id($b),[])])"
        self.assertTrue(TestChecker.test(input,expect,465))
    
    def test_66(self):
        input = """
            Class Shape{}
            Class Rectangle: Shape{
                Var $b,$c: Int = 6,6+23;
                Val d: Float = 12;
                $a(){Return 5/31+43;}
                $b(){Return 5/31+43;}
                d(a: Int; b,e,f: Float){Return 5/31+43;}
            }    
            Class Program {
                Var $a: Array[Array[Float, 2], 3] = Array(
                    Array(1.1, 2.2),
                    Array(3.3, 4.4-21.1/3.7),
                    Array(3.3, 4.4-21.1/3.7)
                );
                main(){    
                    Program::$a[Rectangle::$b][Rectangle::$b()] = New Rectangle() .d(Rectangle::$b, Rectangle::$c, Rectangle::$b, Rectangle::$c);
                    Return;
                }
            }
            
            """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,466))

    def test_67(self):
        input = """
            Class Shape{}
            Class Rectangle: Shape{
                Var $b,$c: Int = 6,6+23;
                Val d: Float = 12;
                $a(){Return 5/31+43;}
                $b(){Return 5/31+43.0;}
                d(a: Int; b,e,f: Float){Return 5/31+43;}
            }    
            Class Program {
                Var $a: Array[Array[Float, 2], 3] = Array(
                    Array(1.1, 2.2),
                    Array(3.3, 4.4-21.1/3.7),
                    Array(3.3, 4.4-21.1/3.7)
                );
                main(){    
                    Program::$a[Rectangle::$b][Rectangle::$b] = New Rectangle() .d(Rectangle::$b(), Rectangle::$c, Rectangle::$b, Rectangle::$c);
                    Return;
                }
            }
            
            """
        expect = "Type Mismatch In Expression: CallExpr(NewExpr(Id(Rectangle),[]),Id(d),[CallExpr(Id(Rectangle),Id($b),[]),FieldAccess(Id(Rectangle),Id($c)),FieldAccess(Id(Rectangle),Id($b)),FieldAccess(Id(Rectangle),Id($c))])"
        self.assertTrue(TestChecker.test(input,expect,467))
    
    def test_68(self):
        input = """Class Program{
            main() {
                Var i: Boolean;
                Var j: Int;
                i = j == j;
                i = j;
                j = i;
            }
        }"""
        expect = "Type Mismatch In Statement: AssignStmt(Id(i),Id(j))"
        self.assertTrue(TestChecker.test(input,expect,468))

    # BinOp: 
    def test_69(self):
        input = """Class Program{
            main() {
                Var i: Boolean;
                Var j: Int;
                Val k: Float = 2.1;
                i = j == j;
                i = j >= k;
                i = (j <= k) && (j < k) || (j > k);
                j = i;
            }
        }"""
        expect = "Type Mismatch In Statement: AssignStmt(Id(j),Id(i))"
        self.assertTrue(TestChecker.test(input,expect,469))
    
    # Coerce Array: Float -> Int
    def test_70(self):
        input = """Class Program{
            main() {
                Var i: Array[Int, 3] = Array(0,1,2);
                Var j: Array[Float, 3] = Array(0.0,1.1,1.2);
                j = i;
                Var b: Boolean;
                b = i;
            }
        }"""
        expect = "Type Mismatch In Statement: AssignStmt(Id(b),Id(i))"
        self.assertTrue(TestChecker.test(input,expect,470))

    ## Merge many things
    def test_71(self):
        input = """Class IO {
            $getInt() { Return 1; }
            $putIntLn(a: Int) {}
            $putFloatLn(a: Float) {}
        }
        Class Program{
            main() {
                IO::$putFloatLn(1345123);
                IO::$putFloatLn(123512131);
                IO::$putIntLn(1212145);
                IO::$putFloatLn(512e-1);
                IO::$putFloatLn(7634.343132);
                IO::$putIntLn(5.3);
            }
        }"""
        expect = "Type Mismatch In Statement: Call(Id(IO),Id($putIntLn),[FloatLit(5.3)])"
        self.assertTrue(TestChecker.test(input,expect,471))

    def test_72(self):
        input = """Class Program{
            main() {
                Val s: Float = 0;
                s.to_string();
            }
        }"""
        expect = "Type Mismatch In Statement: Call(Id(s),Id(to_string),[])"
        self.assertTrue(TestChecker.test(input,expect,472))

    def test_73(self):
        input = """Class Program {
            main() {
                Var idx: Int;
                Foreach(idx In 1 .. 10) {
                    Var newIdx: Int;
                    Foreach(newIdx In 1 .. 10) {
                        Continue;
                    }
                }
                Break;
            }
        }"""
        expect = "Break Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,430))

    def test_74(self):
        input = """Class Program {
            main() {
                If (True) {
                    Break;
                }
                Var i: Int;
                Foreach(i In 1 .. 10) {
                    Continue;
                }
            }
        }"""
        expect = "Break Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,474))

    # For is a part of Assign => Coerce
    def test_75(self):
        input = """Class Program{
            main() {
                Var i: Float;
                Foreach(i In 1 .. 10 By 100) {}
            }
        }"""
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,475))

    def test_76(self):
        input = """Class Program{
            main() {
                Var i: Int;
                Foreach(i In 1 .. 10.2) {}
            }
        }"""
        expect = "Type Mismatch In Statement: For(Id(i),IntLit(1),FloatLit(10.2),IntLit(1),Block([])])"
        self.assertTrue(TestChecker.test(input,expect,476))

    def test_77(self):
        input = """Class Program{
            main() {
                Var i: Float;
                Foreach(i In 1 + 1 .. 10 + 0.5) {}
            }
        }"""
        expect = "Type Mismatch In Statement: For(Id(i),BinaryOp(+,IntLit(1),IntLit(1)),BinaryOp(+,IntLit(10),FloatLit(0.5)),IntLit(1),Block([])])"
        self.assertTrue(TestChecker.test(input,expect,477))

    def test_76(self):
        input = """Class Program{
            main() {
                Var i: Float;
                Foreach(i In 1 + 1 .. "Hello" +. "Quach Minh Tuan") {}
            }
        }"""
        expect = "Type Mismatch In Statement: For(Id(i),BinaryOp(+,IntLit(1),IntLit(1)),BinaryOp(+.,StringLit(Hello),StringLit(Quach Minh Tuan)),IntLit(1),Block([])])"
        self.assertTrue(TestChecker.test(input,expect,476))

    # Assign
    def test_77(self):
        input = """Class Program{
            main() {
                Var i: Float;
                Var j: Int;
                i = j;
                j = i;
            }
        }"""
        expect = "Type Mismatch In Statement: AssignStmt(Id(j),Id(i))"
        self.assertTrue(TestChecker.test(input,expect,477))

    # Assign + Binop
    def test_78(self):
        input = """Class Program{
            main() {
                Var i: Float;
                Var j: Int;
                i = j;
                j = i + j;
            }
        }"""
        expect = "Type Mismatch In Statement: AssignStmt(Id(j),BinaryOp(+,Id(i),Id(j)))"
        self.assertTrue(TestChecker.test(input,expect,478))

    # Constant
    def test_79(self):
        input = """Class Program {
            main() {
                Val idx: Int = 1.2;
            }
        }"""
        expect = "Type Mismatch In Constant Declaration: ConstDecl(Id(idx),IntType,FloatLit(1.2))"
        self.assertTrue(TestChecker.test(input,expect,479))

    def test_80(self):
        input = """Class Program {
            main() {
                Val idx: Boolean = 1;
            }
        }"""
        expect = "Type Mismatch In Constant Declaration: ConstDecl(Id(idx),BoolType,IntLit(1))"
        self.assertTrue(TestChecker.test(input,expect,480))


    def test_81(self):
        input = """Class Program {
            main() {
                Val idx: Int = True;
            }
        }"""
        expect = "Type Mismatch In Constant Declaration: ConstDecl(Id(idx),IntType,BooleanLit(True))"
        self.assertTrue(TestChecker.test(input,expect,481))

    # Assign on Const   
    def test_82(self):
        input = """Class Program {
            main() {
                Val idx: Int = 1/2*42-1213+-12-(12+34--12);
                idx = idx + 1;
            }
        }"""
        expect = "Cannot Assign To Constant: AssignStmt(Id(idx),BinaryOp(+,Id(idx),IntLit(1)))"
        self.assertTrue(TestChecker.test(input,expect,482))
    
    def test_83(self):
        input = """Class Test {
            Var $attri: Float;
        }
        Class Program {
            main() {
                Var a: Int = Test::$attri;
            }
        }"""
        expect = "Type Mismatch In Statement: VarDecl(Id(a),IntType,FieldAccess(Id(Test),Id($attri)))"
        self.assertTrue(TestChecker.test(input,expect,483))

    def test_84(self):
        input = """Class Program {
            main() {
                Val a: Int = 5;
                Val b: Int = 0;
                a = b;
            }
        }"""
        expect = "Cannot Assign To Constant: AssignStmt(Id(a),Id(b))"
        self.assertTrue(TestChecker.test(input,expect,484))

    def test_85(self):
        input = """Class Program {
            Val $constant: Int = 10;

            main() {
                Program::$constant = 10;
            }
        }"""
        expect = "Cannot Assign To Constant: AssignStmt(FieldAccess(Id(Program),Id($constant)),IntLit(10))"
        self.assertTrue(TestChecker.test(input,expect,485))

    # For + Assign
    def test_86(self):
        input = """Class Program {
            ## Test about For + Assign ##
            main() {
                Val idx: Int = 5;
                Foreach(idx In 1 .. 10) {
                    
                }
            }
        }"""
        expect = "Cannot Assign To Constant: AssignStmt(Id(idx),IntLit(1))"
        self.assertTrue(TestChecker.test(input,expect,486))

    # Const expr
    def test_87(self):
        input = """Class Program {
            main() {
                Var inc: Int = 1/2*42-1213+-12-(12+34--12);
                Val idx: Int = 1 + inc;
                
            }
        }"""
        expect = "Illegal Constant Expression: BinaryOp(+,IntLit(1),Id(inc))"
        self.assertTrue(TestChecker.test(input,expect,487))
    
    # Const expr
    def test_88(self):
        input = """Class Program {
            main() {
                Val inc: Int = 1/2*42-1213+-12-(12+34--12);
                Val idx: Int = 1 + inc;
                
            }
        }"""
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,488))
    
    def test_89(self):
        input = """Class Program {
            main() {
                Val inc: Int = 1/2*42-1213+-12-(12+34--12);
                Var a : Float;
                Val idx: Float = a + inc;
                
            }
        }"""
        expect = "Illegal Constant Expression: BinaryOp(+,Id(a),Id(inc))"
        self.assertTrue(TestChecker.test(input,expect,489))
    
    # Task 2.6
    def test_90(self):
        input = """Class Program {
            main() {
                Val inc: Int = 1/2*42-1213+-12-(12+34--12);
                Val a : Float;
                Var idx: Int = a + inc;
                
            }
        }"""
        expect = "Illegal Constant Expression: None"
        self.assertTrue(TestChecker.test(input,expect,490))
    
    # Unde
    def test_91(self):
        input = """Class io {
            $getInt() { Return 1; }
            $putIntLn(a: Int) {}
            $putFloatLn(a: Float) {}
        }
        Class Program {
            main() {
                io::$foo();
            }
        }"""
        expect = "Undeclared Method: $foo"
        self.assertTrue(TestChecker.test(input,expect,491))

    # NO param
    def test_92(self):
        input = """Class io {
            $getInt() { Return 21345; }
            $putIntLn(a: Int) {}
            $putFloatLn(a: Float) {}
        }
        Class Program {
            main() {
                io::$putIntLn();
            }
        }"""
        expect = "Type Mismatch In Statement: Call(Id(io),Id($putIntLn),[])"
        self.assertTrue(TestChecker.test(input,expect,492))
    
    def test_93(self):
        input = """Class io {
            $getInt() { Return 1; }
            $putIntLn(a: Int) {}
            $putFloatLn(a: Float) {}
        }
        Class Program {
            main() {
                io::$putIntLn(io::$getInt(4));
            }
        }"""
        expect = "Type Mismatch In Expression: CallExpr(Id(io),Id($getInt),[IntLit(4)])"
        self.assertTrue(TestChecker.test(input,expect,493))
       
     # Constructor => New expr (pass type)
    def test_94(self):
        input = """
            Class Shape{}
            Class Rectangle: Shape{
                Constructor(x, y: Boolean; z: Float){}
                Var $b,$c: Int = 6,6+23;
                Val d: Float = 12;
                $a(){Return 5/31+43;}
                $b(){Return 5/31+43;}
                d(){Return 5/31+43;}
            }    
            Class Program {
                Var $a: Array[Array[Float, 2], 2] = Array(
                    Array(1.1, 2.2),
                    Array(3.3, 4.4-21.1/3.7)
                );
                main(){    
                    Program::$a[Rectangle::$b][Rectangle::$b()] = New Rectangle(True, False, Rectangle.d) .d();
                    Program::$a[Rectangle::$b][Rectangle::$b()] = New Rectangle() .d();
                }
            }
            
            """
        expect = "Illegal Member Access: FieldAccess(Id(Rectangle),Id(d))"
        self.assertTrue(TestChecker.test(input,expect,494))
    
    
    # Class + Null
    def test_95(self):
        input = """
            Class Shape{}
            Class Rectangle: Shape{
                Constructor(x, y: Boolean; z: Float){}
                Var $b,$c: Int = 6,6+23;
                Val d: Float = 12;
                $a(){Return 5/31+43.0;}
                $b(){Return 5/31+43;}
                d(){Return 5/31+43;}
            }    
            Class Program {

                ##Null ....##
                Var x: Rectangle;
                Var y: Rectangle = Null;
                Var z: Rectangle = New Rectangle();
                main(){    
                    Program::$a = Self.x;
                    Program::$a = Array(Self.y, Self.x);
                }
            }
            
            """
        expect = "Type Mismatch In Statement: VarDecl(Id(x),ClassType(Id(Rectangle)),NullLiteral())"
        self.assertTrue(TestChecker.test(input,expect,495))

    # Illegal Member Access
    def test_96(self):
        input = """
            Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(){Return 12;}
            }    
            Class Program {                
                main(){    
                    Var a: A = New A();
                    
                    A::$a();
                }
            }
            
            """
        expect = "Type Mismatch In Statement: Call(Id(A),Id($a),[])"
        self.assertTrue(TestChecker.test(input,expect,496))


    def test_97(self):
        input = """
            Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(){Return;}
            }    
            Class Program {                
                main(){    
                    Var a: A = New A();
                    A::$a();
                    Var b: Int = A.a;
                }
            }
            
            """
        expect = "Illegal Member Access: FieldAccess(Id(A),Id(a))"
        self.assertTrue(TestChecker.test(input,expect,497))


    def test_98(self):
        input = """
            Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(){Return;}
            }    
            Class Program {                
                main(){    
                    Var a: A = New A();
                    A::$a();
                    Var b: Int = a.b;
                }
            }
            
            """
        expect = "Undeclared Attribute: b"
        self.assertTrue(TestChecker.test(input,expect,498))

    def test_99(self):
        input = Program(
            [
                ClassDecl(
                    Id("Program"),
                    [
                        MethodDecl(
                            Static(),
                            Id("main"),
                            [],
                            Block([
                                ConstDecl(
                                    Id("myVar"),
                                    IntType(),
                                    IntLiteral(5)
                                ),
                                Assign(
                                    Id("myVar"),
                                    IntLiteral(10)
                                )]
                            )
                        )
                    ]
                )
            ]
        )
        expect = "Cannot Assign To Constant: AssignStmt(Id(myVar),IntLit(10))"
        self.assertTrue(TestChecker.test(input,expect,499))

    


