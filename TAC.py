from collections import namedtuple
import AST

# s=open('cpp_code.cpp','r').read()
# print(s)

#https://codearea.in/generate-three-address-code-quadruple-and-triple-using-lex-and-yacc/
#https://github.com/tushcoder/ThreeAddressCode
class threeAC:
	temp=1
	ind = 0
	labelcount = 1
	incode = namedtuple("incode", "op1 op2 opr")
	code =[]
	if_idx=0
	endif_idx=0
	step=0
	labels=[]
	lc=0

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
				op1 = opd1.operand1.id
			else:
				op1 = opd1

		if(opd2 is not None):
			if(isinstance(opd2,AST.Expr)):
				op2 = opd2.operand1.id
			else:
				op2 = opd2

		self.code.append(self.incode(op1 = op1,op2 = op2,opr=opr))
		# if(self.code[self.ind].opr != '='):
		# 	self.temp += 1
		self.ind+=1

	def ThreeAddressCode(self):
		print(self.code)
		temp=self.temp
		cnt=0
		print("THREE ADDRESS CODE")
		while(cnt<self.ind):
			if(self.code[cnt].opr == "switch"):
				self.ThreeAddressCode_switch(cnt)
				break
			elif(self.code[cnt].opr == "if"):
				cnt=self.ThreeAddressCode_if(cnt)-1
			elif(self.code[cnt].opr == "endif"):
				print("("+str(self.step)+") "+ self.labels[self.lc-1] + ":")	
			elif(self.code[cnt].opr == "ifelse"):
				self.ThreeAddressCode_ifelse(cnt)
			elif(self.code[cnt].opr not in ["==","<=",">=",">","<"]):
				self.ThreeAddressCode_expr(cnt)
			cnt+=1
		self.temp+=1
		print("\n")

	def ThreeAddressCode_switch(self,cnt):
		index+=1
		print("if")
		return

	def ThreeAddressCode_ifelse(self,cnt):
		#cnt=self.ThreeAddressCode_if(cnt)

		return

	def ThreeAddressCode_if(self,cnt):
		self.labels.append(self.make_newlabel())
		flag=0
		for i in reversed(self.code):
			for j in i:
				if(j == "endif"):	
			 		flag=1
			 		break
			if(flag==1):
				break
			else:
				self.endif_idx+=1

		condition = str(self.code[cnt+1].op1) + str(self.code[cnt+1].opr) + str(self.code[cnt+1].op2)

		self.step+=1
		print("("+str(self.step)+") "+"<Evaluate " + condition+">")
		self.step+=1
		print("("+str(self.step)+") "+"if_False " + condition + " goto " + self.labels[self.lc])
		self.lc+=1
		# if(eval(cond)):
		# 	execCnt=cnt-stmtCount			
		# 	while(execCnt<cnt):
		# 		self.ThreeAddressCode_expr(execCnt,self.temp)
		# 		execCnt+=1
		
		cnt=cnt+2
		while(cnt<(len(self.code)-self.endif_idx-1)):
			x=self.ThreeAddressCode_expr(cnt)
			if x is not None:
				cnt=x+1
			else:	
				cnt+=1
		if(cnt==(len(self.code)-self.endif_idx-1)):	
			self.step+=1
			print("("+str(self.step)+") "+self.labels[self.lc-1] + ":")
			self.lc-=1
		return cnt

	def ThreeAddressCode_expr(self,cnt):
		if(self.code[cnt].opr == "switch"):
			self.ThreeAddressCode_switch(cnt)
		elif(self.code[cnt].opr == "if"):
			cnt=self.ThreeAddressCode_if(cnt)
		if(self.code[cnt].opr == "endif"):
			return cnt
		
 		
		if(self.code[cnt].opr != '='):			
				self.step+=1
				print("("+str(self.step)+") "+"t"+str(self.temp) +": = ",end='')

		if(str(self.code[cnt].op1).isalnum()):
			if(self.code[cnt].opr == '='):
				self.step+=1
				print("("+str(self.step)+") "+self.code[cnt].op1,end='')
			else:
				print(self.code[cnt].op1,end='')				
		else:
			self.step+=1
			print("("+str(self.step)+") "+"t"+str(self.temp),end='')
			self.temp+=1

		print(self.code[cnt].opr,end='')

		if(str(self.code[cnt].op2).isalnum()):
			print(self.code[cnt].op2,end='')
		else:
			print("t"+str(self.temp),end='')
			self.temp+=1
		print("\n")
		return 

