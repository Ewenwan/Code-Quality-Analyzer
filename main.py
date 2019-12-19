#_*_coding:utf-8_*_
# 代码复杂度
#import subprocess
import sys
#import pycparser
from pycparser import preprocess_file,c_parser
from parse_entropy import find_entropy
from cyclomatic_complexity import findComplexity
from halstead_metrics import *


class CodeQualityAnalyzer(object):

    def __init__ (self, file_name, entropy_subset_length = 5):

        #preprocess the file
        # print("Make sure to remove all the library includes")
        # subprocess.call("gcc -E -std=c99 -I/my_pycparser/utils/fake_libc_include " +
        #                            file_name +  " -o preprocessed.c")
        
        #from pycparser import preprocess_file,c_parser
        cpp_path = 'cpp'                      # 预处理 器 路径
        cpp_args=r'-Iutils/fake_libc_include' # command line arguments 预处理选项
        text = preprocess_file(file_name, cpp_path, cpp_args)
        parser = c_parser.CParser()
        #self.ast = pycparser.parse_file(file_name, use_cpp=True)
        self.ast =  parser.parse(text, file_name)
        self.entropy_subset_length = entropy_subset_length
        self.current_entropy_subset_length = 0
        
        #self.ast.show()
    
    # 混乱度 熵
    def calculate_entropy(self):
        
        if(self.current_entropy_subset_length < self.entropy_subset_length):

            self.current_entropy_subset_length = self.entropy_subset_length
            return find_entropy(self.ast, self.entropy_subset_length)
            
    # 圈复杂度
    def cyclomatic_complexity(self):
        
        no_of_vertices, no_of_edges = findComplexity(self.ast)
        return (no_of_edges - no_of_vertices + 2)
    
    # 复杂度
    def halstead_metrics(self):
        
        listOfOperators, listOfOperands = parse_halstead(self.ast)
        self.hal_metric = HalsteadMetrics(listOfOperators, listOfOperands)

    def print_metrics(self):

        print("Cyclometric complexity : ",self.cyclomatic_complexity())
        #print("\nHalstead Metrics\n")
        #self.halstead_metrics()
        #self.hal_metric.showMetrics()
        #print("\nEntropy : ", self.calculate_entropy())
        print("\n")


if __name__ == "__main__":

    arguments = sys.argv[1:]
    count = len(arguments)
    assert (count>0), "Not enough arguments"

    cqa = CodeQualityAnalyzer(sys.argv[1])
    cqa.print_metrics() 
