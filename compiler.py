import argparse
import tokenizer
import parserC
import copy


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', action='store_true')
    parser.add_argument('-p', action='store_true')
    parser.add_argument('file', type=argparse.FileType('r'))
    

    args = parser.parse_args()
    #print(args)
    s = args.file.read()
    
    #listToStr = ' '.join([str(elem) for elem in s])
    #parser.add_argument('-t', '--tokenizer', dest='tokens', action=tokenizer.tokenize(s))
    #args = parser.parse_args()
    cCopy = copy.deepcopy(s)
    tokens = tokenizer.tokenize(cCopy)
 
    #if -t is passed, print tokens
    if  args.t == True:
        print(tokens)
    
    """ Should the if statement below be in compiler.py or parserC.py? """
    # if c file just contains comments, there will be no tokens and no parse tree
    if not tokens:
        raise RuntimeError("Nothing to Parse")

    parseTree = parserC.createParseTree(tokens)
    if args.p == True:    
        print(parseTree)
    
if __name__ == "__main__":
    main()
