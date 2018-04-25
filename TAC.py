from collections import namedtuple
import AST

# s=open('cpp_code.cpp','r').read()
# print(s)

#https://codearea.in/generate-three-address-code-quadruple-and-triple-using-lex-and-yacc/
#https://github.com/tushcoder/ThreeAddressCode
class threeAC:
	def __init__(self):
		self.temp=1
		self.ind = 0
		self.labelcount = 1
		self.incode = namedtuple("incode", "op1 op2 opr")
		self.code =[]
		self.if_idx=0
		self.endif_idx=0
		self.endelse_idx=0
		self.step=0
		self.labels=[]
		self.lc=0
		self.if_count=0
		self.else_count=0
		
	def make_newlabel(self):
		label = 'L_' + str(self.labelcount)
		self.labelcount += 1
		return label


	def AddToTable(self,opd1,opd2,opr):			
		if(opd1 is not None):
			if(isinstance(opd1,AST.Expr)):
				# if(opd1.expr_type == "binop" or opd2 == ''):
				# 	op1 = opd1.operand1.operand1.id
				# else:
				if(opr == "case"):
					op1 = opd1.operand1
				else:
					op1 = opd1.operand1.id
			else:
				op1 = opd1

		if(opd2 is not None):
			if(isinstance(opd2,AST.Expr)):
				if(opd2.expr_type=="id"):
					op2 = opd2.operand1.id
				else:
					op2 = opd2.operand1
			else:
				#print(opd2)
				op2 = opd2

		self.code.append(self.incode(op1 = op1,op2 = op2,opr=opr))
		# if(self.code[self.ind].opr != '='):
		# 	self.temp += 1
		self.ind+=1

	def ThreeAddressCode(self):
		# print(self.code)
		temp=self.temp
		cnt=0
		print("THREE ADDRESS CODE")
		while(cnt<self.ind):
			if(self.code[cnt].opr == "switch"):
				cnt=self.ThreeAddressCode_switch(cnt)
			elif(self.code[cnt].opr == "if"):
				cnt=self.ThreeAddressCode_if(cnt)-1
				# print("ifmain=",str(cnt))
			elif(self.code[cnt].opr == "endif"):
				self.if_count-=1
				# print("endifmain=",str(cnt))
				#print("("+str(self.step)+") "+ self.labels[self.lc-1] + ":")	
			elif(self.code[cnt].opr == "else"):
				cnt=self.ThreeAddressCode_else(cnt)
				# print("elsemain=",str(cnt))
			elif(self.code[cnt].opr not in ["==","<=",">=",">","<"]):
				self.ThreeAddressCode_expr(cnt)
				# print("exprmain=",str(cnt))
			cnt+=1
			# print("main=",str(cnt))
		self.temp+=1
		print("\n")

	def ThreeAddressCode_switch(self,cnt):
		switch_idx = cnt
		cnt+=1
		condition = self.code[cnt]
		cnt+=1
		while(self.code[cnt].opr!="endswitch"):
			if(self.code[cnt].opr=="case"):
				self.step+=1	
				if(cnt-switch_idx == 2):	
					if(condition.op2!=''):
						print("("+str(self.step)+") "+"if " + str(condition.op1) + str(condition.opr) + str(condition.op2) + "==" + str(self.code[cnt].op1) + ":")
					elif(self.code[cnt].op2==''):
						print("("+str(self.step)+") "+"if " + str(condition.op1) + "==" + str(self.code[cnt+1].op1) + ":")
				else:
					if(condition.op2==''):
						print("("+str(self.step)+") "+"else if " + str(condition.op1) + str(condition.opr) + str(condition.op2) + "==" + str(self.code[cnt].op1) + ":")
					elif(self.code[cnt].op2==''):
						print("("+str(self.step)+") "+"else if " + str(condition.op1) + "==" + str(self.code[cnt+1].op1) + ":")
				cnt+=1
			else:
				while(self.code[cnt].opr!="break"):
					self.ThreeAddressCode_expr(cnt)
					cnt+=1
				cnt+=1

		return cnt

	def ThreeAddressCode_else(self,cnt):
		flag=0
		self.else_count+=1
		if(self.endelse_idx!=0):
			self.endelse_idx=[q for q, n in enumerate(list(reversed(self.code[:(len(self.code)-self.endelse_idx-1)]))) if n.opr == "endelse"][0]
		else:
			self.endelse_idx=[q for q, n in enumerate(list(reversed(self.code[:(len(self.code)-self.endelse_idx)]))) if n.opr == "endelse"][0]

		cnt+=1		
		# print("elsefunc=",str(cnt))

		while(cnt<(len(self.code)-self.endelse_idx-1)):		
			# print("elsewhile=",str(cnt))
			if(self.code[cnt].opr == "switch"):
				self.ThreeAddressCode_switch(cnt)
			elif(self.code[cnt].opr == "if"):
				cnt=self.ThreeAddressCode_if(cnt)
			else:
				self.ThreeAddressCode_expr(cnt)
				cnt+=1
			if(self.code[cnt].opr == "endelse"):
				return cnt


	def ThreeAddressCode_if(self,cnt):
		# print("iffunc=",str(cnt))

		self.labels.append(self.make_newlabel())
		self.if_count+=1
		#print(list(reversed(self.code[:(len(self.code)-self.endif_idx-1)])))
		prev_endif=self.endif_idx+1
		if(self.endif_idx!=0):
			self.endif_idx=[q for q, n in enumerate(list(reversed(self.code[:(len(self.code)-self.endif_idx-1)]))) if n.opr == "endif"][0]
		else:
			self.endif_idx=[q for q, n in enumerate(list(reversed(self.code[:(len(self.code)-self.endif_idx)]))) if n.opr == "endif"][0]
			
		# for i in reversed(self.code):
		# 	for j in i:
		# 		if(j == "endif"):	
		# 	 		flag=1
		# 	 		break
		# 	if(flag==1):
		# 		break
		# 	else:
		# 		self.endif_idx+=1

		if self.code[cnt+1].op2 is not None:
			condition = str(self.code[cnt+1].op1) + str(self.code[cnt+1].opr) + str(self.code[cnt+1].op2)
		else:
			condition = str(self.code[cnt+1].op1)
		#print(condition)

		self.step+=1
		print("("+str(self.step)+") "+"<Evaluate " + condition+">")
		self.step+=1
		if(self.code[cnt-1].opr == "endif"):
			self.lc+=1
		print("("+str(self.step)+") "+"if_False " + condition + " goto " + self.labels[self.lc])
		self.lc+=1
		# print(self.lc)
		# if(eval(cond)):
		# 	execCnt=cnt-stmtCount			
		# 	while(execCnt<cnt):
		# 		self.ThreeAddressCode_expr(execCnt,self.temp)
		# 		execCnt+=1
		
		cnt=cnt+2
		while(cnt<(len(self.code)-prev_endif-self.endif_idx-1)):
			# print("ifwhile=",str(cnt))
			x=self.ThreeAddressCode_expr(cnt)
			if x is not None:
				cnt=x+1
			else:	
				cnt+=1
		# print("outifwhile=",str(cnt))

		# print(len(self.code),prev_endif,self.endif_idx)
		# if(cnt==(len(self.code)-self.endif_idx-1)):	
		# 	self.step+=1
		# 	print("("+str(self.step)+") "+self.labels[self.lc-1] + ":")
		# 	self.lc-=1
		return cnt

	def ThreeAddressCode_expr(self,cnt):
		# print(self.code[cnt])
		# print("expr")
		if(self.code[cnt].opr == "switch"):
			cnt=self.ThreeAddressCode_switch(cnt)
		if(self.code[cnt].opr == "if"):
			cnt=self.ThreeAddressCode_if(cnt)
			# print("expr_if"+str(cnt))
		if(self.code[cnt].opr == "else"):
			cnt=self.ThreeAddressCode_else(cnt)	
		if(self.code[cnt].opr == "endif"):
			self.if_count-=1
			self.lc-=1
			if(self.if_count == self.else_count):
				self.lc-=1
			# print("endif_expr"+str(cnt))
			print("("+str(self.step)+") "+ self.labels[self.lc] + ":")	
			return cnt
		elif(self.code[cnt].opr == "endelse"):
				return cnt
		# print("exprfunc=",str(cnt))
	
		if(self.code[cnt].opr != '='):			
				self.step+=1
				print("("+str(self.step)+") "+"t"+str(self.temp) +": = ",end='')

		if(str(self.code[cnt].op1).isalnum()):
			if(self.code[cnt].opr == '='):
				self.step+=1
				print("("+str(self.step)+") "+self.code[cnt].op1,end='')
			else:
				if self.code[cnt].opr == '':
					print(self.code[cnt].op1)
				else:
					print(self.code[cnt].op1,end='')				
		else:
			self.step+=1
			print("("+str(self.step)+") "+"t"+str(self.temp),end='')
			self.temp+=1

		print(self.code[cnt].opr,end='')

		if(self.code[cnt].op2 is not None and str(self.code[cnt].op2).isalnum()):
			print(self.code[cnt].op2,end='')
		elif self.code[cnt].op2 is not None:
			print("t"+str(self.temp),end='')
			self.temp+=1
		print("\n")
		return 

	#constant propagation	
	def const_prop(self):
		opcode = self.code
		
		const = {}

		for i in range(len(opcode)):
			if(opcode[i].op2 != ''):	
				if(opcode[i].opr == "="):
					const[opcode[i].op1] = opcode[i].op2

			elif(opcode[i].opr == 'endif'): #or opcode[ctr].opr == 'switch'):
				const = {}

			if(opcode[i].opr != '='):
				keys = const.keys()
				if opcode[i].op1 in keys:
					opcode[i]=opcode[i]._replace(op1 = const[opcode[i].op1])
				if opcode[i].op2 in keys:
					opcode[i]=opcode[i]._replace(op2 = const[opcode[i].op2])

		self.code = opcode
		self.temp=1
		self.labelcount = 1
		self.if_idx=0
		self.endif_idx=0
		self.step=0
		self.labels=[]
		self.lc=0
		self.ThreeAddressCode()
		return

	#constant_folding
	def const_fold(self):
		opcode = self.code

		for i in range(len(opcode)):
			if opcode[i].opr != '=':
				if isinstance(opcode[i].op1,int) or isinstance(opcode[i].op1,float):
					if isinstance(opcode[i].op2,int) or isinstance(opcode[i].op2,float):
						opcode[i] = opcode[i]._replace(op1 = eval(str(opcode[i].op1)+opcode[i].opr+str(opcode[i].op2)),op2 = None ,opr = '')
						#print(opcode[i])
		self.code = opcode
		self.temp=1
		self.labelcount = 1
		self.if_idx=0
		self.endif_idx=0
		self.step=0
		self.labels=[]
		self.lc=0
		self.ThreeAddressCode()
		return
					
