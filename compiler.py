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
    if args.a == True:
        print(threeAddressCode['Three_Address_Code'][0].operation,
              threeAddressCode['Three_Address_Code'][0].arg1,
              threeAddressCode['Three_Address_Code'][0].arg2,
              threeAddressCode['Three_Address_Code'][0].result)
        
        print(threeAddressCode['Three_Address_Code'][1].operation,
              threeAddressCode['Three_Address_Code'][1].arg1,
              threeAddressCode['Three_Address_Code'][1].arg2,
              threeAddressCode['Three_Address_Code'][1].result)
        
        print(threeAddressCode['Three_Address_Code'][2].operation,
              threeAddressCode['Three_Address_Code'][2].arg1,
              threeAddressCode['Three_Address_Code'][2].arg2,
              threeAddressCode['Three_Address_Code'][2].result)
        
        print(threeAddressCode['Three_Address_Code'][3].operation,
              threeAddressCode['Three_Address_Code'][3].arg1,
              threeAddressCode['Three_Address_Code'][3].arg2,
              threeAddressCode['Three_Address_Code'][3].result)
        
        print(threeAddressCode['Three_Address_Code'][4].operation,
              threeAddressCode['Three_Address_Code'][4].arg1,
              threeAddressCode['Three_Address_Code'][4].arg2,
              threeAddressCode['Three_Address_Code'][4].result)
        #print(ThreeAddressCode.__str__(threeAddressCode,threeAddressCodeDict=threeAddressCode))
if __name__ == "__main__":
    main()
