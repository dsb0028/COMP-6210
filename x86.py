assembly = []
class Assembly:
    def __init__(self,mnemonic,label,operands,comments):       
        self.label = label
        self.mnemonic = mnemonic
        self.operands = operands
        self.comments = comments
        
def createAssemblyCode(optimizedCode):
    # setting up esp/ebp
    breakpoint()
    asm = Assembly(mnemonic='push',label=None,operands=['ebp'],comments=None)
    assembly.append(asm)
    asm1 = Assembly(mnemonic='mov',label=None,operands=['ebp','esp'],comments=None)
    assembly.append(asm1)
    offset = 0
    offset_var_pairs = []
    for line in optimizedCode:
        breakpoint()
        if line.operation['Operation'] == '=':
            if type(line.arg1['ARG1']) == int:
                lab = 'DWORD PTR'
                offset = offset + 4
                offset_var_pairs.append((line.result['RESULT'],'[ebp - '+str(offset)+']'))
                asm2 = Assembly(mnemonic='mov',label=lab,
                    operands=['[ebp - '+str(offset)+']',line.arg1['ARG1']],comments=None)
                assembly.append(asm2)
                continue
        elif line.operation['Operation'] == '+':
            source_operand1 =  None
            source_operand2 = None
            for offset_var in offset_var_pairs:
                if offset_var[0] == line.arg1['ARG1']:
                   source_operand1 = offset_var[1]
                elif offset_var[0] == line.arg2['ARG2']:
                    source_operand2 = offset_var[1] 
            register1 = None
            register2 = None
            if source_operand1 != None:
                register1 = 'eax'
                as6 = Assembly(mnemonic='mov',label='DWORD PTR',operands=[register1,source_operand1],comments=None)
                assembly.append(as6)
            if source_operand2 != None:
                if source_operand1 == None:
                    register1 = 'eax'
                    as7 = Assembly(mnemonic='mov',label='DWORD PTR',operands=[register1,source_operand2],comments=None)
                else:
                    register2 = 'edx'
                    as7 = Assembly(mnemonic='mov',label='DWORD PTR',operands=[register2,source_operand2],comments=None)
                assembly.append(as7)
            #print("R1",register1,"R2",register2)
            if register2 != None:
                as5 = Assembly(mnemonic='add',label=None,operands=[register1,register2],comments=None)
            elif register1 != None:
                if source_operand2 == None:
                    #print("S2",source_operand2)
                    as5 = Assembly(mnemonic='add',label=None,operands=[register1,line.arg2['ARG2']],comments=None)
                else:
                    #print("S2",source_operand2,register1,line.arg1['ARG1'])

                    as5 = Assembly(mnemonic='add',label=None,operands=[register1,line.arg1['ARG1']],comments=None)
            assembly.append(as5)
            offset = offset + 4
            offset_var_pairs.append((line.result['RESULT'],'[ebp - '+str(offset)+']'))
            as9 =  Assembly(mnemonic='mov',label='DWORD PTR',
                            operands=['[ebp - '+str(offset)+']',register1],comments=None)
            assembly.append(as9)
        elif line.operation['Operation'] == '-':
            source_operand1 =  None
            source_operand2 = None
            for offset_var in offset_var_pairs:
                if offset_var[0] == line.arg1['ARG1']:
                   source_operand1 = offset_var[1]
                elif offset_var[0] == line.arg2['ARG2']:
                    source_operand2 = offset_var[1] 
            register1 = None
            register2 = None
            if source_operand1 != None:
                register1 = 'eax'
                as6 = Assembly(mnemonic='mov',label='DWORD PTR',operands=[register1,source_operand1],comments=None)
                assembly.append(as6)
            if source_operand2 != None:
                if source_operand1 == None:
                    register1 = 'eax'
                    as7 = Assembly(mnemonic='mov',label=None,operands=[register1,line.arg1['ARG1']],comments=None)
                else:
                    register2 = 'edx'
                    as7 = Assembly(mnemonic='mov',label='DWORD PTR',operands=[register2,source_operand2],comments=None)
                assembly.append(as7)
            #print("R1",register1,"R2",register2)
            if register2 != None:
                as5 = Assembly(mnemonic='sub',label=None,operands=[register1,register2],comments=None)
            elif register1 != None:
                if source_operand2 == None:
                    #print("S2",source_operand2)
                    as5 = Assembly(mnemonic='sub',label=None,operands=[register1,line.arg2['ARG2']],comments=None)
                else:
                    #print("S2",source_operand2,register1,line.arg1['ARG1'])
                    as5 = Assembly(mnemonic='sub',label='DWORD PTR',operands=[register1,source_operand2],comments=None)
            assembly.append(as5)
            offset = offset + 4
            offset_var_pairs.append((line.result['RESULT'],'[ebp - '+str(offset)+']'))
            as9 =  Assembly(mnemonic='mov',label='DWORD PTR',
                            operands=['[ebp - '+str(offset)+']',register1],comments=None)
            assembly.append(as9)
        elif line.operation['Operation'] == '*':
            source_operand1 =  None
            source_operand2 = None
            for offset_var in offset_var_pairs:
                #print(offset_var)
                if offset_var[0] == line.arg1['ARG1']:
                   source_operand1 = offset_var[1]
                elif offset_var[0] == line.arg2['ARG2']:
                    source_operand2 = offset_var[1] 
            register1 = None
            register2 = None
            if source_operand1 != None:
                register1 = 'eax'
            if source_operand2 != None:
                register2 = 'edx'
            as6 = Assembly(mnemonic='mov',label='DWORD PTR',operands=[register1,source_operand1],comments=None)
            assembly.append(as6)
            as7 = Assembly(mnemonic='mov',label='DWORD PTR',operands=[register2,source_operand2],comments=None)
            assembly.append(as7)
            as5 = Assembly(mnemonic='mult',label=None,operands=[register1,register2],comments=None)    
            assembly.append(as5)
            offset = offset + 4
            offset_var_pairs.append((line.result['RESULT'],'[ebp - '+str(offset)+']'))
            as9 =  Assembly(mnemonic='mov',label='DWORD PTR',
                            operands=['[ebp - '+str(offset)+']',register1],comments=None)
            assembly.append(as9)
        if line.statement['STATEMENT'] == 'return':
            ret_var_offset = None
            for offset_var in offset_var_pairs:
                print(offset_var,line.arg1['ARG1'])
                if offset_var[0] == line.arg1['ARG1']:
                    ret_var_offset = offset_var[1]
            as3 = Assembly(mnemonic='mov',label='DWORD PTR',operands=['eax',ret_var_offset],comments=None)
            assembly.append(as3)
            as4 = Assembly(mnemonic='pop',label=None,operands=['ebp'],comments=None)
            assembly.append(as4)
            as5 = Assembly(mnemonic='ret',label=None,operands=[],comments=None)
            assembly.append(as5)

    return assembly