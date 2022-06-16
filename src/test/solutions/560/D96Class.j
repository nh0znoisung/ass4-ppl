.source D96Class.java
.class public D96Class
.super java.lang.Object

.method public <init>()V
.var 0 is this LD96Class; from Label0 to Label1
Label0:
	aload_0
	invokespecial java/lang/Object/<init>()V
Label1:
	return
.limit stack 1
.limit locals 1
.end method

.method public static main([Ljava/lang/String;)V
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label0:
.var 1 is a F from Label0 to Label1
	fconst_1
	fconst_2
	fmul
	fconst_1
	fsub
	fstore_1
.var 2 is b F from Label0 to Label1
	iconst_1
	bipush 8
	imul
	bipush 12
	ineg
	bipush 12
	imul
	iadd
	iconst_1
	iadd
	iconst_1
	iadd
	iconst_1
	isub
	i2f
	fstore_2
	fload_1
	fload_2
	fload_1
	fmul
	fadd
	invokestatic io/putFloat(F)V
Label1:
	return
.limit stack 3
.limit locals 3
.end method

.method public static <clinit>()V
	return
.limit stack 0
.limit locals 0
.end method
