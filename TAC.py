from collections import namedtuple

# s=open('cpp_code.cpp','r').read()
# print(s)

#https://codearea.in/generate-three-address-code-quadruple-and-triple-using-lex-and-yacc/
#https://github.com/tushcoder/ThreeAddressCode
class threeAC:
	temp='A'
	ind = 0

	incode = namedtuple("incode", "opd1 opd2 opr")
	code =[]

	def AddToTable(self,opd1,opd2,opr):
		self.code.append(self.incode(opd1=opd1,opd2=opd2,opr=opr))
		self.ind+=1
		self.temp=chr(ord(self.temp)+1)
		return self.temp

	def ThreeAddressCode(self):
		temp='A'
		cnt=0
		temp=chr(ord(temp)+1)
		print("THREE ADDRESS CODE")
		while(cnt<self.ind):
			if(self.code[cnt].opr != '='):			
				print(temp +": = ",end='')
			else:
				temp=chr(ord(temp)-1)
			
			if(self.code[cnt].opd1.isalpha()):
				print(self.code[cnt].opd1,end='')
			else:
				print(self.temp,end='')

			print(self.code[cnt].opr,end='')

			if(self.code[cnt].opd2.isalpha()):
				print(self.code[cnt].opd2,end='')
			else:
				print(self.temp,end='')
			print("\n")
			cnt+=1
			temp=chr(ord(temp)+1)			
		print("\n")


