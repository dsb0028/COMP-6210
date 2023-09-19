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
    if len(visitors) < len(dCopy):
        string = ""
        string = string.join([str(tok.value) for tok in dCopy])
        raise CustomError.NotAllTokensHaveBeenConsumedError(string,"Invalid expression")
    #if expr:
    #treeD = expr 
        #root.addChild(expr)
    return expr

def parseExpr(data):  
    print("Entering Expr")
    exprDict = {'Expr':{}}
    term = parseTerm(data)
    if term:
        exprDict['Expr']['Term'] = term['Term']
    print("exprDict['Expr']['Term'] =>", exprDict['Expr']['Term'], '\n')
    exprPrime = parseExprPrime(data) 
    if exprPrime:
        exprDict['Expr']['ExprP'] = exprPrime['ExprP']
    else:
        exprDict['Expr']['ExprP'] = {}
    print("exprDict['Expr']['ExprP'] =>", exprDict['Expr']['ExprP'], '\n')
    print("Exiting Expr")
    return exprDict

def parseTerm(data):
    print("Entering Term")
    termDict = {'Term':{}}
    factor = parseFactor(data)
    #print("Factor", factor)
    if factor:
        termDict['Term']['Factor'] = factor['Factor']    
    else:
        visitors.append(data[0])
        exprVals = [str(tok.value) for tok in visitors]
        strExpr = ''
        strExpr = strExpr.join(exprVals)
        raise CustomError.MissingFactorError(strExpr, "Expected a Factor at", 
                                                    {'line': visitors[1].line, 'column': visitors[1].column + 1})
    print("termDict['Term']['Factor'] =>", termDict['Term']['Factor'], '\n')
    termPrime = parseTermPrime(data)
    if termPrime:
        termDict['Term']['TermP'] = termPrime['TermP']
    print("termDict['Term']['TermP'] =>", termDict['Term']['TermP'], '\n')
    print("Exiting Term")
    return termDict

def parseFactor(data):
    print("Entering Factor")
    factorDict = {'Factor':{}}
    if data[0].type == 'LPAREN':
        string = ""
        string = string.join([str(tok.value) for tok in dCopy])
       
        if string.rfind(')') == -1:
            raise CustomError.MissingRParenError(string, "Expected ')' at", 
                                                {'line': dCopy[len(dCopy)-1].line, 'column': dCopy[len(dCopy)-1].column + 1})
        else:
            if len(dCopy) == 2:
                raise CustomError.MissingExprError(string, "Missing expresssion at", 
                                               {'line': dCopy[len(dCopy)-1].line, 'column': dCopy[len(dCopy)-1].column + 1})
        """
        if data[1].type == 'RPAREN':
            exprVals = [tok.value for tok in data]
            strExpr = ''
            strExpr = strExpr.join(exprVals)
            print(exprVals)
            raise CustomError.MissingExprError(strExpr,"Missing expresssion at", 
                                               {'line': data[0].line, 'column':data[0].column + 1})
        """
        factorDict['Factor']['LPAREN'] = '('
        visitors.append(data[0])
        data.pop(0)
        expr = parseExpr(data)
        if expr:
            factorDict['Factor']['Expr'] = expr['Expr']
        print("factorDict['Factor']['Expr'] =>", factorDict['Factor']['Expr'], '\n')   
        """
        if len(data) == 0:
            exprVals = [str(tok.value) for tok in visitors]
            strExpr = ''
            strExpr = strExpr.join(exprVals)
            raise CustomError.MissingRParenError(strExpr, "Expected ')' at", 
                                               {'line': visitors[1].line, 'column': visitors[1].column + 1})
        """
        factorDict['Factor']['RPAREN'] = ')'
        #return factorDict
    elif data[0].type == 'NUMBER':
        factorDict['Factor'] = {'NUMBER':{data[0].value}}
        #return factorDict
    elif data[0].type == 'ID':
        factorDict['Factor'] = {'ID':{data[0].value}}
    print("factorDict['Factor'] =>", factorDict['Factor'], '\n')
        #return factorDict
    if factorDict['Factor'] == {}:
        visitors.append(data[0])
        exprVals = [str(tok.value) for tok in visitors]
        strExpr = ''
        strExpr = strExpr.join(exprVals)
        raise CustomError.MissingFactorError(strExpr, "Expected a Factor at", 
                                                {'line': visitors[1].line, 'column': visitors[1].column + 1})
    print("Exiting Factor")
    return factorDict
    
