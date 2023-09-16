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


"""
#treeDict = {'Expr': {'Term':{'Factor': {'NUMBER':{4}},'TermP':' '},'ExprP': {'+':'','Term':{'Factor':{'NUMBER':{4}}, 'TermP':''},'ExprP':''}}}
#treeDict2 = {'Expr': {'Term': {'Factor': {'NUMBER': {4}}}, 'TermP': {}}, 'ExprP': {}}
treeDict3 = {'Expr': {'Term': {'Factor': {'NUMBER': {4}}, 'TermP': {}}, 'ExprP': {}}}

treeDict4  = {'Expr': {'Term': {'Factor': {'NUMBER': {4}}, 'TermP': {}}, 'ExprP': {'-': {}, 'Term': {'Factor': {'NUMBER': {5}}, 'TermP': {}}, 'ExprP': {'+': {}, 'Term': {'Factor': {'NUMBER': {5}}, 'TermP': {}}, 'ExprP': {}}}}}
treeDict5 = {'Expr': {'Term': {'Factor': {'NUMBER': {4}}, 'TermP': {'*': {}, 'Factor': {'NUMBER': {4}}, 'TermP': {}}}, 'ExprP': {}}}
treeDict6 = {'Expr': {'Term': {'Factor': {'NUMBER': {4}}, 'TermP': {'*': {}, 'Factor': {'NUMBER': {5}}, 'TermP': {'/': {}, 'Factor': {'NUMBER': {4}}, 'TermP': {}}}}, 'ExprP': {}}} #4 * 5 / 4
treeDict7 = {'Expr': {'Term': {'Factor': {'NUMBER': {4}}, 'TermP': {}}, 'ExprP': {'+': {}, 'Term': {'Factor': {'NUMBER': {7}}, 'TermP': {'/': {}, 'Factor': {'NUMBER': {4}}, 'TermP': {}}}, 'ExprP': {}}}}
treeDict8 = {'Expr': {'Term': {'Factor': {'NUMBER': {4}}, 'TermP': {}}, 'ExprP': {'+': {}, 'Term': {'Factor': {'NUMBER': {4}}, 'TermP': {}}, 'ExprP': {'-': {}, 'Term': {'Factor': {'NUMBER': {4}}, 'TermP': {}}, 'ExprP': {}}}}} #4 + 4 - 4
treeDict9 = {'Expr': {'Term': {'Factor': {'NUMBER': {4}}, 'TermP': {}}, 'ExprP': {'-': {}, 'Term': {'Factor': {'NUMBER': {4}}, 'TermP': {}}, 'ExprP': {'+': {}, 'Term': {'Factor': {'NUMBER': {4}}, 'TermP': {}}, 'ExprP': {}}}}} #4 - 4 + 4
treeDict10 = {'Expr': {'Term': {'Factor': {'NUMBER': {4}}, 'TermP': {}}, 'ExprP': {'+': {}, 'Term': {'Factor': {'NUMBER': {8}}, 'TermP': {'*': {}, 'Factor': {'NUMBER': {4}}, 'TermP': {}}}, 'ExprP': {}}}} #4 + 8 * 4
treeDict11 = {'Expr': {'Term': {'Factor': {'NUMBER': {4}}, 'TermP': {}}, 'ExprP': {'+': {}, 'Term': {'Factor': {'NUMBER': {8}}, 'TermP': {'/': {}, 'Factor': {'NUMBER': {4}}, 'TermP': {}}}, 'ExprP': {}}}} #4 + 8 / 4 
treeDict12 = {'Expr': {'Term': {'Factor': {'NUMBER': {4}}, 'TermP': {}}, 'ExprP': {'-': {}, 'Term': {'Factor': {'NUMBER': {8}}, 'TermP': {'/': {}, 'Factor': {'NUMBER': {4}}, 'TermP': {}}}, 'ExprP': {}}}} #4 - 8 / 4  
treeDict13 = {'Expr': {'Term': {'Factor': {'NUMBER': {4}}, 'TermP': {}}, 'ExprP': {'-': {}, 'Term': {'Factor': {'NUMBER': {8}}, 'TermP': {'/': {}, 'Factor': {'NUMBER': {4}}, 'TermP': {}}}, 'ExprP': {'+': {}, 'Term': {'Factor': {'NUMBER': {2}}, 'TermP': {}}, 'ExprP': {}}}}} # 4 - 8 / 4 + 2
treeDict14 = {'Expr': {'Term': {'Factor': {'NUMBER': {4}}, 'TermP': {}}, 'ExprP': {'+': {}, 'Term': {'Factor': {'NUMBER': {8}}, 'TermP': {'/': {}, 'Factor': {'NUMBER': {4}}, 'TermP': {}}}, 'ExprP': {'-': {}, 'Term': {'Factor': {'NUMBER': {2}}, 'TermP': {}}, 'ExprP': {}}}}} # 4 + 8 / 4 - 2
treeDict15 = {'Expr': {'Term': {'Factor': {'NUMBER': {4}}, 'TermP': {}}, 'ExprP': {'+': {}, 'Term': {'Factor': {'NUMBER': {8}}, 'TermP': {'*': {}, 'Factor': {'NUMBER': {4}}, 'TermP': {}}}, 'ExprP': {'-': {}, 'Term': {'Factor': {'NUMBER': {2}}, 'TermP': {}}, 'ExprP': {}}}}} # 4 + 8 * 4 - 2
treeDict16 = {'Expr': {'Term': {'Factor': {'NUMBER': {4}}, 'TermP': {}}, 'ExprP': {'+': {}, 'Term': {'Factor': {'NUMBER': {8}}, 'TermP': {'*': {}, 'Factor': {'NUMBER': {4}}, 'TermP': {}}}, 'ExprP': {'-': {}, 'Term': {'Factor': {'NUMBER': {2}}, 'TermP': {'/': {}, 'Factor': {'NUMBER': {8}}, 'TermP': {}}}, 'ExprP': {}}}}} #4 + 8 * 4 - 2 / 8
treeDict17 = {'Expr': {'Term': {'Factor': {'NUMBER': {4}}, 'TermP': {}}, 'ExprP': {'+': {}, 'Term': {'Factor': {'NUMBER': {8}}, 'TermP': {}}, 'ExprP': {'+': {}, 'Term': {'Factor': {'NUMBER': {4}}, 'TermP': {}}, 'ExprP': {'-': {}, 'Term': {'Factor': {'NUMBER': {2}}, 'TermP': {'/': {}, 'Factor': {'NUMBER': {8}}, 'TermP': {}}}, 'ExprP': {}}}}}} #4 + 8 + 4 - 2 / 8
treeDict19 = {'Expr':{'Term': {'Factor':{'LPAREN':'(','Expr':{'Term': {'Factor':{'NUMBER':{4}}, 'TermP':{}},'ExprP':{'+': {}, 'Term':{'Factor':{'NUMBER':{8}},'TermP':{}}, 'ExprP':{}}}, 'RPAREN':')'}, 'TermP':{} }, 'ExprP':{}}}
"""
 
