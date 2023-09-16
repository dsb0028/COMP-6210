import argparse
import tokenizer
import parserC
import copy

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', action='store_true')
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
    
    
    parseTree = parserC.createParseTree(tokens)
    """
    root = parserC.TreeNode("Expr")
    term = parserC.TreeNode("Term")
    plusSign = parserC.TreeNode("+")
    expr = parserC.TreeNode("Expr")
    factor = parserC.TreeNode("Factor")
    number = parserC.TreeNode("NUMBER")
    value1 = parserC.TreeNode("4")
    term1 = parserC.TreeNode("Term")
    root.addChild(term)
    root.addChild(plusSign)
    root.addChild(expr)
    expr   
    #term.addChild(factor)
    #factor.addChild(number)
    #number.addChild(value1)

    #expr.addChild(term1)
    print(root)
    """
    print(parseTree)
    #print(parseTree.children)
    #childs = [child for child in parseTree.children]
    #print(childs)
if __name__ == "__main__":
    main()
