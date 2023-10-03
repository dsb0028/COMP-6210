from CustomError import *
from symboltable import *
"""
Program -> Declarations
Declarations => type id (args) compound-statement

args -> epsilon

compound-statement:
	{localDeclarations statements}

localDeclarations:
	type id assignment-expression; 
	type id;
	epsilon

assignment-expression:
	= Expr

statements:
	jump-statement

jump-statement:
	return Expr;


Expr -> Term Expr'

Expr' -> + Term Expr' | - Term Expr' | epsilon

Term -> Factor Term' 

Term' -> * Factor Term' | / Factor Term' | epsilon

Factor -> ( Expr )  | num  | ID


"""
symTable = SymbolTable()
consumed = []
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
    #Stores the tokens into a tokenBuffer
    #The token buffer stores tokens in the order that they are going to be consumed
    tokenBuffer = tokens
    #Stores the parse tree resulting from my recursive decent parser with no back tracking
    #expr = parseExpr(tokenBuffer)
    declarations = parseDeclarations(tokenBuffer)
    #checks to make sure that all tokens have been consumed, i.e token buffer should be empty
    # if all tokens have not been consumed yet, then we need to throw an error message
    if tokenBuffer:
        #Convert the values of all the consumed tokens into string format
        errorString = generateErrorString(tokenBuffer, isParseTreeGenerated=True)
        raise NotAllTokensHaveBeenConsumedError(errorString,"Invalid expression")
    return declarations

def createAST(parseTree):
    astTree = {}
    non_terminals = ['(', ')', '*', '+', '-', '*', '/']
    operators = ['*','/','+','-']
    nonTermKeys = parseTree.values()
    #print("Parse Tree",parseTree, "Keys",nonTermKeys)
    dictionaryItems = [item for item in getDictionaryItems(parseTree)]
    for item in dictionaryItems:
        if item[1] in operators:
            astTree = {item[1]:{}}
    
    print(astTree)
    #print(dictionaryItems)
    
# from https://stackoverflow.com/questions/39233973/get-all-keys-of-a-nested-dictionary
def getDictionaryItems(parseTree):
    for key, value in parseTree.items():
        if type(value) is dict:
            yield from getDictionaryItems(value)
        else:
            yield (key, value)
    
