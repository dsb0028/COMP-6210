#from collections import defaultdict
from collections import Counter

#optimizedCode = [] 
#table = {'Assignment'}
simpleAssignments = []
linesNumbered = []
def performOptimizations(threeAddressCode):
    optimizedCode = None
     #make note of lines that are defined multiple times and take note of their line number
    breakpoint()
    """
    varsUsed = []
    for line in threeAddressCode:
        varsUsed.append(line.result['RESULT'])
    print(varsUsed)
    varsDefined = set(varsUsed)
    print(varsDefined)
    """
    breakpoint()
    threeAddressCode = convertToSSA(threeAddressCode)
    while isOptimized(threeAddressCode) == False:
        global linesNumbered
        linesNumbered = [l for l in enumerate(threeAddressCode)]
        for threeAddrCode in threeAddressCode:
            print(threeAddrCode.operation,threeAddrCode.arg1,threeAddrCode.arg2,threeAddrCode.result, threeAddrCode.statement)
        breakpoint()
        optimizedCode = executeConstProp(threeAddressCode)
        for threeAddrCode in optimizedCode:
            print(threeAddrCode.operation,threeAddrCode.arg1,threeAddrCode.arg2,threeAddrCode.result, threeAddrCode.statement)
        #print(len(optimizedCode))
        breakpoint()
        optimizedCode = executeConstFolding(optimizedCode)
        breakpoint()
        for threeAddrCode in optimizedCode:
            print(threeAddrCode.operation,threeAddrCode.arg1,threeAddrCode.arg2,threeAddrCode.result, threeAddrCode.statement)
        breakpoint()
        optimizedCode = deadCodeRemoval(optimizedCode)
        #breakpoint()
        for threeAddrCode in optimizedCode:
            print(threeAddrCode.operation,threeAddrCode.arg1,threeAddrCode.arg2,threeAddrCode.result, threeAddrCode.statement)
        threeAddressCode = optimizedCode
        breakpoint()
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
    #varsDefined = []
    linesThatContainDuplicates = []
    """
    for i,line in linesNumbered:
        if line.statement['STATEMENT'] != 'return':
            varsDefined.append(line.result['RESULT'])
        else:
            varsDefined.append(line.arg1['ARG1']) 
    breakpoint()
    """
    varsDefinedMoreThanOnce = [line for line in linesNumbered if line[1]]
    cnt = Counter()
    return_var = threeAddressCode[-1].arg1['ARG1']
    #breakpoint()
    linesThatHaveSameInitializingVarAsReturnVar = []
    for line in threeAddressCode:
        if line.result['RESULT'] == return_var \
              and line.statement['STATEMENT'] == 'Simple_Assignment_Statement':
            linesThatHaveSameInitializingVarAsReturnVar.append(line)
    #breakpoint()
    for line in linesThatHaveSameInitializingVarAsReturnVar:
        print(line.operation,line.arg1,line.arg2,line.result)
    #breakpoint()
    verdict = False
    if len(linesThatHaveSameInitializingVarAsReturnVar) > 1:
        verdict = True
    ind = None
    if verdict == True:
        ind = threeAddressCode.index(linesThatHaveSameInitializingVarAsReturnVar[-1])
    print(ind)
    #breakpoint()
    """"
    for line in linesNumbered:
        if line[1].statement['STATEMENT'] != 'return':
            cnt[line[1].result['RESULT']] += 1     
        else:
            cnt[line[1].arg1['ARG1']] += 1 
    """    
    #breakpoint()
    for threeAddrCode in threeAddressCode:
        #check for optimization type
        #if isConstantProgagationNeeded == True:
        #   perform constant propagation
        #elif isConstantFoldingNeeded == True:
        #   perfrom contant folding
        isSimpleAssign = isSimpleAssignmentStmt(threeAddrCode)
        if isSimpleAssign == True and \
            threeAddrCode.statement['STATEMENT'] != 'Simple_Assignment_Statement':
            threeAddrCode.statement['STATEMENT'] = 'Simple_Assignment_Statement'
            simpleAssignments.append(threeAddrCode)
            #print(isSimpleAssign)
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
        if isSimpleAssign == True and \
                threeAddrCode.statement['STATEMENT'] != 'Simple_Assignment_Statement':
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
        for threeAddrCode in linesToRemove:
            print(threeAddrCode.operation,threeAddrCode.arg1,
              threeAddrCode.arg2,threeAddrCode.result,threeAddrCode.statement)
        
        breakpoint()
        number_removed = 0
        while number_removed != len(linesToRemove):
            for line in optimizedCode: 
                if line in linesToRemove:
                    optimizedCode.remove(line) 
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
        for threeAddrCode in optimizedCode:
            print(threeAddrCode.operation,threeAddrCode.arg1,
              threeAddrCode.arg2,threeAddrCode.result,threeAddrCode.statement)
        breakpoint()
        for threeAddrCode in simpleAssignments:
            print(threeAddrCode.operation,threeAddrCode.arg1,
              threeAddrCode.arg2,threeAddrCode.result,threeAddrCode.statement)
        breakpoint()
        #optimizedCode.reverse()
        #breakpoint()
        simpleAssignments = list(set(simpleAssignments) - set(linesToRemove))
        for threeAddrCode in simpleAssignments:
            print(threeAddrCode.operation,threeAddrCode.arg1,
              threeAddrCode.arg2,threeAddrCode.result,threeAddrCode.statement)
        linesToRemove.clear()
        breakpoint()
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

