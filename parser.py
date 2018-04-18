# Yacc example
import copy
import ply.yacc as yacc
import AST

# Get the token map from the lexer.  This is required.
from lex import tokens
from lex import main_table

import sys

from symbolTable import SymbolTable

dec=0

import warnings
warnings.filterwarnings("ignore")





#def p_preProc(p):
#	'''preProc : HASH INCLUDE LT identifier GT stdNamespace '''
	
#def p_stdNamespace(p):
#	'''stdNamespace : USING NAMESPACE STD TERMINAL mainFunc '''

#main function
def p_mainFunc(p):
	'''mainFunc : INT MAIN LPAREN RPAREN statement '''	
	p[0] = p[5]

def p_expression(p):
	'''expression : assignmentExpression
               		| expression COMMA assignmentExpression'''
	if(len(p)==2):
		p[0]=p[1]

def p_assignmentExpression(p):
	'''assignmentExpression : conditionalExpression
				| unaryExpression assignOper assignmentExpression'''
	if(len(p)==2):
		p[0]=p[1]
	else:
		if(p[1].type=="char" || p[3].type=="char"):
			print "Error! Cannot perform operation on character datatype!"
		elif (p[1].type==p[3].type):
			if (p[1].type=="int"):
				p[0].type=="int"
			else:
				p[0].type=="float"
		elif (p[1].type!=p[3].type):
			print "Datatype mismatch, performing coercion!"
			#mismatch has to mean int and float, hence coercion to float
			p[0].type=="float"
		p[0] = AST.Expr("binop",operator=p[2],operand1=p[1],operand2=p[3])

def p_unaryExpression(p):
	'''unaryExpression : postfixExpression 
			| PLUSPLUS unaryExpression
			| MINUSMINUS unaryExpression
			| unaryOper unaryExpression
			| SIZEOF unaryExpression
			| SIZEOF LPAREN simpleTypeName RPAREN '''
	if(len(p)==2):
		p[0]=p[1]
	elif len(p) == 3:
		p[0] = AST.Expr("unPreOp",operator=p[1],operand1=p[2])
	else:
		p[0] = AST.Expr("unaryop",operator=p[1],operand1=p[3])

def p_primaryExpression(p):
	'''primaryExpression : identifier
                       | constant
                       | STRING
                       | LPAREN expression RPAREN '''
	if(len(p)==2):
		if(isinstance(p[1],AST.Identifier)):
			p[0] = AST.Expr("id",operand1=p[1])
		else:	#constant or string
			p[0]  = AST.Expr("constant",operand1=p[1])
	else:
		p[0]=p[2]
	#have to write for others

def p_postfixExpression(p):
	'''postfixExpression : primaryExpression
			| postfixExpression LEFTSQRBRACKET expression RIGHTSQRBRACKET
			| postfixExpression PLUSPLUS
			| postfixExpression MINUSMINUS'''
			#| DYNAMIC_CAST LT simpleTypeName GT LPAREN expression RPAREN 
			#| STATIC_CAST LT simpleTypeName GT LPAREN expression RPAREN
			#| CONST_CAST LT simpleTypeName GT LPAREN expression RPAREN 
			#| postfixExpression DEREF_ONE identifier
			#| postfixExpression DEREF_TWO identifier
	if(len(p)==2):
		p[0]=p[1]
	elif len(p)==5:
		p[0] = AST.Expr("arrayop",operator='[]',operand1=p[1],operand2=p[3])
	else:
		p[0] = AST.Expr("unPostOp",operator=p[2],operand1=p[1])

def p_constant(p):
	'''constant : INTNUM
		| FLOATNUM
		| CHAR_CONST'''
	p[0] = AST.Expr("constant",operand1=p[1])

def p_assignOper(p):
	'''assignOper : ASSIGNMENT
			| MULT_EQ
			 |  DIVIDE_EQ
			 | MOD_EQ
			 | PLUS_EQ 
			 | MINUS_EQ
			 | GTEQ
			 | LTEQ
			 | AND_EQ
			 | XOR_EQ
			 | OR_EQ '''
	p[0]=p[1]