def parseDeclarations(tokenBuffer):
    """
    Description:
        Simulates the Declaractions productions from the grammar.
    Args:
        tokenBuffer: tokens that have yet to be consumed
    Returns:
        declarationsTree: a nested dict object that contains all children resulting from declarations productions 
    """
    #type ID (args) {localDeclarations statements}
    #Assuming that the only numeric data types in C are int, double, and float
    types = {'int', 'double', 'float'}
    #Next token to be consumed from the token buffer
    tokenToBeConsumed = tokenBuffer[0]
    #Initializes a dictionary object that will store the children of Declarations
    declarationsTree = {'Declarations':{}}
    #If the token to be consumed is either a int, double, or float, update the declarationsTree
    #to contain both the data type and value of the token under the key Declarations
    if tokenToBeConsumed.type in types:
        #SymbolTable.functionType = tokenToBeConsumed.type
        declarationsTree['Declarations'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed, tokenBuffer)
        tokenToBeConsumed = tokenBuffer[0]
        if tokenToBeConsumed.type == 'ID':
            #SymbolTable.functionName = tokenToBeConsumed.value
            #print(SymbolTable.functionName)
            symTable.addAFunction(tokenToBeConsumed.value,consumed[-1].value)
            declarationsTree['Declarations'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
            consume(tokenToBeConsumed,tokenBuffer)
            tokenToBeConsumed = tokenBuffer[0]
            if tokenToBeConsumed.type == 'LPAREN':
                declarationsTree['Declarations'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
                consume(tokenToBeConsumed,tokenBuffer)
                args = parseArgs(tokenBuffer)
                declarationsTree['Declarations'].update(args)
                tokenToBeConsumed = tokenBuffer[0]
                if tokenToBeConsumed.type == 'RPAREN':
                    declarationsTree['Declarations'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
                    consume(tokenToBeConsumed,tokenBuffer)
                    compoundStmt = parseCompoundStatement(tokenBuffer)
                    declarationsTree['Declarations'].update(compoundStmt)
    return declarationsTree

def parseCompoundStatement(tokenBuffer):
    """
    Description:
    Args:
    Returns:
    """
    compoundStmtTree = {'Compound Statement':{}}
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.type == 'LBRACE':
        compoundStmtTree['Compound Statement'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        localDecls = parseLocalDeclarations(tokenBuffer)
        compoundStmtTree['Compound Statement'].update(localDecls)
        statements = parseStatements(tokenBuffer)
        compoundStmtTree['Compound Statement'].update(statements)
        tokenToBeConsumed = tokenBuffer[0]
        if tokenToBeConsumed.type == 'RBRACE':
            compoundStmtTree['Compound Statement'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
            consume(tokenToBeConsumed, tokenBuffer)
    return compoundStmtTree

def parseArgs(tokenBuffer):
    """
    Description:
    Args:
    Returns:
    """
    argsTree = {'Arguments':{}}
    return argsTree

def parseLocalDeclarations(tokenBuffer):
    """
    Description:
    Args:
    Returns:
    """
    localDeclsTree = {'Local Declarations':{}}
    types = {'int', 'double', 'float'}
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.type in types:
        localDeclsTree['Local Declarations'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        #SymbolTable.varType = tokenToBeConsumed.type
        consume(tokenToBeConsumed,tokenBuffer)
        tokenToBeConsumed = tokenBuffer[0]
        if tokenToBeConsumed.type == 'ID':
            localDeclsTree['Local Declarations'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
            #SymbolTable.varName = tokenToBeConsumed.value 
            #NEED TO START HERE TOMMOROW
            symTable.addAVariable(tokenToBeConsumed.value,consumed[-1].value, symTable.lookUpFunction)
            consume(tokenToBeConsumed,tokenBuffer)
            tokenToBeConsumed = tokenBuffer[0]
            assignStatement = parseAssignStatement(tokenBuffer)
            if assignStatement['Assignment Statement'] != {}:
                localDeclsTree['Local Declarations'].update(assignStatement)
            else:
                tokenToBeConsumed = tokenBuffer[0]
                if tokenToBeConsumed.type == 'END':
                    localDeclsTree['Local Declarations'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
                    consume(tokenToBeConsumed,tokenBuffer)
    return localDeclsTree

def parseStatements(tokenBuffer):
    """
    Description:
    Args:
    Returns:
    """
    stmtsTree = {'Statements':{}}
    jumpStmt = parseJumpStatement(tokenBuffer)
    stmtsTree['Statements'].update(jumpStmt)
    return stmtsTree


def parseAssignStatement(tokenBuffer):
    """
    Description:
    Args:
    Returns:
    """
    assignmentStmtTree = {'Assignment Statement':{}}
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.value == '=':
        assignmentStmtTree['Assignment Statement'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        tokenToBeConsumed = tokenBuffer[0]
        expr = parseExpr(tokenBuffer)
        assignmentStmtTree['Assignment Statement'].update(expr)
        tokenToBeConsumed = tokenBuffer[0]
        if tokenToBeConsumed.type == 'END':
            assignmentStmtTree['Assignment Statement'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
            consume(tokenToBeConsumed,tokenBuffer)
    return assignmentStmtTree

def parseJumpStatement(tokenBuffer):
    """
    Description:
    Args:
    Returns:
    """
    jumpStmtTree = {'Jump Statement':{}}
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.type == 'return':
        jumpStmtTree['Jump Statement'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        expr = parseExpr(tokenBuffer)
        jumpStmtTree['Jump Statement'].update(expr)
        tokenToBeConsumed = tokenBuffer[0]
        if tokenToBeConsumed.type == 'END':
            jumpStmtTree['Jump Statement'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
            consume(tokenToBeConsumed,tokenBuffer)
    
    #WILL DELETE COMMENT BLOCK LATER
    #NEED TO IMPLEMENT ELSE IF LAST TOKEN IN SO CALLED STATEMENT IS NOT OF TYPE END        
    #if currToken is 'return':
    #   consume(currToken, tokenBuffer)
    #   parseExpr(tokenBuffer)
    #   if currToken is END:
    #       store jump statement in dictionary
    #   else:
    #       return error "expected semicolon at end of statement"
    return jumpStmtTree

def parseExpr(tokenBuffer):
    """
    Description:
        Simulates the Expr productions from the grammar
    Args:
        tokenBuffer: tokens that have yet to be consumed
    Returns:
        exprTree: A nested dictionary object that contains all children resulting from Expr productions
    """ 
    print("Entering Expr")
    #Initializes a dictionary object that will store the children of Expr
    exprTree = {'Expr':{}}
    #parse Term
    term = parseTerm(tokenBuffer)
    if term:
        exprTree['Expr'].update(term)
    print("exprTree['Expr']['Term'] =>", exprTree['Expr']['Term'], '\n')
    exprPrime = parseExprPrime(tokenBuffer) 
    if exprPrime:
        exprTree['Expr'].update(exprPrime)
    print("exprTree['Expr']['ExprP'] =>", exprTree['Expr']['ExprP'], '\n')
    print("Exiting Expr")
    return exprTree

def parseTerm(tokenBuffer):
    """
    Description:
        Simulates the Term productions from the grammar
    Args:
        tokenBuffer: tokens that have yet to be consumed
    Returns:
        termTree: A nested dictionary object that contains all children resulting from Term productions 
    """
    print("Entering Term")
    #Initializes a dictionary object called termDict that has a key called Term 
    # and an empty dictionary as the value to store children
    termTree = {'Term':{}}
    #Contains the tree for factor given the tokens that remain in the buffer
    factor = parseFactor(tokenBuffer)
    #The value of factor will only be stored as a child of Term in Term dictionary if factor exists
    if factor:
        termTree['Term'].update(factor)
    #Contains the tree for Term' given the tokens that remain in the buffer
    termPrime = parseTermPrime(tokenBuffer)
    #The resulting Term' tree will ony be stored as a child of Term if termPrime exists
    if termPrime:
        termTree['Term'].update(termPrime)
    print("Exiting Term")
    return termTree

def parseFactor(tokenBuffer):
    """
    Description:
        Simulates the Factor productions from the grammar
    Args:
        tokenBuffer: tokens that have yet to be consumed
    Returns:
        factorTree: A nested dictionary object that contains all children resulting from Factor productions
    """
    print("Entering Factor")
    #Initalizes a dictionary object that stores the children resulting from a matching factor production
    factorTree = {'Factor':{}}
    #Checks to make sure there are tokens left in the token buffer, if not there must be an error
    if tokenBuffer:
        #the next token to be consumed will be set to the token that is next in the tokens buffer 
        tokenToBeConsumed = tokenBuffer[0]
    else:
        errorString = generateErrorString(tokenBuffer)
        raise MissingFactorError(errorString,"Expected an Identifier or Number",
                                 {'line': consumed[len(consumed)-1].line, 'column': consumed[len(consumed)-1].column+1})
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
    #determines if the token to be consumed matches the type of one of the terminal nodes from Factor productions
    leafNode = match(tokenToBeConsumed, terminalNodes,isFactor=True)
    # if a match exists, check to see if the type is a LPAREN
    if leafNode:
        if leafNode.type == 'LPAREN':
            factorTree['Factor'].update({leafNode.type:leafNode.value})
            consume(tokenToBeConsumed,tokenBuffer)
            expr = parseExpr(tokenBuffer)
            if expr:
                factorTree['Factor'].update(expr)
            tokenToBeConsumed = tokenBuffer[0]
            leafNode = match(tokenToBeConsumed, terminalNodes,True)
            if leafNode.type == 'RPAREN':
                factorTree['Factor'].update({leafNode.type:leafNode.value})
                consume(tokenToBeConsumed,tokenBuffer)
        else:
            if leafNode.type == 'RPAREN':
                errorString = generateErrorString(tokenBuffer)
                raise MissingFactorError(errorString,"Expected an Identifier or Number",
                                 {'line': consumed[len(consumed)-1].line, 'column': consumed[len(consumed)-1].column+1})             
            factorTree['Factor'].update({leafNode.type:leafNode.value})
            consume(tokenToBeConsumed,tokenBuffer)
    else:
        errorString = generateErrorString(tokenBuffer)
        raise MissingFactorError(errorString,"Expected an Identifier or Number",
                                 {'line': consumed[len(consumed)-1].line, 'column': consumed[len(consumed)-1].column+1})
    print("Exiting Factor")
    return factorTree

def generateErrorString(tokenBuffer, isParseTreeGenerated = False):
    """
    Description:
    Args:
    Returns:
    """
    #Convert the values of all the consumed tokens into string format
    consumedString = ""
    consumedTokValues = [str(tok.value) for tok in consumed]
    if isParseTreeGenerated != True:
        consumedTokValues.append(' ˽ ')
    consumedString = consumedString.join(consumedTokValues)
    #Convert the values of all the tokens that remain in the token buffer into string format
    tokensBufferString = ""
    tokenBufferValues = [str(tok.value) for tok in tokenBuffer]
    tokensBufferString = tokensBufferString.join(tokenBufferValues)
    #Concatenates the string that contains the values of the consumed tokens with the string 
    # that contains the values of the tokens that remain in the token buffer 
    errorString = consumedString + tokensBufferString
    return errorString
    
def parseExprPrime(tokenBuffer):
    """
    Description:
        Simulates the Expr' productions from the grammar
    Args:
        tokenBuffer: the tokens that have yet to be consumed
    Returns:
        exprPrimeTree: A nested dictionary object that contains all children resulting from Expr' productions
    """
    print("Entering Expr'")
    #Initalizes a dictionary object that stores the children resulting from a matching Expr' production
    exprPrimeTree = {'ExprP':'ε'}
    #If tokens have yet to be consumed, match the value of the next token to be consumed to a '+' or '-' 
    if tokenBuffer:    
        tokenToBeConsumed = tokenBuffer[0]
        terminalNodes = {'+','-'}
        leafNode = match(tokenToBeConsumed, terminalNodes)
        if leafNode:
            exprPrimeTree = {'ExprP':{}} 
            exprPrimeTree['ExprP'].update({leafNode.type:leafNode.value})
            consume(tokenToBeConsumed,tokenBuffer)
            term = parseTerm(tokenBuffer)
            if term:
                exprPrimeTree['ExprP'].update(term)
            exprPrime = parseExprPrime(tokenBuffer)
            if exprPrime:
                exprPrimeTree['ExprP'].update(exprPrime)
    print("Exiting Expr'")        
    return exprPrimeTree

def parseTermPrime(tokenBuffer):
    """
    Description: 
        Simulates the Term' productions from the grammar
    Args:
        tokenBuffer: tokens that have yet to be consumed
    Return:
        termPrimeTree: A nested dictionary object that contains all children resulting from Term' productions
    """
    print("Entering Term'")
    termPrimeTree = {'TermP':'ε'}
    if tokenBuffer:
        tokenToBeConsumed = tokenBuffer[0]
        terminalNodes = {'*','/'}
        leafNode = match(tokenToBeConsumed, terminalNodes)
        if leafNode:
            termPrimeTree = {'TermP':{}}
            termPrimeTree['TermP'].update({leafNode.type:leafNode.value})
            consume(tokenToBeConsumed,tokenBuffer)
            factor = parseFactor(tokenBuffer)
            if factor:
                termPrimeTree['TermP'].update(factor)
            termPrime = parseTermPrime(tokenBuffer)
            if termPrime:
                termPrimeTree['TermP'].update(termPrime)
    print("Exiting Term'")
    return termPrimeTree

def match(currToken, terminalNodes, isFactor = False):
    """
    Description:
        If token to be consumed matches a terminal node that is part of a production, return the matching token 
    Args:
        currToken: is the next token to be consumed
        terminalNodes: represents all leaf nodes defined under a specific set of productions
        isFactor: a boolean that determines whether we are in a Factor production or not 
    Returns:
        matchToken: a token object that contains the matching token
    """
    
    matchToken = None
    if isFactor == True:
        if currToken.type in terminalNodes:
            matchToken = currToken
    else:
        if currToken.value in terminalNodes:
            matchToken = currToken
    return matchToken

def consume(currToken,tokenBuffer):
    """
    Description:
        Places the token to be consumed in consumed before removing it from the token buffer 
    Args:
        currToken: the token being consumed
        tokenBuffer: the tokens that have yet to be consumed
    Returns:
        None
    """
    consumed.append(currToken)
    tokenBuffer.pop(0)

def main():
    #tokens = [(), (), (), ()]    
    dict1 = {'Expr': {'Term': {'Factor': {'NUMBER': {4}}, 'TermP': {}}, 'ExprP': {}}}
    
if __name__ == '__main__':
    main()
