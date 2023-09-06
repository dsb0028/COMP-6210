import argparse
import tokenizer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=argparse.FileType('r'))
    parser.add_argument('-t')

    args = parser.parse_args()
    s = args.file.readlines()
    
    listToStr = ' '.join([str(elem) for elem in s])
    #parser.add_argument('-t', '--tokenizer', dest='tokens', action=tokenizer.tokenize(s))
    #args = parser.parse_args()

    tokens = tokenizer.tokenize(listToStr)
    
    if tokens is not None:
        print(tokens)
    
if __name__ == "__main__":
    main()
