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

exprRules = {"Term ExprP"}
exprPRules = {"+ Term ExprP", "- Term ExprP"}
termRules = {"Factor TermP"}
termPrimeRules = {"* Factor TermP", "/ Factor TermP"}
factorRules = {"(Expr)", "NUMBER", "ID"}

terminals = {"+", "-", "*", "/", "(", ")", "num", "ID"}

#Used ChatGPT to create node class and functions


"""
class TreeNode:
    def __init__(self,type,value=None):
        self.type =  type
        self.value = value
        self.children = []
    
    def addChild(self,child_type):
        self.children.append(child_type)
"""

#treeDict = {'Expr': {'Term':{'Factor': {'NUMBER':{4}},'TermP':' '},'ExprP': {'+':'','Term':{'Factor':{'NUMBER':{4}}, 'TermP':''},'ExprP':''}}}
#treeDict1 = {'Expr': {'Term':{'Factor':{'NUMBER':''}}, 'TermP':{}},'ExprP':{}}}
#treeDict2 = {'Expr': {'Term': {'Factor': {'NUMBER': {4}}}, 'TermP': {}}, 'ExprP': {}}
#treeDict3 = {'Expr': {'Term': {'Factor': {'NUMBER': {4}}, 'TermP': {}}, 'ExprP': {}}}
treeDict4  = {'Expr': {'Term': {'Factor': {'NUMBER': {4}}, 'TermP': {}}, 'ExprP': {'-': {}, 'Term': {'Factor': {'NUMBER': {5}}, 'TermP': {}}, 'ExprP': {'+': {}, 'Term': {'Factor': {'NUMBER': {5}}, 'TermP': {}}, 'ExprP': {}}}}}
#root = TreeNode("Expr")
def createParseTree(data):
    #validTree = False
    #if no op tokens exist, must be a term
    #print(data
    treeD = {'Expr':{}}
    expr = parseExpr(data)
    if expr:
        treeD = expr 
        #root.addChild(expr)
    return treeD

def parseExpr(data):  
    exprDict = {'Expr':{}}
    
    term = parseTerm(data)
    if term:
        exprDict['Expr']['Term'] = term['Term']
    #expr = parseExpr(data,index+1)
    
    exprPrime = parseExprPrime(data) 
    if exprPrime:
        #print(exprPrime)
        #tempSet = frozenset(exprPrime)
        #print(tempSet)
        #frozenset(set(exprDict['Expr']).add(tempSet))
        exprDict['Expr']['ExprP'] = exprPrime['ExprP']
    else:
        exprDict['Expr']['ExprP'] = {}
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
    return exprDict
    
def parseTerm(data):
    termDict = {'Term':{}}
    factor = parseFactor(data)
    if factor:
        termDict['Term']['Factor'] = factor['Factor']
    
    termPrime = parseTermPrime(data)

    if termPrime:
        termDict['Term']['TermP'] = termPrime['TermP']
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
    return termDict

def parseFactor(data):
    factorDict = {'Factor':{}}
    if data[0].type == 'NUMBER':
        #termDict = {'Term':'Term'}
        #root.addChild(termNode)
        #factorNode = TreeNode("Factor")
        #root.addChild(factorNode)
        #numNode = TreeNode("NUMBER")
        #root.addChild(numNode)
        #val = TreeNode(data[index].value)
        #root.addChild(val)
        factorDict['Factor'] = {'NUMBER':{data[0].value}}
        return factorDict
    
    elif data[0].type == 'ID':
        factorDict['Factor'] = {'ID':{data[0].value}}
        #root.addChild(data[index].value)
        return factorDict
    

def parseExprPrime(data):
    print("Entered ExprPrime")
    exprPrimeDict = {'ExprP':{}}
    
    if data:
        data.pop(0)
        if data[0].value == '+':
            #plusSign = data.value
            exprPrimeDict['ExprP']['+'] = {} 
            data.pop(0)
            term = parseTerm(data)
        
        #print('\n',"Term",term)
            if term:
                exprPrimeDict['ExprP']['Term'] = term['Term']
        
            exprPrime = parseExprPrime(data)
            
            if exprPrime:
                exprPrimeDict['ExprP']['ExprP'] = exprPrime['ExprP']
        #tree.extend(str(data[index].value))
        #data.pop(0)
        #parseTerm(data)
        #print("Tree",tree)
        #data.pop(0)
        elif data[0].value == '-':
            exprPrimeDict['ExprP']['-'] = {}
            data.pop(0)
            term = parseTerm(data)

            if term:
                exprPrimeDict['ExprP']['Term'] = term['Term']
        
            exprPrime = parseExprPrime(data)
            
            if exprPrime:
                exprPrimeDict['ExprP']['ExprP'] = exprPrime['ExprP']

   
    return exprPrimeDict

def parseTermPrime(data):
    #print("D", data)
    termPrimeDict = {'TermP':{}}
    data.pop(0)
    if data:
        if data[0].value == '*':
            termPrimeDict['TermP']['*'] = {} 
            data.pop(0)
            factor = parseFactor(data)
        
        #print('\n',"Term",term)
            if factor:
                termPrimeDict['TermP']['Factor'] = factor['Factor']
        
            termPrime = parseTermPrime(data)
        
            if termPrime:
                termPrimeDict['TermP']['TermP'] = termPrime['TermP']
            pass
        elif data[0].value == '/':
            #tree.extend(str(data[0].value))
            #data.pop(0)
            #tree.extend(str(parseFactor(data)))
            #data.pop(0)
            #parseTermPrime(data)
            pass
    return termPrimeDict

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

"""
def main():
    #tokens = [(), (), (), ()]    
    pass


if __name__ == '__main__':
    main()
