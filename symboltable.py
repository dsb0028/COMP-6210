class SymbolTable:
    def __init__(self):
        self.table = {}

    def addAFunction(self,name,return_type):
        self.table[name] = {}
        self.table[name]['Return_Type'] = return_type
        self.table[name]['Variables'] = {}
    
    def addAVariable(self,name,type,function):
        #type1 = self.lookUpVariable(name,function)
        """
        if type1 == type:
            raise SyntaxError(["Variable already has been defined",name])
        """
        self.table[function]['Variables'][name] = type
         
    def lookUpVariable(self,name,function):
        if self.table[function]['Variables'].get(name):
            return self.table[function]['Variables'][name]
        else:
            return None
def main():
    symTable = SymbolTable()
    symTable.addAFunction("main","int")
    print(symTable.table)
    symTable.addAVariable("food","int","main")
    symTable.lookUpVariable("food","main")
    #print(symTable.table)
    #symTable.addAVariable("cream","double","main")
    #print(symTable.table)
    #symTable.addAFunction("bar","double")
    #symTable.addAVariable("wow", "int","bar")
    #{'main': {'Return_Type': 'int', 'Variables':{'food': 'int'}}}
    #print(symTable.table)
if __name__ == "__main__":
    main()