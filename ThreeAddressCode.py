from symboltable import *
#from parserC import *
from collections import defaultdict


class ThreeAddressCode:
    def __init__(self,operation,arg1,arg2,result, statement):
        if (statement == 'Assignment_Statement'):
            self.operation = {'Operation':operation}
            self.arg1 = {'ARG1':arg1}
            self.arg2 = {'ARG2':arg2}
            self.result = {'RESULT':result}
            self.statement = {'STATEMENT':statement}
        elif statement == 'return':
            self.operation = {'Operation':operation}
            self.arg1 = {'ARG1':arg1}
            self.arg2 = {'ARG2':arg2}
            self.result = {'RESULT':result}
            self.statement = {'STATEMENT':statement}
            #self.statement = {'STATEMENT':statement}
            #self.arg1 = {'ARG1':arg1}
    """
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
    """
threeAddressCodeDict = defaultdict(list)
og_variable = None
statement_type = None
def createThreeAddressCode(astTree, symbolTable):
    function_name = 'main'
    statementList = astTree[function_name]['Statement']
    for statement in statementList: 
        global visited_elements
        visited_elements = []
        if '=' in statement:
            global statement_type
            statement_type = 'Assignment_Statement'
            global og_variable
            og_variable = statement['='].pop('ID')
            print(og_variable)
            #global threeAddressCodeDict
            threeAddressCodeDict = walk_through_ast(statement['='])
            print(threeAddressCodeDict)
        elif 'return' in statement:
            statement_type = 'return'
            threeAddressCode1 = walk_through_ast(statement['return'])
    return threeAddressCodeDict

visited_elements = []
i = 1
isMultOperation = False
lastElem = None
def walk_through_ast(astSubTree):
    print("TREE",astSubTree)
    NUMBER_OF_CHILDREN = len(astSubTree)
    print(NUMBER_OF_CHILDREN)
    if NUMBER_OF_CHILDREN == 1:
       if type(astSubTree) is list:
        if '*' in astSubTree[0] or '/' in astSubTree[0] or '%' in astSubTree[0]:
            NUMBER_OF_CHILDREN = NUMBER_OF_CHILDREN + 1
    print("Children",NUMBER_OF_CHILDREN)
    
    if type(astSubTree) is dict:       
        if NUMBER_OF_CHILDREN == 2:
            left_child = list(astSubTree.values())[-2]
            visited_elements.append(left_child)
            right_child = list(astSubTree.keys())[-1]
            #visited_elements.append(right_child)
        elif NUMBER_OF_CHILDREN == 1:
            left_child = list(astSubTree.values())[-1]
            visited_elements.append(left_child)
            right_child = None
        #if right_child:
            
        #print(right_child)
        if NUMBER_OF_CHILDREN == 3:
            #NUMBER_OF_CHILDREN = NUMBER_OF_CHILDREN - 1
            left_child = list(astSubTree.values())[-3]
            visited_elements.append(left_child)
            #print(visited_elements)
            #print(list(astSubTree.keys())[-2])
            #right_child = list(astSubTree.values())[-2]
            right_child = list(astSubTree.keys())[-2]
            #visited_elements.append(right_child)
            #print(visited_elements)
            NUMBER_OF_CHILDREN = NUMBER_OF_CHILDREN - 1
        #visited_elements.append(left_child)

    else:
        left_child = list(astSubTree[0].values())[0]
        if list(visited_elements[-1])[0] != 't':
            visited_elements.append(left_child)
        
        if NUMBER_OF_CHILDREN == 2:
            if '*' in astSubTree[0] or '/' in astSubTree[0] or '%' in astSubTree[0]:
                right_child = {'*':astSubTree[0]['*']}
            else:
                right_child = astSubTree[1]
                #print("r",right_child)
        elif NUMBER_OF_CHILDREN == 1:
            """
            global isMultOperation
            if isMultOperation == True:
                print("l",len(list(astSubTree)))
                #visited_elements.append('+')
            """
            right_child = None
        
    internal_nodes = ['+','-','*','/','%']
    
    if right_child == None and NUMBER_OF_CHILDREN == 1:
        print(visited_elements)
        """
        global lastElem
        if lastElem:
            visited_elements.append(lastElem[0]['NUMBER'])
            print("v", visited_elements)
        """
        """
        if statement_type == 'return':
            threeAddressCode =  ThreeAddressCode(None, 
                                                 visited_elements[0],
                                                 None,
                                                 None,statement_type)
            #return threeAddressCodeDict
        """
        global statement_type
        if len(visited_elements) == 3:
            threeAddressCode  = ThreeAddressCode(visited_elements[1],
                                              visited_elements[0],
                                              visited_elements[2],
                                              og_variable,statement_type)
            #lastElem = None
            threeAddressCodeDict['Three_Address_Code'].append(threeAddressCode)
            return threeAddressCodeDict
        
        elif len(visited_elements) >= 3:
            global i
            threeAddressCode  = ThreeAddressCode(visited_elements[-2],
                                              visited_elements[-3],
                                              visited_elements[-1],
                                              "t" + str(i),statement_type)
            threeAddressCodeDict['Three_Address_Code'].append(threeAddressCode)
            visited_elements[-3] = "t" + str(i)
            visited_elements.pop(-2)
            visited_elements.pop(-1)
            print(visited_elements)
            #lastElem = None
            i = i + 1
            return walk_through_ast(astSubTree)
        
        elif statement_type == 'return':
            threeAddressCode  = ThreeAddressCode(None,
                                              visited_elements[0],
                                              None,None,statement_type)
            threeAddressCodeDict['Three_Address_Code'].append(threeAddressCode)
            #return threeAddressCodeDict
        else:
            threeAddressCode  = ThreeAddressCode('=',
                                              visited_elements[0],
                                              None,
                                              og_variable,statement_type)
            threeAddressCodeDict['Three_Address_Code'].append(threeAddressCode)    
            return threeAddressCodeDict
    
    if NUMBER_OF_CHILDREN == 2:
        if type(right_child) is not str: 
            operator_type = list(right_child.keys())[0]
        if right_child in internal_nodes:
            #print(right_child)
            visited_elements.append(right_child)
            print(astSubTree[right_child])
            print("Length",len(list(astSubTree.values())), visited_elements
                 ,list(astSubTree.keys())[-1])
            if len(list(astSubTree.values())) == 3:
                isMultOperation = True
                lastElem = list(astSubTree.keys())[-1]
                """
                if '+' in astSubTree or '-' in astSubTree:
                    visited_elements.append('+')
                    #return walk_through_ast(right_child['*'])
                """
            return walk_through_ast(astSubTree[right_child])            

        elif operator_type in internal_nodes:
           #print("p",operator_type)
           visited_elements.append(operator_type)
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