# AST implementation
# 20121022 Young Seok Kim

debugNode = False


class Node(object):
    def printast(self):
        return "NOT IMPLEMENTED!"

    def insertLineNumInfo(self, linenumber, position):
        self.line_position = (linenumber, position)

    def position(self):
        return "Line %d, Column %d" % self.line_position

class Program(Node):
    def __init__(self, declist=None, funclist=None):
        self.DecList = declist
        self.FuncList = funclist

    def __str__(self):
        outputstr = "[Program] : \n"
        if self.DecList is not None:
            outputstr += "DeclList : " + str(self.DecList)
        if self.FuncList is not None:
            outputstr += "FuncList : " + str(self.FuncList)
        return outputstr

    def printast(self):
        outputstr = ""
        if debugNode:
            outputstr += "[Program]"
        if self.DecList is not None:
            outputstr += self.DecList.printast()
        if self.FuncList is not None:
            outputstr += "\n"
            outputstr += self.FuncList.printast()
        return outputstr


class DecList(Node):
    def __init__(self):
        self.declarations = []    # This will be list of Declaration object

    def add_decl(self, decl):
        self.declarations.append(decl)

    def __str__(self):
        outputstr = "\n[DecList] : \n"
        if self.declarations is not None:
            outputstr += "\nDeclarations : "
            outputstr += "["
            for element in self.declarations:
                outputstr += str(element) + " "
            outputstr += "]\n"
        return outputstr

    def printast(self):
        outputstr = ""
        if debugNode:
            outputstr += "[DecList]"
        l = []
        for element in self.declarations:
            l.append(element.printast())
        return outputstr + "\n".join(l)


class FuncList(Node):
    def __init__(self):
        self.functions = []          # This will be list of Function object

    def add_function(self, function):
        self.functions.append(function)

    def __str__(self):
        outputstr = "[FuncList] : \n"
        if self.functions is not None:
            outputstr += "functions : "
            outputstr += "["
            for element in self.functions:
                outputstr += str(element) + " "
            outputstr += "]"
        return outputstr

    def printast(self):
        outputstr = ""
        if debugNode:
            outputstr += "[FuncList]"
        l = []
        for element in self.functions:
            l.append(element.printast())
        return outputstr + "\n".join(l)


class Declaration(Node):
    def __init__(self, type, identlist):
        self.type = type
        self.identlist = identlist

    def __str__(self):
        outputstr = "\n[Declaration] : \n"
        if self.type is not None:
            outputstr += "type : " + str(self.type)
        if self.identlist is not None:
            outputstr += "\nidentlist : " + str(self.identlist)
        return outputstr

    def printast(self):
        outputstr = ""
        if debugNode:
            outputstr += "[Declaration]"
        outputstr += self.type.printast().lower() + " "
        outputstr += self.identlist.printast()
        outputstr += ";"
        return outputstr


class IdentList(Node):
    def __init__(self, identifiers):
        self.identifiers = identifiers      # This will be the list of Identifier object

    def add_identifier(self, ident):
        self.identifiers.append(ident)

    def __str__(self):
        outputstr = "\n[IdentList] : \n"
        if self.identifiers is not None:
            outputstr += "identifiers : "
            outputstr += "["
            for element in self.identifiers:
                outputstr += str(element) + " "
            outputstr += "]\n"
        return outputstr

    def printast(self):
        l = []
        for element in self.identifiers:
            l.append(element.printast())
        return ", ".join(l)


