grammar D96;

// Student ID: 1910663
@lexer::header {
# Student ID: 1910663
from lexererr import *
}

options {
	language = Python3;
}

// Lexer
////////////////////////////////////////

IMMUTABLE: 'Val'; //constant
MUTABLE: 'Var'; //variable
BOOLTYPE: 'Boolean';
INTTYPE: 'Int';
FLOATTYPE: 'Float';
STRINGTYPE: 'String';

TRUE: 'True';
FALSE: 'False';

NULL: 'Null';
NEW: 'New';
SELF: 'Self';

DOT: '.';
DOUBLECOLON: '::';
COLON: ':';

LC: '[';
RC: ']';

// 6. Separator (9 items)
// SEPARATOR: '['|RC;
LB: '(';
RB: ')';
LP: '{';
RP: '}';
SEMI: ';';
COMMA: ',';

CONSTRUCTOR: 'Constructor';
DESTRUCTOR: 'Destructor';

// 4.KeyWord (23 items) (from top to bottom and left to right)
KEYWORD: 'Break'|'Foreach'|'Continue'|'If'|'Elseif'|'By'|'Else'|'In'|'Return'; 


// 1. Charset
WS: [ \t\b\f\r\n]+ -> skip; // skip spaces, tabs, newlines

// 2.Comment
BLOCK_COMMENT: '##' .*? '##' -> skip;// Return 0 token || Or <EOF>, Not ##

// 3.Identifier
ID: [a-zA-Z_][a-zA-Z_0-9]*; //may contain
DOLLARID: '$'[a-zA-Z_0-9]+; //non-empty



// 5.Operator (20 items) (from top to bottom and left to right)
OPERATOR: '..'|'+'|'!'|'!='|'==.'|'-'|'&&'|'<'|'+.'|'*'|'||'|'<='|'/'|'=='|'>'|'%'|'='|'>='; // New is overlap



// 7. Literal 
// 7.1.Integer base 10, 16,8,2 + Underscores between digits
fragment INT10GROUP: [0-9]+;
fragment INT10GROUP1: [1-9][0-9]*;
INT10LOWERBOUND: (INT10GROUP1| ((INT10GROUP1)('_' INT10GROUP)*)) {self.text=self.text.replace('_',"");};

fragment INT8GROUP: [0-7]+;
fragment INT8GROUP1: [1-7][0-7]*;
INT8LOWERBOUND: '0'(INT8GROUP1 | ((INT8GROUP1)('_' INT8GROUP)*)) {self.text=self.text.replace('_',"");};

fragment INT16GROUP: [0-9A-F]+; //A-F Uppercase
fragment INT16GROUP1: [1-9A-F][0-9A-F]*;
INT16LOWERBOUND: '0'[xX](INT16GROUP1 | ((INT16GROUP1)('_' INT16GROUP)*)) {self.text=self.text.replace('_',"");};

fragment INT2GROUP: [0-1]+;
fragment INT2GROUP1: '1'[0-1]*;
INT2LOWERBOUND: '0'[bB](INT2GROUP1 | ((INT2GROUP1)('_' INT2GROUP)*)) {self.text=self.text.replace('_',"");};

INT0: '00'|'0'|'0'[bB]'0'|'0'[xX]'0';

// 7.2.Float   Only one can be absent
fragment INTPART: INT10LOWERBOUND | '0';
fragment DECPART: '.' [0-9]*; // [0-9]*
fragment EXPPART: [eE] ('-'|'+')? [0-9]+; //not empty
FLOAT: (INTPART DECPART EXPPART | INTPART DECPART | INTPART EXPPART | DECPART EXPPART)  {self.text=self.text.replace('_',"");};

