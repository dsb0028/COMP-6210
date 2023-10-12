import argparse
import tokenizer
import parserC
import ThreeAddressCode
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
        print("Parse Tree",parseTree,'\n',"Symbol Table",symbolTable.table)
        print(astTree)
    threeAddressCode = ThreeAddressCode.createThreeAddressCode(parseTree,symbolTable)
    if args.a == True:
        pass
        #print(threeAddressCode)
if __name__ == "__main__":
    main()
