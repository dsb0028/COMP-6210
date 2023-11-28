from symboltable import *
#from parserC import *
from collections import defaultdict
import copy

class ThreeAddressCode:
    def __init__(self,operation,arg1,arg2,result,statement):
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
temps = []
"""
parentNode  = None
branch1 = None
branch2 = None
left_branch_temp = None
right_branch_temp = None
"""
def createThreeAddressCode(astTree, symbolTable):
    function_name = 'main'
    statementList = astTree[function_name]['Statement']
    for statement in statementList: 
        global visited_elements
        visited_elements = []
        global parentNode
        parentNode = None
        global left_branch_temp
        left_branch_temp = None
        global right_branch_temp
        right_branch_temp = None
        global branch1,branch2
        branch1 = None
        branch2 = None
        if '=' in statement:
            global statement_type
            statement_type = 'Assignment_Statement'
            #print(statement['='])
            global og_variable
            
            og_variable = statement['='][0].pop('ID')
            #print(og_variable)
            #print(statement['='][1])
            statement['='][0] = statement['='][1]
            statement['='].pop(1)
            #print(statement['='])
            #global threeAddressCodeDict
            #breakpoint()
            global number_of_nodes
            number_of_nodes = totalNodes(statement['='][0])
            walk_through_ast(statement['='][0])
            #breakpoint()
            if temp_dicts != {}:
                last_temp_var = list(temp_dicts)[-1]
                temp_dicts[og_variable] = temp_dicts.pop(last_temp_var)
            else:
                temp_dicts.update({og_variable:statement['='][0]})
            #print("Dict",threeAddressCodeDict)
            #breakpoint()
            #breakpoint()
            print(temp_dicts)
        elif 'return' in statement:
            statement_type = 'return'
            number_of_nodes = totalNodes(statement['return'][0])
            walk_through_ast(statement['return'][0])
        temps.append(copy.deepcopy(temp_dicts))
        temp_dicts.clear()
    #breakpoint()
    for temp in temps:
        #print(temp)
        for item in temp.items():
            stmt = None
            operator = None
            op1 = None
            op2 = None
            res = None
            if item[0] == 'return':
                stmt = 'return'
                operator = list(item[1].keys())[0]
                if operator not in ['+','-','*','/']:
                    op1 = item[1][operator]
                    operator = None
            else:
                stmt = 'Assignment_Statement'
                operator = list(item[1].keys())[0]
                op2 = item[1][operator][1]
                if type(op2) is dict:
                    key = list(op2.keys())[0]
                    op2 = op2[key]
                res = item[0]
                #breakpoint()
                op1 = item[1][operator][0]
                if type(op1) is dict:
                    key = list(op1.keys())[0]
                    op1 = op1[key]
           
            
            threeAddressCode =  \
                ThreeAddressCode(operation=operator
                                 ,arg1=op1,arg2=op2,result=res,statement=stmt)
            threeAddressCodeDict['Three_Address_Code'].append(threeAddressCode)
    #print(threeAddressCodeDict)
    return threeAddressCodeDict


visited_elements = []
temp_dicts = {}
visited = None
l_temp = None
r_temp = None
temp_root = None
i = 1