// 7.4.String
fragment CHARACTER: ('\\' [bfrnt'\\] | ~[\n"\r\b\f\t\\] | '\'"' ); 
STRING: '"' CHARACTER* '"'{self.text = self.text[1: -1];}; 





/////////////////////////////// Syntax
program: class_decls EOF;	 //many class declaration

class_decls: class_decl+;

// 2. Class declaration
class_decl: 'Class' ID parent? LP class_body RP; 
parent: COLON ID;
class_body: class_member*; // nullable list of members => *

class_member:  attribute_decl | method_decl;
member: ID | DOLLARID; 


attribute_decl: (IMMUTABLE | MUTABLE) attr_list  COLON typedecl SEMI 
			| (IMMUTABLE | MUTABLE)  attr_equal SEMI 
			;
attr_equal: member COMMA attr_equal COMMA expr| member (COLON typedecl '=') expr;
attr_list: member (COMMA member)*; //non-null, commma
expr_list: expr (COMMA expr)*; //non-null, commma


// Method declaration
method_decl: normal | special;
normal: member LB method_params RB block_statement; //Name is ID and canbe Static
method_params: (param_decl (SEMI param_decl)*)?; //nullable, semi-colon

param_decl: id_list COLON typedecl; 
id_list: ID (COMMA ID)*; //non-null identifiers, commma


block_statement: LP state_list RP;
state_list: statement*; //nullable


special: constructor | destructor;
// Constructor declaration
constructor: CONSTRUCTOR '(' method_params ')' block_constructor;
block_constructor: '{' state_list '}'; // Return nothing 
// Destructor declaration
destructor: DESTRUCTOR '(' ')' block_destructor;
block_destructor: '{' state_list '}'; // No return statement



// 4. Type and value
typedecl: array_type | class_type | BOOLTYPE | INTTYPE | FLOATTYPE | STRINGTYPE ; //type keyword
array_type: 'Array' LC primitive_type ',' intlitlowerbound RC ; 
primitive_type: BOOLTYPE | INTTYPE | FLOATTYPE | STRINGTYPE | array_type; //type array keyword
// Lowerbound = 1
intlitlowerbound: INT10LOWERBOUND | INT8LOWERBOUND | INT16LOWERBOUND | INT2LOWERBOUND;
class_type: ID; // name of class is ID



// Value of type/operand
bool_value: TRUE | FALSE;
int_value: INT10LOWERBOUND | INT16LOWERBOUND | INT8LOWERBOUND | INT2LOWERBOUND | INT0; 
float_value: FLOAT; 
string_value: STRING; 
class_value: NULL | NEW class_type '(' ')';
array_value: 'Array' '(' expr_list ')'; //indexed array, non-null
muldim_array: 'Array' '(' muldim_array (COMMA muldim_array)* ')' | array_type; //non-null, commma.. NO AST

operand: bool_value | int_value | float_value | string_value | class_value | array_value;



// 5. Expression


// 5.6: Member access
instance_attr_access: expr DOT ID; 
static_attr_access: ID DOUBLECOLON DOLLARID; 
instance_method_access: expr DOT ID '(' (expr_list)? ')'; 
static_method_access: ID DOUBLECOLON DOLLARID '(' (expr_list)? ')'; 

// 5.7: Object creation
object_creation: NEW class_type '(' (expr_list)? ')'; //Nullable


// 5.9 Expression ranking: Highest -> Lowest
expr : LB expr RB
	| NEW ID LB (expr_list)? RB
	| static_attr_access
	| static_method_access
	| expr DOT ID (LB (expr_list)? RB)?
	| expr (LC expr RC)+
	| ('-') expr
	| ('!') expr
	| expr ('*' | '/' | '%') expr
	| expr ('+' | '-') expr
	| expr ('&&' | '||') expr
	| expr ('==' | '!=' | '<' | '>' | '<=' | '>=') expr
	| expr ('+.' | '==.') expr
	| operand
	| ID
	| DOLLARID
	| SELF
	| NULL;

// 5.5: Index operators
// element_expr: expr index_operator;
// index_operator: LC expr RC | (LC expr RC) index_operator;

//6. Statement 
scalar_type: ID | DOLLARID; //scalar variable

statement: varconst_decl | ass | ifstmt | forstmt | breakstmt | continuestmt | retu | method_invoke | block_statement; 
varconst_decl: (IMMUTABLE | MUTABLE) attrId_list  COLON typedecl SEMI 
			| (IMMUTABLE | MUTABLE)  attrId_equal SEMI 
			;
attrId_equal: ID COMMA attr_equal COMMA expr| ID (COLON typedecl '=') expr;
attrId_list: ID (COMMA ID)*; //non-null, commma

// ??? index op: expr[expr]: expr(0) = a[1][2]
ass : expr '=' expr ';'; 
// (scalar_type | element_expr | static_attr_access | instance_attr_access)

ifstmt: if_stmt (elseif_stmt)* (else_stmt)?; 
if_stmt: 'If' '(' expr ')' block_statement;
elseif_stmt: 'Elseif' '(' expr ')' block_statement;
else_stmt: 'Else'  block_statement;

forstmt: 'Foreach' '(' scalar_type 'In' expr '..' expr ('By' expr)? ')' block_statement; 

breakstmt: 'Break' ';';
continuestmt: 'Continue' ';';
retu : 'Return' (expr)? ';';//expr is optional
method_invoke: (static_method_access | instance_method_access) ';'; 



// Semantic analysis Task:
// + Check indexed array with same type
// + Run entry program function main() in class Program
// + Type with operator + Cast type
// + Scope


fragment NOTCHARACTER: '\\' ~[bfrnt'\\] | '\\'; 
UNCLOSE_STRING: ('"' CHARACTER* ([\n\r\b\f\t\\]|EOF)) //EOF is not in CHARACTER
	{
		if self.text[-1] in ['\n', '\r', '\b', '\f', '\t', '\\']:
			raise UncloseString(self.text[1:-1])
		else:
			raise UncloseString(self.text[1:])
	};
ILLEGAL_ESCAPE: ('"' CHARACTER* NOTCHARACTER) {raise IllegalEscape(self.text[1:])};
ERROR_CHAR: . {raise ErrorToken(self.text)};