def p_conditionalExpression(p):
	'''conditionalExpression : logicalOrExpression 
                          | logicalOrExpression QUES_MARK expression COLON conditionalExpression''' #need to implement
	if(len(p)==2):
		p[0]=p[1]
	
def p_logicalOrExpression(p):
	'''logicalOrExpression : logicalAndExpression 
				| logicalOrExpression  OR   logicalAndExpression'''
	if(len(p)==2):
		p[0]=p[1]
	else:
		p[0] = AST.Expr("binop",operator=p[2],operand1=p[1],operand2=p[3])

def p_logicalAndExpression(p):
	'''logicalAndExpression : inclusiveOrExpression 
				| logicalAndExpression  AND   inclusiveOrExpression'''	
	if(len(p)==2):
		p[0]=p[1]
	else:
		p[0] = AST.Expr("binop",operator=p[2],operand1=p[1],operand2=p[3])

def p_inclusiveOrExpression(p):
	'''inclusiveOrExpression : exclusiveOrExpression 
			| inclusiveOrExpression BIT_OR exclusiveOrExpression'''
	if(len(p)==2):
		p[0]=p[1]
	else:
		p[0] = AST.Expr("binop",operator=p[2],operand1=p[1],operand2=p[3])

def p_exclusiveOrExpression(p):
	'''exclusiveOrExpression : andExpression 
			| exclusiveOrExpression BIT_XOR andExpression'''
	if(len(p)==2):
		p[0]=p[1]
	else:
		p[0] = AST.Expr("binop",operator=p[2],operand1=p[1],operand2=p[3])

def p_andExpression(p):
	'''andExpression : equalityExpression 
			| andExpression BIT_AND equalityExpression'''
	if(len(p)==2):
		p[0]=p[1]
	else:
		p[0] = AST.Expr("binop",operator=p[2],operand1=p[1],operand2=p[3])

def p_equalityExpression(p):
	'''equalityExpression : relationalExpression 
			| equalityExpression EQUAL relationalExpression
			| equalityExpression NEQUAL relationalExpression'''
	if(len(p)==2):
		p[0]=p[1]
	else:
		p[0] = AST.Expr("binop",operator=p[2],operand1=p[1],operand2=p[3])
			
def p_relationalExpression(p):
	'''relationalExpression : shiftExpression
			| relationalExpression LT shiftExpression
			| relationalExpression GT shiftExpression
			| relationalExpression LTEQ shiftExpression
			| relationalExpression GTEQ shiftExpression'''
	if(len(p)==2):
		p[0]=p[1]
	else:
		p[0] = AST.Expr("binop",operator=p[2],operand1=p[1],operand2=p[3])
			
def p_shiftExpression(p):
	'''shiftExpression : additiveExpression
			| shiftExpression LSHIFT additiveExpression
			| shiftExpression RSHIFT additiveExpression'''
	if(len(p)==2):
		p[0]=p[1]
	else:
		p[0] = AST.Expr("binop",operator=p[2],operand1=p[1],operand2=p[3])
			
def p_additiveExpression(p):
	'''additiveExpression : multiplicativeExpression
			| additiveExpression U_PLUS multiplicativeExpression
			| additiveExpression U_MINUS multiplicativeExpression'''
	if(len(p)==2):
		p[0]=p[1]
			
def p_multiplicativeExpression(p):
	'''multiplicativeExpression : castExpression
			| multiplicativeExpression TIMES castExpression
			| multiplicativeExpression DIVIDE castExpression
			| multiplicativeExpression MOD castExpression'''
	if(len(p)==2):
		p[0]=p[1]
	else:
		p[0] = AST.Expr("binop",operator=p[2],operand1=p[1],operand2=p[3])

def p_castExpression(p):
	'''castExpression : unaryExpression
			| LPAREN simpleTypeName RPAREN castExpression'''
	if(len(p)==2):
		p[0]=p[1]

def p_unaryOper(p):
	'''unaryOper : TIMES
			| BIT_AND
			| U_PLUS
			| U_MINUS
			| NOT
			| BIT_NOT'''
	p[0]=p[1]
		
