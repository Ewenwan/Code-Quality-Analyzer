#coding:utf-8
#Halstead 复杂度
'''
Halstead 复杂度 (Maurice H. Halstead, 1977) 是软件科学提出的第一个计算机软件的分析“定律”，用以确定计算机软件开发中的一些定量规律。

Halstead 复杂度采用一组基本的度量值，这些度量值通常在程序产生之后得出，或者在设计完成之后进行估算。


Halstead 复杂度根据程序中语句行的操作符和操作数的数量计算程序复杂性。

操作符和操作数的量越大，程序结构就越复杂。
操作符:通常包括 语言 保留字、函数调用、运算符，也可以包括有关的 分隔符 等。
       IF-ELSE，While（），return，for(;;),?:,sizeof
       <    +=   -=   +   -   *  /   % 
操作数:可以是 常数 和 变量 等 标识符。

具体方法：
    设 ：
    n1 表示程序中不同的 操作符 个数，
    n2 表示程序中不同的 操作数 个数，
    N1 表示程序中出现的 操作符 总数，
    N2 表示程序中出现的 操作数 总数。
    
1. 程序词汇表长度 Program vocabulary: n = n1 + n2
2. 程序长度或简单长度 Program length: N = N1 + N2  (N 定义为 Halstead 长度，并非源代码行数)
3. 程序预测长度                     N_P = n1 * log2(n1)  +  n2 * log2(n2)
4. 程序体积或容量             Volume: V = N*log2(n)，表明了程序在词汇上的复杂性
5. 程序级别                  Level: L_P = (2/n1) * (n2/N2)，表明了一个程序的最紧凑形式的程序量与实际程序量之比，反映了程序的效率。
6. 程序难度             Difficulty: D_  = 1/L_P，表明了实现算法的困难程度。
7. 编程工作量                 Effort: E = V * D = V/L_P
8. 语言级别:                        L_L = L_P * L_P * V
9. 编程时间 (hours):                  T = E/(S * f)，这里 S = 60 × 60, f = 18 .
10.程序中的错误数预测值:              B = V/3000 = N*log2(n)/3000

Halstead 方法的优点：
    不需要对程序进行深层次的分析，就能够预测错误率，预测维护工作量；
    有利于项目规划，衡量所有程序的复杂度；
    计算方法简单；
    与所用的高级程序设计语言类型无关。


Halstead 方法的缺点：
    仅仅考虑程序数据量和程序体积，不考虑程序控制流的情况；
    不能从根本上反映程序复杂性。

'''
import pycparser
import sys
from more_itertools import accumulate
import math

def merge(dict1, dict2):

    for key in dict2.keys():
        dict1[key] = dict1.get(key, 0) + dict2[key]  # 值是出现的次数

