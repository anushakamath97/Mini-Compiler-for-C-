# Yacc example
import copy
import ply.yacc as yacc
import AST

# Get the token map from the lexer.  This is required.
from lex import tokens

#def p_preProc(p):
#	'''preProc : HASH INCLUDE LT identifier GT stdNamespace '''
	
#def p_stdNamespace(p):
#	'''stdNamespace : USING NAMESPACE STD TERMINAL mainFunc '''

#main function
def p_mainFunc(p):
	'''mainFunc : INT MAIN LPAREN RPAREN statement '''	

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

def p_unaryExpression(p):
	'''unaryExpression : postfixExpression 
			| PLUSPLUS unaryExpression
			| MINUSMINUS unaryExpression
			| unaryOper unaryExpression
			| SIZEOF unaryExpression
			| SIZEOF LPAREN simpleTypeName RPAREN '''
	if(len(p)==2):
		p[0]=p[1]

def p_primaryExpression(p):
	'''primaryExpression : identifier
                       | constant
                       | STRING
                       | LPAREN expression RPAREN '''
	if(len(p)==2):
		if(isinstance(p[1],AST.Identifier)):
			p[0] = AST.Expr("id",operand1=p[1])
		else:	#constant
			p[0]  = p[1]
	#have to write for others

def p_postfixExpression(p):
	'''postfixExpression : primaryExpression
			| postfixExpression LEFTSQRBRACKET expression RIGHTSQRBRACKET
			| postfixExpression DEREF_ONE identifier
			| postfixExpression DEREF_TWO identifier
			| postfixExpression PLUSPLUS
			| postfixExpression MINUSMINUS
			| DYNAMIC_CAST LT simpleTypeName GT LPAREN expression RPAREN 
			| STATIC_CAST LT simpleTypeName GT LPAREN expression RPAREN
			| CONST_CAST LT simpleTypeName GT LPAREN expression RPAREN '''
	if(len(p)==2):
		p[0]=p[1]

def p_constant(p):
	'''constant : INTNUM
			 | FLOATNUM
             | CHAR_CONST'''
	p[0] = AST.Expr("constant",operand1=p[1])
#             | enumerationConstant '''

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

def p_conditionalExpression(p):
	'''conditionalExpression : logicalOrExpression 
                          | logicalOrExpression QUES_MARK expression COLON conditionalExpression'''
	if(len(p)==2):
		p[0]=p[1]

def p_logicalOrExpression(p):
	'''logicalOrExpression : logicalAndExpression 
				| logicalOrExpression  OR   logicalAndExpression'''
	if(len(p)==2):
		p[0]=p[1]

def p_logicalAndExpression(p):
	'''logicalAndExpression : inclusiveOrExpression 
				| logicalAndExpression  AND   inclusiveOrExpression'''	
	if(len(p)==2):
		p[0]=p[1]

def p_inclusiveOrExpression(p):
	'''inclusiveOrExpression : exclusiveOrExpression 
			| inclusiveOrExpression BIT_OR exclusiveOrExpression'''
	if(len(p)==2):
		p[0]=p[1]

def p_exclusiveOrExpression(p):
	'''exclusiveOrExpression : andExpression 
			| exclusiveOrExpression BIT_XOR andExpression'''
	if(len(p)==2):
		p[0]=p[1]

def p_andExpression(p):
	'''andExpression : equalityExpression 
			| andExpression BIT_AND equalityExpression'''
	if(len(p)==2):
		p[0]=p[1]