"""
def walk_through_ast(root):
    left = None
    right = None
    internal_nodes = ['+','-','*','/']
    if root:
        root_key = list(root.keys())[0]
        global parentNode,branch1,branch2

        if parentNode == None:
            parentNode = (root_key, root[root_key])
            branch1 = root[root_key][0]
            branch2 = root[root_key][1]
        if root_key in internal_nodes:
            children = root[root_key]
            left = children[0]
            right = children[1]
            if list(left.keys())[0] == 'NUMBER' \
                and list(right.keys())[0] == 'NUMBER':
                temp_dicts.update({"t"+str(i):root})
            breakpoint()
            walk_through_ast(left)
            if branch1 == left:
                print("cool")
                global left_branch_temp
                
            breakpoint()
            walk_through_ast(right)
            if branch2 == right:
                global right_branch_temp
                
            #print(visited_elements)
           
        else:
            breakpoint()
            print(branch1,left_branch_temp)
"""
isLeftTerminalNode = False
isRightTerminalNode = False
def walk_through_ast(root):
    internal_nodes = ['+','-','*','/']
    left = None
    right = None
    if root:
        root_key = list(root.keys())[0]
        if root_key in internal_nodes:
            children = root[root_key]
            left = children[0]
            right = children[1]
            walk_through_ast(left)
            visited_elements.append(root_key)
            walk_through_ast(right)
            global i
            #breakpoint()
            """
            if number_of_nodes == len(visited_elements):
                temp_dicts.update({og_variable:root})
            """
            m = [item for item in temp_dicts.items() if item[1] == left]
            if list(left.keys())[0] in internal_nodes:
                if m != []:
                    root[root_key][0] = m[0][0]
                    left = root[root_key][0]
            m1 = [item for item in temp_dicts.items() if item[1] == right]
            if list(right.keys())[0] in internal_nodes:
                if m1 != []:
                    root[root_key][1] = m1[0][0]
                    right = root[root_key][1]
            global isLeftTerminalNode,isRightTerminalNode
            if type(left) is str or list(left.keys())[0] not in internal_nodes:
                isLeftTerminalNode = True 
            if type(right) is str or list(right.keys())[0] not in internal_nodes:
                isRightTerminalNode = True
            if isLeftTerminalNode == True and isRightTerminalNode == True:
                temp_dicts.update({"t"+str(i):root})
                i = i + 1
                isLeftTerminalNode = False
                isRightTerminalNode = False 
        else:
            visited_elements.append(root[root_key])
            if number_of_nodes == len(visited_elements):
                if statement_type == 'return':
                    temp_dicts.update({statement_type:root})
                """
                else:
                    temp_dicts.update({og_variable:root})
                """
"""
def walk_through_ast(root):
    left = None
    right = None
    internal_nodes = ['+','-','*','/']
    if root:
        root_key = list(root.keys())[0]
        global parentNode,branch1,branch2

        if parentNode == None:
            parentNode = (root_key, root[root_key])
            branch1 = root[root_key][0]
            branch2 = root[root_key][1]
        if root_key in internal_nodes:
            children = root[root_key]
            left = children[0]
            right = children[1]
            breakpoint()
            
            l_key = list(left.keys())[0] 
            if l_key in internal_nodes \
                and left[l_key][0] not in internal_nodes \
                and left[l_key][1] not in internal_nodes:
                left[l_key] = 't1'
        
            walk_through_ast(left)
            if branch1 == left:
                print("cool")
                global left_branch_temp
                left_branch_temp = visited_elements[0]
                visited_elements.clear()
            breakpoint()
            #visited = visited_elements
            #print(visited)
            
            if len(children) == 2:
                right = children[1]
            
            if visited_elements != []:
                if len(visited_elements) == 1:
                    if type(visited_elements[0]) is str \
                        and root_key in internal_nodes:
                        m = [item for item in temp_dicts.items() if item[1] == left]
                        if m != []:
                            root[root_key][0] = m[0][0]
                            left = m[0][0]
                            
                visited_elements.append(root_key)
            walk_through_ast(right)
            if branch2 == right:
                global right_branch_temp
                print("way cooler")
                print(visited_elements)
                right_branch_temp = visited_elements[0]
                visited_elements.clear()
            #print(visited_elements)
           
        else:
            breakpoint()
            print(branch1,left_branch_temp)
            
            visited_elements.append(root[root_key])
            global i
            if len(visited_elements) == 3:
                #temps.append( "t" + str(i))
                threeAddressCode  = ThreeAddressCode(visited_elements[1],
                                              visited_elements[0],
                                              visited_elements[2],
                                              "t" + str(i),statement_type)
                threeAddressCodeDict['Three_Address_Code'].append(threeAddressCode)
                                
                visited_elements[-3] = "t" + str(i)
                visited_elements.pop(-2)
                visited_elements.pop(-1)             
                i = i + 1
    
    if len(visited_elements) == 1:
        if type(visited_elements[0]) is str \
            and root_key in internal_nodes:
            temp_dicts.update({visited_elements[0]:root}) 
    
    if left_branch_temp != None and right_branch_temp != None:
        threeAddressCode  = ThreeAddressCode(root_key,
                                              left_branch_temp,
                                              right_branch_temp,
                                              og_variable,statement_type)
        threeAddressCodeDict['Three_Address_Code'].append(threeAddressCode)
   """

