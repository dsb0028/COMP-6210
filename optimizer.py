#from collections import defaultdict

#optimizedCode = [] 
#table = {'Assignment'}
simpleAssignments = set()

def performOptimizations(threeAddressCode):
    optimizedCode = None
    breakpoint()
    while isOptimized(threeAddressCode) == False:
        for threeAddrCode in threeAddressCode:
            print(threeAddrCode.operation,threeAddrCode.arg1,threeAddrCode.arg2,threeAddrCode.result, threeAddrCode.statement)
        #breakpoint()
        optimizedCode = executeConstProp(threeAddressCode)
        for threeAddrCode in optimizedCode:
            print(threeAddrCode.operation,threeAddrCode.arg1,threeAddrCode.arg2,threeAddrCode.result, threeAddrCode.statement)
        #print(len(optimizedCode))
        #breakpoint()
        optimizedCode = executeConstFolding(optimizedCode)
        #breakpoint()
        for threeAddrCode in optimizedCode:
            print(threeAddrCode.operation,threeAddrCode.arg1,threeAddrCode.arg2,threeAddrCode.result, threeAddrCode.statement)
        #breakpoint()
        optimizedCode = deadCodeRemoval(optimizedCode)
        #breakpoint()
        for threeAddrCode in optimizedCode:
            print(threeAddrCode.operation,threeAddrCode.arg1,threeAddrCode.arg2,threeAddrCode.result, threeAddrCode.statement)
        threeAddressCode = optimizedCode
        #print(stmt)
        #print(otherAssignments)
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

def isConstFoldingPossible(optmizedCode):
    result = False
    operations = ['+','-','*','/']
    for threeAddrCode in optmizedCode:
        if (threeAddrCode.operation['Operation'] in operations
            and type(threeAddrCode.arg1['ARG1']) == int
            and type(threeAddrCode.arg2['ARG2']) == int):
            result = True
            break
    return result

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
            simpleAssignments.add(threeAddrCode)
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

def isConstPropPossible(threeAddressCode):
    result = False
    for threeAddrCode in threeAddressCode:
        isSimpleAssign = isSimpleAssignmentStmt(threeAddrCode)
        if isSimpleAssign == True:
            threeAddrCode.statement['STATEMENT'] = 'Simple_Assignment_Statement'
            simpleAssignments.add(threeAddrCode)
            #print(isSimpleAssign)
            continue
        if type(threeAddrCode.arg1['ARG1']) == str: 
            if threeAddrCode.arg1['ARG1'].isidentifier():
                #check if variable is listed in simple_assignment_statement
                #if so, extract the value of it and then change matching var to its value
                for simple_assignment in simpleAssignments:
                    if simple_assignment.result['RESULT'] == threeAddrCode.arg1['ARG1']:
                        result = True
                        break
        if type(threeAddrCode.arg2['ARG2']) == str:
            if threeAddrCode.arg2['ARG2'].isidentifier():
                #check if variable is listed in simple_assignment_statement
                #if so, extract the value of it and then change matching var to its value
                for simple_assignment in simpleAssignments:
                    if simple_assignment.result['RESULT'] == threeAddrCode.arg2['ARG2']:
                        result = True
                        break
        if result == True:
            break
    return result

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

def deadCodeRemoval(threeAddressCode):
    linesToRemove = []
    optimizedCode = None
    global simpleAssignments
    for threeAddrCode in threeAddressCode:
        isSimpleAssign = isSimpleAssignmentStmt(threeAddrCode)
        if isSimpleAssign == True:
            threeAddrCode.statement['STATEMENT'] = 'Simple_Assignment_Statement'
            simpleAssignments.add(threeAddrCode)
            #print(isSimpleAssign) 
            continue
    """
    for threeAddrCode in threeAddressCode:
        print(threeAddrCode.operation,threeAddrCode.arg1,
              threeAddrCode.arg2,threeAddrCode.result,threeAddrCode.statement)
    print('\n','\n')
    for simpleAssign in simpleAssignments:
        print(simpleAssign.operation,simpleAssign.arg1,
              simpleAssign.arg2,simpleAssign.result,simpleAssign.statement)
    """
    #breakpoint()
    if simpleAssignments != set():

        otherAssignments = set(threeAddressCode).difference(set(simpleAssignments))
        """
        for oA in otherAssignments:
            print(oA.operation,oA.arg1,oA.arg2,oA.result,oA.statement)
        """
        #breakpoint()
        lines_with_irrelevant_vars = 0
        for simpleAssign in simpleAssignments:
            for stmt in otherAssignments:    
                #print(simpleAssign.operation, simpleAssign.arg1, simpleAssign.arg2, simpleAssign.result)
                #print(stmt.operation,stmt.arg1,stmt.arg2,stmt.result)
                #print('\n\n')    
                #breakpoint()
                if simpleAssign.result['RESULT'] != stmt.result['RESULT'] \
                    and simpleAssign.result['RESULT'] != simpleAssign.arg1['ARG1'] \
                    and simpleAssign.result['RESULT'] != simpleAssign.arg2['ARG2'] \
                    and simpleAssign.result['RESULT'] != stmt.arg1['ARG1'] \
                    and simpleAssign.result['RESULT'] != stmt.arg2['ARG2']:
                    lines_with_irrelevant_vars = lines_with_irrelevant_vars + 1
            if lines_with_irrelevant_vars == len(otherAssignments):
                lines_with_irrelevant_vars = 0
                linesToRemove.append(simpleAssign)
    if linesToRemove != []:
        breakpoint()
        optimizedCode = list(set(threeAddressCode).difference(set(linesToRemove)))
        simpleAssignments = simpleAssignments.difference(set(linesToRemove))
    else:
        optimizedCode = threeAddressCode
    return optimizedCode    

def isdeadCodeRemovalPossible(threeAddressCode):
    result = False
    if simpleAssignments != {}:
        otherAssignments = set(threeAddressCode).difference(set(simpleAssignments))
        """
        for oA in otherAssignments:
            print(oA.operation,oA.arg1,oA.arg2,oA.result)
        """
        lines_with_irrelevant_vars = 0
        for simpleAssign in simpleAssignments:
            for stmt in otherAssignments:    
                #print(simpleAssign.operation, simpleAssign.arg1, simpleAssign.arg2, simpleAssign.result)
                #print(stmt.operation,stmt.arg1,stmt.arg2,stmt.result)    
                if simpleAssign.result['RESULT'] != stmt.result['RESULT'] \
                    and simpleAssign.result['RESULT'] != simpleAssign.arg1['ARG1'] \
                    and simpleAssign.result['RESULT'] != simpleAssign.arg2['ARG2'] \
                    and simpleAssign.result['RESULT'] != stmt.arg1['ARG1'] \
                    and simpleAssign.result['RESULT'] != stmt.arg2['ARG2']:
                    lines_with_irrelevant_vars = lines_with_irrelevant_vars + 1
            if lines_with_irrelevant_vars == len(otherAssignments):
                result = True
                break
    return result

def isOptimized(threeAddressCode):
    result = False
    if isConstFoldingPossible(threeAddressCode) == False \
        and isConstPropPossible(threeAddressCode) == False \
        and isdeadCodeRemovalPossible(threeAddressCode) == False:
        result = True
    return result

    