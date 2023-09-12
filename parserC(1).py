import re 

"""
Expr -> Expr + Term  | Expr - Term  | Term

Term -> Term * Factor  | Term / Factor  | Factor

Factor -> ( Expr )  | num  | ID

eliminate left recursion

Expr -> Term Expr'

Expr' -> + Term Expr' | - Term Expr' | epsilon

Term -> Factor Term' 

Term' -> * Factor Term' | / Factor Term' | epsilon

Factor -> ( Expr )  | num  | ID



"""

ExprRules = {"Expr + Term", "Exr - Term", "Term"}
tree = []
subTree = []
def createParseTree(data):
    #if no op tokens exist, must be a term
    #print(data)
    values = [tok.value for tok in data]
    subTree = parseExpr(data)
    #print("subTree",subTree)
    return tree

def parseExpr(data):
    subTree = parseTerm(data)
    if len(data) > 1 and (data[1].value == '+' or data[1].value == '-'):
        #print("ok")
        parseExprPrime(data)
    #tree.append(subtree)
    #print("Final Tree", tree)
    return subTree

def parseTerm(data):
    subTree = []
    LHS = parseFactor(data)
    #print(LHS)
    tree.extend(str(LHS))
    data.pop(0)

    #print(tree)
    if len(data) > 1:
        print(True, data[0])
    if len(data) > 1 and (data[1].value == '*' or data[1].value == '/'):
        #print("ok")
        subTree = parseTermPrime(data)
        print("Sub",subTree)
        #print("Tree",tree)
    #tree.append(subtree)
    return subTree

def parseFactor(data):
    #print("Data",data)
    if data[0].type == 'NUMBER':
        return data[0].value
    """
    elif data[0].type == 'ID':
        return data[0].value
    """
def parseExprPrime(data):
    if data[0].value == '+':
        tree.extend(str(data[0].value))
        data.pop(0)
        parseTerm(data)
        print("Tree",tree)
        #data.pop(0)
    elif data[0].value == '-':
        tree.extend(parseTerm(data))
    if len(data) > 1:
        parseExprPrime(data)
    return tree

def parseTermPrime(data):
    print("D", data)
    if data[0].value == '*':
        tree.extend(str(data[0].value))
        #print(tree)
        #print("Entered")
        #print("0", data)
        #print("cool")
        #need get the next token to ensure that there is a factor after '+' token
        # if the next token does not contain a factor, throw an error (may need a try catch) 
        data.pop(0)
        #print("1", data)
        tree.extend(str(parseFactor(data)))
        #print(tree)
        data.pop(0)
        #print("2",data)
    elif data[0].value == '/':
        tree.extend(str(data[0].value))
        data.pop(0)
        tree.extend(str(parseFactor(data)))
        data.pop(0)
        #parseTermPrime(data)
    if len(data) > 1:
        parseTermPrime(data)

    return tree
"""
def parseExpr(data):
    subTree = []
    #subTree.append(parseTerm(data[0]))
    #ops = [tok for tok in data if tok.type == 'MATH_OP']
    
    #check for the existence of an op token (+ | -)
    #maybe have some function that matches a + or - to determine production rule
    #if '+' or '-' op token is found locate the index of the op token 
    #if op token is a '+'
    #   store left hand side of '+' as term, append the '+' token to Expr, then check for token after '+'
    #      i.e. if the '+' token is the last token, return error '<production rule> : expected a term 
    #if op token is a '-'
    #   Choose production Expr - Term
    #   store left hand side of '-' as term, append the '-' token to Expr, then check for token after '-'
    #      i.e if the '-' token is the last token, return error '<production rule> : expected a term 
    #else
    #   replace Expr with Term
    #   Term
    return subTree
"""

"""
def parseTerm(data):
    subTree = parseFactor(data)
    #check for next token to be    
    return subTree

def parseFactor(data):
    return data.value
"""


"""
class Node:
    def __init__(self,key):
        self.left = None
        self.right = None
        self.val = key
    
    def insert(temp, key):
        if temp.key is None:
            temp.key = key
        if not temp.left:
            temp.left = temp.insert(temp.left, key)
        if not temp.right:
            temp.right = temp.insert(temp.right, key)


if __name__ == '__main__':
    main()
"""    