from symboltable import *
#from parserC import *
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
threeAddressCode = {}
def createThreeAddressCode(astTree,symbolTable):
    print(astTree)
    for item in recursive_items(astTree):
        print(item)
    """
    for key,val in astTree.items():
        print(key, val)
    """
    #terminalNodes.clear()
    #findTerminalNodes(astTree)
    #print(terminalNodes)
    return threeAddressCode

def recursive_items(dictionary):
    for key, value in dictionary.items():
        if type(value) is dict:
            yield key
            yield from recursive_items(value)
        else:
            yield (key, value)