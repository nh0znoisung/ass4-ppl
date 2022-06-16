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
.var 1 is a Z from Label0 to Label1
	iconst_1
	istore_1
.var 2 is b Z from Label0 to Label1
	iconst_0
	istore_2
.var 3 is d Z from Label0 to Label1
	iconst_1
	istore_3
.var 4 is e Z from Label0 to Label1
	iconst_0
	istore 4
	iload_1
	iload_2
	ior
	iload_3
	ior
	iload 4
	ior
	invokestatic io/putBool(Z)V
Label1:
	return
.limit stack 6
.limit locals 5
.end method

.method public static <clinit>()V
	return
.limit stack 0
.limit locals 0
.end method
