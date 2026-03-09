class Frame:
    
    #
    # local variables in main (static methods):
    # 0: argv
    # 1: mc$
    #
    # local variables for all other MiniC functions (instance methods)
    # 0: "this" ptr
    #
    #

    def __init__(self, isMain):
        self.isMain = isMain
        self.LabelNr = -1
        if self.isMain:
            self.LocalVarNr = 1
        else:
            self.LocalVarNr = 0
    
    def getNewLabel(self):
        self.LabelNr += 1
        return self.LabelNr

    def getNewLocalVarIndex(self):
        self.LocalVarNr+=1
        return self.LocalVarNr
     
