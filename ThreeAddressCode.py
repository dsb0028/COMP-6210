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
og_variable = None
def createThreeAddressCode(astTree, symbolTable):
    function_name = 'main'
    statementList = astTree[function_name]['Statement']
    for statement in statementList: 
        if '=' in statement:
            NUMBER_OF_CHILDREN = len(statement['=']) - 1
            #print(NUMBER_OF_CHILDREN)
            if NUMBER_OF_CHILDREN == 1:
                #og_variable = list(statement['='].values())[-2]
                left_child = list(statement['='].values())[-1]
                #threeAddrCode = ThreeAddressCode('=',left_child,None,og_variable)
                #threeAddressCodeDict['Three_Address_Code'].append(threeAddrCode)
            else:
                global og_variable
                og_variable = statement['='].pop('ID')
                threeAddressCodeDict = walk_through_ast(statement['='])
                #print(list(statement['='].values())[-1])
                #threeAddrCode = ThreeAddressCode('=', '')
                #threeAddressCodeDict['Three Address Code'].append
    return threeAddressCodeDict


visited_elements = []
i = 1
def walk_through_ast(astSubTree):
    print("TREE",astSubTree)
    NUMBER_OF_CHILDREN = len(astSubTree)
    if NUMBER_OF_CHILDREN == 1:
        if '*' in astSubTree[0] or '/' in astSubTree[0] or '%' in astSubTree[0]:
            NUMBER_OF_CHILDREN = NUMBER_OF_CHILDREN + 1
            print("Uh")
    print("Children",NUMBER_OF_CHILDREN)
    
    if type(astSubTree) is dict:
        

        left_child = list(astSubTree.values())[-2]
        
        right_child = list(astSubTree.keys())[-1]
        if NUMBER_OF_CHILDREN == 3:
            NUMBER_OF_CHILDREN = NUMBER_OF_CHILDREN - 1
            left_child = list(astSubTree.values())[-3]
            #right_child = list(astSubTree.values())[-2]
            right_child = '*'
        visited_elements.append(left_child)
       
        print("HMM",left_child,right_child)
        #visited_elements.append(right_child)
        #print(left_child,right_child)
    else:
        left_child = list(astSubTree[0].values())[0]
        if list(visited_elements[-1])[0] != 't':
            visited_elements.append(left_child)
        
        if NUMBER_OF_CHILDREN == 2:
            if '*' in astSubTree[0] or '/' in astSubTree[0] or '%' in astSubTree[0]:
                #print("P",astSubTree[0]['*'])
                right_child = {'*':astSubTree[0]['*']}
                #print("R",right_child)
                #right_child =  dict(astSubTree[0]['*'].pop())
                #right_child =  astSubTree[0]
            else:
                right_child = astSubTree[1]
                #print("R",right_child)
        else:
            #print("wee")
            right_child = None
        
    #print("Left",left_child,"Right",right_child)
    internal_nodes = ['+','-','*','/','%']
    
    if right_child == None and NUMBER_OF_CHILDREN == 1:
        print(visited_elements)
        if len(visited_elements) == 3:
            threeAddressCode  = ThreeAddressCode(visited_elements[1],
                                              visited_elements[0],
                                              visited_elements[2],
                                              og_variable)
            threeAddressCodeDict['Three_Address_Code'].append(threeAddressCode)
            return threeAddressCodeDict
        else:
            global i
            threeAddressCode  = ThreeAddressCode(visited_elements[-2],
                                              visited_elements[-3],
                                              visited_elements[-1],
                                              "t" + str(i))
            threeAddressCodeDict['Three_Address_Code'].append(threeAddressCode)
            visited_elements[-3] = "t" + str(i)
            visited_elements.pop(-2)
            visited_elements.pop(-1)
            print(visited_elements)
            i = i + 1
            return walk_through_ast(astSubTree)
    
    
    if NUMBER_OF_CHILDREN == 2:
        print("right",right_child)
        if type(right_child) is not str: 
            operator_type = list(right_child.keys())[0]
        if right_child in internal_nodes:
           #print("wow")
           visited_elements.append(right_child)
           #i = i + 1
           print("H",astSubTree[right_child])
           return walk_through_ast(astSubTree[right_child]) 
           #return walk_through_ast(astSubTree)           

        elif operator_type in internal_nodes:
            #print("wo1")
           visited_elements.append(operator_type)
           print("V",visited_elements)
           #i = i + 1
           return walk_through_ast(right_child[operator_type])
         



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