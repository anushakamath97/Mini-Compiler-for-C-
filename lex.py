import ply.lex as lex
import sys
from tabulate import tabulate

reserved = dict.fromkeys(
	['asm', 'else', 'new', 'this', 'auto', 'enum', 'operator', 'throw', 'bool', 'explicit', 'private', 'true', 'break', 'export', 'protected', 'try', 'case', 'extern', 'public', 'typedef', 'catch', 'false', 'register', 'typeid', 'char', 'float', 'reinterpret_cast', 'typename', 'class', 'for', 'return', 'union', 'const', 'friend', 'short', 'unsigned', 'const_cast', 'goto', 'signed', 'using', 'continue', 'if', 'sizeof', 'virtual', 'default', 'inline', 'static', 'void', 'delete', 'int', 'static_cast', 'volatile', 'do', 'long', 'struct', 'wchar_t', 'double', 'mutable', 'switch', 'while', 'dynamic_cast', 'namespace', 'template'] , 'KEYWORD'
)

data_types=('enum', 'bool', 'char', 'float', 'short', 'unsigned', 'signed', 'void', 'int', 'long', 'double')

predef_func = dict.fromkeys(
	['cin', 'cout','cerr','exit','gets','puts','malloc','calloc','realloc','atoi'] , 'PREDEFINED_FUNCTION'
)

# List of token names.   This is always required
tokens = [
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
   'OPERATOR',
   'ID',
   'STRING',
   'KEYWORD',
   'OSCOPE',
   'CSCOPE',
   'PREDEFINED_FUNCTION', 
   'ASSIGNMENT',
   'TERMINAL'
] 

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_OPERATOR  = r'\<|\>'
t_ASSIGNMENT = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_STRING = r'[a-zA-Z_]?\"(\\.|[^\\"])*\"'
t_OSCOPE = r'{'
t_CSCOPE = r'}'
t_TERMINAL = r';'

def t_COMMENT(t):
    r"(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)"
    pass
    # No return value. Token discarded

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_HEADER(t):
	r'\#.*' 
	pass

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    t.type = predef_func.get(t.value,'ID') 
    return t

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t' + r'$|,|\'|:'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

#inputs=[data,data2,data3,data4]
data = open('cpp_code.cpp','r').read()
inputs =[data,]

data_type=''

for data in inputs:
	# Give the lexer some input
	lexer.input(data)

	main_table=[]
	sym_table={}

	inScope=1
	outScope=0
	prev_inScope=1

	for key in reserved:
		sym_table[key]=(reserved[key],(inScope,outScope),data_type)
		
	for key in predef_func:
		sym_table[key]=(predef_func[key],(inScope,outScope),data_type)

	main_table.append(sym_table)
	# Tokenize
	while True:
		tok = lexer.token()
		if not tok: 
			break      # No more input

		if tok.type == 'OSCOPE':
			inScope=prev_inScope+1
			prev_inScope+=1
			outScope+=1
			main_table.append({})
		elif tok.type == 'CSCOPE':
			inScope-=1
			outScope-=1
	
		if tok.value in data_types:
			data_type=tok.value

		if tok.type == 'LPAREN' or tok.type == 'TERMINAL': 
			if len(data_type)!=0:
				data_type=''
		flag=1
		if tok.value in reserved.keys() or tok.value in predef_func.keys():
			flag=0
		
		if tok.type == 'ID' and len(data_type)!=0 and flag==1:
			main_table[inScope-1][tok.value]=(tok.type,(inScope,outScope),data_type)


	heading=["NAME","TYPE","IN_SCOPE","OUT_SCOPE","ATTRIBUTE"]
	
	for table in main_table:
		temp=[]
		for key in table:
			temp.append([key,table[key][0],table[key][1][0],table[key][1][1],table[key][2]])
		print(tabulate(temp,headers=heading,tablefmt="psql"))
		print("\n\n")
	