"""
def walk_through_ast(astSubTree,left=None,right=None):
    breakpoint()
    internal_nodes = ['+','-','*','/']
    root_key = list(astSubTree.keys())[0]
    
    if root_key not in internal_nodes:
        root_value = astSubTree[root_key]
        visited_elements.append(root_value)
        threeAddressCode  = ThreeAddressCode('=',
                                              visited_elements[0],
                                              None,
                                              og_variable,statement_type)
        threeAddressCodeDict['Three_Address_Code'].append(threeAddressCode)    
        return threeAddressCodeDict
    else:
        children = astSubTree[root_key]
        NUM_OF_CHILDREN = len(children)
        if NUM_OF_CHILDREN == 2:
            l_child = children[0]
            r_child = children[1]    
            l_child_type = list(l_child.keys())[0]
            r_child_type = list(r_child.keys())[0]
            if l_child_type not in internal_nodes  \
                and r_child_type not in internal_nodes:
                visited_elements.append(l_child[l_child_type])
                visited_elements.append(root_key)
                visited_elements.append(r_child[r_child_type])
                threeAddressCode  = ThreeAddressCode(visited_elements[1],
                                              visited_elements[0],
                                              visited_elements[2],
                                              og_variable,statement_type)
                threeAddressCodeDict['Three_Address_Code'].append(threeAddressCode)    
                return threeAddressCodeDict
            
            if l_child_type in internal_nodes:
                walk_through_ast(l_child)
            
            if r_child_type in internal_nodes:
                walk_through_ast(r_child)
                #visited_elements.append(root_key)
"""
                
