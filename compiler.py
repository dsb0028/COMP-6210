import argparse
import tokenizer
import parserC

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', action='store_true')
    parser.add_argument('-p', action='store_true')
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
    parseTree,symbolTable = parserC.createParseTree(tokens)
    #ast = parserC.createAST(parseTree)
    if args.p == True:    
        print("Parse Tree",parseTree,'\n',"Symbol Table",symbolTable.table)
    
if __name__ == "__main__":
    main()
