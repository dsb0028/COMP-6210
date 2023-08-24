import argparse
import tokenizer


def main():
    """
    #s = 'gcd.cpp'
    #open the file before tokenizing 
    tokens = tokenizer.tokenize(s)
    
    print(parser.parse_args([]))
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=argparse.FileType('r'))
    args = parser.parse_args()

    s = args.file.readlines()
    
    tokens = tokenizer.tokenize(s)
    
    if tokens is not None:
        print(tokens)
    
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument(dest ='vars', action='store', nargs='?', type=str)
    parser.add_argument(dest = 'integers', action='store', nargs='*', type=int)
    
    
    args = parser.parse_args()
    print(args)
    """
    #s = read in file
    #tokens = tokenize(s)

    #if (printedOutTokens != Null):
    
if __name__ == "__main__":
    main()