"""
def walk_through_ast(astSubTree):
    breakpoint()
    NUMBER_OF_CHILDREN = len(astSubTree)
    left_child = None
    right_child = None
    breakpoint()
    if type(astSubTree) is dict:
        #right_child = None
        internal_nodes = ['+','-','*','/']       
        if NUMBER_OF_CHILDREN == 1:
            print(astSubTree.keys())
            #check to see if the first key of the dictionary is a '-' sign
            dict_key = list(astSubTree.keys())[0]
            print(dict_key)
            global statement_type
            if dict_key in internal_nodes:
                #breakpoint()
                left_child = list(list(astSubTree.values())[0][0].values())[0]
                visited_elements.append(left_child)
                visited_elements.append(dict_key)
                right_subtree = list(astSubTree.values())[0][1]
                #check the first key of the right_subtree, if it is an internal node or operator
                #then walk through that subtree
                if list(right_subtree.keys())[0] in internal_nodes:
                    #visited_elements.append(list(right_subtree.keys())[0])
                    return walk_through_ast(right_subtree)  
                right_child = list(right_subtree.values())[0]
                #visited_elements.append(left_child)
                #visited_elements.append(dict_key)
                visited_elements.append(right_child)
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
                    #breakpoint()
                    #print(visited_elements)
                    #lastElem = None
                    i = i + 1
                    if len(visited_elements) == 3:
                        threeAddressCode  = ThreeAddressCode(visited_elements[1],
                                              visited_elements[0],
                                              visited_elements[2],
                                              og_variable,statement_type)
                        #lastElem = None
                        threeAddressCodeDict['Three_Address_Code'].append(threeAddressCode)
                        return threeAddressCodeDict
                    else:
                        return walk_through_ast(right_subtree)
            else:
                #left_child = list(astSubTree.values())[-1]
                #visited_elements.append(left_child)
            #right_child = None
                if len(visited_elements) == 3:
                    threeAddressCode  = ThreeAddressCode(visited_elements[1],
                                              visited_elements[0],
                                              visited_elements[2],
                                              og_variable,statement_type)
                    #lastElem = None
                    threeAddressCodeDict['Three_Address_Code'].append(threeAddressCode)
                    return threeAddressCodeDict
        
                elif len(visited_elements) >= 3:
                    
                    threeAddressCode  = ThreeAddressCode(visited_elements[-2],
                                              visited_elements[-3],
                                              visited_elements[-1],
                                              "t" + str(i),statement_type)
                    threeAddressCodeDict['Three_Address_Code'].append(threeAddressCode)
                    visited_elements[-3] = "t" + str(i)
                    visited_elements.pop(-2)
                    visited_elements.pop(-1)
                    #print(visited_elements)
                    #lastElem = None
                    i = i + 1
                    return walk_through_ast(astSubTree)
                else:
                    left_child = list(astSubTree.values())[-1]
                    visited_elements.append(left_child)
            #breakpoint()    

    if right_child == None and NUMBER_OF_CHILDREN == 1:
        #print(visited_elements)
        if statement_type == 'return':
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

"""
"""
def walk_through_ast(astSubTree):
    #print("TREE",astSubTree)
    NUMBER_OF_CHILDREN = len(astSubTree)
    #print(NUMBER_OF_CHILDREN)
    #breakpoint()
    
    if type(astSubTree) is list:
        NUMBER_OF_CHILDREN = len(astSubTree[0])
    else:
        NUMBER_OF_CHILDREN = len(astSubTree)
    #breakpoint()
    if NUMBER_OF_CHILDREN == 1:
       if type(astSubTree) is list:
        if '*' in astSubTree[0] or '/' in astSubTree[0] or '%' in astSubTree[0]:
            NUMBER_OF_CHILDREN = NUMBER_OF_CHILDREN + 1
    #print("Children",NUMBER_OF_CHILDREN)
    
    left_child = None
    right_child = None
    if type(astSubTree) is dict:
        #right_child = None       
        if NUMBER_OF_CHILDREN == 2:
            left_child = list(astSubTree.values())[-2]
            visited_elements.append(left_child)
            right_child = list(astSubTree.keys())[-1]
            #visited_elements.append(right_child)
        elif NUMBER_OF_CHILDREN == 1:
            breakpoint()
            print(astSubTree.keys())
            #check to see if the first key of the dictionary is a '-' sign
            dict_key = list(astSubTree.keys())[0]
            print(dict_key)
            if dict_key == '+':
                left_child = list(astSubTree.values())[0][0]
                right_child = list(astSubTree.values())[0][1]
                visited_elements.append(left_child)
                visited_elements.append(dict_key)
                visited_elements.append(right_child)
                
            else:
                left_child = list(astSubTree.values())[-1]
                visited_elements.append(left_child)
            #right_child = None
            breakpoint()
    if right_child == None and NUMBER_OF_CHILDREN == 1:
        #print(visited_elements)
       
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
            #print(visited_elements)
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

    else:
        left_child = list(astSubTree[0].values())[0]
        if visited_elements and list(visited_elements[-1])[0] != 't':
            visited_elements.append(left_child)
        elif visited_elements == []:
            visited_elements.append(left_child)
        if NUMBER_OF_CHILDREN == 2:
            if '*' in astSubTree[0] or '/' in astSubTree[0] or '%' in astSubTree[0]:
                right_child = {'*':astSubTree[0]['*']}
            else:
                right_child = list(astSubTree[0].keys())[1]
                #right_child = astSubTree[1]
                #print("r",right_child)
        elif NUMBER_OF_CHILDREN == 1:
            #left_child = list(astSubTree[0].values())[0]
            #visited_elements.append(left_child)
            right_child = None

    internal_nodes = ['+','-','*','/','%']
    
    if right_child == None and NUMBER_OF_CHILDREN == 1:
        #print(visited_elements)
       
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
            #print(visited_elements)
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
            #print(astSubTree[right_child])
            #breakpoint()
            return walk_through_ast(astSubTree[0][right_child])            

        elif operator_type in internal_nodes:
           #print("p",operator_type)
           visited_elements.append(operator_type)
           return walk_through_ast(right_child[operator_type])
"""    
# from https://www.geeksforgeeks.org/count-number-of-nodes-in-a-complete-binary-tree/
# Function to get the count of nodes
# in complete binary tree
def totalNodes(root):
  # Base case
    internal_nodes = ['+','-','*','/']
    if(root == None):
        return 0
    # Find the left height and the
    # right heights
    root_type = list(root.keys())[0]
    if root_type not in internal_nodes:
        l = 0
        r = 0
    else:
        l = totalNodes(root[root_type][0])
        r = totalNodes(root[root_type][1])
 
    return 1 + l + r