def p_simpleTypeName(p):
	'''simpleTypeName : CHAR
			| SHORT
			| INT
			| LONG
			| SIGNED
			| UNSIGNED
			| FLOAT
			| DOUBLE
			| VOID'''
	#p[0] = {'type':p[1]}
	p[0] = AST.Type(p[1])
			
#empty production used in optional cases		

def p_empty(p):
    'empty :'
    pass
    
			
def p_statement(p):
	'''statement : labeledStatement
			| expressionStatement
			| compoundStatement
			| selectionStatement
			| jumpStatement'''	#| iterationStatement
	p[0] = p[1]
	
			
def p_labeledStatement(p):
	'''labeledStatement : identifier COLON statement
			| caseList default '''
	if len(p) == 3:
		p[0] = AST.CaseList(p[1], p[2])

def p_caseList(p):
	'''caseList : caseList CASE constantExpression COLON statement
		| empty'''
	if len(p) == 6:
		p[1].add_case(p[3], p[5])
		p[0] = p[1]
	else:
        	p[0] = AST.Case()

def p_default(p):
	'''default : DEFAULT COLON statement	
		| empty '''
	if(len(p)==4):
		p[0] = AST.CaseDefault(p[3])
	else:
		p[0]=None
			
def p_constantExpression(p):
	'''constantExpression : conditionalExpression '''
	p[0]=p[1]

def p_expressionStatement(p):
	'''expressionStatement : expression TERMINAL
			| empty'''
	if len(p)==3:
		p[0] = p[1]
	else:
		p[0] = None
			
def p_compoundStatement(p):
	'''compoundStatement : oscope declarationList statementList cscope
			| empty'''
	if len(p) == 5:
		if len(p[2].declarations) != 0:
			p[0] = AST.CompoundStmt(p[3], p[2])
		else:	
			p[0] = AST.CompoundStmt(p[3])
	else:
		p[0] = None

def p_oscope(p):
	'''oscope : LEFTCURLYBRACKET'''
	main_table.inScope=main_table.prev_inScope+1
	main_table.prev_inScope+=1
	main_table.outScope+=1
	tab = SymbolTable()
	main_table.add_table(tab)
		
def p_cscope(p):
	'''cscope : RIGHTCURLYBRACKET'''
	main_table.inScope-=1
	main_table.outScope-=1											
	
def p_statementList(p):
	'''statementList : statementList statement
			| empty '''
	if len(p) == 3:
		p[1].add_stmt(p[2])
		p[0] = p[1]
	else:
		p[0] = AST.StmtList()

def p_declarationList(p):
	'''declarationList : declarationList declaration
			| empty '''
	if len(p) == 2:
		p[0] = AST.DecList()
	else:
        	p[1].add_decl(p[2])
        	p[0] = p[1]

def p_declaration(p):
	'''declaration :  decSpecList initDecList TERMINAL '''
	global dec	
	dec = 0
	main_table.insert = 0
	p[0] = AST.Declaration(p[1], p[2])

def p_initDecList(p):
	'''initDecList : initDecList COMMA markDec initDec
			| initDec '''
	if len(p)==2:
		p[0] = AST.IdentList([p[1]])
	else:
		p[1].add_identifier(p[4])
		p[0] = p[1]
	

def p_markDec(p):
	'''markDec : empty '''
	p[0] = p[-3]

def p_decSpecList(p):
	'''decSpecList : decSpecList decSpec
			| decSpec '''
	if(len(p)==2):
		p[0] = p[1]
	else:
		p[0] = p[1].combine(p[2].type)
	global dec
	dec=1
	main_table.insert=1

def p_initDec(p):
	''' initDec : declarator
                    | declarator ASSIGNMENT assignmentExpression'''	
	if len(p)==4:
		p[1].add_value(p[3])
	p[0] = p[1]

def p_declarator(p):
	'''declarator : pointerList directDec'''
	p[0] = p[2]

def p_pointerList(p):
	''' pointerList : pointer
			| empty '''
	if (p[1] != None):
		p[0] = p[1]

def p_pointer(p):
	'''pointer : star typeQualList
		| empty	'''
	if(len(p)==3):
		p[0] = { 'type': p[1]['type'] + p[2]['type'] }	

