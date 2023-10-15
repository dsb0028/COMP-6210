from symboltable import *
#from parserC import *
from collections import defaultdict
"""
class ThreeAddressCode():
    def __init__(self,parseTree):
        self.parseTree = parseTree
        self.threeAddressCode = {}
"""    
"""
Initalize a variable that is of the same type as the return type of each function
For example, if the return_type of main() is of type int, 
int A.####;, where #### is a 4-digit randomly generated number
for each declaration
"""
threeAddressCode = defaultdict(list)
assignStmtAddrCode = []
returnVariable = None
def createThreeAddressCode(astTree,symbolTable):
    for item in recursive_items(astTree):
        if item == 'main':
            threeAddressCode['function'] = item
            threeAddressCode['LBRACE'].append('{')
        elif item[1] == '{':
            #print(item)
            threeAddressCode['LBRACE'].append(item[1])
            #print(threeAddressCode)
        elif item[0] == 'Declaration':
            for decl in astTree['main']['Declaration']:
                print("Decl",decl)
                if decl.get('='):
                    var = None
                    var_type = None
                    for operandType in decl.get('='):
                        if operandType == 'ID':
                            var = decl['='][operandType]
                            var_type = symbolTable.lookUpVariable(var,'main') 
                            #global assignStmtAddrCode
                            assignStmtAddrCode.extend([var_type,decl['='][operandType],';'])
                            
                            threeAddressCode['Assign'].append(assignStmtAddrCode)
                else:
                    var = None
                    var_type = None
                    for operandType in decl:
                        if operandType == 'ID':
                            var = decl[operandType]
                            var_type = symbolTable.lookUpVariable(var,'main') 
                            #global assignStmtAddrCode
                            assignStmtAddrCode.append([var_type,decl[operandType],';'])
                            threeAddressCode['Assign'].append(assignStmtAddrCode)
        
        elif item[0] == 'Statement':
            for stmt in astTree['main']['Statement']:
                if stmt.get('='):
                    for operandType in stmt.get('='):
                        if operandType == 'ID':
                            assignStmtAddrCode.append([stmt['='][operandType],'='])
                        elif operandType == 'NUMBER':
                            assignStmtAddrCode.append([stmt['='][operandType],';'])
                if stmt.get('return'):
                    for operandType in stmt.get('return'):
                        if operandType == 'NUMBER':
                            if type(stmt['return'][operandType]) == int:
                                global returnVariable
                                returnVariable = 'D.1914'
                                assignStmtAddrCode.append([returnVariable,'=',stmt['return'][operandType],';'])
                                assignStmtAddrCode.append(['return',returnVariable,';'])
                                threeAddressCode['LBRACE'].append(['int', returnVariable,';'])
            #print(threeAddressCode)
        elif item[1] == '}':
            #print(item)
            threeAddressCode['RBRACE'].append(item)
            threeAddressCode['main'].append([assignStmtAddrCode[-2], assignStmtAddrCode[-1]])
            
            print(threeAddressCode)
        print(item)
    """
    for key,val in astTree.items():
        print(key, val)
    """
    #terminalNodes.clear()
    #findTerminalNodes(astTree)
    #print(terminalNodes)
    return threeAddressCode

def recursive_items(dictionary):
    for key, value in dictionary.items():
        if type(value) is dict:
            yield key
            yield from recursive_items(value)
        else:
            yield (key, value)