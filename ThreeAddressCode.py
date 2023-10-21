from symboltable import *
#from parserC import *
from collections import defaultdict


class ThreeAddressCode:
    def __init__(self,operation,arg1,arg2,result):
        self.operation = {'Operation':operation}
        self.arg1 = {'ARG1':arg1}
        self.arg2 = {'ARG2':arg2}
        self.result = {'RESULT':result}
    
    def __str__(self,threeAddressCodeDict):
        for threeAddrCode in threeAddressCodeDict['Three Address Code']:
            isArg2 = False            
            #print(threeAddrCode.operation,threeAddrCode.arg1,threeAddrCode.arg2, threeAddrCode.result)
            if threeAddrCode.arg2['ARG2'] != None:
                isArg2 = True
            if threeAddrCode.operation['Operation'] != '=':
                print(threeAddrCode.result['RESULT'],'='
                      ,threeAddrCode.operation['Operation'],threeAddrCode.arg1['ARG1'])
            else:
                if isArg2 == False:
                    print(threeAddrCode.result['RESULT']
                      ,threeAddrCode.operation['Operation'],threeAddrCode.arg1['ARG1'])
                else:
                    print(threeAddrCode.result['RESULT'], '=',
                      threeAddrCode.arg1['ARG1'],threeAddrCode.operation['Operation'],
                      threeAddrCode.arg1['ARG2'])
    
threeAddressCodeDict = defaultdict(list)
ogVarName = None
def createThreeAddressCode(astTree, symbolTable):
    function_name = 'main'
    statementList = astTree[function_name]['Statement']
    for statement in statementList: 
        if '=' in statement:
            NUMBER_OF_CHILDREN = len(statement['=']) - 1
            #print(NUMBER_OF_CHILDREN)
            if NUMBER_OF_CHILDREN == 1:
                og_variable = list(statement['='].values())[-2]
                left_child = list(statement['='].values())[-1]
                threeAddrCode = ThreeAddressCode('=',left_child,None,og_variable)
                threeAddressCodeDict['Three_Address_Code'].append(threeAddrCode)
            else:
                og_variable = statement['='].pop('ID')
                threeAddressCodeDict = walk_through_ast(statement['='])
                #print(list(statement['='].values())[-1])
                #threeAddrCode = ThreeAddressCode('=', '')
                #threeAddressCodeDict['Three Address Code'].append
    return threeAddressCodeDict


visited_elements = []
def walk_through_ast(astSubTree):
    print("TREE",astSubTree)
    NUMBER_OF_CHILDREN = len(astSubTree)
    print("Children",NUMBER_OF_CHILDREN)
    #right_child = list(astSubTree.keys())[-1]
    #print(right_child)
    if type(astSubTree) is dict:
        left_child = list(astSubTree.keys())[-2]
        visited_elements.append(left_child)
        right_child = list(astSubTree.keys())[-1]
        visited_elements.append(right_child)
        #print(left_child,right_child)
    else:
        left_child = astSubTree[0]
        right_child = astSubTree[1]
    internal_nodes = ['+','-','*','/','%']
    
    if NUMBER_OF_CHILDREN == 2:
        print("right",right_child)
        if right_child in internal_nodes:
           
           return walk_through_ast(astSubTree[right_child])
           print(astSubTree[right_child])
           l_child = astSubTree[right_child][0]
           r_child = astSubTree[right_child][1]
           print("Left",l_child,"Right",r_child)  
        elif '+' in right_child:
           return walk_through_ast(right_child['+'])
           """
           r1_child = astSubTree[right_child][1]['+']
           print(len(r1_child))
           
           l2_child = astSubTree[right_child][1]['+'][0]
           r2_child = astSubTree[right_child][1]['+'][1]
           
           print(r1_child)
           print("Left",l2_child,"Right",r2_child)
          
           l3_child = astSubTree[right_child][1]['+'][1]['+'][0]
           r3_child = astSubTree[right_child][1]['+'][1]['+'][1]
           
           print("Left",l3_child,"Right",r3_child)
           

           #print(type(astSubTree['+']))
           #print(astSubTree[left_child])
           
           #print(astSubTree[right_child][0]['NUMBER'])
           #return walk_through_ast(astSubTree[right_child][0])
           """



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
    """
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
    """
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