def parse_halstead(node):
    #print str(type(node))
    if(str(type(node)).split("'")[1] == "tuple"):
        if(len(node) == 0): 
            return ({}, {})
        elif (len(node) == 2 and str(type(node[0])).split("'")[1] == "str"):
            return parse_halstead(node[1])
        else:
            #print("came here")
            operators = {} # 操作符
            operands = {}  #操作数
            node_list = node
            for child in node_list:
                ops, opr = parse_halstead(child)
                merge(operators, ops)
                merge(operands, opr)
            return (operators, operands)

    if(node is None):
        return ({}, {})
    
    # 最大的文件AST节点
    elif(str(type(node)) == "<class 'pycparser.c_ast.FileAST'>"):
        operators = {}
        operands = {}
        node_list = node.children()
        for child in node_list:
            #print(type(child))
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)
    # 函数定义
    elif(str(type(node)) == "<class 'pycparser.c_ast.FuncDef'>"):
        operators = {}
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)
    # 函数声明
    elif(str(type(node)) == "<class 'pycparser.c_ast.FuncDecl'>"):
        operators = {}
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)
    #数组声明
    elif(str(type(node)) == "<class 'pycparser.c_ast.ArrayDecl'>"):
        operators = {'[]' : 1}  # 方括号 操作符
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)
    # 指针声明
    elif(str(type(node)) == "<class 'pycparser.c_ast.PtrDecl'>"):
        operators = {}
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.ParamList'>"):
        operators = {'{}' : 1, '()' : 1}#, ', ;' : len(node.params) - 1}
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.ExprList'>"):
        operators = {'()' : 1, ', ;' : len(node.exprs) - 1}
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.EnumeratorList'>"):
        operators = {'{}' : 1}#, ', ;' : len(node.enumerators) - 1}
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.DeclList'>"):
        operators = {'{}' : 1}#, ', ;' : len(node.decls) - 1}
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.InitList'>"):
        operators = {'{}' : 1}#, ', ;' : len(node.exprs) - 1}
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.Cast'>"):
        operators = {}
        operands = {'->' : 1}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.Compound'>"):
        operators = {}
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.CompoundLiteral'>"):
        operators = {}
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.ArrayRef'>"):
        operators = {'[]' : 1}
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.If'>"):
        if(node.iffalse is not None):
            operators = {'if' : 1, 'else' : 1, '()' : 1, '{}' : 2}
            operands = {}
        else:
            operators = {'if' : 1, '()' : 1, '{}' : 1}
            operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.For'>"):
        operators = {'for' : 1, '()' : 1, '{}' : 1, ', ;' : 2}
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.While'>"):
        operators = {'while' : 1, '()' : 1, '{}' : 1}
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.DoWhile'>"):
        operators = {'dowhile' : 1, '()' : 1, '{}' : 1, ', ;' : 1}
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.Switch'>"):
        operators = {'switch' : 1, '()' : 1}
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.Case'>"):
        operators = {'case' : 1, ':' : 1}
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.Continue'>"):
        operators = {'continue' : 1, ', ;' : 1}
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.Default'>"):
        operators = {'default' : 1, ', ;' : 1}
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.Return'>"):
        operators = {'return' : 1, ', ;' : 1}
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.Break'>"):
        operators = {'break' : 1, ', ;' : 1}
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.EllipsisParam'>"):
        operators = {'...' : 1}
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.EmptyStatement'>"):
        operators = {}
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.Decl'>"):
        if(str(type(node.type)) == "<class 'pycparser.c_ast.Enum'>" and
            str(type(node.type.values)) == "<class 'pycparser.c_ast.EnumeratorList'>"):
            operators = {', ;' : (len(node.type.values.enumerators) - 1)}
        elif(str(type(node.init)) == "<class 'pycparser.c_ast.InitList'>"):
            operators = {', ;' : len(node.init.exprs) - 1}
        elif(str(type(node.type)) == "<class 'pycparser.c_ast.FuncDecl'>" and
            str(type(node.type.args)) == "<class 'pycparser.c_ast.ParamList'>"):
            operators = {', ;' : len(node.type.args.params) - 2}
        else:
            operators = {', ;' : 1}
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.Enum'>"):
        operators = {'enum' : 2}
        operands = {str(node.name) : 1}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.Enumerator'>"):
        operators = {}
        operands = {str(node.name) : 1}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.FuncCall'>"):
        operators = {', ;' : 1}
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.Goto'>"):
        operators = {'goto' : 1, ', ;' : 1}
        operands = {str(node.name) : 1}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.ID'>"):
        operators = {}
        operands = {str(node.name) : 1}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.IdentifierType'>"):
        operators = {str((node.names)[0]) : 1}
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.Label'>"):
        operators = {':', 1}
        operands = {str(node.name) : 1}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.NamedInitializer'>"):
        operators = {str(node.name) : 1}
        operands = {str(node.name) : 1}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.Struct'>"):
        operators = {'struct' : 1, '{}' : 1, ', ;' : 1}
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.StructRef'>"):
        operators = {}
        operands = {str(node.name) : 1}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.Typedef'>"): #TypeDef
        operators = {str(node.name) : 1}
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.TypeDecl'>"):
        if(node.declname == 'main'):
            operators = {str(node.declname) : 1}
            operands = {}
        else:
            operators = {}
            operands = {str(node.declname) : 1}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.Typename'>"): #TypeName
        operators = {}
        operands = {str(node.name) : 1} #declname
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.Union'>"):
        operators = {'union' : 1, '{}' : 1, ', ;' : 1}
        operands = {str(node.name) : 1}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.UnaryOp'>"):
        operators = {str(node.op) : 1}
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.BinaryOp'>"):
        operators = {str(node.op) : 1}
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.TernaryOp'>"):
        if(node.iffalse is not None):
            operators = {':' : 1, '?' : 1}
            operands = {}
        else:
            operators = {':' : 1}
            operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.Assignment'>"):
        operators = {str(node.op) : 1, ', ;' : 1}
        operands = {}
        node_list = node.children()
        for child in node_list:
            oprt, oprn = parse_halstead(child)
            merge(operators, oprt)
            merge(operands, oprn)
        return (operators, operands)

    elif(str(type(node)) == "<class 'pycparser.c_ast.Constant'>"):
        return ({}, {node.value : 1})

