import argparse
import tokenizer
import parserC
import copy

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', action='store_true')
    parser.add_argument('file', type=argparse.FileType('r'))
    

    args = parser.parse_args()
    print(args)
    s = args.file.read()
    
    #listToStr = ' '.join([str(elem) for elem in s])
    #parser.add_argument('-t', '--tokenizer', dest='tokens', action=tokenizer.tokenize(s))
    #args = parser.parse_args()
    cCopy = copy.deepcopy(s)
    tokens = tokenizer.tokenize(cCopy)
    parseTree = parserC.createParseTree(tokens)
    #if -t is passed, printed
    if  args.t == True:
        print(tokens)
    print(parseTree)
if __name__ == "__main__":
    main()
