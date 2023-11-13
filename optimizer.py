#from collections import defaultdict

#optimizedCode = [] 
#table = {'Assignment'}
simpleAssignments = []

def performOptimizations(threeAddressCode):
    optimizedCode = executeConstProp(threeAddressCode)
    #print(len(optimizedCode))
    optimizedCode = executeConstFolding(optimizedCode)
    
    optimizedCode = executeConstProp(threeAddressCode)
    #print(len(optimizedCode))
    optimizedCode = executeConstFolding(optimizedCode)
    optimizedCode = executeConstProp(threeAddressCode)
    optimizedCode = executeConstFolding(optimizedCode)
    optimizedCode = executeConstProp(threeAddressCode)
    optimizedCode = executeConstFolding(optimizedCode)
    optimizedCode = executeConstProp(threeAddressCode)
    #print(len(optimizedCode))
    #optimizedCode = executeConstFolding(optimizedCode)
    """
    for threeAddrCode in optimizedCode:
        print(threeAddrCode.operation,threeAddrCode.arg1, 
              threeAddrCode.arg2, 
              threeAddrCode.result, threeAddrCode.statement)
    """
    return optimizedCode

def executeConstFolding(optimizedCode):
    optimizedThreeAddrCode = []
    operations = ['+','-','*','/']
    for threeAddrCode in optimizedCode:
        if (threeAddrCode.operation['Operation'] in operations
            and type(threeAddrCode.arg1['ARG1']) == int
            and type(threeAddrCode.arg2['ARG2']) == int):
                threeAddrCode.arg1['ARG1'] = eval(str(threeAddrCode.arg1['ARG1'])
                     + threeAddrCode.operation['Operation'] 
                     + str(threeAddrCode.arg2['ARG2']))
                threeAddrCode.operation['Operation'] = '='
                threeAddrCode.arg2['ARG2'] = None
        optimizedThreeAddrCode.append(threeAddrCode)
    return optimizedThreeAddrCode

def executeConstProp(threeAddressCode):
    optimizedThreeAddrCode = []
    for threeAddrCode in threeAddressCode:
        #check for optimization type
        #if isConstantProgagationNeeded == True:
        #   perform constant propagation
        #elif isConstantFoldingNeeded == True:
        #   perfrom contant folding 
        isSimpleAssign = isSimpleAssignmentStmt(threeAddrCode)
        if isSimpleAssign == True:
            threeAddrCode.statement['STATEMENT'] = 'Simple_Assignment_Statement'
            simpleAssignments.append(threeAddrCode)
            #print(isSimpleAssign)
            optimizedThreeAddrCode.append(threeAddrCode)
            continue
        
        if type(threeAddrCode.arg1['ARG1']) == str: 
            if threeAddrCode.arg1['ARG1'].isidentifier():
                #check if variable is listed in simple_assignment_statement
                #if so, extract the value of it and then change matching var to its value
                for simple_assignment in simpleAssignments:
                    if simple_assignment.result['RESULT'] == threeAddrCode.arg1['ARG1']:
                        threeAddrCode.arg1['ARG1'] = simple_assignment.arg1['ARG1']
        if type(threeAddrCode.arg2['ARG2']) == str:
            if threeAddrCode.arg2['ARG2'].isidentifier():
                #check if variable is listed in simple_assignment_statement
                #if so, extract the value of it and then change matching var to its value
                for simple_assignment in simpleAssignments:
                    if simple_assignment.result['RESULT'] == threeAddrCode.arg2['ARG2']:
                        threeAddrCode.arg2['ARG2'] = simple_assignment.arg1['ARG1']
        #print(isSimpleAssign)
        #print(threeAddrCode.operation
        #      ,threeAddrCode.arg1
        #      ,threeAddrCode.arg2,
        #      threeAddrCode.result,
        #      threeAddrCode.statement
        optimizedThreeAddrCode.append(threeAddrCode)
    return optimizedThreeAddrCode
# ID = NUMBER
def isSimpleAssignmentStmt(threeAddressCodeStmt): 
    result = False
    #print(type(threeAddressCodeStmt.arg1['ARG1']))
    #print(threeAddressCodeStmt.arg2['ARG2'])
    if ((type(threeAddressCodeStmt.arg1['ARG1']) == int
         or type(threeAddressCodeStmt.arg1['ARG1']) == float)
        and threeAddressCodeStmt.arg2['ARG2'] == None
        and threeAddressCodeStmt.operation['Operation'] == '='):
        result = True
        #print(result)
    return result

def isOptimized(threeAddressCode):
    result = False
    return result

    