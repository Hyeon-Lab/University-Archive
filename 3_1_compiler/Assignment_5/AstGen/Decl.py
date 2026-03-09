from Scanner.SourcePos import *
from AstGen.AST import *

class Decl(AST):
    def __init__(self, pos):
        super().__init__(pos)
        self._global = False
        self._index = -1
    
    def setGlobal(self):
        self._global = True
    
    def isGlobal(self):
        return self._global