class Identifier(Node):
    def __init__(self, id,intnum=None, idtype="non-array"):
        self.id = id
        self.intnum = intnum	#This value will be not None if array
        self.type = idtype
        self.value = None              

    def __str__(self):
        outputstr = "\n[Identifier] : \n"
        if self.id is not None:
            outputstr += "id : " + str(self.id) + ",\t"
        if self.intnum is not None:
            outputstr += "intnum : " + str(self.intnum) + ",\t"
        if self.type is not None:
            outputstr += "idtype : " + str(self.type)
        if self.value is not None:
            outputstr += ",\t" "value :" + str(self.value)
        return outputstr+"\n"
 
    def changeToArray(self,val):
        for x in val:
          self.type += '['+str(x) +']'

    def add_value(self,valNode):
        self.value = valNode

    def printast(self):
        if self.type == "array":
            return str(self.id)+"["+str(self.intnum)+"]"
        else:
            return str(self.id)


class Function(Node):
    def __init__(self, type, id, compoundstmt, params=None):
        self.type = type
        self.id = id
        self.comoundstmt = compoundstmt
        self.params = params                # This value is one ParamList object

    def __str__(self):
        outputstr = "[Function] : \n"
        if self.type is not None:
            outputstr += "type : " + str(self.type)
        if self.id is not None:
            outputstr += "id : " + str(self.id)
        if self.comoundstmt is not None:
            outputstr += "comoundstmt : " + str(self.comoundstmt)
        if self.params is not None:
            outputstr += "params : " + str(self.params)
        return outputstr

    def printast(self):
        outputstr = ""
        outputstr += self.type.printast() + " "
        outputstr += str(self.id)
        outputstr += "("
        if self.params is not None:
            outputstr += self.params.printast()
        outputstr += ")\n"
        outputstr += self.comoundstmt.printast()
        return outputstr


class ParamList(Node):
    def __init__(self):
        self.paramlist = []

    def addparam(self, ptype, identifier):
        self.paramlist.append((ptype, identifier))

    def __str__(self):
        outputstr = "[ParamList] : \n"
        if self.paramlist is not None:
            outputstr += "paramlist : "
            outputstr += "["
            for element in self.paramlist:
                outputstr += str(element) + " "
            outputstr += "]"
        return outputstr

    def printast(self):
        l = []
        for (t, id) in self.paramlist:
            l.append(t.printast()+" "+id.printast())
        return ", ".join(l)


class Type(Node):
    def __init__(self, type):
        self.type = type                    # This value can be either "int" or "float"

    def __str__(self):
        outputstr = "\n[Type] : \n"
        if self.type is not None:
            outputstr += "type : " + str(self.type)+"\n"
        return outputstr

    def combine(self,extra):
        self.type += " " + extra
        return self

    def printast(self):
        return str(self.type).lower()


class CompoundStmt(Node):
    def __init__(self, stmtlist, decllist=None): # Note the order of the parameter
        self.declist = decllist
        self.stmtlist = stmtlist

    def __str__(self):
        outputstr = "\n[CompoundStmt] : \n"
        if self.declist is not None:
            outputstr += "DeclList : " + str(self.declist)
        if self.stmtlist is not None:
            outputstr += "\nstmtlist : " + str(self.stmtlist)
        return outputstr

    def printast(self):
        outputstr = ""
        outputstr += "{\n"
        if self.declist is not None:
            outputstr += self.declist.printast() + "\n"
        outputstr += self.stmtlist.printast()
        outputstr += "\n}"
        return outputstr


class StmtList(Node):
    def __init__(self):
        self.stmts = []                  # This will be list of Stmt object

    def add_stmt(self, stmt):
        self.stmts.append(stmt)

    def __str__(self):
        outputstr = "\n[StmtList] : \n"
        if self.stmts is not None:
            outputstr += "\nstmts : "
            outputstr += "["
            for element in self.stmts:
                outputstr += str(element) + " "
            outputstr += "]\n"
        return outputstr

    def printast(self):
        l = []
        for e in self.stmts:
            l.append(e.printast())
        return "\n".join(l)


