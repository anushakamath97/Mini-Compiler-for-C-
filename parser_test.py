# Yacc example
import copy
import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lex import tokens

import TAC as TAC

threeAC = TAC.threeAC()

# def p_relationalExpression(p):
# 	'''relationalExpression : shiftExpression
# 			| relationalExpression LT shiftExpression
# 			| relationalExpression GT shiftExpression
# 			| relationalExpression LTEQ shiftExpression
# 			| relationalExpression GTEQ shiftExpression'''
# 	if(len(p)==2):
# 		p[0]=p[1]
# 	else:
# 		p[0] = AST.Expr("binop",operator=p[2],operand1=p[1],operand2=p[3])
			
# def p_shiftExpression(p):
# 	'''shiftExpression : additiveExpression
# 			| shiftExpression LSHIFT additiveExpression
# 			| shiftExpression RSHIFT additiveExpression'''
# 	if(len(p)==2):
# 		p[0]=p[1]
			
# def p_additiveExpression(p):
# 	'''additiveExpression : multiplicativeExpression
# 			| additiveExpression U_PLUS multiplicativeExpression
# 			| additiveExpression U_MINUS multiplicativeExpression'''
# 	if(len(p)==2):
# 		p[0]=p[1]
			
# def p_multiplicativeExpression(p):
# 	'''multiplicativeExpression : castExpression
# 			| multiplicativeExpression TIMES castExpression
# 			| multiplicativeExpression DIVIDE castExpression
# 			| multiplicativeExpression MOD castExpression'''


def p_assignment(p):
	'''assignment : ID ASSIGNMENT  expr 
			| expr 
			| empty '''
	if(len(p)==4):
		if(p[2] == '='):
			threeAC.AddToTable(p[1],p[3],'=')

def p_mark(p):
	'''mark : empty'''
	print(p[-1])

def p_expr(p):
	'''expr : expr U_PLUS expr 
			| expr U_MINUS expr
			| expr TIMES expr 
			| expr DIVIDE expr 
			| LPAREN expr RPAREN 
			| INTNUM
			| ID  '''

	if(len(p)==4):
		if p[2] == '+':
			p[0]=threeAC.AddToTable(p[1],p[3],'+')
		elif p[2] == '-':
			p[0]=threeAC.AddToTable(p[1],p[3],'-')
		elif p[2] == '*':
			p[0]=threeAC.AddToTable(p[1],p[3],'*')	
		elif p[2] == '/':
			p[0]=threeAC.AddToTable(p[1],p[3],'/')
		elif (p[1] == '(' and p[3] == ')'):
			p[0]=p[2]
	elif len(p) == 2:
		p[0] = p[1]

def p_empty(p):
    'empty :'
    pass

parser = yacc.yacc()
s=open('test.txt','r').read()
result = parser.parse(s)
print("Expression : " + s )
threeAC.ThreeAddressCode()
