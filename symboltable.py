class SymbolTable:
    def __init__(self):
        self.entries = []

    def addAFunction(self,name,type):
        isFunctionInTable = self.lookUpFunction(name)
        if isFunctionInTable == False:
            self.entries.append(['Function:',[name,type]])
        else:
            raise SyntaxError("Hold on there Tiger")
            
    def addAVariable(self,name,type,function):
        isVariableInTable = self.lookUpVariable(name,function)
        if isVariableInTable == False:
            self.entries.append(['Variable:',[name,type,function]])
        else:
            raise SyntaxError("Variable Naming Conflict: Two Vars cannot have the same name")
    
    def lookUpVariable(self,name,function):
        variables = [entry for entry in self.entries if entry[0] == 'Variable:']
        foundVariable = False
        for var in variables:
            varName = var[1][0]
            functName = var[1][2]
            if varName == name and functName == function:
                foundVariable = True
        return foundVariable

    def lookUpFunction(self,function):
        functions = [entry for entry in self.entries if entry[0] == 'Function:']
        foundFunction = False
        for fun in functions:
            funName = fun[1][0]
            if funName == function:
                foundFunction = True
        return foundFunction

def main():
    symTable = SymbolTable()
    symTable.addAFunction("main","int")
    symTable.addAFunction("bar",'float')
    symTable.addAVariable("igloo",'double', "bar")
    print(symTable.entries)
    print(symTable.lookUpVariable('blue','bar'))
    print(symTable.lookUpFunction('main'))
    symTable.addAVariable('bar', 'int','main')
    #symTable.addAFunction('main', 'float')
    print(symTable.entries)
    #symTable.addAFunction("main",'float')
    #symTable.addAVariable('igloo','float','bar')
    
if __name__ == "__main__":
    main()