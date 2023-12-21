class SymbolTable:
    def __init__(self):
        self.table = {}
        #self.table['Functions'] = {}
        self.table['Globals'] = {}

    def addAFunction(self,name,return_type):
        self.table[name] = {}
        self.table[name]['Return_Type'] = return_type
        self.table[name]['Parameters'] = {}
        self.table[name]['Locals'] = {}

    def addAVariable(self,name,type,scope,function=None):
        #type1 = self.lookUpVariable(name,function)
        """
        if type1 == type:
            raise SyntaxError(["Variable already has been defined",name])
        """
        if scope == 'local':
            self.table[function]['Locals'][name] = type
        elif scope == 'global':
            self.table['Globals'][name] = type
    
    def addAParameter(self,name,type,function):
        self.table[function]['Parameters'][name] = type
         
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