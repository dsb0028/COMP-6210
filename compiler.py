import argparse
import tokenizer
import parserC
from ThreeAddressCode import *
from pprint import pprint 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', action='store_true')
    parser.add_argument('-p', action='store_true')
    parser.add_argument('-a',action='store_true')
    parser.add_argument('file', type=argparse.FileType('r'))
    args = parser.parse_args()
    #print(args)
    s = args.file.read()
    tokens = tokenizer.tokenize(s)
    #if -t is passed, print tokens
    if  args.t == True:
        print("Tokens",tokens,'\n')
    # if c file just contains comments, there will be no tokens and no parse tree
    if not tokens:
        raise RuntimeError("Nothing to Parse")
    parseTree,astTree,symbolTable = parserC.createParseTree(tokens)
    #ast = parserC.createAST(parseTree)
    if args.p == True:    
        print("Parse Tree",parseTree,'\n',"Symbol Table",symbolTable.table,'\n')
        print("AST",astTree,'\n')
    threeAddressCode = createThreeAddressCode(astTree,symbolTable)
    print(threeAddressCode)
    if args.a == True:
        
        for threeAddrCode in threeAddressCode['Three_Address_Code']:
            #print(threeAddressCode)
            #print(threeAddrCode.statement)
            #if threeAddrCode.statement == 'Assignment_Statement':
            if threeAddrCode.statement['STATEMENT'] == 'return':
                print(threeAddrCode.statement,threeAddrCode.arg1)
            else:
                  print(threeAddrCode.operation, threeAddrCode.arg1, threeAddrCode.arg2, 
                      threeAddrCode.result, threeAddrCode.statement)
            #elif threeAddrCode.statement == 'return':
            #    pass
           
        #print(ThreeAddressCode.__str__(threeAddressCode,threeAddressCodeDict=threeAddressCode))
if __name__ == "__main__":
    main()