def p_star(p):
	'''star : star TIMES
		| TIMES	'''
	if(len(p)==2):
		p[0]={'type':'*'}
	else:
		p[0] = p[1]
		p[0]['type']+='*'

def p_typeQualList(p):
	''' typeQualList : typeQualifier
			| empty '''
	if(p[1] != None):
		p[0] = p[1]
	else:
		p[0] = {'type':''}

def p_directDec(p):
	'''directDec : identifier
                      | identifier arrayDec'''
		      #| LEFTCURLYBRACKET declarator RIGHTCURLYBRACKET
                      #| directDec LEFTCURLYBRACKET idList RIGHTCURLYBRACKET
		      #| directDec LPAREN parTypeList RPAREN 
	if(len(p)==3):
		symbol_table = main_table.get_table(main_table.inScope-1)
		p[1].changeToArray(p[2]['val'])
		symbol_table.change_array(p[2]['val'])
	p[0]=p[1]

def p_arrayDec(p): #constExprList
	'''arrayDec : arrayDec LEFTSQRBRACKET INTNUM RIGHTSQRBRACKET	
		| LEFTSQRBRACKET INTNUM RIGHTSQRBRACKET	'''
	if(len(p)==4):
		p[0] = {'val': [int(p[2]),]}
	else:
		p[1]['val'].append(int(p[3]))
		p[0] = p[1]
	

def p_identifier(p):
	'''identifier : ID'''
	symbol_table = main_table.get_table(main_table.inScope-1)
	if(dec==1):
		ret = symbol_table.check_existing(p[1])
		if ret ==-1:
			print("Redeclaration of variable:",p[1])
			sys.exit()	
		elif(p[-1] is None):
			p[0] = AST.Identifier(p[1],idtype = p[-2].type)
			symbol_table.add_type(p[-2].type)
		else:
			p[0] = AST.Identifier(p[1],idtype = p[-2].type+p[-1]['type'])
			symbol_table.add_type(p[-2].type+p[-1]['type'])
	else:
		#return sym table entry
		symbol_table.check_existing(p[1])
		p[0] = AST.Identifier(p[1])
	#remember while adding to symbol table make changes in directDec for array type

def p_decSpec(p):
	'''decSpec : StorageClassSpec
                          | simpleTypeName
                          | typeQualifier '''
	p[0] = p[1]

def p_typeQualifier(p):
	''' typeQualifier : CONST
			  | VOLATILE '''
	p[0] = AST.Type(p[1])

def p_StorageClassSpec(p):
	'''StorageClassSpec : AUTO
                            | REGISTER
                            | STATIC
                            | EXTERN
                            | TYPEDEF '''
	p[0] = AST.Type(p[1])
			
def p_selectionStatement(p):
	'''selectionStatement : IF LPAREN expression RPAREN statement
			| IF LPAREN expression RPAREN statement ELSE statement
			| SWITCH LPAREN expression RPAREN statement'''
	if len(p)==8:
		p[0] = AST.IfStmt(p[3], p[5], p[7])
	elif len(p) == 6:
		if (p[1] == "if"):
			p[0] = AST.IfStmt(p[3], p[5])
		else:
			p[0] = AST.SwitchStmt(p[3], p[5])

		
def p_jumpStatement(p):
	'''jumpStatement : BREAK TERMINAL
			| CONTINUE TERMINAL
			| RETURN expression TERMINAL
			| RETURN TERMINAL
			| GOTO identifier TERMINAL'''
	if(p[1]=="break"):
		p[0]=AST.JumpStmt()
	elif(p[1]=="continue"):
		p[0]=AST.JumpStmt("continue")
	elif p[1] == "return":
		if len(p)==4:
			p[0] = AST.RetStmt(p[2])
		else:
			p[0] = AST.RetStmt()

# Error rule for syntax errorscl
def p_error(p):
    if p is not None:
       print("Syntax error in input\n error: near",p.value,"at line:",p.lineno)
	

# 	Build the parser
parser = yacc.yacc()

s=open('cpp_code.cpp','r').read()
result = parser.parse(s)
if result is not None:
	with open("AST.txt",'w') as f:
		f.write(str(result))

main_table.print_table()
