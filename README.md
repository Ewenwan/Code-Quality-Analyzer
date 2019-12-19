# Code Quality Analyzer
Carried Static code Analysis using Code 
Quality Metrics(代码质量度量 ) like 
Maintainability Index(可维护性指数), Halstead Metrics(复杂度) and Cyclomatic Complexity(圈复杂度).
All the code is implemented in python and the code quality analysis is performed/tested on C programs.


Halstead 方法的优点
不需要对程序进行深层次的分析，就能够预测错误率，预测维护工作量；
有利于项目规划，衡量所有程序的复杂度；
计算方法简单；
与所用的高级程序设计语言类型无关。
Halstead 方法的缺点
仅仅考虑程序数据量和程序体积，不考虑程序控制流的情况；
不能从根本上反映程序复杂性。


圈复杂度(Cyclomatic Complexity)是一种代码复杂度的衡量标准。
它可以用来衡量一个模块判定结构的复杂程度，数量上表现为独立线性路径条数，
也可理解为覆盖所有的可能情况最少使用的测试用例数。
圈复杂度大说明程序代码的判断逻辑复杂，可能质量低且难于测试和维护。
程序的可能错误和高的圈复杂度有着很大关系。
圈复杂度主要与分支语句（if、else、，switch 等）的个数成正相关。
当一段代码中含有较多的分支语句，其逻辑复杂程度就会增加。 
