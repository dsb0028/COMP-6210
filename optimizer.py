#from collections import defaultdict
from collections import Counter

#optimizedCode = [] 
#table = {'Assignment'}
simpleAssignments = []
linesNumbered = []
func = None
def performOptimizations(threeAddressCode,symbolTable):
    optimizedCode = {}
    breakpoint()
    functions = list(threeAddressCode.keys())
    global func
    for func in functions:
        threeAddressCode[func],livelinessTable = convertToSSA(threeAddressCode[func],symbolTable)
        while isOptimized(threeAddressCode[func]) == False:
            global linesNumbered
            linesNumbered = [l for l in enumerate(threeAddressCode[func])]
            """
            for threeAddrCode in threeAddressCode[func]:
                print(threeAddrCode.operation,threeAddrCode.arg1,threeAddrCode.arg2,threeAddrCode.result, threeAddrCode.statement)
            breakpoint()
            """
            optimizedCode[func] = executeConstProp(threeAddressCode[func])
            """
            for threeAddrCode in optimizedCode[func]:
                print(threeAddrCode.operation,threeAddrCode.arg1,threeAddrCode.arg2,threeAddrCode.result, threeAddrCode.statement)
            #print(len(optimizedCode))
            """
            #breakpoint()
            optimizedCode[func] = executeConstFolding(optimizedCode[func])
            #breakpoint()
            """
            for threeAddrCode in optimizedCode[func]:
                print(threeAddrCode.operation,threeAddrCode.arg1,threeAddrCode.arg2,threeAddrCode.result, threeAddrCode.statement)
            """
            #breakpoint()
            optimizedCode[func] = deadCodeRemoval(optimizedCode[func],symbolTable)
            #breakpoint()
            """
            for threeAddrCode in optimizedCode[func]:
                print(threeAddrCode.operation,threeAddrCode.arg1,threeAddrCode.arg2,threeAddrCode.result, threeAddrCode.statement)
            
            """
            threeAddressCode[func] = optimizedCode[func]
            #breakpoint()
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
                threeAddrCode.arg1['ARG1'] = int(eval(str(threeAddrCode.arg1['ARG1'])
                     + threeAddrCode.operation['Operation']
                     + str(threeAddrCode.arg2['ARG2'])))
                threeAddrCode.operation['Operation'] = '='
                threeAddrCode.arg2['ARG2'] = None
        optimizedThreeAddrCode.append(threeAddrCode)
    return optimizedThreeAddrCode

def isConstFoldingPossible(optimizedCode):
    result = False
    operations = ['+','-','*','/']
    for threeAddrCode in optimizedCode:
        if (threeAddrCode.operation['Operation'] in operations
            and type(threeAddrCode.arg1['ARG1']) == int
            and type(threeAddrCode.arg2['ARG2']) == int):
            result = True
            break
    return result

