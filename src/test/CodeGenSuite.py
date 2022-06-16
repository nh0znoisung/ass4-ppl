import unittest
from TestUtils import TestCodeGen
from AST import *


class CheckCodeGenSuite(unittest.TestCase):
    # Basic case putInt
    def test_0(self):
        input = """
        Class Program {
            main(){
                io.writeInt(1);
            }
        }
        """
        expect = "1"
        self.assertTrue(TestCodeGen.test(input, expect, 500))

    # Big number
    def test_1(self):
        input = """
        Class Program {
            main(){
                io.writeInt(100);
            }
        }
        """
        expect = "100"
        self.assertTrue(TestCodeGen.test(input, expect, 501))

    # Negative case writeInt
    def test_2(self):
        input = """
        Class Program {
            main(){
                io.writeInt(-1);
            }
        }
        """
        expect = "-1"
        self.assertTrue(TestCodeGen.test(input, expect, 502))

    # Negative + big number
    def test_3(self):
        input = """
        Class Program {
            main(){
                io.writeInt(-100);
            }
        }
        """
        expect = "-100"
        self.assertTrue(TestCodeGen.test(input, expect, 503))

    # 2 Class
    def test_4(self):
        input = """
        Class A {}
        Class Program {
            main(){}
        }
        """
        expect = ""
        self.assertTrue(TestCodeGen.test(input, expect, 504))

    # Inheritance
    def test_5(self):
        input = """
        Class B {}
        Class C:B {}
        Class Program {
            main(){}
        }
        """
        expect = ""
        self.assertTrue(TestCodeGen.test(input, expect, 505))

    def test_6(self):
        input = """
        Class A {}
        Class B:A {}
        Class C:B {}
        Class Program {
            main(){}
        }
        """
        expect = ""
        self.assertTrue(TestCodeGen.test(input, expect, 506))
    
    # StoreDecl
    # VarDecl
    def test_7(self):
        input = """
        Class Program {
            main(){
                Var a: Int = 12;
                io.writeInt(a);
            }
        }
        """
        expect = "12"
        self.assertTrue(TestCodeGen.test(input, expect, 507))

    def test_8(self):
        input = """
        Class Program {
            main(){
                Val a: Int = 1;
                io.writeInt(a);
            }
        }
        """
        expect = "1"
        self.assertTrue(TestCodeGen.test(input, expect, 508))

    # Binop
    def test_9(self):
        input = """
        Class Shape{
            abc(a: Float){
                Return a;
            }
            cde(c: String){
                Return;
            }
            sdd(d: Boolean){
                Return d;
            }
        }
        Class Program {
            main(){
                Val a : Int = 12;
                io.writeInt(a);
            }
        }
        """
        expect = "12"
        self.assertTrue(TestCodeGen.test(input, expect, 509))

    def test_10(self):
        input = """
        Class Shape{
            abc(a: Float){
                Return 2;
            }
        }
        Class Program {
            main(){
                io.writeInt(1+2);
            }
        }
        """
        expect = "3"
        self.assertTrue(TestCodeGen.test(input, expect, 510))

    def test_11(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: Int = 12;
                io.writeInt(a);
            }
        }
        """
        expect = "12"
        self.assertTrue(TestCodeGen.test(input, expect, 511))

    # Write multitype
    def test_12(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: Float = 12;
                io.writeFloat(a);
            }
        }
        """
        expect = "12.0"
        self.assertTrue(TestCodeGen.test(input, expect, 512))

    def test_13(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: Boolean = True;
                io.writeBool(a);
            }
        }
        """
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 513))

    def test_14(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: String = "H";
                io.writeStr(a);
            }
        }
        """
        expect = "H"
        self.assertTrue(TestCodeGen.test(input, expect, 514))

    def test_15(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: String = "Hello world. My name is Quach Minh Tuan. Welcome to the biggest party";
                io.writeStr(a);
            }
        }
        """
        expect = "Hello world. My name is Quach Minh Tuan. Welcome to the biggest party"
        self.assertTrue(TestCodeGen.test(input, expect, 515))

    def test_16(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: Boolean = False;
                io.writeBool(a);
            }
        }
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 516))

    def test_17(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: Boolean = False;
                io.writeBool(!a);
            }
        }
        """
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 517))

    def test_18(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: Boolean = False;
                Var b: Boolean = False;
                io.writeBool(a && b);
            }
        }
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 518))

    def test_19(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: Boolean = False;
                Var b: Boolean = False;
                io.putBool(a || b);
            }
        }
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 519))


    # Short circuit
    def test_20(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: Boolean = False;
                Var b,d,e: Boolean = False, True, False;
                io.writeBool(a || b || d || e);
            }
        }
        """
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 520))

    def test_21(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: Boolean = True;
                Var b,d,e: Boolean = False, True, False;
                io.writeBool(a || b || d || e);
            }
        }
        """
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 521))

    # Relational
    def test_22(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Var a,b,c,d: Int = 1 + 2, 1 + 2, 1 + 2, 1 + 2;
                io.writeBool(a == b);
            }
        }
        """
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 522))

    def test_23(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Var a,b,c,d: Int = 1 + 2 * 3, (1 +2) * 3, 1 + 2, 1 + 2;
                io.writeBool(a == b);
            }
        }
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 523))

    def test_24(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Var a,b,c,d: Int = 1 + 2 * 3, (1 +2) * 3, 1 + 2, 1 + 2;
                io.writeBool(a > b);
            }
        }
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 524))



    def test_25(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Var a,b,c,d: Int = 1 + 2 * 3, (1 +2) * 3, 1 + 2, 1 + 2;
                io.writeBool(a >= b);
            }
        }
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 525))

    def test_26(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Var a,b,c,d: Int = 1 + 2 * 3, (1 +2) * 3, 1 + 2, 1 + 2;
                io.writeBool(a <= b);
            }
        }
        """
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 526))

    def test_27(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Var a,b,c,d: Int = 1 + 2 * 3, (1 +2) * 3, 1 + 2, 1 + 2;
                io.writeBool(a >= b);
            }
        }
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 527))

    # Coercion: Float -> Int
    def test_28(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val b: Int = 1 - 1;
                
                io.writeInt(b);
            }
        }
        """
        expect = "0"
        self.assertTrue(TestCodeGen.test(input, expect, 528))

    def test_29(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Var a,b,c,d: Int = 1 + 2 * 3, (1 +2) * 3, 1 + 2, 1 + 2;
                io.writeBool(a < b);
            }
        }
        """
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 529))

    def test_30(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Var a: Float = 1.0 * 2.0 - 1.0;
                Val b: Float = 1* 8 +(-12) * 12 + 1 + 1 - (1);
                io.writeFloat(a + b * a);
            }
        }
        """
        expect = "-134.0"
        self.assertTrue(TestCodeGen.test(input, expect, 530))
    

    ### CUT: 31->60
    def test_31(self):
        input = """
        Class Program {
            main(){
                io.writeInt(100);
            }
        }
        """
        expect = "100"
        self.assertTrue(TestCodeGen.test(input, expect, 531))

    # Negative case writeInt
    def test_32(self):
        input = """
        Class Program {
            main(){
                io.writeInt(-1);
            }
        }
        """
        expect = "-1"
        self.assertTrue(TestCodeGen.test(input, expect, 532))

    # Negative + big number
    def test_33(self):
        input = """
        Class Program {
            main(){
                io.writeInt(-100);
            }
        }
        """
        expect = "-100"
        self.assertTrue(TestCodeGen.test(input, expect, 533))

    # 2 Class
    def test_34(self):
        input = """
        Class A {}
        Class Program {
            main(){}
        }
        """
        expect = ""
        self.assertTrue(TestCodeGen.test(input, expect, 534))

    # Inheritance
    def test_35(self):
        input = """
        Class B {}
        Class C:B {}
        Class Program {
            main(){}
        }
        """
        expect = ""
        self.assertTrue(TestCodeGen.test(input, expect, 535))

    def test_36(self):
        input = """
        Class A {}
        Class B:A {}
        Class C:B {}
        Class Program {
            main(){}
        }
        """
        expect = ""
        self.assertTrue(TestCodeGen.test(input, expect, 536))
    
    # StoreDecl
    # VarDecl
    def test_37(self):
        input = """
        Class Program {
            main(){
                Var a: Int = 12;
                io.writeInt(a);
            }
        }
        """
        expect = "12"
        self.assertTrue(TestCodeGen.test(input, expect, 537))

    def test_38(self):
        input = """
        Class Program {
            main(){
                Val a: Int = 1;
                io.writeInt(a);
            }
        }
        """
        expect = "1"
        self.assertTrue(TestCodeGen.test(input, expect, 538))

    # Binop
    def test_39(self):
        input = """
        Class Shape{
            abc(a: Float){
                Return a;
            }
            cde(c: String){
                Return;
            }
            sdd(d: Boolean){
                Return d;
            }
        }
        Class Program {
            main(){
                Val a : Int = 12;
                io.writeInt(a);
            }
        }
        """
        expect = "12"
        self.assertTrue(TestCodeGen.test(input, expect, 539))

    def test_40(self):
        input = """
        Class Shape{
            abc(a: Float){
                Return 2;
            }
        }
        Class Program {
            main(){
                io.writeInt(1+2);
            }
        }
        """
        expect = "3"
        self.assertTrue(TestCodeGen.test(input, expect, 540))

    def test_41(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: Int = 12;
                io.writeInt(a);
            }
        }
        """
        expect = "12"
        self.assertTrue(TestCodeGen.test(input, expect, 541))

    # Write multitype
    def test_42(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: Float = 12;
                io.writeFloat(a);
            }
        }
        """
        expect = "12.0"
        self.assertTrue(TestCodeGen.test(input, expect, 542))

    def test_43(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: Boolean = True;
                io.writeBool(a);
            }
        }
        """
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 543))

    def test_44(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: String = "H";
                io.writeStr(a);
            }
        }
        """
        expect = "H"
        self.assertTrue(TestCodeGen.test(input, expect, 544))

    def test_45(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: String = "Hello world. My name is Quach Minh Tuan. Welcome to the biggest party";
                io.writeStr(a);
            }
        }
        """
        expect = "Hello world. My name is Quach Minh Tuan. Welcome to the biggest party"
        self.assertTrue(TestCodeGen.test(input, expect, 545))

    def test_46(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: Boolean = False;
                io.writeBool(a);
            }
        }
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 546))

    def test_47(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: Boolean = False;
                io.writeBool(!a);
            }
        }
        """
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 547))

    def test_48(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: Boolean = False;
                Var b: Boolean = False;
                io.writeBool(a && b);
            }
        }
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 548))

    def test_49(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: Boolean = False;
                Var b: Boolean = False;
                io.putBool(a || b);
            }
        }
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 549))


    # Short circuit
    def test_50(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: Boolean = False;
                Var b,d,e: Boolean = False, True, False;
                io.writeBool(a || b || d || e);
            }
        }
        """
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 550))

    def test_51(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: Boolean = True;
                Var b,d,e: Boolean = False, True, False;
                io.writeBool(a || b || d || e);
            }
        }
        """
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 551))

    # Relational
    def test_52(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Var a,b,c,d: Int = 1 + 2, 1 + 2, 1 + 2, 1 + 2;
                io.writeBool(a == b);
            }
        }
        """
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 552))

    def test_53(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Var a,b,c,d: Int = 1 + 2 * 3, (1 +2) * 3, 1 + 2, 1 + 2;
                io.writeBool(a == b);
            }
        }
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 553))

    def test_54(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Var a,b,c,d: Int = 1 + 2 * 3, (1 +2) * 3, 1 + 2, 1 + 2;
                io.writeBool(a > b);
            }
        }
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 554))



    def test_55(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Var a,b,c,d: Int = 1 + 2 * 3, (1 +2) * 3, 1 + 2, 1 + 2;
                io.writeBool(a >= b);
            }
        }
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 555))

    def test_56(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Var a,b,c,d: Int = 1 + 2 * 3, (1 +2) * 3, 1 + 2, 1 + 2;
                io.writeBool(a <= b);
            }
        }
        """
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 556))

    def test_57(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Var a,b,c,d: Int = 1 + 2 * 3, (1 +2) * 3, 1 + 2, 1 + 2;
                io.writeBool(a >= b);
            }
        }
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 557))

    # Coercion: Float -> Int
    def test_58(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val b: Int = 1 - 1;
                
                io.writeInt(b);
            }
        }
        """
        expect = "0"
        self.assertTrue(TestCodeGen.test(input, expect, 558))

    def test_59(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Var a,b,c,d: Int = 1 + 2 * 3, (1 +2) * 3, 1 + 2, 1 + 2;
                io.writeBool(a < b);
            }
        }
        """
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 559))

    def test_60(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Var a: Float = 1.0 * 2.0 - 1.0;
                Val b: Float = 1* 8 +(-12) * 12 + 1 + 1 - (1);
                io.writeFloat(a + b * a);
            }
        }
        """
        expect = "-134.0"
        self.assertTrue(TestCodeGen.test(input, expect, 560))

    ### CUT: 61->90
    def test_61(self):
        input = """
        Class Program {
            main(){
                io.writeInt(100);
            }
        }
        """
        expect = "100"
        self.assertTrue(TestCodeGen.test(input, expect, 561))

    # Negative case writeInt
    def test_62(self):
        input = """
        Class Program {
            main(){
                io.writeInt(-1);
            }
        }
        """
        expect = "-1"
        self.assertTrue(TestCodeGen.test(input, expect, 562))

    # Negative + big number
    def test_63(self):
        input = """
        Class Program {
            main(){
                io.writeInt(-100);
            }
        }
        """
        expect = "-100"
        self.assertTrue(TestCodeGen.test(input, expect, 563))

    # 2 Class
    def test_64(self):
        input = """
        Class A {}
        Class Program {
            main(){}
        }
        """
        expect = ""
        self.assertTrue(TestCodeGen.test(input, expect, 564))

    # Inheritance
    def test_65(self):
        input = """
        Class B {}
        Class C:B {}
        Class Program {
            main(){}
        }
        """
        expect = ""
        self.assertTrue(TestCodeGen.test(input, expect, 565))

    def test_66(self):
        input = """
        Class A {}
        Class B:A {}
        Class C:B {}
        Class Program {
            main(){}
        }
        """
        expect = ""
        self.assertTrue(TestCodeGen.test(input, expect, 566))
    
    # StoreDecl
    # VarDecl
    def test_67(self):
        input = """
        Class Program {
            main(){
                Var a: Int = 12;
                io.writeInt(a);
            }
        }
        """
        expect = "12"
        self.assertTrue(TestCodeGen.test(input, expect, 567))

    def test_68(self):
        input = """
        Class Program {
            main(){
                Val a: Int = 1;
                io.writeInt(a);
            }
        }
        """
        expect = "1"
        self.assertTrue(TestCodeGen.test(input, expect, 568))

    # Binop
    def test_69(self):
        input = """
        Class Shape{
            abc(a: Float){
                Return a;
            }
            cde(c: String){
                Return;
            }
            sdd(d: Boolean){
                Return d;
            }
        }
        Class Program {
            main(){
                Val a : Int = 12;
                io.writeInt(a);
            }
        }
        """
        expect = "12"
        self.assertTrue(TestCodeGen.test(input, expect, 569))

    def test_70(self):
        input = """
        Class Shape{
            abc(a: Float){
                Return 2;
            }
        }
        Class Program {
            main(){
                io.writeInt(1+2);
            }
        }
        """
        expect = "3"
        self.assertTrue(TestCodeGen.test(input, expect, 570))

    def test_71(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: Int = 12;
                io.writeInt(a);
            }
        }
        """
        expect = "12"
        self.assertTrue(TestCodeGen.test(input, expect, 571))

    # Write multitype
    def test_72(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: Float = 12;
                io.writeFloat(a);
            }
        }
        """
        expect = "12.0"
        self.assertTrue(TestCodeGen.test(input, expect, 572))

    def test_73(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: Boolean = True;
                io.writeBool(a);
            }
        }
        """
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 573))

    def test_74(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: String = "H";
                io.writeStr(a);
            }
        }
        """
        expect = "H"
        self.assertTrue(TestCodeGen.test(input, expect, 574))

    def test_75(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: String = "Hello world. My name is Quach Minh Tuan. Welcome to the biggest party";
                io.writeStr(a);
            }
        }
        """
        expect = "Hello world. My name is Quach Minh Tuan. Welcome to the biggest party"
        self.assertTrue(TestCodeGen.test(input, expect, 575))

    def test_76(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: Boolean = False;
                io.writeBool(a);
            }
        }
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 576))

    def test_77(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: Boolean = False;
                io.writeBool(!a);
            }
        }
        """
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 577))

    def test_78(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: Boolean = False;
                Var b: Boolean = False;
                io.writeBool(a && b);
            }
        }
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 578))

    def test_79(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: Boolean = False;
                Var b: Boolean = False;
                io.putBool(a || b);
            }
        }
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 579))


    # Short circuit
    def test_80(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: Boolean = False;
                Var b,d,e: Boolean = False, True, False;
                io.writeBool(a || b || d || e);
            }
        }
        """
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 580))

    def test_81(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: Boolean = True;
                Var b,d,e: Boolean = False, True, False;
                io.writeBool(a || b || d || e);
            }
        }
        """
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 581))

    # Relational
    def test_82(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Var a,b,c,d: Int = 1 + 2, 1 + 2, 1 + 2, 1 + 2;
                io.writeBool(a == b);
            }
        }
        """
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 582))

    def test_83(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Var a,b,c,d: Int = 1 + 2 * 3, (1 +2) * 3, 1 + 2, 1 + 2;
                io.writeBool(a == b);
            }
        }
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 583))

    def test_84(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Var a,b,c,d: Int = 1 + 2 * 3, (1 +2) * 3, 1 + 2, 1 + 2;
                io.writeBool(a > b);
            }
        }
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 584))



    def test_85(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Var a,b,c,d: Int = 1 + 2 * 3, (1 +2) * 3, 1 + 2, 1 + 2;
                io.writeBool(a >= b);
            }
        }
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 585))

    def test_86(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Var a,b,c,d: Int = 1 + 2 * 3, (1 +2) * 3, 1 + 2, 1 + 2;
                io.writeBool(a <= b);
            }
        }
        """
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 586))

    def test_87(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Var a,b,c,d: Int = 1 + 2 * 3, (1 +2) * 3, 1 + 2, 1 + 2;
                io.writeBool(a >= b);
            }
        }
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 587))

    # Coercion: Float -> Int
    def test_88(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val b: Int = 1 - 1;
                
                io.writeInt(b);
            }
        }
        """
        expect = "0"
        self.assertTrue(TestCodeGen.test(input, expect, 588))

    def test_89(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Var a,b,c,d: Int = 1 + 2 * 3, (1 +2) * 3, 1 + 2, 1 + 2;
                io.writeBool(a < b);
            }
        }
        """
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 589))

    def test_90(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Var a: Float = 1.0 * 2.0 - 1.0;
                Val b: Float = 1* 8 +(-12) * 12 + 1 + 1 - (1);
                io.writeFloat(a + b * a);
            }
        }
        """
        expect = "-134.0"
        self.assertTrue(TestCodeGen.test(input, expect, 590))


    def test_91(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val a: Boolean = True;
                Var b,d,e: Boolean = False, True, False;
                io.writeBool(a || b || d || e);
            }
        }
        """
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 591))

    # Relational
    def test_92(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Var a,b,c,d: Int = 1 + 2, 1 + 2, 1 + 2, 1 + 2;
                io.writeBool(a == b);
            }
        }
        """
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 592))

    def test_93(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Var a,b,c,d: Int = 1 + 2 * 3, (1 +2) * 3, 1 + 2, 1 + 2;
                io.writeBool(a == b);
            }
        }
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 593))

    def test_94(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Var a,b,c,d: Int = 1 + 2 * 3, (1 +2) * 3, 1 + 2, 1 + 2;
                io.writeBool(a > b);
            }
        }
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 594))



    def test_95(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Var a,b,c,d: Int = 1 + 2 * 3, (1 +2) * 3, 1 + 2, 1 + 2;
                io.writeBool(a >= b);
            }
        }
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 595))

    def test_96(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Var a,b,c,d: Int = 1 + 2 * 3, (1 +2) * 3, 1 + 2, 1 + 2;
                io.writeBool(a <= b);
            }
        }
        """
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 596))

    def test_97(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Var a,b,c,d: Int = 1 + 2 * 3, (1 +2) * 3, 1 + 2, 1 + 2;
                io.writeBool(a >= b);
            }
        }
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 597))

    # Coercion: Float -> Int
    def test_98(self):
        input = """
        Class B{}
            Class A: B{
                Val a: Int = 12;
                $a(a: String){Return a;}
            }  
        Class Program {
            main(){
                Val b: Int = 1 - 1;
                
                io.writeInt(b);
            }
        }
        """
        expect = "0"
        self.assertTrue(TestCodeGen.test(input, expect, 598))

    def test_99(self):
        input = """
        Class Program {
            main(){
                io.writeInt(12);
            }
        }
        """
        expect = "12"
        self.assertTrue(TestCodeGen.test(input, expect, 599))


    # # 1 param, many param, 1 function, many function
    # # params + diff method
    # # Constructor