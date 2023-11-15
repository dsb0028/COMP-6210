assembly = []
class Assembly:
    def __init__(self,mnemonic,label,operands,comments):
        
        self.label = label
        self.mnemonic = mnemonic
        self.operands = operands
        self.comments = comments
        
def createAssemblyCode(optimizedCode):
    # setting up esp/ebp
    asm = Assembly(mnemonic='push',label=None,operands='ebp',comments=None)
    assembly.append(asm)
    asm1 = Assembly(mnemonic='mov',label=None,operands=['ebp','esp'],comments=None)
    assembly.append(asm1)
    offset = 0
    offsets = []
    for line in optimizedCode:
        #label = None
        if line.statement['STATEMENT'] == 'Simple_Assignment_Statement':
            if type(line.arg1['ARG1']) == int:
                lab = 'DWORD PTR'
                offset = offset + 4
                asm2 = Assembly(mnemonic='mov',label=lab,
                    operands=['[ebp - '+str(offset)+']',line.arg1['ARG1']],comments=None)
                assembly.append(asm2)
                continue
        as3 = Assembly(mnemonic='mov',label='DWORD PTR',operands=['eax','[ebp - '+str(offset)+']'],comments=None)
        assembly.append(as3)
        as4 = Assembly(mnemonic='pop',label=None,operands=['ebp'],comments=None)
        assembly.append(as4)
        breakpoint()
        if line.statement['STATEMENT'] == 'return':
            as5 = Assembly(mnemonic='ret',label=None,operands=[],comments=None)
            assembly.append(as5)

    return assembly