def createParseTree(data):
    expr = parseExpr(data)
    #if expr:
    #treeD = expr 
        #root.addChild(expr)
    return expr

def parseExpr(data):  
    exprDict = {'Expr':{}}
    term = parseTerm(data)
    if term:
        exprDict['Expr']['Term'] = term['Term']
    #expr = parseExpr(data,index+1)
    exprPrime = parseExprPrime(data) 
    if exprPrime:
        exprDict['Expr']['ExprP'] = exprPrime['ExprP']
        #treeD['Expr']['ExprP'] = exprPrime['ExprP']
    else:
        exprDict['Expr']['ExprP'] = {}
        #treeD['Expr']['ExprP'] = {}
    #treeD['Expr'] = exprDict['Expr']
    return exprDict
    
def parseTerm(data):
    termDict = {'Term':{}}
    factor = parseFactor(data)
    #print("Factor", factor)
    if factor:
        termDict['Term']['Factor'] = factor['Factor']
    
    termPrime = parseTermPrime(data)

    if termPrime:
        termDict['Term']['TermP'] = termPrime['TermP']
    return termDict

def parseFactor(data):
    factorDict = {'Factor':{}}
    if data[0].type == 'LPAREN':
        factorDict['Factor']['LPAREN'] = '('
        data.pop(0)
        expr = parseExpr(data)
        if expr:
            factorDict['Factor']['Expr'] = expr['Expr']
        factorDict['Factor']['RPAREN'] = ')'
        return factorDict
    if data[0].type == 'NUMBER':
        factorDict['Factor'] = {'NUMBER':{data[0].value}}
        return factorDict
    elif data[0].type == 'ID':
        factorDict['Factor'] = {'ID':{data[0].value}}
        return factorDict
    
def parseExprPrime(data):
    #print("Entered ExprPrime")
    exprPrimeDict = {'ExprP':{}}
    
    if data:
        #data.pop(0)
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

        elif data[0].value == '/':
            termPrimeDict['TermP']['/'] = {}
            data.pop(0)
            factor = parseFactor(data)

            if factor:
                termPrimeDict['TermP']['Factor'] = factor['Factor']

            termPrime = parseTermPrime(data)

            if termPrime:
                termPrimeDict['TermP']['TermP'] = termPrime['TermP']
            
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
    dict1 = {'Expr': {'Term': {'Factor': {'NUMBER': {4}}, 'TermP': {}}, 'ExprP': {}}}
    
        

if __name__ == '__main__':
    main()