def main():
    #threeAddressCodeDict = list()
    #threeAddressCode = ThreeAddressCode("=","4",None,'d')
    #threeAddressCodeDict.append(threeAddressCode)
    #threeAddressCode = ThreeAddressCode()
    #print(threeAddressCode.operation,threeAddressCode.arg1, threeAddressCode.arg2,threeAddressCode.result)
    #astTree = {'=': {'ID': 'a', '+': [{'NUMBER': 3}, {'*': [{'NUMBER': 4}, {'NUMBER': 5}]}]}}
    #astTree = {'main': {'LBRACE': '{', 'Statement': [{'=': {'ID': 'a', '+': [{'NUMBER': 3}, {'*': [{'NUMBER': 4}, {'NUMBER': 5}]}]}}, {'return': {'NUMBER': 0}}], 'RBRACE': '}'}} 
    threeAddressCode = list()
    operatorsFound = []
    operators = ['+','-','*','/']
    astTree = {'+': [{'+': [{'NUMBER': 4}, {'NUMBER': 5}]},
                                      {'NUMBER': 8}]}
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
    #print(threeAddressCode) 
    #print(operatorsFound)
    branches = []
    print(astTree)  
    print(astTree['+']) #root
    print(astTree['+'][0]) #root.left
    
    print(astTree['+'][0]['+']) 
    print(list(astTree['+'][0].keys())[0],astTree['+'][0]['+'][0],astTree['+'][0]['+'][1]) 
    t1 = astTree['+'][0]
    branches.append(t1)
    astTree['+'][0] = 't1'
    print(astTree)
    """
    print(astTree['+'][0]['+'][0]) #root.left.left
    print(astTree['+'][0]['+'][1]) #root.left.right
    print(astTree['+'][1]) #root.right
    #print(astTree['=']['+'][1])
    #r1 = astTree['=']['+'][1]
    #astTree['=']['+'][1] = "r1"
    #print("r1",r1)
    #print(astTree)
    """
    #threeAddressCode = [[{'=':{"tempVar","r1"}},r1],astTree]
    #iterate through the astTree and log all operations in the order that they have been visited
    #find the index of the last operation to be found in the astTree
    #assign the ast at that index to a temporary variable r1
    #add it a table to keep track of all variables created and their values
    #need to be able to replace the last operation found in the ast with the tempoerary variable
    #,which points to the subtree being replaced.
    # an ast will be created from the temporary variable along with the values that it is pointing too 
    #print(threeAddressCode)
if __name__ == "__main__":
    main()