from symboltable import *
#from parserC import *
from collections import defaultdict


"""
Initalize a variable that is of the same type as the return type of each function
For example, if the return_type of main() is of type int, 
int A.####;, where #### is a 4-digit randomly generated number
for each declaration
"""

class ThreeAddressCode:
    def __init__(self,operation,arg1,arg2,result):
        self.operation = {'OP':operation}
        self.arg1 = {'ARG1':arg1}
        self.arg2 = {'ARG2':arg2}
        self.result = {'RESULT':result}


threeAddressCodeDict = defaultdict(list)
def createThreeAddressCode(astTree, symbolTable):
    operator = None
    arg1 = None
    arg2 = None
    result = None
    for item in recursive_items(astTree):
        if item[0] == 'Statement':
            for stmt in astTree['main']['Statement']:
                if stmt.get('='):
                    operator = '='
                    for operandType in stmt.get('='):
                        if operandType == 'ID':
                            if arg1 == None:
                                arg1 = stmt['='][operandType]
                            elif arg2 == None:
                                arg2 = stmt['='][operandType]
                        elif operandType == 'NUMBER':
                            if arg1 == None:
                                arg1 = stmt['='][operandType]
                            elif arg2 == None:
                                arg2 = stmt['='][operandType]
                    threeAdrCode = ThreeAddressCode(operator,arg1,arg2,None)
                    threeAddressCodeDict['Three Address Code'].append(threeAdrCode)
    return threeAddressCodeDict




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
                #print("Decl",decl)
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
    
    for key,val in astTree.items():
        print(key, val)
    
    #terminalNodes.clear()
    #findTerminalNodes(astTree)
    #print(terminalNodes)
    return threeAddressCode

"""
def recursive_items(dictionary):
    for key, value in dictionary.items():
        if type(value) is dict:
            yield key
            yield from recursive_items(value)
        else:
            yield (key, value)
def main():
    #threeAddressCodeDict = list()
    #threeAddressCode = ThreeAddressCode("=","4",None,'d')
    #threeAddressCodeDict.append(threeAddressCode)
    #threeAddressCode = ThreeAddressCode()
    #print(threeAddressCode.operation,threeAddressCode.arg1, threeAddressCode.arg2,threeAddressCode.result)
    astTree = {'=': {'ID': 'a', '+': [{'NUMBER': 3}, {'*': [{'NUMBER': 4}, {'NUMBER': 5}]}]}}
    #astTree = {'main': {'LBRACE': '{', 'Statement': [{'=': {'ID': 'a', '+': [{'NUMBER': 3}, {'*': [{'NUMBER': 4}, {'NUMBER': 5}]}]}}, {'return': {'NUMBER': 0}}], 'RBRACE': '}'}} 
    threeAddressCode = list()
    operatorsFound = []
    operators = ['+','-','*','/']
    for item in recursive_items(astTree):
        if item[0] == '=':
            for operand in astTree[item].items():
                if operand[0] in operators:
                    operatorsFound.append(operand[0])
                    threeAddressCode.append({operand[0]:[]})
                    for op in operand[1]:
                        k = op.keys()
                        for key in k:
                            if key in operators:
                                operatorsFound.append(key)
                        if op.keys() in operators:
                            pass
                else:
                    threeAddressCode.append(operand[1])
    
    print(threeAddressCode) 
    print(operatorsFound)
    print(astTree)
    print(astTree['=']['+'][1])
    r1 = astTree['=']['+'][1]
    astTree['=']['+'][1] = "r1"
    print("r1",r1)
    print(astTree)

    threeAddressCode = [[{'=':{"tempVar","r1"}},r1],astTree]
    #iterate through the astTree and log all operations in the order that they have been visited
    #find the index of the last operation to be found in the astTree
    #assign the ast at that index to a temporary variable r1
    #add it a table to keep track of all variables created and their values
    #need to be able to replace the last operation found in the ast with the tempoerary variable
    #,which points to the subtree being replaced.
    # an ast will be created from the temporary variable along with the values that it is pointing too 
    print(threeAddressCode)
if __name__ == "__main__":
    main()