class HalsteadMetrics():

    def __init__(self, operators, operands):
        self.operators = operators
        self.operands = operands
        self.n1 = len(operators.keys()) # 不同的 操作符 数量
        self.n2 = len(operands.keys())  # 不同的 操作数 数量
        self.N1 = list(accumulate(list(operators.values())))[-1] # 操作数 总数
        self.N2 = list(accumulate(list(operands.values())))[-1]  # 操作数 总数
        print "operators:"
        print operators
        #print "operands:"
        #print operands
        
    def programLength(self):
        N = self.N1 + self.N2
        N_ = math.log(self.n1, 2) + math.log(self.n2, 2)
        Nj = math.log(math.factorial(self.n1), 2) + math.log(math.factorial(self.n2), 2)
        Nb = self.n1*(math.sqrt(self.n1)) + self.n2*(math.sqrt(self.n2))
        Nc = self.n1*(math.sqrt(self.n1)) + self.n2*(math.sqrt(self.n2))
        Ns = ((self.n1+self.n2) * math.log(self.n1+self.n2, 2))/2
        N_return = N
        return N_return

    def programVocabulary(self):
        return (self.n1 + self.n2)

    def programVolume(self):
        return (self.programLength())*(math.log(self.programVocabulary(), 2))

    def programDifficulty(self):
        return (((self.n1)/2) * (self.N2)/(self.n2))

    def programLevel(self):
        return 1/(self.programDifficulty())

    def programMinimumVolume(self):
        return (self.programLevel() * self.programVolume())

    def programEffort(self):
        return (self.programDifficulty() * self.programVolume())

    def languageLevel(self):
        return (self.programVolume() * (1/math.sqrt(self.programDifficulty())))

    def intelligenceContent(self):
        return (self.programVolume())/(self.programDifficulty())

    def programmingTime(self):
        S = 60 * 60
        f = 18
        return (self.programEffort()/(f * S))

    def showMetrics(self):
        print('Program Length: ', self.programLength())          # 程序长度或简单长度
        print('Program Vocabulary:  ', self.programVocabulary()) # 程序词汇表长度
        print('Program Volume: ', self.programVolume())          # 程序体积或容量
        print('Program Difficulty: ', self.programDifficulty())  # 程序难度
        print('Program Level: ', self.programLevel())            # 程序级别
        print('Program Minimum Volume: ', self.programMinimumVolume())
        print('Program Effort: ', self.programEffort())          # 编程工作量
        print('Language Level: ', self.languageLevel())          # 语言级别
        print('Intelligence Content: ', self.intelligenceContent())
        print('Programming Time: ', self.programmingTime())      # 编程时间 小时

if __name__ == "__main__":

	arguments = sys.argv[1:]
	count = len(arguments)
	if(count < 0) : print("Insufficient arguments")

	ast = pycparser.parse_file("testp.c", use_cpp = True)
	main = ast.children()[-1]

	listOfOperators = parse_halstead(ast)[0]
	listOfOperands = parse_halstead(ast)[1]

	print('List of Operators : ', listOfOperators)
	print()
	print()
	print('List of Operands : ', listOfOperands)
	print()
	print("******Halstead Metrics******")
	hal_metric = HalsteadMetrics(listOfOperators, listOfOperands)
	hal_metric.showMetrics()