def parseExprPrime(data):
    print("Entering Expr'")
    exprPrimeDict = {'ExprP':{}}    
    if data:
        if (len(data) == 1 and data[0].type == 'MATH_OP'):
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
            print("Expr'[Expr']['Term'] =>", exprPrimeDict['ExprP']['Term'], '\n')
            exprPrime = parseExprPrime(data)
            if exprPrime:
                exprPrimeDict['ExprP']['ExprP'] = exprPrime['ExprP']
            print("Expr'[Expr'][Expr'] =>", exprPrimeDict['ExprP']['ExprP'], '\n')    
        elif data[0].value == '-':
            exprPrimeDict['ExprP']['-'] = {}
            visitors.append(data[0])
            data.pop(0)
            term = parseTerm(data)
            if term:
                exprPrimeDict['ExprP']['Term'] = term['Term']
            print("Expr'['ExprP']['Term'] =>", exprPrimeDict['ExprP']['Term'], '\n') 
            exprPrime = parseExprPrime(data)
            if exprPrime:
                exprPrimeDict['ExprP']['ExprP'] = exprPrime['ExprP']
            print("Expr'['ExprP']['ExprP'] =>", exprPrimeDict['ExprP']['ExprP'], '\n')
    print("Exiting Expr'")        
    return exprPrimeDict

def parseTermPrime(data):
    print("Entering Term'")
    termPrimeDict = {'TermP':{}}
    visitors.append(data[0])
    data.pop(0)
    if data:
        if (len(data) == 1 and data[0].type == 'MATH_OP'):
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
            else:
                visitors.append(data[0])
                exprVals = [str(tok.value) for tok in visitors]
                strExpr = ''
                strExpr = strExpr.join(exprVals)
                raise CustomError.MissingFactorError(strExpr, "Expected a Factor at", 
                                                {'line': visitors[1].line, 'column': visitors[1].column + 1})
            print("termPrimeDict['TermP']['Factor'] =>", termPrimeDict['TermP']['Factor'], '\n')
            termPrime = parseTermPrime(data)
            if termPrime:
                termPrimeDict['TermP']['TermP'] = termPrime['TermP']
            print("termPrimeDict['TermP']['TermP'] =>", termPrimeDict['TermP']['TermP'], '\n') 
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
            else:
                visitors.append(data[0])
                exprVals = [str(tok.value) for tok in visitors]
                strExpr = ''
                strExpr = strExpr.join(exprVals)
                raise CustomError.MissingFactorError(strExpr, "Expected a Factor at", 
                                                {'line': visitors[1].line, 'column': visitors[1].column + 1})
            print("termPrimeDict['TermP']['Factor'] =>", termPrimeDict['TermP']['Factor'],'\n')
            termPrime = parseTermPrime(data)
            if termPrime:
                termPrimeDict['TermP']['TermP'] = termPrime['TermP']
            print("termPrimeDict['TermP']['TermP'] =>", termPrimeDict['TermP']['TermP'], '\n')
    print("Exiting Term'")
    return termPrimeDict


def main():
    #tokens = [(), (), (), ()]    
    dict1 = {'Expr': {'Term': {'Factor': {'NUMBER': {4}}, 'TermP': {}}, 'ExprP': {}}}
    
        

if __name__ == '__main__':
    main()
