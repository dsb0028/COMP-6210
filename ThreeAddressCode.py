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
        
threeAddressCodeDict = defaultdict(list)
og_variable = None
statement_type = None
temps = []

def createThreeAddressCode(astTree, symbolTable):
    function_name = 'main'
    statementList = astTree[function_name]['Statement']
    for statement in statementList: 
        global visited_elements
        visited_elements = []
        global parentNode
        parentNode = None
        if '=' in statement:
            global statement_type
            statement_type = 'Assignment_Statement'
            global og_variable
            og_variable = statement['='][0].pop('ID')
            statement['='][0] = statement['='][1]
            statement['='].pop(1)
            global number_of_nodes
            number_of_nodes = totalNodes(statement['='][0])
            walk_through_ast(statement['='][0])
            if temp_dicts != {}:
                last_temp_var = list(temp_dicts)[-1]
                temp_dicts[og_variable] = temp_dicts.pop(last_temp_var)
                global i
                i = i - 1
            else:
                temp_dicts.update({og_variable:statement['='][0]})
            print(temp_dicts)
        elif 'return' in statement:
            statement_type = 'return'
            number_of_nodes = totalNodes(statement['return'][0])
            breakpoint()
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
                    #operator
            else:
                stmt = 'Assignment_Statement'
                operator = list(item[1].keys())[0]
                if operator in ['+','-','*','/']:
                    op1 = item[1][operator][0]
                    if type(op1) is dict:
                        key = list(op1.keys())[0]
                        op1 = op1[key]
                    op2 = item[1][operator][1]
                    if type(op2) is dict:
                        key = list(op2.keys())[0]
                        op2 = op2[key]
                else:
                    val_type = list(item[1].keys())[0]
                    op1 = item[1][val_type]
                    operator = '='
                    breakpoint
                res = item[0]
                #print(res)
                #breakpoint()
                symbolTable.addAVariable(res,'int','main')
                #breakpoint()
               
            
            threeAddressCode =  \
                ThreeAddressCode(operation=operator
                                 ,arg1=op1,arg2=op2,result=res,statement=stmt)
            threeAddressCodeDict['Three_Address_Code'].append(threeAddressCode)
    #print(threeAddressCodeDict)
    return threeAddressCodeDict,symbolTable


visited_elements = []
temp_dicts = {}
i = 1
isLeftTerminalNode = False
isRightTerminalNode = False
parentNode = None
def walk_through_ast(root,isReturn=False):
    internal_nodes = ['+','-','*','/']
    left = None
    right = None
    if root:
        root_key = list(root.keys())[0]
        global parentNode
        if parentNode == None:
            parentNode = root
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
                    breakpoint()
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
                breakpoint()
                isLeftTerminalNode = False
                isRightTerminalNode = False 
        else:
            visited_elements.append(root[root_key])
            if number_of_nodes == len(visited_elements) and parentNode == root:
                if statement_type == 'return':
                    temp_dicts.update({statement_type:root})
                """
                else:
                    temp_dicts.update({og_variable:root})
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