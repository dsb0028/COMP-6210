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
visited = []
def createParseTree(tokens):
    global tokensCopy
    tokensCopy = copy.deepcopy(tokens)
    expr = parseExpr(tokens)
    if len(visited) < len(tokensCopy):
        string = ""
        string = string.join([str(tok.value) for tok in tokensCopy])
        raise CustomError.NotAllTokensHaveBeenConsumedError(string,"Invalid expression")
    return expr

def parseExpr(tokens):  
    print("Entering Expr")
    exprDict = {'Expr':{}}
    term = parseTerm(tokens)
    if term:
        exprDict['Expr']['Term'] = term['Term']
    print("exprDict['Expr']['Term'] =>", exprDict['Expr']['Term'], '\n')
    exprPrime = parseExprPrime(tokens) 
    if exprPrime:
        exprDict['Expr']['ExprP'] = exprPrime['ExprP']
    print("exprDict['Expr']['ExprP'] =>", exprDict['Expr']['ExprP'], '\n')
    print("Exiting Expr")
    return exprDict

def parseTerm(tokens):
    print("Entering Term")
    termDict = {'Term':{}}
    factor = parseFactor(tokens)
    if factor:
        termDict['Term']['Factor'] = factor['Factor']    
    print("termDict['Term']['Factor'] =>", termDict['Term']['Factor'], '\n')
    termPrime = parseTermPrime(tokens)
    if termPrime:
        termDict['Term']['TermP'] = termPrime['TermP']
    print("termDict['Term']['TermP'] =>", termDict['Term']['TermP'], '\n')
    print("Exiting Term")
    return termDict

def parseFactor(tokens):
    print("Entering Factor")
    factorDict = {'Factor':{}}
    if not tokens:
        inputVals = [str(tok.value) for tok in tokensCopy]
        index = 0
        if not visited:
            visited.append(tokens[0])
            tokens.pop(0)
        reversedList = []
        isListReversed = False
        if len(visited) == len(tokensCopy):
           reversedList = copy.deepcopy(inputVals)
           reversedList.reverse()
           isListReversed = True
        else:
            reversedList = inputVals        
        lastVisitor = visited[len(visited)-1].value
        strExpr = ''
        strExpr = strExpr.join(reversedList)
        index = strExpr.find(lastVisitor)
        reversedList.insert(index,' ˽ ')
        if isListReversed == True:
            reversedList.reverse()
        rString = ''
        rString = rString.join(reversedList)
        #rString = insertPlaceHolder(exprVals, index)
        raise CustomError.MissingFactorError(rString, "Expected a Factor at", 
                                                {'line': visited[len(visited)-1].line, 'column': visited[len(visited)-1].column+1}) 
    if tokens[0].type == 'LPAREN':
        string = ""        
        string = string.join([str(tok.value) for tok in tokensCopy])
        index = 0
        rString = insertPlaceHolder(string, index)
        if string.rfind(')') == -1:
            raise CustomError.MissingRParenError(rString, "Expected ')' at", 
                                                {'line': tokensCopy[len(tokensCopy)-1].line, 'column': tokensCopy[len(tokensCopy)-1].column + 1})

        factorDict['Factor']['LPAREN'] = tokens[0].value
        visited.append(tokens[0])
        tokens.pop(0)
        expr = parseExpr(tokens)
        if expr:
            factorDict['Factor']['Expr'] = expr['Expr']
        print("factorDict['Factor']['Expr'] =>", factorDict['Factor']['Expr'], '\n')   
        if tokens:
            #not enough to check if there are still tokens that need to be parsed 
            if tokens[0].type == 'RPAREN':
                factorDict['Factor']['RPAREN'] = ')'
            #tokens.pop(0)
            #pop first index of tokens here so the first index of tokens contains the next token
            if len(tokens) > 1:
                if tokens[1].type == 'LPAREN':
                    string = ""
                    string = string.join([str(tok.value) for tok in tokensCopy])
                    raise SyntaxError("Expected an operator after )")
                #expecting an operator
                # raise an error called MissingLParenError(visitors,error message,loc of error)    
        else:
            string = ""
            string = string.join([str(tok.value) for tok in tokensCopy])
            raise CustomError.MissingRParenError(string, "Expected ')' at", 
                                                {'line': tokensCopy[len(tokensCopy)-1].line, 'column': tokensCopy[len(tokensCopy)-1].column + 1})
        
    elif tokens[0].type == 'NUMBER':
        factorDict['Factor'] = {'NUMBER':{tokens[0].value}}
    elif tokens[0].type == 'ID':
        factorDict['Factor'] = {'ID':{tokens[0].value}}
    print("factorDict['Factor'] =>", factorDict['Factor'], '\n')
    if factorDict['Factor'] == {}:
        inputVals = [str(tok.value) for tok in tokensCopy]
        isThereVisitor = True
        if not visited:
            isThereVisitor = False #no tokens have been parsed thus far
            visited.append(tokens[0]) #need to append token where the error occurred
            tokens.pop(0)
        isListReversed = False # mechanism to work around limitation of str.insert method
        if isThereVisitor == True:
           inputVals.reverse()
           isListReversed = True        
        lastVisitor = visited[len(visited)-1].value
        index = [i for i,tok in enumerate(inputVals) if tok == lastVisitor]
        inputVals.insert(index[0],' ˽ ')
        if isListReversed == True:
            inputVals.reverse()
        rString = ''
        rString = rString.join(inputVals)
        raise CustomError.MissingFactorError(rString, "Expected a Factor at", 
                                                {'line': visited[len(visited)-1].line, 'column': visited[len(visited)-1].column})
    visited.append(tokens[0])
    tokens.pop(0)
    print("Exiting Factor")
    return factorDict
    