class Stmt(Node):
    def __init__(self, stmttype, stmt):
        self.stmttype = stmttype
        # This stmttype value is either
        # "assignStmt", "callStmt", "retStmt", "whileStmt",
        # "forStmt", "ifStmt", "switchStmt", "compoundStmt", or "SEMI"
        self.stmt = stmt

    def printast(self):
        outputstr = ""
        if self.stmttype == "SEMI":
            outputstr += ";"
        else:
            outputstr += self.stmt.printast()
        return outputstr


class AssignStmt(Node):
    def __init__(self, assign):
        self.assign = assign

    def printast(self):
        outputstr = ""
        outputstr += self.assign.printast()+";"
        return outputstr


class Assign(Node):
    def __init__(self, assigntype, id, reval, leval=None):
        self.assigntype = assigntype        # This value is either 'array' or 'non-array'
        self.id = id
        self.reval = reval
        self.leval = leval

    def __str__(self):
        outputstr = "[Assign] : \n"
        if self.assigntype is not None:
            outputstr += "assigntype : " + str(self.assigntype)
        if self.id is not None:
            outputstr += "id : " + str(self.id)
        if self.reval is not None:
            outputstr += "reval : " + str(self.reval)
        if self.leval is not None:
            outputstr += "leval : " + str(self.leval)
        return outputstr

    def printast(self):
        if self.assigntype == "non-array":
            return str(self.id)+" = "+self.reval.printast()
        else:
            return str(self.id)+"["+self.leval.printast()+"]"+" = "+self.reval.printast()


class CallStmt(Node):
    def __init__(self, call):
        self.call = call

    def printast(self):
        outputstr = ""
        outputstr += self.call.printast() + ";"
        return outputstr


class Call(Node):
    def __init__(self, id, arglist=None):
        self.id = id
        self.arglist = arglist

    def __str__(self):
        outputstr = "[Call] : \n"
        if self.id is not None:
            outputstr += "id : " + str(self.id)
        if self.arglist is not None:
            outputstr += "arglist : " + str(self.arglist)
        return outputstr

    def printast(self):
        outputstr = ""
        outputstr += str(self.id)
        outputstr += "("
        if self.arglist is not None:
            outputstr += self.arglist.printast()
        outputstr += ")"
        return outputstr

    def return_type(self):
        if hasattr(self, '_return_type'):
            return self._return_type
        else:
            return None

    def set_return_type(self, return_type):
        setattr(self, '_return_type', return_type)


class RetStmt(Node):
    def __init__(self, expr=None):
        self.expr = expr

    def __str__(self):
        outputstr = "\n[RetStmt] : \n"
        if self.expr is not None:
            outputstr += "expr : " + str(self.expr)
        return outputstr

    def printast(self):
        outputstr = "return "
        if self.expr is not None:
            outputstr += self.expr.printast()
        outputstr += ";"
        return outputstr

class JumpStmt(Node):
    def __init__(self,begin="break"):
        self.begin = begin

    def __str__(self):
        outputstr  = self.begin +"\n"
        return outputstr

    def printast(self):
        outputstr = self.begin +" ;"
        return outputstr

class WhileStmt(Node):
    def __init__(self, style, conditionexpr, repeatstmt):
        self.style = style                  # This value is either 'while' or 'dowhile'
        self.conditionexpr = conditionexpr
        self.repeatstmt = repeatstmt

    def __str__(self):
        outputstr = "[WhileStmt] : \n"
        if self.style is not None:
            outputstr += "style : " + str(self.style)
        if self.conditionexpr is not None:
            outputstr += "conditionexpr : " + str(self.conditionexpr)
        if self.repeatstmt is not None:
            outputstr += "repeatstmt : " + str(self.repeatstmt)
        return outputstr

    def printast(self):
        outputstr = ""
        if self.style == "while":
            outputstr += "while ("
            outputstr += self.conditionexpr.printast()
            outputstr += ")\n"
            outputstr += self.repeatstmt.printast()
        else:
            outputstr += "do\n"
            outputstr += self.repeatstmt.printast()
            outputstr += " while ("
            outputstr += self.conditionexpr.printast()
            outputstr += ");"
        return outputstr