def executeConstProp(threeAddressCode):
    optimizedThreeAddrCode = []
    return_var = threeAddressCode[-1].arg1['ARG1']
    linesThatHaveSameInitializingVarAsReturnVar = []
    for line in threeAddressCode:
        if line.result['RESULT'] == return_var \
              and line.statement['STATEMENT'] == 'Simple_Assignment_Statement':
            linesThatHaveSameInitializingVarAsReturnVar.append(line)
    for line in linesThatHaveSameInitializingVarAsReturnVar:
        print(line.operation,line.arg1,line.arg2,line.result)
    verdict = False
    if len(linesThatHaveSameInitializingVarAsReturnVar) > 1:
        verdict = True
    ind = None
    if verdict == True:
        ind = threeAddressCode.index(linesThatHaveSameInitializingVarAsReturnVar[-1])
    print(ind)
   
    for threeAddrCode in threeAddressCode:
        isSimpleAssign = isSimpleAssignmentStmt(threeAddrCode)
        if isSimpleAssign == True and threeAddrCode.statement['STATEMENT'] != 'Simple_Assignment_Statement':
            threeAddrCode.statement['STATEMENT'] = 'Simple_Assignment_Statement'
            simpleAssignments.append(threeAddrCode)
            optimizedThreeAddrCode.append(threeAddrCode)
            continue
        #breakpoint()
        if type(threeAddrCode.arg1['ARG1']) == str: 
            if threeAddrCode.arg1['ARG1'].isidentifier():
                #check if variable is listed in simple_assignment_statement
                #if so, extract the value of it and then change matching var to its value
                for simple_assignment in simpleAssignments:
                    if simple_assignment.result['RESULT'] == threeAddrCode.arg1['ARG1']:
                        if ind != None:
                            threeAddrCode.arg1['ARG1'] = threeAddressCode[ind].arg1['ARG1']    
                        else:
                            threeAddrCode.arg1['ARG1'] = simple_assignment.arg1['ARG1']
        if type(threeAddrCode.arg2['ARG2']) == str:
            if threeAddrCode.arg2['ARG2'].isidentifier():
                #check if variable is listed in simple_assignment_statement
                #if so, extract the value of it and then change matching var to its value
                for simple_assignment in simpleAssignments:
                    if simple_assignment.result['RESULT'] == threeAddrCode.arg2['ARG2']:
                        threeAddrCode.arg2['ARG2'] = simple_assignment.arg1['ARG1']
        optimizedThreeAddrCode.append(threeAddrCode)
    return optimizedThreeAddrCode

def isConstPropPossible(threeAddressCode):
    result = False
    for threeAddrCode in threeAddressCode:
        isSimpleAssign = isSimpleAssignmentStmt(threeAddrCode)
        if isSimpleAssign == True and threeAddrCode.statement['STATEMENT'] != 'Simple_Assignment_Statement':
            threeAddrCode.statement['STATEMENT'] = 'Simple_Assignment_Statement'
            simpleAssignments.append(threeAddrCode)
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
    if ((type(threeAddressCodeStmt.arg1['ARG1']) == int
         or type(threeAddressCodeStmt.arg1['ARG1']) == float)
        and threeAddressCodeStmt.arg2['ARG2'] == None
        and threeAddressCodeStmt.operation['Operation'] == '='):
        result = True
    return result

def deadCodeRemoval(threeAddressCode,symbolTable):
    linesToRemove = []
    optimizedCode = None
    global simpleAssignments
    #linesNumbered = enumerate(threeAddressCode)
    for threeAddrCode in threeAddressCode:
        isSimpleAssign = isSimpleAssignmentStmt(threeAddrCode)
        if isSimpleAssign == True \
            and threeAddrCode.statement['STATEMENT'] != 'Simple_Assignment_Statement':
            threeAddrCode.statement['STATEMENT'] = 'Simple_Assignment_Statement'
            #breakpoint()
            simpleAssignments.append(threeAddrCode)
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
    #otherAssignments
    if simpleAssignments != []:

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
        #breakpoint()
        #linesNumbered = enumerate(threeAddressCode)
        #optimizedCode = list(set(linesNumbered) - set(linesToRemove))
        #print(len(list(linesNumbered)),len(optimizedCode))
        #breakpoint()
        #optimizedCode = sorted(optimizedCode[:-1],key=lambda x: [x.result['RESULT'] if x.result['RESULT'] != None else  '']) 
        optimizedCode = threeAddressCode
        
        """
        for threeAddrCode in linesToRemove:
            print(threeAddrCode.operation,threeAddrCode.arg1,
              threeAddrCode.arg2,threeAddrCode.result,threeAddrCode.statement)
        """
        #breakpoint()
        number_removed = 0
        while number_removed != len(linesToRemove):
            for line in optimizedCode: 
                if line in linesToRemove:
                    #breakpoint()
                    optimizedCode.remove(line) 
                    #breakpoint()
                    global func
                    symbolTable.table[func]['Variables'].pop(line.result['RESULT'])
                    number_removed += 1
        """
        for line in optimizedCode:
            if line in linesToRemove:
                #linesToRemove.remove(line)
                optimizedCode.remove(line)
                #i = optimizedCode.index(line)
                #optimizedCode.pop(i)
                    #optimizedCode[i] = None
        """
        """
        for threeAddrCode in optimizedCode:
            print(threeAddrCode.operation,threeAddrCode.arg1,
              threeAddrCode.arg2,threeAddrCode.result,threeAddrCode.statement)
        breakpoint()
        for threeAddrCode in simpleAssignments:
            print(threeAddrCode.operation,threeAddrCode.arg1,
              threeAddrCode.arg2,threeAddrCode.result,threeAddrCode.statement)
        """
        #breakpoint()
        #optimizedCode.reverse()
        #breakpoint()
        simpleAssignments = list(set(simpleAssignments) - set(linesToRemove))
        """
        for threeAddrCode in simpleAssignments:
            print(threeAddrCode.operation,threeAddrCode.arg1,
              threeAddrCode.arg2,threeAddrCode.result,threeAddrCode.statement)
        """
        linesToRemove.clear()
        #breakpoint()
        #simpleAssignments.reverse()
    else:
        optimizedCode = threeAddressCode
    return optimizedCode    

