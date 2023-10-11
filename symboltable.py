class SymbolTable:
    def __init__(self):
        self.table = {}

    def addAFunction(self,name,return_type):
        self.table[name] = {}
        self.table[name]['Return_Type'] = return_type
        self.table[name]['Variables'] = {}
    def addAVariable(self,name,type,function):
        self.table[function]['Variables'][name] = type
         
    def lookUpVariable(self,name,function):
        if name not in self.table[function]['Variables']:
            raise SyntaxError("Variable not found")
        else:
            return self.table[function]['Variables'][name]
def main():
    symTable = SymbolTable()
    symTable.addAFunction("main","int")
    print(symTable.table)
    symTable.addAVariable("food","int","main")
    print(symTable.table)
    print(symTable.lookUpVariable("food","main"))
    print(symTable.table)
    #symTable.addAVariable("cream","double","main")
    #print(symTable.table)
    #symTable.addAFunction("bar","double")
    #symTable.addAVariable("wow", "int","bar")
    #{'main': {'Return_Type': 'int', 'Variables':{'food': 'int'}}}
    #print(symTable.table)
if __name__ == "__main__":
    main()