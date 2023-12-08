assembly = {}
class Assembly:
    def __init__(self,mnemonic,label,operands,comments):       
        self.label = label
        self.mnemonic = mnemonic
        self.operands = operands
        self.comments = comments
        
offset = 0
func = None
def createAssemblyCode(optimizedCode,symbolTable):
    functions = list(optimizedCode.keys())
    global func
    for func in functions:
        global offset
        offset = 0
        #offset = 0
        assembly.update({func:[]})
        #breakpoint()
        offset_var_pairs = []
        lab = None
        asm = Assembly(mnemonic='push',label=None,operands=['ebp'],comments=None)
        assembly[func].append(asm)
        asm1 = Assembly(mnemonic='mov',label=None,operands=['ebp','esp'],comments=None)
        assembly[func].append(asm1)
        #count how many local variables there are
        spaceToAllocToStack = len(symbolTable.table[func]['Variables'])
        asm2 = Assembly(mnemonic='sub',label=None,operands=['ebp',spaceToAllocToStack*4],comments=None)
        assembly[func].append(asm2)
        number_of_lines = len(optimizedCode[func])
        for i,line in enumerate(optimizedCode[func]):
            breakpoint()
            ret_var_offset = None
            if line.statement['STATEMENT'] == 'return':
                breakpoint()
                if offset_var_pairs != []:
                    for offset_var in offset_var_pairs:
                        print(offset_var,line.arg1['ARG1'])
                        if offset_var[0] == line.arg1['ARG1']:
                            ret_var_offset = offset_var[1]
                    lab = 'DWORD PTR'
                if ret_var_offset == None:
                    lab = None
                    ret_var_offset = line.arg1['ARG1']
                """
                as3 = Assembly(mnemonic='mov',label=lab,operands=['eax',ret_var_offset],comments=None)
                assembly[func].append(as3)
                as4 = Assembly(mnemonic='pop',label=None,operands=['ebp'],comments=None)
                assembly[func].append(as4)
                as5 = Assembly(mnemonic='ret',label=None,operands=[],comments=None)
                assembly[func].append(as5)
                """
        
            elif line.operation['Operation'] == '=':
                if type(line.arg1['ARG1']) == int:
                    lab = 'DWORD PTR'
                    #global offset
                    offset = offset + 4
                    offset_var_pairs.append((line.result['RESULT'],'[ebp - '+str(offset)+']'))     
                    asm2 = Assembly(mnemonic='mov',label=lab, operands=['[ebp - '+str(offset)+']',line.arg1['ARG1']],comments=None)
                    assembly[func].append(asm2)
                    
            
                elif str(line.arg1['ARG1']).isidentifier():
                    op1 = None
                    #breakpoint()
                    for offset_var in offset_var_pairs:
                        if offset_var[0] == line.arg1['ARG1']:
                            op1 = offset_var[1]
                            asm2 = Assembly(mnemonic='mov',label='DWORD PTR', operands=['eax',op1],comments=None)
                            assembly[func].append(asm2)
                    if op1 == None:
                        #breakpoint()
                        offset = offset + 4
                        offset_var_pairs.append((line.arg1['ARG1'],'[ebp - '+str(offset)+']'))
                        asm2 = Assembly(mnemonic='mov',label=lab, operands=['eax','[ebp - '+str(offset)+']'],comments=None)
                        assembly[func].append(asm2)
                    match = None
                    for offset_var in offset_var_pairs:
                        if offset_var[0] == line.result['RESULT']:
                            match = offset_var[0]
                            asm3 = Assembly(mnemonic='mov',label=lab, operands=[offset_var[1],'eax'],comments=None)
                            assembly[func].append(asm3)
                            break
                    if match == None:
                        offset = offset + 4
                        offset_var_pairs.append((line.result['RESULT'],'[ebp - '+str(offset)+']'))
                        asm3 = Assembly(mnemonic='mov',label='DWORD PTR', 
                                        operands=['[ebp - '+str(offset)+']','eax'],comments=None)
                        assembly[func].append(asm3)


            else:
                source_operand1, source_operand2 = getSourceOperands(offset_var_pairs, line) 
                register1 = 'eax'
                register2 = 'edx'
                as5 = generateIntr(line.operation['Operation'],source_operand1,source_operand2,register1,register2)
                assembly[func].append(as5)
                variableWrittenTo = line.result['RESULT']
                dest_mem = getDestMemory(offset_var_pairs, variableWrittenTo)                  
                as9 =  Assembly(mnemonic='mov',label='DWORD PTR', operands=[dest_mem,register1],comments=None)
                assembly[func].append(as9)
            if i == number_of_lines - 1:
                breakpoint()
                if ret_var_offset == None:
                    ret_var_offset = 0
                    lab = None
                as3 = Assembly(mnemonic='mov',label=lab,operands=['eax',ret_var_offset],comments=None)
                assembly[func].append(as3)
                as4 = Assembly(mnemonic='pop',label=None,operands=['ebp'],comments=None)
                assembly[func].append(as4)
                as5 = Assembly(mnemonic='ret',label=None,operands=[],comments=None)
                assembly[func].append(as5)
            
    
    return assembly