def isdeadCodeRemovalPossible(threeAddressCode):
    result = False
    if simpleAssignments != []:
        otherAssignments = set(threeAddressCode) - set(simpleAssignments)
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

def convertToSSA(threeAddressCode,symbolTable):
    #conduct livliness analysis
    livelinessTable = conductLivelinessAnalysis(threeAddressCode,symbolTable)  
    return threeAddressCode, livelinessTable
    
def conductLivelinessAnalysis(threeAddressCode,symbolTable):
    #stores all live variables and their ranges
    livelinessTable = {}
    #numbers all the lines of three address code
    linesNumbered = [l for l in enumerate(threeAddressCode)]
    isLiveArray = [False for i in range(len(linesNumbered))]
    line_num = 0
    linesExpanded = []
    for line in linesNumbered:
        linesExpanded.append([line])
        linesExpanded[line_num].append(isLiveArray[line_num])
        line_num = line_num + 1
    """        
    for threeAddrCode in threeAddressCode:
            #liveVariableAndRange = ['Live Variable':None,}
            print(threeAddrCode.operation,
                  threeAddrCode.arg1,threeAddrCode.arg2,
                  threeAddrCode.result, threeAddrCode.statement) 
    """
    #breakpoint()
    v_no = 1
    #the first variable will automatically be live
    for n_line,isLive in linesExpanded:
        #breakpoint()
        i = n_line[0]
        line = n_line[1]
        if i == 0:
            isLiveArray[0] = True
            linesExpanded[i][1] = True
            #breakpoint()
            livelinessTable.update({line.result['RESULT']:[i,None]})
            continue
        if line.statement['STATEMENT'] == 'return':
            if line.arg1['ARG1'] in livelinessTable:
               var_versions = [key for key in livelinessTable.keys() if key.startswith(line.arg1['ARG1'])]
               livelinessTable[var_versions[-1]][1] = i
               line.arg1['ARG1'] = var_versions[-1]
               #breakpoint()
        elif line.result['RESULT'] not in livelinessTable:
            isLiveArray[i] = True
            linesExpanded[i][1] = True
            #breakpoint()
            livelinessTable.update({line.result['RESULT']:[i,None]})
            if line.arg1['ARG1'] in livelinessTable:
                #breakpoint()
                var_versions = [key for key in livelinessTable.keys() if key.startswith(line.arg1['ARG1'])]
                if len(var_versions) > 1:
                    if not var_versions[-1].startswith('t'):
                        line.arg1['ARG1'] =  var_versions[-1] 
    
            if line.arg2['ARG2'] in livelinessTable:
                #breakpoint()
                var_versions = [key for key in livelinessTable.keys() if key.startswith(line.arg2['ARG2'])]
                if len(var_versions) > 1:
                    if not var_versions[-1].startswith('t'):
                        line.arg2['ARG2'] =  var_versions[-1] 
                #livelinessTable[line.arg2['ARG2']][1] = i
        else:
            #breakpoint()
            #var_versions = [key for key in livelinessTable.keys() if key.startswith(line.result['RESULT'])]
            line.result['RESULT'] = line.result['RESULT']+str(v_no)
            symbolTable.addAVariable(line.result['RESULT'],'int',func)
          
            livelinessTable.update({line.result['RESULT']:[i,None]})
            isLiveArray[i] = True
            linesExpanded[i][1] = True
            if len(line.result['RESULT']) > 1 and not line.result['RESULT'].startswith('t'):
                var_versions = [key for key in livelinessTable.keys() if key.startswith(line.result['RESULT'][0])]
                var_versions_extended = []
                for version in var_versions:
                    start_index_for_version = livelinessTable[version][0] 
                    verdict = linesExpanded[start_index_for_version][1]
                    var_versions_extended.append([version,verdict])
                var_versions_extended.reverse()
                for n,p in enumerate(var_versions_extended):
                    if n != 0:
                        var_versions_extended[n][1] = False
                var_versions_extended.reverse()
                for pair in var_versions_extended:
                   if pair[1] == False and livelinessTable[pair[0]][1] == None: 
                        livelinessTable[pair[0]][1] = i
                for pair in var_versions_extended:
                    start_index_for_version = livelinessTable[pair[0]][0]
                    linesExpanded[start_index_for_version][1] = pair[1] 
            if line.arg1['ARG1'] in livelinessTable:
                #var_versions = [key for key in livelinessTable.keys() if key.startswith(line.arg1['ARG1'])]
                var_versions = [key for key in livelinessTable.keys() if key.startswith(line.arg1['ARG1'])]
                #var_versions = [key for key in livelinessTable.keys() if key.startswith(line.result['RESULT'][0])]
                var_versions_extended = []
                for version in var_versions:
                    start_index_for_version = livelinessTable[version][0] 
                    verdict = linesExpanded[start_index_for_version][1]
                    var_versions_extended.append([version,verdict])
                #breakpoint()
                if len(var_versions) > 1:
                    if not var_versions[-1].startswith('t'):
                        var_versions_extended.reverse()
                        for pair in var_versions_extended:
                            if line.result['RESULT'][0] == line.arg1['ARG1'][0]:
                                if pair[1] == False:
                                    line.arg1['ARG1'] =  pair[0]
                                    break
                            else:
                                if pair[1] == True:
                                    line.arg1['ARG1'] =  pair[0]
                                    break
                        var_versions_extended.reverse()
            if line.arg2['ARG2'] in livelinessTable:
                var_versions = [key for key in livelinessTable.keys() if key.startswith(line.arg2['ARG2'])]
                var_versions_extended = []
                for version in var_versions:
                    start_index_for_version = livelinessTable[version][0] 
                    verdict = linesExpanded[start_index_for_version][1]
                    var_versions_extended.append([version,verdict])
                #breakpoint()
                if len(var_versions) > 1:
                    if not var_versions[-1].startswith('t'):
                        var_versions_extended.reverse()
                        for pair in var_versions_extended:
                            if line.result['RESULT'][0] == line.arg2['ARG2'][0]:
                                if pair[1] == False:
                                    line.arg2['ARG2'] =  pair[0]
                                    break
                            else:
                                if pair[1] == True:
                                    line.arg2['ARG2'] =  pair[0]
                                    break
                        var_versions_extended.reverse() 
               #livelinessTable[line.arg2['ARG2']][1] = i
            #breakpoint()
            v_no = v_no + 1
            #breakpoint()
            #find the variable that this line is associated with
            #mark it not live and mark the new variable live
    return livelinessTable 