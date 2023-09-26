import re 
from CustomError import *
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

visited = []
internalNodeKeys = {'Expr', 'Term', 'TermP', 'Factor','ExprP'}
def createParseTree(tokens):
    """
    Description: 
    Creates a parse tree using a recursive descent parser with no back tracking
    Args:
        tokens: a list of tokens generated from the tokenizer
    
    Returns:
        expr: nested dictionary object that contains the resulting parse tree
    """
    # deepcopy is necessary to make sure that the original tokens list will be perserved in case of error
    # all recursive functions need to have access to the original token list
    global originalTokensList
    originalTokensList = copy.deepcopy(tokens)
    #returns the parse tree resulting from my recursive decent parser with no back tracking
    expr = parseExpr(tokens)
    #checks to make sure that all tokens have been parsed
    # if all tokens have not been parsed yet, then we need to throw an error message
    if tokens:
        tokenString = ""
        # The value of each token in the original tokens list is converted into a string 
        # before being appended to a list using list comprehension. The resulting list of token value strings
        # is joined with the value of tokenString, which is originally empty
        # tokenString will be a string containing the values of each token in the original token list
        tokenString = tokenString.join([str(tok.value) for tok in originalTokensList])
        raise NotAllTokensHaveBeenConsumedError(tokenString,"Invalid expression")
    return expr

def parseExpr(tokens):
    """
    Description:
        Simulates the expr rules from the grammar
    Args:
        tokens: tokens that have yet to be parsed from the original token list
    Returns:
        exprDict: A nested dictionary object that contains all children resulting from Term and Expr' rules
    """ 
    print("Entering Expr")
    #Initializes a dictionary object that will store the children of expr rule
    exprDict = {'Expr':{}}
    #parse Term
    term = parseTerm(tokens)
    if term:
        exprDict['Expr'].update(term)
    print("exprDict['Expr']['Term'] =>", exprDict['Expr']['Term'], '\n')
    exprPrime = parseExprPrime(tokens) 
    if exprPrime:
        exprDict['Expr'].update(exprPrime)
    print("exprDict['Expr']['ExprP'] =>", exprDict['Expr']['ExprP'], '\n')
    print("Exiting Expr")
    return exprDict

def parseTerm(tokens):
    """
    Description:
    Args:
    Returns:
    """
    print("Entering Term")
    #Initializes a dictionary object called termDict that has a key called Term 
    # and an empty dictionary as the value to store children
    termDict = {'Term':{}}
    #Contains the tree for factor given the tokens that have yet to be parsed
    factor = parseFactor(tokens)
    #The value of factor will only be stored as a child of Term in Term dictionary if factor exists
    if factor:
        #lookup key associated with Factor symbol
        termDict['Term'].update(factor)
    print("termDict['Term']['Factor'] =>", termDict['Term']['Factor'], '\n')
    #Contains the tree resulting from Term Prime productions given tokens that have yet to be parsed
    termPrime = parseTermPrime(tokens)
    #The resulting Term' tree will ony be stored as a child of Term if termPrime exists
    if termPrime:
        termDict['Term'].update(termPrime)
    print("termDict['Term']['TermP'] =>", termDict['Term']['TermP'], '\n')
    print("Exiting Term")
    return termDict