class ForStmt(Node):
    def __init__(self, initial_assign, conditionexpr, assign, repeatstmt):
        self.initial_assign = initial_assign
        self.conditionexpr = conditionexpr
        self.assign = assign
        self.repeatstmt = repeatstmt

    def __str__(self):
        outputstr = "[ForStmt] : \n"
        if self.initial_assign is not None:
            outputstr += "initial_assign : " + str(self.initial_assign)
        if self.conditionexpr is not None:
            outputstr += "conditionexpr : " + str(self.conditionexpr)
        if self.assign is not None:
            outputstr += "assign : " + str(self.assign)
        if self.repeatstmt is not None:
            outputstr += "repeatstmt : " + str(self.repeatstmt)
        return outputstr

    def printast(self):
        outputstr = "for ("
        outputstr += self.initial_assign.printast()+ ";"
        outputstr += self.conditionexpr.printast() + ";"
        outputstr += self.assign.printast() + ")\n"
        outputstr += self.repeatstmt.printast()
        return outputstr


class IfStmt(Node):
    def __init__(self, conditionexpr, thenstmt, elsestmt=None):
        self.conditionexpr = conditionexpr
        self.thenstmt = thenstmt
        self.elsestmt = elsestmt

    def __str__(self):
        outputstr = "\n[IfStmt] : \n"
        if self.conditionexpr is not None:
            outputstr += "conditionexpr : " + str(self.conditionexpr)
        if self.thenstmt is not None:
            outputstr += "\nthenstmt : " + str(self.thenstmt)
        if self.elsestmt is not None:
            outputstr += "\nelsestmt : " + str(self.elsestmt)
        return outputstr

    def printast(self):
        outputstr = "if ("
        outputstr += self.conditionexpr.printast() + ")\n"
        outputstr += self.thenstmt.printast() + "\n"
        if self.elsestmt is not None:
            outputstr += "else\n" + self.elsestmt.printast()
        return outputstr


class SwitchStmt(Node):
    def __init__(self, expr, caselist):
        self.expression = expr
        self.caselist = caselist

    def __str__(self):
        outputstr = "\n[SwitchStmt] : \n"
        if self.expression is not None:
            outputstr += "Expr : " + str(self.expression)
        if self.caselist is not None:
            outputstr += "\ncaselist : " + str(self.caselist)
        return outputstr

    def printast(self):
        outputstr = "switch ("
        outputstr += self.id.printast() + ") {" + "\n"
        outputstr += self.caselist.printast() + "\n" + "}"
        return outputstr


class CaseList(Node):
    def __init__(self, cases, default=None):
        self.cases = cases                  # This will be the list of Case object
        self.default = default

    def __str__(self):
        outputstr = "\n[CaseList] : \n"
        if self.cases is not None:
            outputstr += "cases : " + str(self.cases)
        if self.default is not None:
            outputstr += "\ndefault : " + str(self.default)
        return outputstr

    def printast(self):
        outputstr = ""
        if self.cases is not None:
            outputstr += self.cases.printast()
        if self.default is not None:
            outputstr += "\n" + self.default.printast()
        return outputstr


class Case(Node):
    def __init__(self):
        self.cases = []

    def add_case(self, expr, stmtlist, break_exist=False):
        self.cases.append((expr, stmtlist))

    def __str__(self):
        outputstr = "\n[Case] : \n"
        if self.cases is not None:
            outputstr += "cases : "
            outputstr += "["
            for element in self.cases:
                outputstr += "\ncase: "
                if element[0] is not None:
                   outputstr += str(element[0]) + " \t"
                if element[1] is not None:
                   outputstr += str(element[1])
            outputstr += "\t\t]\n"
        return outputstr

    def printast(self):
        l = []
        for (intnum, stmtlist, break_exist) in self.cases:
            casestr = "case "
            casestr += str(intnum) + ":\n"
            casestr += stmtlist.printast()
            #if break_exist:
                #casestr += "\nbreak;"
            l.append(casestr)
        return "\n".join(l)


