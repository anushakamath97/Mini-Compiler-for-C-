from tabulate import tabulate

class MainSymbolTable:
	def __init__(self):
		self.tables = []
		self.inScope=1
		self.outScope=0
		self.prev_inScope=1

	def add_table(self,tab):
		self.tables.append(tab)

	def get_table(self,ind):
		return self.tables[ind]

	def print_table(self):
		for tab in self.tables:
			tab.print_table()

class SymbolTable:
	def __init__(self):
		self.symtab = []
		self.variables = []

	def add_entry(self,tok):
		token = [tok.type,None,tok.value,tok.lineno,tok.lexpos]
		self.symtab.append(token)
		self.variables.append(tok.value)

	def check_existing(self,val):
		indicies = [index for index, value in enumerate(self.variables) if value == val]
		if len(indicies)>1:
			del self.symtab[indicies[1]]
			del self.variables[indicies[1]]
			return -1
		return 0

	def add_type(self,dtype):
		self.symtab[-1][1] = dtype

	def change_array(self,val):
		for x in val:
			self.symtab[-1][1] += '['+str(x)+']'

	def print_table(self):
		heading=["TOK_TYPE","DTYPE","NAME","LINE_NO","POSITION"]
		sym_tab =[]
		for x in self.symtab:
			if x[1] is not None:
				sym_tab.append(x)
		if len(sym_tab)!=0:
			print(tabulate(sym_tab,headers=heading,tablefmt="psql"))