def parseExprPrime(tokens):
    print("Entering Expr'")
    exprPrimeDict = {'ExprP':{}}    
    if tokens:
        if tokens[0].value == '+':
            exprPrimeDict['ExprP']['+'] = {} 
            visited.append(tokens[0])
            tokens.pop(0)
            term = parseTerm(tokens)
            if term:
                exprPrimeDict['ExprP']['Term'] = term['Term']
            print("Expr'[Expr']['Term'] =>", exprPrimeDict['ExprP']['Term'], '\n')
            exprPrime = parseExprPrime(tokens)
            if exprPrime:
                exprPrimeDict['ExprP']['ExprP'] = exprPrime['ExprP']
            print("Expr'[Expr'][Expr'] =>", exprPrimeDict['ExprP']['ExprP'], '\n')    
        elif tokens[0].value == '-':
            exprPrimeDict['ExprP']['-'] = {}
            visited.append(tokens[0])
            tokens.pop(0)
            term = parseTerm(tokens)
            if term:
                exprPrimeDict['ExprP']['Term'] = term['Term']
            print("Expr'['ExprP']['Term'] =>", exprPrimeDict['ExprP']['Term'], '\n') 
            exprPrime = parseExprPrime(tokens)
            if exprPrime:
                exprPrimeDict['ExprP']['ExprP'] = exprPrime['ExprP']
            print("Expr'['ExprP']['ExprP'] =>", exprPrimeDict['ExprP']['ExprP'], '\n')
    print("Exiting Expr'")        
    return exprPrimeDict

def parseTermPrime(tokens):
    print("Entering Term'")
    termPrimeDict = {'TermP':{}}
    if tokens:
        if tokens[0].value == '*':
            termPrimeDict['TermP']['*'] = {} 
            visited.append(tokens[0])
            tokens.pop(0)
            factor = parseFactor(tokens)
            if factor:
                termPrimeDict['TermP']['Factor'] = factor['Factor']
            print("termPrimeDict['TermP']['Factor'] =>", termPrimeDict['TermP']['Factor'], '\n')
            termPrime = parseTermPrime(tokens)
            if termPrime:
                termPrimeDict['TermP']['TermP'] = termPrime['TermP']
            print("termPrimeDict['TermP']['TermP'] =>", termPrimeDict['TermP']['TermP'], '\n') 
        elif tokens[0].value == '/':
            termPrimeDict['TermP']['/'] = {}
            visited.append(tokens[0])
            tokens.pop(0)
            factor = parseFactor(tokens)
            if factor:
                termPrimeDict['TermP']['Factor'] = factor['Factor']
            else:
                visited.append(tokens[0])
                exprVals = [str(tok.value) for tok in visited]
                strExpr = ''
                strExpr = strExpr.join(exprVals)
                raise CustomError.MissingFactorError(strExpr, "Expected a Factor at", 
                                                {'line': visited[len(visited)-1].line, 'column': visited[len(visited)-1].column + 2})
            print("termPrimeDict['TermP']['Factor'] =>", termPrimeDict['TermP']['Factor'],'\n')
            termPrime = parseTermPrime(tokens)
            if termPrime:
                termPrimeDict['TermP']['TermP'] = termPrime['TermP']
            print("termPrimeDict['TermP']['TermP'] =>", termPrimeDict['TermP']['TermP'], '\n')
    print("Exiting Term'")
    return termPrimeDict

def insertPlaceHolder(exprVals, index):
    
    strExpr = ''
    strExpr = strExpr.join(exprVals)
    lastChar = strExpr[len(strExpr)-1]
    rString = strExpr[:len(strExpr)-1]
    rString = rString + lastChar + ' ˽ '  #tried to put a placeholder where the error is
    
    """
    isThereVisitor = True
    if not visitors:
        isThereVisitor = False #no tokens have been parsed thus far
        visitors.append(tokens[0]) #need to append token where the error occurred
        tokens.pop(0)
    
    isListReversed = False # mechanism to work around limitation of str.insert method
    if isThereVisitor == True:
        inputVals.reverse()
        isListReversed = True        
    lastVisitor = visitors[len(visitors)-1].value
    index = [i for i,tok in enumerate(inputVals) if tok == lastVisitor]
    inputVals.insert(index[0],' ˽ ')
    if isListReversed == True:
        inputVals.reverse()
    """
    return rString    

def main():
    #tokens = [(), (), (), ()]    
    dict1 = {'Expr': {'Term': {'Factor': {'NUMBER': {4}}, 'TermP': {}}, 'ExprP': {}}}
    
if __name__ == '__main__':
    main()