def convertToSSA(threeAddressCode):
    #conduct livliness analysis
    livelinessTable = conductLivelinessAnalysis(threeAddressCode)  
    return threeAddressCode
    
def conductLivelinessAnalysis(threeAddressCode):
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

    breakpoint()
    #i = 0
   
    for threeAddrCode in threeAddressCode:
            #liveVariableAndRange = ['Live Variable':None,}
            print(threeAddrCode.operation,
                  threeAddrCode.arg1,threeAddrCode.arg2,
                  threeAddrCode.result, threeAddrCode.statement) 
    breakpoint()
    v_no = 1
    #the first variable will automatically be live
    for n_line,isLive in linesExpanded:
        breakpoint()
        i = n_line[0]
        line = n_line[1]
        if i == 0:
            isLiveArray[0] = True
            linesExpanded[i][1] = True
            breakpoint()
            livelinessTable.update({line.result['RESULT']:[i,None]})
            continue
        if line.statement['STATEMENT'] == 'return':
            if line.arg1['ARG1'] in livelinessTable:
               var_versions = [key for key in livelinessTable.keys() if key.startswith(line.arg1['ARG1'])]
               livelinessTable[var_versions[-1]][1] = i
               breakpoint()
        elif line.result['RESULT'] not in livelinessTable:
            isLiveArray[i] = True
            linesExpanded[i][1] = True
            breakpoint()
            livelinessTable.update({line.result['RESULT']:[i,None]})
            if line.arg1['ARG1'] in livelinessTable:
               #var_versions = [key for key in livelinessTable.keys() if key.startswith(line.arg1['ARG1'])]
               #livelinessTable[var_versions[-1]][1] = i
               livelinessTable[line.arg1['ARG1']][1] = i
               #isLiveArray[livelinessTable[line.arg1['ARG1']][0]] = False
               breakpoint()
            if line.arg2['ARG2'] in livelinessTable:
               livelinessTable[line.arg2['ARG2']][1] = i
        else:
            breakpoint()
            line.result['RESULT'] = line.result['RESULT']+str(v_no)
            #start_index = livelinessTable[line.result['RESULT']][0]
            #livelinessTable[line.result['RESULT']][1] = i
            #isLiveArray[start_index] = False
            livelinessTable.update({line.result['RESULT']:[i,None]})
            var_versions = [key for key in livelinessTable.keys() if key.startswith(line.arg1['ARG1'])]
            isLiveArray[i] = True
            linesExpanded[i][1] = True
            breakpoint()
            var_versions_extended = []
            for version in var_versions:
                start_index_for_version = livelinessTable[version][0] 
                verdict = linesExpanded[start_index_for_version][1]
                var_versions_extended.append([version,verdict])
                #breakpoint()
            breakpoint()
            #var_versions_extended = [i if n != 0 else None for n,i in enumerate(var_versions_extended.reverse())]
            var_versions_extended.reverse()
            for n,p in enumerate(var_versions_extended):
                if n != 0:
                    var_versions_extended[n][1] = False
            var_versions_extended.reverse()
            breakpoint()
            if line.arg1['ARG1'] in livelinessTable:
               for pair in var_versions_extended:
                   if pair[1] == False and livelinessTable[pair[0]][1] == None: 
                        livelinessTable[pair[0]][1] = i
               #isLiveArray[livelinessTable[line.arg1['ARG1']][0]] = False
            if line.arg2['ARG2'] in livelinessTable:
               livelinessTable[line.arg2['ARG2']][1] = i
            breakpoint()
            v_no = v_no + 1
            #breakpoint()
            #find the variable that this line is associated with
            #mark it not live and mark the new variable live
    """
    for threeAddrCode in threeAddressCode:
            #liveVariableAndRange = ['Live Variable':None,}
            print(threeAddrCode.operation,
                  threeAddrCode.arg1,threeAddrCode.arg2,
                  threeAddrCode.result, threeAddrCode.statement)
            breakpoint()
            end_index = None
            if threeAddrCode.statement['STATEMENT'] != 'return':
                if threeAddrCode.result['RESULT'] not in livelinessTable:
                #liveVariableAndRange['Live Variable'] = threeAddrCode.result['RESULT']
                #liveVariableAndRange['Live Range'].append(threeAddressCode.index(threeAddrCode))
                    livelinessTable.update({threeAddrCode.result['RESULT']:[threeAddressCode.index(threeAddrCode)]})
                    breakpoint()
                    if threeAddrCode.arg1['ARG1'] in livelinessTable:
                        end_index = threeAddressCode.index(threeAddrCode)
                        var_versions = [key for key in livelinessTable.keys() if key.startswith(threeAddrCode.arg1['ARG1'])]
                        var_versions_checked = 0
                        while var_versions_checked < len(var_versions):
                            if len(livelinessTable[var_versions[var_versions_checked]]) != 2:
                                livelinessTable[var_versions[var_versions_checked]].append(end_index)
                                break
                            var_versions_checked =  var_versions_checked + 1
                    elif threeAddrCode.arg2['ARG2'] in livelinessTable:
                        end_index = threeAddressCode.index(threeAddrCode)
                        var_versions = [key for key in livelinessTable.keys() if key.startswith(threeAddrCode.arg2['ARG2'])]
                        var_versions_checked = 0
                        while var_versions_checked < len(var_versions):
                            if len(livelinessTable[var_versions[var_versions_checked]]) != 2:
                                livelinessTable[var_versions[var_versions_checked]].append(end_index)
                                break
                            var_versions_checked =  var_versions_checked + 1       
                else:
                    if threeAddrCode.result['RESULT'] == threeAddrCode.arg1['ARG1'] \
                        or threeAddrCode.result['RESULT'] == threeAddrCode.arg2['ARG2']:
                        end_index = threeAddressCode.index(threeAddrCode)
                    else:
                        end_index = threeAddressCode.index(threeAddrCode) - 1
                    var_versions = [key for key in livelinessTable.keys() if key.startswith(threeAddrCode.result['RESULT'])]
                    var_versions_checked = 0
                    while var_versions_checked < len(var_versions):
                        if end_index not in livelinessTable[var_versions[var_versions_checked]]:
                            if len(livelinessTable[var_versions[var_versions_checked]]) == 2:
                                livelinessTable[var_versions[var_versions_checked]][-1] = end_index
                            else:
                                livelinessTable[var_versions[var_versions_checked]].append(end_index)
                            break
                        var_versions_checked =  var_versions_checked + 1
                    threeAddrCode.result['RESULT'] = threeAddrCode.result['RESULT'] + str(i)
                    livelinessTable.update({threeAddrCode.result['RESULT']:[threeAddressCode.index(threeAddrCode)]})
                    i = i + 1
                    breakpoint()
                    if threeAddrCode.arg1['ARG1'] in livelinessTable:
                        end_index = threeAddressCode.index(threeAddrCode)
                        var_versions = [key for key in livelinessTable.keys() if key.startswith(threeAddrCode.arg1['ARG1'])]
                        var_versions_checked = 0
                        while var_versions_checked < len(var_versions):
                            if end_index not in livelinessTable[var_versions[var_versions_checked]]:
                                if len(livelinessTable[var_versions[var_versions_checked]]) == 2:
                                    livelinessTable[var_versions[var_versions_checked]][-1] = end_index
                                else:
                                    livelinessTable[var_versions[var_versions_checked]].append(end_index)
                                break
                            var_versions_checked =  var_versions_checked + 1
                    if threeAddrCode.arg2['ARG2'] in livelinessTable:
                        end_index = threeAddressCode.index(threeAddrCode)
                        var_versions = [key for key in livelinessTable.keys() if key.startswith(threeAddrCode.arg2['ARG2'])]
                        var_versions_checked = 0
                        while var_versions_checked < len(var_versions):
                            if end_index not in livelinessTable[var_versions[var_versions_checked]]:
                                if len(livelinessTable[var_versions[var_versions_checked]]) == 2:
                                    #do other versions of the variable have an index that is within range 
                                    livelinessTable[var_versions[var_versions_checked]][-1] = end_index
                                else:
                                    livelinessTable[var_versions[var_versions_checked]].append(end_index)
                                break
                            var_versions_checked =  var_versions_checked + 1   

    """
    breakpoint()
    return livelinessTable 