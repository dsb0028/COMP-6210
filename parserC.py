import re 

"""
Expr -> Expr + Term  | Expr - Term  | Term

Term -> Term * Factor  | Term / Factor  | Factor

Factor -> ( Expr )  | num  | ID

eliminate left recursion
Expr -> Term + Expr  | - Term + Expr  | Term

Term -> Factor * Term  | Factor / Term  | Factor

Factor -> ( Expr )  | num  | ID

"""

ExprRules = {"Expr + Term", "Exr - Term", "Term"}

#Used ChatGPT to create node class and functions
class TreeNode:
    def __init__(self,type, value=None):
        self.type =  type
        self.value = value
        self.children = []
    
    def addChild(self,child_type):
        self.children.append(child_type)
    
    def __str__(self, level=0):
        indent = " " * level
        result = f"{indent}{self.type}"
        if self.value is not None:
            result = f", Value: {self.value}"
        if self.children:
            result += "\n"
            for child in self.children:
                result += child.__str__()
        return result

root = TreeNode("Expr")
def createParseTree(data):
    validTree = False
    #if no op tokens exist, must be a term
    #print(data
    index = 0
    while index < len(data):
        expr = parseExpr(data,index)
        #root.addChild(expr)
        index = index + 1
    return root

def parseExpr(data,index):  
    if data[index].value == '+':
        root.addChild("+")
        root.addChild("Expr")

    term = parseTerm(data,index)
    
    #expr = parseExpr(data,index+1)
    """
    if term:
        root.addChild("Term")
    """
    """
    if len(data) > 1:
        #print("ok")
        parseExprPrime(data)
    #tree.append(subtree)
    #print("Final Tree", tree)
    """
    return term
    
def parseTerm(data,index):
    #print(tree)
    factor = parseFactor(data,index)
    """
    if factor:
        root.addChild("Factor")
    """
    #print(LHS)
    #tree.extend(str(LHS))
    #data.pop(0)

    """
    if len(data) > 1:
        #print("ok")
        subTree = parseTermPrime(data)
        print("Sub",subTree)
        #print("Tree",tree)
    #tree.append(subtree)
    """
    return factor

def parseFactor(data,index):
    if data[index].type == 'NUMBER':
        termNode = TreeNode("Term")
        root.addChild(termNode)
        factorNode = TreeNode("Factor")
        root.addChild(factorNode)
        numNode = TreeNode("NUMBER")
        root.addChild(numNode)
        val = TreeNode(data[index].value)
        root.addChild(val)
        return data[index].value
    
    elif data[index].type == 'ID':
        root.addChild('ID')
        #root.addChild(data[index].value)
        return data[index].value
    
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
    #print("D", data)
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