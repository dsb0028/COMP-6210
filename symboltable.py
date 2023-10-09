class SymbolTable:
    def __init__(self):
        self.table = {}

    def addAFunction(self,name):
        self.table[name] = {}
    
    def addAVariable(self,name,type,function):
        self.table[function][name] = type
    
    def lookUpVariable(self,name,function):
        if name not in self.table[function]:
            raise SyntaxError("Variable not found")
        else:
            return self.table[function][name]
def main():
    symTable = SymbolTable()
    symTable.addAFunction("main")
    print(symTable.table)
    symTable.addAVariable("food","int","main")
    print(symTable.table)
    symTable.addAVariable("cream","double","main")
    print(symTable.table)
    symTable.addAFunction("bar")
    print(symTable.table)
if __name__ == "__main__":
    main()