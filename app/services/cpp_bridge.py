import sys
import os

sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','..','cpp_lib'))

import cpp_core

class CppBridge:
    """C++组件桥接层"""

    _instance=None

    def __new__(cls):
        if cls._instance is None:
            cls._instance=super().__new__(cls)
            cls._instance._tokenizer=cpp_core.Tokenizer()
            cls._instance._calculator=cpp_core.Calculator()
        return cls._instance
    
    def tokenize(self,text: str,dict_words:set=None)->list:
        """中文分词器"""
        if dict_words:
            self._tokenizer.load_dict(dict_words)
        return self._tokenizer.tokenize(text)

    def calculate(self,expr:str)->float:
        """表达式求值"""
        return self._calculator.evaluate(expr)

cpp_bridge=CppBridge()