class CaseDefault(Node):
    def __init__(self, stmtlist, break_exist=False):
        self.stmtlist = stmtlist
        self.break_exist = break_exist

    def __str__(self):
        outputstr = "\t[CaseDefault] : \n"
        if self.stmtlist is not None:
            outputstr += "stmtlist : "
            outputstr += "["
            outputstr += str(self.stmtlist) + " "
            outputstr += "]\t"
        #if self.break_exist is not None:
            #outputstr += "break_exist : " + str(self.break_exist)
        return outputstr

    def printast(self):
        outputstr = "default:\n"
        outputstr += self.stmtlist.printast()
        #if self.break_exist:
            #outputstr += "\nbreak;"
        return outputstr


class Expr(Node):
    def __init__(self, expr_type, operand1=None, operand2=None, operator=None, idval=None, idIDX=None,constType=None):
        self.expr_type = expr_type
        # This expr_type value is either
        # 'unop', 'binop'
        # 'call', 'intnum', 'floatnum', 'id', 'arrayID'
        self.operator = operator
        # This value can be 'unop',  PLUS, MINUS, TIMES, DIVIDE, ...
        self.idval = idval
        self.idIDX = idIDX
        self.operand1 = operand1
        self.operand2 = operand2
        if expr_type == 'constant' or expr_type == 'id':
           self.type = constType
        else: #need to change
           self.type = None

    def __str__(self):
        outputstr = "\n[Expr] : \n"
        if self.expr_type is not None:
            outputstr += "expr_type : " + str(self.expr_type)
        if self.operator is not None:
            outputstr += "\t" + "operator : " + str(self.operator)
        if self.idval is not None:
            outputstr += "\t" + "idval : " + str(self.idval)
        if self.idIDX is not None:
            outputstr += "\t" + "idIDX : " + str(self.idIDX)
        if self.operand1 is not None:
            outputstr += "\t" + "operand1 : " + str(self.operand1)
        if self.operand2 is not None:
            outputstr += "\t" + "operand2 : " + str(self.operand2)
        return outputstr

    def printast(self):
        if self.expr_type == "unop":
            return "-"+self.operand1.printast()
        elif self.expr_type == "binop":
            return self.operand1.printast()+str(self.operator)+self.operand2.printast()
        elif self.expr_type == "arrayID":
            return str(self.idval)+"["+self.idIDX.printast()+"]"
        elif self.expr_type == "call":
            return self.operand1.printast()
        elif self.expr_type == "id":
            return str(self.operand1)
        elif self.expr_type == "paren":
            return "("+self.operand1.printast()+")"
        else:  # intnum/floatnum case
            return str(self.operand1)

    def return_type(self):
        if hasattr(self, '_return_type'):
            return self._return_type
        else:
            return None

    def set_return_type(self, return_type):
        setattr(self, '_return_type', return_type)


class ArgList(Node):
    def __init__(self, expr):
        self.args = [expr]

    def addarg(self, expr):
        self.args.append(expr)

    def __str__(self):
        outputstr = "[ArgList] : \n"
        if self.args is not None:
            outputstr += "stmtlist : "
            outputstr += "["
            for element in self.args:
                outputstr += str(element) + " "
            outputstr += "]"
        return outputstr

    def printast(self):
        l = []
        for element in self.args:
            l.append(element.printast())
        return ", ".join(l)


class Semi(Node):
    def __str__(self):
        return ";"

    def printast(self):
        return ";"


class TypeCast(Node):
    def __init__(self, expr: Expr, cast_type: str):
        self.expr = expr
        self.cast_type = cast_type

    def printast(self):
        return "((%s) %s)" % (self.cast_type, self.expr.printast())

    def return_type(self):
        return self.cast_type
