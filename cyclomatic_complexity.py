#coding:utf-8
# 圈复杂度
'''
圈复杂度(Cyclomatic complexity)是一种代码复杂度的衡量标准，在1976年由Thomas J. McCabe, Sr. 提出。
在软件测试的概念里，圈复杂度用来衡量一个模块判定结构的复杂程度，
数量上表现为线性无关的路径条数，即合理的预防错误所需测试的最少路径条数。
圈复杂度大说明程序代码可能质量低且难于测试和维护，
根据经验，程序的可能错误和高的圈复杂度有着很大关系。

圈复杂度主要与分支语句（if、else、，switch 等）的个数成正相关。
当一段代码中含有较多的分支语句，其逻辑复杂程度就会增加。
在计算圈复杂度时，可以通过程序控制流图方便的计算出来。


通常使用的计算公式是
V(G) = e – n + 2 , 
e 代表在控制流图中的边的数量（对应代码中顺序结构的部分），
n 代表在控制流图中的节点数量，
包括起点和终点（
1、所有终点只计算一次，即便有多个return或者throw；
2、节点对应代码中的分支语句）。

采用圈复杂度去衡量代码的好处:
1.指出极复杂模块或方法，这样的模块或方法也许可以进一步细化。
2.限制程序逻辑过长。
    McCabe&Associates 公司建议尽可能使 V（G） <= 10。
    NIST（国家标准技术研究所）认为在一些特定情形下，模块圈复杂度上限放宽到 15 会比较合适。
    因此圈复杂度 V（G）与代码质量的关系如下： 
    V（G） ∈ [ 0 , 10 ]：代码质量不错； 
    V（G） ∈ [ 11 , 15 ]：可能存在需要拆分的代码，应当尽可能想措施重构； 
    V（G） ∈ [ 16 , ∞ )：必须进行重构；


3.方便做测试计划，确定测试重点。
    许多研究指出一模块及方法的圈复杂度和其中的缺陷个数有相关性，
    许多这类研究发现圈复杂度和模块或者方法的缺陷个数有正相关的关系：
    圈复杂度最高的模块及方法，
    其中的缺陷个数也最多，做测试时做重点测试。

'''
import pycparser

dictionary = {}

def findComplexity(ast):
    total_node = 0
    total_edgit = 0
    children = ast.children()
    #print(children)
    
    # 先生成一个函数查找字典
    for child in children:
        
        if str(type(child[1])) == "<class 'pycparser.c_ast.FuncDef'>":
            # 函数定义
            dictionary[str(child[1].decl.name)] = child[1].body # 函数名: 函数体
    
    # 递归计算每一个函数的圈复杂度
    for child in children:
        if str(type(child[1])) == "<class 'pycparser.c_ast.FuncDef'>":
            nn, ne = funcComplexity(child[1].body)
            #print (str(child[1].decl.name), "- no of vertices and edges", ":", nn, ne)
            print ("func: %s, vertices: %d , edges: %d" % (str(child[1].decl.name), nn, ne))
            
            # 统计从main函数开始的圈复杂度
            if(str(child[1].decl.name) == 'memmgr_alloc'):
                total_node = nn
                total_edgit = ne
    
    return total_node, total_edgit

    
def parser_one(item,nn,ne):
    #print(type(item))
    if ((str(type(item)) == "<class 'pycparser.c_ast.Assignment'>") or
        (str(type(item)) == "<class 'pycparser.c_ast.UnaryOp'>") or
        (str(type(item)) == "<class 'pycparser.c_ast.BinaryOp'>")):
        nn, ne = nn+1, ne+1

    elif str(type(item)) == "<class 'pycparser.c_ast.If'>":
        nn1, ne1 = funcComplexity(item.iftrue)
        nn2, ne2 = funcComplexity(item.iffalse)
        # if 分支两个边 一个节点, 再加上各自true/false分支的圈复杂度
        nn, ne = (1 + nn1 + nn2 + nn), (2 + ne1 + ne2 + ne)

    elif str(type(item)) == "<class 'pycparser.c_ast.For'>":
        nn3, ne3 = funcComplexity(item.stmt)
        nn, ne = (3 + nn3 + nn), (4 + ne3 + ne)

    elif str(type(item)) == "<class 'pycparser.c_ast.While'>":
        nn4, ne4 = funcComplexity(item.stmt)
        nn, ne = (1 + nn4 + nn), (2 + ne4 + ne)

    elif str(type(item)) == "<class 'pycparser.c_ast.Break'>":
        nn8, ne8 = 1, 1
        nn, ne = (nn8 + nn), (ne8 + ne)

    elif str(type(item)) == "<class 'pycparser.c_ast.FuncCall'>":
        # 系统级的函数调用 默认节点数和 边数 均为1
        if(str(item.name.name) == 'printf' or
            str(item.name.name) == 'scanf'):
            nn5, ne5 = 1, 1
            nn, ne = (nn5 + nn), (ne5 + ne)
        else:
            nn6, ne6 = funcComplexity(dictionary[str(item.name.name)])
            nn, ne = (1 + nn6 + nn), (2 + ne6 + ne)
    
    # 接收节点Return  边记为1  节点不记录
    elif str(type(item)) == "<class 'pycparser.c_ast.Return'>":
        nn7, ne7 = 1, 0
        nn, ne = (nn7 + nn), (ne7 + ne)
        
    return (nn, ne)
    
def funcComplexity(child):
    # 输入为函数体
    if (child is None):
        return (0, 0)
    nn = 0  # 节点数
    ne = 0  # 边数
    try:
        for item in child.block_items:
            nn,ne = parser_one(item,nn,ne)
    except:
        nn,ne = parser_one(child,nn,ne)
    return (nn, ne)

if __name__ == "__main__":
	ast = pycparser.parse_file("testp.c", use_cpp=True)
	no_of_vertices, no_of_edges = findComplexity(ast)
	print("Cyclomatic Complexity:", no_of_edges - no_of_vertices + 2) 
