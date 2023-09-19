import argparse
import tokenizer
import parserC
import copy


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', action='store_true')
    #parser.add_argument('-p', action='store_true')
    parser.add_argument('file', type=argparse.FileType('r'))
    

    args = parser.parse_args()
    #print(args)
    s = args.file.read()
    
    #listToStr = ' '.join([str(elem) for elem in s])
    #parser.add_argument('-t', '--tokenizer', dest='tokens', action=tokenizer.tokenize(s))
    #args = parser.parse_args()
    cCopy = copy.deepcopy(s)
    tokens = tokenizer.tokenize(cCopy)
 
    #if -t is passed, printed
    if  args.t == True:
        print(tokens)
    
    #tCopy = copy.deepcopy(tokens)
    parseTree = parserC.createParseTree(tokens)
    
    print(parseTree)
    
    #print(parseTree.children)
    #childs = [child for child in parseTree.children]
    #print(childs)
if __name__ == "__main__":
    main()