def p_equalityExpression(p):
	'''equalityExpression : relationalExpression 
			| equalityExpression EQUAL relationalExpression
			| equalityExpression NEQUAL relationalExpression'''
	if(len(p)==2):
		p[0]=p[1]
			
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
			| iterationStatement
			| jumpStatement'''
	
			
def p_labeledStatement(p):
	'''labeledStatement : identifier COLON statement
			| CASE constantExpression COLON statement
			| DEFAULT COLON statement'''
	if len(p) == 4:
		if (p[1] == "default"):
		p[0] = AST.CaseDefault(p[3])
			
def p_constantExpression(p):
	'''constantExpression : conditionalExpression '''

def p_expressionStatement(p):
	'''expressionStatement : expression TERMINAL
			| empty'''
			
def p_compoundStatement(p):
	'''compoundStatement : LEFTCURLYBRACKET declarationList statementList RIGHTCURLYBRACKET
			| empty'''
	if len(p) == 5:
		p[0] = AST.CompoundStmt(p[3], p[2])
			
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

def p_declaration(p):
	'''declaration :  decSpecList initDecList TERMINAL '''
	#decSpecList Done

def p_initDecList(p):
	'''initDecList : initDecList COMMA markDec initDec
			| initDec '''
	if len(p)==2:
		p[0] = p[1]
	

def p_markDec(p):
	'''markDec : empty '''
	p[0] = p[-3]
	print("marker:",p[0])

def p_decSpecList(p):
	'''decSpecList : decSpecList decSpec
			| decSpec '''
	if(len(p)==2):
		#p[0] = copy.deepcopy(p[1])
		p[0] = p[1]
	else:
		#p[0] = copy.deepcopy(p[1])
		#p[0]['type']+=p[2]['type']
		p[0] = p[1].combine(p[2].type)
	
	print(p[0].type)

def p_initDec(p):
	''' initDec : declarator
                    | declarator ASSIGNMENT initializer'''	#not handled
	if(len(p)==2):
		p[0] = p[1]
	#print("initDec:",p[0])

def p_declarator(p):
	'''declarator : pointerList directDec'''
	p[0] = p[2]
	#if(p[1]!=None):
		#p[0]['type']+=p[1]['type']

def p_pointerList(p):
	''' pointerList : pointer
			| empty '''
	if (p[1] != None):
		p[0] = p[1]
	print("pointerList:",p[0])

def p_pointer(p):
	'''pointer : star typeQualList
		| empty	'''
	if(len(p)==3):
		p[0] = { 'type': p[1]['type'] + p[2]['type'] }	
	print("pointer:",p[0])

def p_star(p):
	'''star : star TIMES
		| TIMES	'''
	if(len(p)==2):
		p[0]={'type':'*'}
	else:
		p[0] = p[1]
		p[0]['type']+='*'
	#print("star:",p[0])

def p_typeQualList(p):
	''' typeQualList : typeQualifier
			| empty '''
	if(p[1] != None):
		p[0] = p[1]
	else:
		p[0] = {'type':''}

def p_directDec(p):
	'''directDec : identifier
                      | LEFTCURLYBRACKET declarator RIGHTCURLYBRACKET
                      | identifier arrayDec
                      | directDec LEFTCURLYBRACKET idList RIGHTCURLYBRACKET
		      | directDec LPAREN parTypeList RPAREN ''' 
	#print("directDec:",p[1])
	if(len(p)==3):
		#p[0] = copy.deepcopy(p[1])
		p[1].changeToArray(p[2]['val'])
		print(p[1].idtype,p[1].intnum)

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
	#print(p[-2])
	if(p[-1] is None):
		p[0] = AST.Identifier(p[1],idtype = p[-2].type)
	else:
		p[0] = AST.Identifier(p[1],idtype = p[-2].type+p[-1]['type']) #{'type':p[-2]['type']+p[-1]['type'],'lexval':p[1]}
	print("identifier:",p[0].idtype,p[0].id)

	#remember while adding to symbol table make changes in directDec for array type

def p_parTypeList(p):
	'''parTypeList : parList
                        | parList COMMA DEREF_ONE DEREF_ONE DEREF_ONE '''

def p_parList(p):
	'''parList : parDec
                   | parList COMMA parDec '''

def p_parDec(p):
	'''parDec : decSpecList declarator
			| decSpecList abstractDec
                        | decSpecList '''

def p_abstractDec(p):
	'''abstractDec : pointer
                        | pointer directAbsDec
                        | directAbsDec '''

def p_directAbsDec(p):
	'''directAbsDec : LPAREN abstractDec RPAREN
			| directAbsDecList LEFTSQRBRACKET constExprList RIGHTSQRBRACKET
                        | directAbsDecList LPAREN parTypeList RPAREN '''

def p_directAbsDecList(p):
	'''directAbsDecList : directAbsDec
			    | empty '''

def p_constExprList(p):
	'''constExprList : constantExpression
			| empty '''

def p_idList(p):
	'''idList : idList identifier
		| empty '''

# | <direct-declarator> ( <parameter-type-list> )


def p_initializer(p):
	'''initializer : assignmentExpression
                | LEFTCURLYBRACKET initializerList RIGHTCURLYBRACKET
                | LEFTCURLYBRACKET initializerList COMMA RIGHTCURLYBRACKET '''

def p_initializerList(p):
	'''initializerList : initializer
                     | initializerList COMMA initializer'''

def p_decSpec(p):
	'''decSpec : StorageClassSpec
                          | simpleTypeName
                          | typeQualifier '''
	#p[0]=copy.deepcopy(p[1])
	p[0] = p[1]

def p_typeQualifier(p):
	''' typeQualifier : CONST
			  | VOLATILE '''
	#p[0] = {'type':p[1]}
	p[0] = AST.Type(p[1])

def p_StorageClassSpec(p):
	'''StorageClassSpec : AUTO
                            | REGISTER
                            | STATIC
                            | EXTERN
                            | TYPEDEF '''
	#p[0] = {'type':p[1]}
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
		
def p_iterationStatement(p):
	'''iterationStatement : WHILE LPAREN expression RPAREN statement
			| DO statement WHILE LPAREN expression RPAREN TERMINAL
			| FOR LPAREN forInitStatementExpression TERMINAL expression RPAREN statement'''
	if len(p) == 6:
        p[0] = AST.WhileStmt("while", p[3], p[5])
        
    elif len(p) == 8:
		if (p[1] == "for"):
			 p[0] = AST.ForStmt(p[3], p[5], p[7])
		else:
			p[0] = AST.WhileStmt("dowhile", p[5], p[2])
			
def p_forInitStatementExpression(p):
	'''forInitStatementExpression : expressionStatement'''
	#		| declarationStatement'''
	p[0]=p[1]

		
def p_jumpStatement(p):
	'''jumpStatement : BREAK TERMINAL
			| CONTINUE TERMINAL
			| RETURN expression TERMINAL
			| RETURN TERMINAL
			| GOTO identifier TERMINAL'''

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input\n error:",p,"at line:",p.lineno)

# 	Build the parser
parser = yacc.yacc()

s=open('cpp_code.cpp','r').read()
result = parser.parse(s)
print(result)
