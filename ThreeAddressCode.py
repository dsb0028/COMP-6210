from symboltable import *
from parserC import *
"""
class ThreeAddressCode():
    def __init__(self,parseTree):
        self.parseTree = parseTree
        self.threeAddressCode = {}
"""    
"""
Initalize a variable that is of the same type as the return type of each function
For example, if the return_type of main() is of type int, 
int A.####;, where #### is a 4-digit randomly generated number
for each declaration
"""
def createThreeAddressCode(parseTree,symbolTable):
    terminalNodes.clear()
    findTerminalNodes(parseTree)
    #print(terminalNodes)
    
    return 0