def parseFactor(tokens):
    """
    Description:
    Args:
    Returns:
    """
    print("Entering Factor")
    #Initalizes a dictionary object that stores the children resulting from a matching factor production
    factorSubTree = {'Factor':{}}
    #Checks to make sure there are tokens left in the token buffer, if not there must be an error
    if tokens:
        #the next token to be consumed will be set to the token that is next in the tokens buffer 
        tokenToBeConsumed = tokens[0]
    else:
        visitedString = ""
        visitedTokValues = [str(tok.value) for tok in visited]
        visitedTokValues.append(' ˽ ')
        visitedString = visitedString.join(visitedTokValues)
        tokensBufferString = ""
        tokenBufferValues = [str(tok.value) for tok in tokens]
        tokensBufferString = tokensBufferString.join(tokenBufferValues)
        expression = visitedString + tokensBufferString
        raise MissingFactorError(expression,"Expected an Identifier or Number",
                                 {'line': visited[len(visited)-1].line, 'column': visited[len(visited)-1].column+1})
    #terminalNodes contains the token types versus the token values
    """
    TYPES ARE USED INSTEAD OF VALUES BECAUSE A NUMBER, AND ID CAN HAVE ANY VALUE
    IN OTHER WORDS, THE TOKEN VALUES FOR NUMBER AND ID CANNOT BE HARDCODED
    FOR EXPRPRIME AND TERMPRIME, IT IS NECESSARY TO SPECIFY TOKEN VALUES INSTEAD OF TOKEN TYPES FOR 
    THE TERMINAL NODES BECAUSE '+', '-', '*', AND '/' ALL ARE OF TYPE MATH_OP. THIS BECOMES PROBLAMATIC 
    IF THE NEXT TOKEN TO BE CONSUMED IN EXPRPRIME HAS A VALUE OF '*' OR '/' AND WE ARE GOING OFF OF ITS TYPE, 
    THERE WILL BE A MATCH WHEN THERE SHOULDN'T BE ONE. THE ONLY TERMINAL NODES IN EXPRPRIME ARE '+' AND '-'.  
    """
    terminalNodes = {'LPAREN','RPAREN','NUMBER','ID'}
    leafNode = match(tokenToBeConsumed, terminalNodes,True)
    if leafNode:
        if leafNode.type == 'LPAREN':
            factorSubTree['Factor'].update({leafNode.type:leafNode.value})
            consume(tokenToBeConsumed,tokens)
            expr = parseExpr(tokens)
            if expr:
                factorSubTree['Factor'].update(expr)
            tokenToBeConsumed = tokens[0]
            leafNode = match(tokenToBeConsumed, terminalNodes,True)
            if leafNode.type == 'RPAREN':
                factorSubTree['Factor'].update({leafNode.type:leafNode.value})
                consume(tokenToBeConsumed,tokens)
        else:
            if leafNode.type == 'RPAREN':
                visitedString = ""
                visitedTokValues = [str(tok.value) for tok in visited]
                visitedTokValues.append(' ˽ ')
                visitedString = visitedString.join(visitedTokValues)
                tokensBufferString = ""
                tokenBufferValues = [str(tok.value) for tok in tokens]
                tokensBufferString = tokensBufferString.join(tokenBufferValues)
                expression = visitedString + tokensBufferString
                raise MissingFactorError(expression,"Expected an Identifier or Number",
                                 {'line': visited[len(visited)-1].line, 'column': visited[len(visited)-1].column+1})             
            factorSubTree['Factor'].update({leafNode.type:leafNode.value})
            consume(tokenToBeConsumed,tokens)
    else:
        visitedString = ""
        visitedTokValues = [str(tok.value) for tok in visited]
        visitedTokValues.append(' ˽ ')
        visitedString = visitedString.join(visitedTokValues)
        tokensBufferString = ""
        tokenBufferValues = [str(tok.value) for tok in tokens]
        tokensBufferString = tokensBufferString.join(tokenBufferValues)
        expression = visitedString + tokensBufferString
        raise MissingFactorError(expression,"Expected an Identifier or Number",
                                 {'line': visited[len(visited)-1].line, 'column': visited[len(visited)-1].column+1})
    print("Exiting Factor")
    return factorSubTree
    
def parseExprPrime(tokens):
    """
    Description:
    Args:
    Returns:
    """
    print("Entering Expr'")
    #Initalizes a dictionary object that stores the children resulting from a matching Expr' production
    exprPrimeDict = {'ExprP':'ε'}
    #If tokens have yet to be consumed, match the value of the next token to be consumed to a '+' or '-' 
    if tokens:    
        tokenToBeConsumed = tokens[0]
        terminalNodes = {'+','-'}
        leafNode = match(tokenToBeConsumed, terminalNodes)
        if leafNode:
            exprPrimeDict = {'ExprP':{}} 
            exprPrimeDict['ExprP'].update({leafNode.type:leafNode.value})
            consume(tokenToBeConsumed,tokens)
            term = parseTerm(tokens)
            if term:
                exprPrimeDict['ExprP'].update(term)
            exprPrime = parseExprPrime(tokens)
            if exprPrime:
                exprPrimeDict['ExprP'].update(exprPrime)
    print("Exiting Expr'")        
    return exprPrimeDict

def parseTermPrime(tokens):
    """
    Description: 
    Args:
    Return:
    """
    print("Entering Term'")
    termPrimeDict = {'TermP':'ε'}
    if tokens:
        tokenToBeConsumed = tokens[0]
        terminalNodes = {'*','/'}
        leafNode = match(tokenToBeConsumed, terminalNodes)
        if leafNode:
            termPrimeDict = {'TermP':{}}
            termPrimeDict['TermP'].update({leafNode.type:leafNode.value})
            consume(tokenToBeConsumed,tokens)
            factor = parseFactor(tokens)
            if factor:
                termPrimeDict['TermP'].update(factor)
            termPrime = parseTermPrime(tokens)
            if termPrime:
                termPrimeDict['TermP'].update(termPrime)
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

def match(currToken, terminalNodes, isFactor = False):
    """
    Description:
        If token to be consumed matches a terminal node that is part of rule, return true
        Else: return False
    Args:
        currToken: is the next token to be consumed
        terminalNodes: represents all leaf nodes defined under a specific set of rules 
    Returns:
        isAMatch: boolean that represents whether a match exists or not
    """
    isAMatch = False
    matchToken = None
    if isFactor == True:
        if currToken.type in terminalNodes:
            isAMatch = True
            matchToken = currToken
    else:
        if currToken.value in terminalNodes:
            isAMatch = True
            matchToken = currToken
    return matchToken

def consume(currToken,tokens):
    """
    Description:
        Consumes the current token 
    Args:
        currToken: the token being consumed
    Returns:
        None
    """
    visited.append(currToken)
    tokens.pop(0)

def main():
    #tokens = [(), (), (), ()]    
    dict1 = {'Expr': {'Term': {'Factor': {'NUMBER': {4}}, 'TermP': {}}, 'ExprP': {}}}
    
if __name__ == '__main__':
    main()
