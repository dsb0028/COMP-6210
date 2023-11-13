import argparse
import tokenizer
import parserC
import optimizer
from ThreeAddressCode import *
from pprint import pprint

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', action='store_true')
    parser.add_argument('-p', action='store_true')
    parser.add_argument('-a',action='store_true')
    parser.add_argument('-O2',action='store_true')
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
        #from https://stackoverflow.com/questions/17280534/prettyprint-to-a-file  
        with open('parseTree.txt', 'wt') as out:
            pprint(parseTree, stream=out,sort_dicts=False)
        print("Parse Tree",parseTree,'\n',"Symbol Table",symbolTable.table,'\n')
        #from https://stackoverflow.com/questions/17280534/prettyprint-to-a-file  
        with open('astTree.txt', 'wt') as out:
            pprint(astTree, stream=out,sort_dicts=False)
        #print("AST",astTree,'\n')
    breakpoint()
    threeAddressCode = createThreeAddressCode(astTree,symbolTable)
    if args.a == True:
        for threeAddrCode in threeAddressCode['Three_Address_Code']:
            if threeAddrCode.statement['STATEMENT'] == 'return':
                print(threeAddrCode.statement,threeAddrCode.arg1)
            else:
                  print(threeAddrCode.operation, threeAddrCode.arg1, threeAddrCode.arg2, 
                      threeAddrCode.result, threeAddrCode.statement)
            #elif threeAddrCode.statement == 'return':
            #    pass
        print('\n')
           
        #print(ThreeAddressCode.__str__(threeAddressCode,threeAddressCodeDict=threeAddressCode))
    optimizedCode = optimizer.performOptimizations(threeAddressCode['Three_Address_Code'])
    if args.O2 == True:
        """
        for threeAddrCode in optimizedCode:
            print(threeAddrCode.operation,threeAddrCode.arg1, 
              threeAddrCode.arg2, 
              threeAddrCode.result, threeAddrCode.statement)
        """
        for threeAddrCode in optimizedCode:
            if threeAddrCode.statement['STATEMENT'] == 'return':
                print(threeAddrCode.statement,threeAddrCode.arg1)
            else:
                  print(threeAddrCode.operation, threeAddrCode.arg1, threeAddrCode.arg2, 
                      threeAddrCode.result, threeAddrCode.statement)
            #elif threeAddrCode.statement == 'return':
            #    pass
        print('\n')
if __name__ == "__main__":
    main()
