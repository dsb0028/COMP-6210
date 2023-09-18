import re 
import CustomError
import copy
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
visitors = []

def createParseTree(data):
    global dCopy
    dCopy = copy.deepcopy(data)
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
    exprPrime = parseExprPrime(data) 
    if exprPrime:
        exprDict['Expr']['ExprP'] = exprPrime['ExprP']
    else:
        exprDict['Expr']['ExprP'] = {}
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
        string = ""
        string = string.join([str(tok.value) for tok in dCopy])
       
        if string.rfind(')') == -1:
            raise CustomError.MissingRParenError(string, "Expected ')' at", 
                                                {'line': dCopy[len(dCopy)-1].line, 'column': dCopy[len(dCopy)-1].column + 1})
        
        if data[1].type == 'RPAREN':
            exprVals = [tok.value for tok in data]
            strExpr = ''
            strExpr = strExpr.join(exprVals)
            print(exprVals)
            raise CustomError.MissingExprError(strExpr,"Missing expresssion at", 
                                               {'line': data[0].line, 'column':data[0].column + 1})
        factorDict['Factor']['LPAREN'] = '('
        visitors.append(data[0])
        data.pop(0)
        expr = parseExpr(data)
        if expr:
            factorDict['Factor']['Expr'] = expr['Expr']
            #print("cool")
        """
        if len(data) == 0:
            exprVals = [str(tok.value) for tok in visitors]
            strExpr = ''
            strExpr = strExpr.join(exprVals)
            raise CustomError.MissingRParenError(strExpr, "Expected ')' at", 
                                               {'line': visitors[1].line, 'column': visitors[1].column + 1})
        """
        factorDict['Factor']['RPAREN'] = ')'
        return factorDict
    if data[0].type == 'NUMBER':
        factorDict['Factor'] = {'NUMBER':{data[0].value}}
        return factorDict
    elif data[0].type == 'ID':
        factorDict['Factor'] = {'ID':{data[0].value}}
        return factorDict
    
def parseExprPrime(data):
    exprPrimeDict = {'ExprP':{}}    
    if data:
        if (len(data) == 1 and data[0].type == 'MATH_OP') or data[1].type == 'RPAREN':
                    visitors.append(data[0])
                    exprVals = [str(tok.value) for tok in visitors]
                    strExpr = ''
                    strExpr = strExpr.join(exprVals)
                    raise CustomError.MissingFactorError(strExpr, "Expected a Factor at", 
                                                    {'line': visitors[1].line, 'column': visitors[1].column + 1})
        
        if data[0].value == '+':
            exprPrimeDict['ExprP']['+'] = {} 
            visitors.append(data[0])
            data.pop(0)
            term = parseTerm(data)
            if term:
                exprPrimeDict['ExprP']['Term'] = term['Term']
            exprPrime = parseExprPrime(data)
            if exprPrime:
                exprPrimeDict['ExprP']['ExprP'] = exprPrime['ExprP']
        elif data[0].value == '-':
            exprPrimeDict['ExprP']['-'] = {}
            visitors.append(data[0])
            data.pop(0)
            term = parseTerm(data)
            if term:
                exprPrimeDict['ExprP']['Term'] = term['Term']
            exprPrime = parseExprPrime(data)
            if exprPrime:
                exprPrimeDict['ExprP']['ExprP'] = exprPrime['ExprP']   
    return exprPrimeDict

def parseTermPrime(data):
    termPrimeDict = {'TermP':{}}
    visitors.append(data[0])
    data.pop(0)
    if data:
        if (len(data) == 1 and data[0].type == 'MATH_OP') or data[1].type == 'RPAREN':
                    visitors.append(data[0])
                    exprVals = [str(tok.value) for tok in visitors]
                    strExpr = ''
                    strExpr = strExpr.join(exprVals)
                    raise CustomError.MissingFactorError(strExpr, "Expected a Factor at", 
                                                    {'line': visitors[1].line, 'column': visitors[1].column + 1})
        if data[0].value == '*':
            termPrimeDict['TermP']['*'] = {} 
            visitors.append(data[0])
            #print("data", data)
            data.pop(0)
            #print("data", data)
            factor = parseFactor(data)
            if factor:
                termPrimeDict['TermP']['Factor'] = factor['Factor']
            termPrime = parseTermPrime(data)
            if termPrime:
                termPrimeDict['TermP']['TermP'] = termPrime['TermP']
        elif data[0].value == '/':
            termPrimeDict['TermP']['/'] = {}
            visitors.append(data[0])
            """
            if len(data) == 1:
                raise CustomError.MissingFactorError 
            """
            #print("Data", data)
            data.pop(0)
            factor = parseFactor(data)
            #print(data, visitors)
            if factor:
                termPrimeDict['TermP']['Factor'] = factor['Factor']
            termPrime = parseTermPrime(data)
            if termPrime:
                termPrimeDict['TermP']['TermP'] = termPrime['TermP']
    return termPrimeDict


def main():
    #tokens = [(), (), (), ()]    
    dict1 = {'Expr': {'Term': {'Factor': {'NUMBER': {4}}, 'TermP': {}}, 'ExprP': {}}}
    
        

if __name__ == '__main__':
    main()