def generateIntr(operation,source_operand1,source_operand2,register1,register2):
    mnemonic = getMnemonic(operation)
    isSub = False
    if mnemonic == 'sub' or mnemonic == 'div':
        isSub = True
    allocateRegistersPreOperation(source_operand1,source_operand2,register1,register2,isSub)           
    line = generateArithmeticInstr(mnemonic,source_operand1, source_operand2, register1, register2)
    return line


def getDestMemory(offset_var_pairs, variableWrittenTo):
    dest_mem = None
    breakpoint()
    if offset_var_pairs != []:
        dest_mem = [offset_var[1] for offset_var in offset_var_pairs if offset_var[0] == variableWrittenTo]
        if dest_mem != []:
            dest_mem = dest_mem[0]
    if dest_mem == None or dest_mem == []:
        global offset
        offset = offset + 4
        offset_var_pairs.append((variableWrittenTo,'[ebp - '+str(offset)+']'))
        dest_mem = '[ebp - '+str(offset)+']'
    return dest_mem

def generateArithmeticInstr(mnemonic,source_operand1, source_operand2, register1, register2):
    label = None
    if isMemory(source_operand1) and isImmediate(source_operand2):
                    #print("S2",source_operand2)
        as5 = Assembly(mnemonic=mnemonic,label=None,operands=[register1,source_operand2],comments=None)
    elif isMemory(source_operand2) and isImmediate(source_operand1):
                    #print("S2",source_operand2,register1,line.arg1['ARG1'])
        if mnemonic == 'sub' or mnemonic == 'div':
            label = 'DWORD PTR'
            source_operand1 = source_operand2     
        as5 = Assembly(mnemonic=mnemonic,label=label,operands=[register1,source_operand1],comments=None)
    else:
        as5 = Assembly(mnemonic=mnemonic,label=None,operands=[register1,register2],comments=None)
    return as5

def getSourceOperands(offset_var_pairs, line):
    source_operand1 = None
    source_operand2 = None
    for offset_var in offset_var_pairs:
        if offset_var[0] == line.arg1['ARG1']:
           source_operand1 = offset_var[1]
        if offset_var[0] == line.arg2['ARG2']:
            source_operand2 = offset_var[1]
    if source_operand1 == None:
        source_operand1 = line.arg1['ARG1']
    if source_operand2 == None:
        source_operand2 = line.arg2['ARG2']
    return source_operand1,source_operand2

def allocateRegistersPreOperation(source_operand1,source_operand2,register1,register2,isSub=False):
    lab = None
    if isMemory(source_operand1):
        as6 = Assembly(mnemonic='mov',label='DWORD PTR',operands=[register1,source_operand1],comments=None)
        assembly[func].append(as6)
    if isMemory(source_operand2):
        as7 = None
        if isMemory(source_operand1) == False:
            #register1 = 'eax'
            if isSub != True:
                lab = 'DWORD PTR'
                as7 = Assembly(mnemonic='mov',label=lab,operands=[register1,source_operand2],comments=None)
            else:
                as7 = Assembly(mnemonic='mov',label=lab,operands=[register1,source_operand1],comments=None)
        else:
            #register2 = 'edx'
            as7 = Assembly(mnemonic='mov',label='DWORD PTR',operands=[register2,source_operand2],comments=None)
        assembly[func].append(as7)
    if isMemory(source_operand1) == False and isMemory(source_operand2) == False:
        as12 = Assembly(mnemonic='mov',label=None,operands=[register1,source_operand1],comments=None)
        assembly[func].append(as12)
        as13 = Assembly(mnemonic='mov',label=None,operands=[register2,source_operand2],comments=None)
        assembly[func].append(as13)
    
def isMemory(source_operand):
    verdict = False
    if type(source_operand) is str:
        if source_operand.startswith('['):
            verdict = True
    return verdict

def isImmediate(source_operand):
    verdict = False
    if type(source_operand) is not str:
        verdict = True
    return verdict

def getMnemonic(operation):
    mnemonic = None
    if operation == '+':
        mnemonic = 'add'
    elif operation == '-':
        mnemonic = 'sub'
    elif operation == '*':
        mnemonic = 'mult'
    elif operation == '/':
        mnemonic = 'div'
    return mnemonic

            

