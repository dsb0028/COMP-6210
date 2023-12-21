from CustomError import *
from symboltable import *
from collections import defaultdict
import copy

"""
Program:
    translation-unit

translation-unit:
    external-declaration translation-unit

external-declaration:
    declaration
    function-definition

function-definition:
    type-specifier ID (parameter-list) compound-statement

parameter-list:
    parameter-declaration parameter-list'

parameter-list':
    , parameter-declaration parameter-list'
    epsilon

parameter-declaration:
    type-specifier ID

compound-statement:
    { block-item-list }

block-item-list:
    block-item block-item-list
    epsilon

block-item:
    declaration
    statement

declaration:
    type-specifier init-declarator;

init-declarator:
    ID
    ID = expr
   
statement:
    assignment-statement
    return-statement

assignment-statement:
    ID = expr;

Expr -> Term Expr'

Expr' -> + Term Expr' | - Term Expr' | epsilon

Term -> Factor Term' 

Term' -> * Factor Term' | / Factor Term' | epsilon

Factor -> ( Expr )  | num  | ID

return-statement:
    return expropt;
"""

symTable = SymbolTable()
#astTree = {}
consumed = []
tokenBuffer = []
def createParseTree(tokens):
    """
    Description: 
    Creates a parse tree using a recursive descent parser with no back tracking
    Args:
        tokens: a list of tokens generated from the tokenizer
    Returns:
        translationUnit: nested dictionary object that contains the resulting parse tree
    """
    #Stores the tokens into a tokenBuffer
    #The token buffer stores tokens in the order that they are going to be consumed
    global tokenBuffer
    tokenBuffer = tokens
    #Stores the parse tree resulting from my recursive decent parser with some back tracking
    translationUnit, astTranlTree = parseTranslationUnit(tokenBuffer)
    #checks to make sure that all tokens have been consumed, i.e token buffer should be empty
    # if all tokens have not been consumed yet, then we need to throw an error message
    if tokenBuffer:
        #Convert the values of all the consumed tokens into string format
        #errorString = generateErrorString(tokenBuffer, isParseTreeGenerated=True)
        #raise NotAllTokensHaveBeenConsumedError(errorString,"Invalid expression")
        raise SyntaxError("Oh No")
    return translationUnit,astTranlTree,symTable

#from https://stackoverflow.com/questions/43752962/how-to-iterate-through-a-nested-dict
def get_all_keys(d):
    for key, value in d.items():
        yield key
        if isinstance(value, dict):
            yield from get_all_keys(value)

"""
translation-unit:
    external-declaration translation-unit
"""

def parseTranslationUnit(tokens):
    """
    Description:
        Simulates the translation-unit productions     
    Arguments:
        tokenBuffer: tokens that have yet to be consumed
    Returns:
        translationUnitTree: a dictionary obj that stores all children from translation-unit productions 
    """
    #Initializes a dictionary object that will store the children of translation-unit
    translationUnitTree = {'Translation-Unit':{}}
    astTranslUnitTree = {}
    global tokenBuffer
    externalDeclaration, astExternalDecl = parseExternalDeclaration(tokenBuffer)
    #Updating the translatationUnitTree with the externalDeclation subtree
    if externalDeclaration:
        translationUnitTree['Translation-Unit'].update(externalDeclaration)
        astTranslUnitTree.update(astExternalDecl)
        #breakpoint()
        if tokenBuffer:
            consumed.clear()
            astStmtTree.clear()
            #tokens = tokenBuffer
            translationUnit,astTranslUnit = parseTranslationUnit(tokenBuffer)
            if astTranslUnit != {}:
                translationUnitTree['Translation-Unit'].update(translationUnit)
                astTranslUnitTree.update(astTranslUnit)
        #externalDeclarationPrime,astExternalDeclPrime = parseExternalDeclarationPrime(tokens)  
        
    return translationUnitTree, astTranslUnitTree

"""
external-declaration:
    declaration
    function-definition
"""

def parseExternalDeclaration(tokens):
    """
    Description:
    Arguments:
    Returns:
    
    """
    externalDeclarationTree = {'External-Declaration':{}}
    astExternalDeclarationTree = {}
    #breakpoint()
    global tokenBuffer
    declaration, astDeclaration = parseDeclaration(tokenBuffer)
    if declaration['Declaration'].get('END') != None:
        externalDeclarationTree['External-Declaration'].update(declaration)
        astExternalDeclarationTree.update(astDeclaration)
        var_name = declaration['Declaration']['Init-Declarator']['ID']
        var_type = declaration['Declaration']['type-specifier']
        breakpoint()
        symTable.addAVariable(var_name,var_type,'global')
    else:
        #global tokenBuffer
        #breakpoint()
        tokenBuffer = consumed + tokenBuffer
        astDeclarationTree.clear()
        consumed.clear()
        functionDef, astFunctionDef = parseFunctionDefinition(tokenBuffer)
        if functionDef['Function-Definition'] != {}:
            externalDeclarationTree['External-Declaration'].update(functionDef)
            astExternalDeclarationTree.update(astFunctionDef)
    return externalDeclarationTree, astExternalDeclarationTree


"""
declaration:
    type-specifier init-declarator;
"""
astDeclarationTree = defaultdict(list)
def parseDeclaration(tokens):
    """
    Description:
    Arguments:
    Returns:
    
    """
    declarationTree = {'Declaration':{}}
    type_specifiers = ['int','double','float']
    #breakpoint()
    global tokenBuffer
    tokens = tokenBuffer
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.type in type_specifiers:
        declarationTree['Declaration'].update({'type-specifier':tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)  
        initDecl,astIntDecl = parseInitDeclarator(tokens)
        if initDecl['Init-Declarator'] != None:
            declarationTree['Declaration'].update(initDecl)
            astDeclarationTree.update(astIntDecl)
            tokenToBeConsumed = tokenBuffer[0]
            #breakpoint()
            #print("Declaration",declarationTree)
            if tokenToBeConsumed.value == ';':
                declarationTree['Declaration'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
                #breakpoint()
                #astDeclarationTree.update()
                consume(tokenToBeConsumed,tokenBuffer)
    return declarationTree, astDeclarationTree

"""
init-declarator:
    ID
    ID = expr
"""
def parseInitDeclarator(tokens):
    """
    Description:
    Arguments:
    Returns:
    """
    initDeclaratorTree = {'Init-Declarator':{}}
    astInitDeclaratorTree = {}
    global tokenBuffer
    tokens = tokenBuffer
    tokenToBeConsumed = tokenBuffer[0]
    variable_being_assigned = None
    if tokenToBeConsumed.type == 'ID':
        initDeclaratorTree['Init-Declarator'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        #breakpoint()
        consume(tokenToBeConsumed,tokenBuffer)
        variable_being_assigned = {tokenToBeConsumed.type:tokenToBeConsumed.value}
        #tokenToBeConsumed = tokenBuffer[0]
        tokenToBeConsumed = tokenBuffer[0]
        breakpoint()
        
        if tokenToBeConsumed.value == '=':
            initDeclaratorTree['Init-Declarator'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
            astInitDeclaratorTree.update({tokenToBeConsumed.value:[]})
            astInitDeclaratorTree[tokenToBeConsumed.value].append(variable_being_assigned)
            consume(tokenToBeConsumed,tokenBuffer)
            expr,astExpr = parseExpr(tokens)
            #breakpoint()
            if expr['Expr'] != None:
                initDeclaratorTree['Init-Declarator'].update(expr)
                astInitDeclaratorTree['='].append(astExpr)
            #astInitDeclaratorTree['='].update(astDeclarator)
            #astInitDeclaratorTree['='].update(astInitializer)
    return initDeclaratorTree, astInitDeclaratorTree

    
"""
function-definition:
    type-specifier ID (parameter-list) compound-statement
"""    
function_name = None
def parseFunctionDefinition(tokens):
    """
    Description:
    Arguments:
    Returns:
    """
    functionDefTree = {'Function-Definition':{}}
    astFunctionDefTree = {}
    type_specifiers = ['int','double', 'float']
    #global tokenBuffer
    #tokens = tokenBuffer
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.type in type_specifiers:
        functionDefTree['Function-Definition'].update({'return-type':tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        tokenToBeConsumed = tokenBuffer[0]
        if tokenToBeConsumed.type == 'ID':
            functionDefTree['Function-Definition'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
            #print(functionDefTree)
            global function_name
            function_name = functionDefTree['Function-Definition']['ID']
            astFunctionDefTree.update({function_name:{}})
            return_type = functionDefTree['Function-Definition']['return-type']
            symTable.addAFunction(function_name, return_type)
            consume(tokenToBeConsumed,tokenBuffer)
            tokenToBeConsumed = tokenBuffer[0]
            if tokenToBeConsumed.type == 'LPAREN':
                functionDefTree['Function-Definition'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
                consume(tokenToBeConsumed,tokenBuffer)
                param_list, astParm = parseParameterList(tokenBuffer)
                #print(param_list[0])
                if param_list['Parameter-List']:
                    functionDefTree['Function-Definition'].update(param_list)
                    tokenToBeConsumed = tokenBuffer[0]
                    if tokenToBeConsumed.type == 'RPAREN':
                        functionDefTree['Function-Definition'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
                        consume(tokenToBeConsumed,tokenBuffer)
                        #breakpoint()
                        compoundStmt, astCompStmt = parseCompoundStatement(tokenBuffer)
                        if compoundStmt['Compound-Statement'] != None:
                            functionDefTree['Function-Definition'].update(compoundStmt)
                            astFunctionDefTree[function_name].update(astCompStmt)
    return functionDefTree, astFunctionDefTree


"""
parameter-list:
    parameter-declaration parameter-list'
"""

def parseParameterList(tokens):
    """
    Description:
    Arguments:
        tokenBuffer: tokens that have yet to be consumed
    Returns:
        parameterListTree: dict object that contains the children resulting from parameter-list productions
    """
    parameterListTree = {'Parameter-List':{}}
    astParameterListTree = {}
    global tokenBuffer
    tokens = tokenBuffer
    parameterDeclaration, astParamDeclTree = parseParameterDeclaration(tokens)
    if parameterDeclaration:
        #print(parameterDeclaration)
        parameterListTree['Parameter-List'].update(parameterDeclaration)
        astParameterListTree.update(astParamDeclTree)
        parameterListPrime = parseParameterListPrime(tokens)
        if parameterListPrime['Parameter-List-Prime'] != None:
            parameterListTree['Parameter-List'].update(parameterListPrime)
    return parameterListTree, astParameterListTree


"""
parameter-list':
    , parameter-declaration parameter-list'
    epsilon
"""

def parseParameterListPrime(tokens):
    """
    Description:
    Arguments:
        tokenBuffer: tokens that have yet to be consumed
    Returns:
        parameterListPrimeTree: dict object that contains the children resulting from parameter-list' productions
    """
    parameterListPrimeTree = {'Parameter-List-Prime':{}}
    global tokenBuffer
    tokens = tokenBuffer
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.type == 'COMMA':
        parameterListPrimeTree['Parameter-List-Prime'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        parameterDeclaration, astParamDecl = parseParameterDeclaration(tokens)
        if parameterDeclaration:
            parameterListPrimeTree['Parameter-List-Prime'].update(parameterDeclaration)
            parameterListPrime = parseParameterListPrime(tokens)
            if parameterListPrime['Parameter-List-Prime'] != None:
                parameterListPrimeTree['Parameter-List-Prime'].update(parameterListPrime)
    return parameterListPrimeTree

"""
parameter-declaration:
    type-specifier ID

"""
def parseParameterDeclaration(tokens):
    """
    Description:
    Arguments:
        tokenBuffer: tokens that have yet to be consumed
    Returns:
        parameterDeclarationTree: dict object that contains the children resulting from parameter-declaration productions
    """
    parameterDeclarationTree = {'Parameter-Declaration':{}}
    astParameterDeclarationTree = {}
    
    type_specifiers = ['int','double','float']
    global tokenBuffer
    tokens = tokenBuffer
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.type in type_specifiers:
        parameterDeclarationTree['Parameter-Declaration'].update({'type-specifier':tokenToBeConsumed.value}) 
        consume(tokenToBeConsumed,tokenBuffer)
        tokenToBeConsumed = tokenBuffer[0]
        if tokenToBeConsumed.type == 'ID':
            parameterDeclarationTree['Parameter-Declaration'].update({tokenToBeConsumed.type:tokenToBeConsumed.value}) 
            consume(tokenToBeConsumed,tokenBuffer)
            print(parameterDeclarationTree)
            var_type = parameterDeclarationTree['Parameter-Declaration']['type-specifier']
            var_name = parameterDeclarationTree['Parameter-Declaration']['ID']
            symTable.addAParameter(var_name,var_type,function_name)
    return parameterDeclarationTree, astParameterDeclarationTree

"""     
compound-statement:
    { block-item-list }
"""
def parseCompoundStatement(tokens):
    """
    Description:
    Arguments:
    Returns:
    """
    compoundStatementTree = {'Compound-Statement':{}}
    astCompoundStatementTree = {}
    global tokenBuffer
    tokens = tokenBuffer
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.type == 'LBRACE':
        compoundStatementTree['Compound-Statement'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        astCompoundStatementTree.update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        #breakpoint()
        blockItemList, astBlockItemList = parseBlockItemList(tokens)
        if blockItemList['Block-Item-List'] != None:
            compoundStatementTree['Compound-Statement'].update(blockItemList)
            #breakpoint()
            if astBlockItemList == {} and astStmtTree['Statement'] != []:
                astBlockItemList = astStmtTree
            astCompoundStatementTree.update(astBlockItemList)
            tokenToBeConsumed = tokenBuffer[0]
            if tokenToBeConsumed.type == 'RBRACE':
                compoundStatementTree['Compound-Statement'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
                astCompoundStatementTree.update({tokenToBeConsumed.type:tokenToBeConsumed.value})
                consume(tokenToBeConsumed,tokenBuffer)
    return compoundStatementTree, astCompoundStatementTree

"""
block-item-list:
    block-item block-item-list
    epsilon
"""
def parseBlockItemList(tokens):
    blockItemListTree = {'Block-Item-List':{}}
    astBlockItemListTree = defaultdict(list)
    global tokenBuffer
    tokens = tokenBuffer
    if tokenBuffer[0].type != 'RBRACE':
        blockItem, astBlockItem = parseBlockItem(tokens)
        if blockItem['Block-Item'] != {}:
            blockItemListTree['Block-Item-List'].update(blockItem)
            #breakpoint()
            if '=' in astBlockItem:
                astStmtTree['Statement'].append(astBlockItem)
                #astBlockItemListTree = {}
                #astBlockItem = None
            else:
                astBlockItemListTree.update(astBlockItem)
            blockItemList, astBlockItemList = parseBlockItemList(tokens)
            if blockItemList['Block-Item-List'] != {}:
                blockItemListTree['Block-Item-List'].update(blockItemList)
                #astBlockItemListTree.setdefault(k, []).append(v)
                astBlockItemListTree.update(astBlockItemList)
    return blockItemListTree, astBlockItemListTree

"""
block-item:
    declaration
    statement
"""
def parseBlockItem(tokens):
    """
    Description:
    Arguments:
    Returns:
    """
    blockItemTree = {'Block-Item':{}}
    astBlockItemTree = {}
    #breakpoint()
    global tokenBuffer
    tokens = tokenBuffer
    declaration, astDeclaration = parseDeclaration(tokens)
    if declaration['Declaration'].get('END') == None:
        statement,astStmt = parseStatement(tokenBuffer)
        if statement:
            blockItemTree['Block-Item'].update(statement)
            astBlockItemTree.update(astStmt)
    else:
        #print(declaration)
        blockItemTree['Block-Item'].update(declaration)
        #print("Declaration",declaration)
        var_name = declaration['Declaration']['Init-Declarator']['ID']
        var_type = declaration['Declaration']['type-specifier']
        symTable.addAVariable(var_name,var_type,function_name,'local')
        breakpoint()
        #var_name = declaration['Declaration'][]
        #breakpoint()
        astBlockItemTree.update(astDeclaration)
        #breakpoint()
        astDeclaration.clear()
    return blockItemTree, astBlockItemTree

"""
statement:
    assignment-statement
    return-statement
"""

astStmtTree = defaultdict(list)
def parseStatement(tokens):
    """
    Description:
    Arguments:
    Returns:
    """
    statementTree = {'Statement':{}}
    #astStmtTree = {}
    global tokenBuffer
    tokens = tokenBuffer
    assignStatement,astAssignStmt = parseAssignmentStatement(tokens)
    if assignStatement['Assignment-Statement'] != {}:
        #breakpoint()
        statementTree['Statement'].update(assignStatement)
        astStmtTree['Statement'].append(astAssignStmt)
    else:
        returnStatement, astReturnStmt = parseReturnStatement(tokens)
        if returnStatement['Return-Statement'] != {}:
            #breakpoint()
            statementTree['Statement'].update(returnStatement)
            astStmtTree['Statement'].append(astReturnStmt)
    #astStmtTree = defaultdict(list)
    return statementTree, astStmtTree

"""
assignment-statement:
    ID = expr;

"""
def parseAssignmentStatement(tokens):
    assignmentStmtTree = {'Assignment-Statement':{}}
    astAssignmentStmtTree = {}
    global tokenBuffer
    tokens = tokenBuffer
    tokenToBeConsumed = tokenBuffer[0]
    #breakpoint()
    variable_being_assigned = None
    if tokenToBeConsumed.type == 'ID':
        assignmentStmtTree['Assignment-Statement'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        variable_being_assigned = {tokenToBeConsumed.type:tokenToBeConsumed.value}
        tokenToBeConsumed = tokenBuffer[0]
        if tokenToBeConsumed.value == '=':
            assignmentStmtTree['Assignment-Statement'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
            astAssignmentStmtTree = {tokenToBeConsumed.value:[]}
            astAssignmentStmtTree[tokenToBeConsumed.value].append(variable_being_assigned)
            consume(tokenToBeConsumed,tokenBuffer)
            expr,astExpr = parseExpr(tokens)
            if expr['Expr'] != None:
                assignmentStmtTree['Assignment-Statement'].update(expr)
                astAssignmentStmtTree['='].append(astExpr)
                #print(astExpr)
                tokenToBeConsumed = tokenBuffer[0]
                if tokenToBeConsumed.value == ';':
                    assignmentStmtTree['Assignment-Statement'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
                    consume(tokenToBeConsumed,tokenBuffer)
    return assignmentStmtTree,astAssignmentStmtTree

"""
return-statement:
    return expr;
"""
def parseReturnStatement(tokens):
    """
    Description:
    Arguments:
    Returns:
    """
   
    returnStmtTree = {'Return-Statement':{}}
    astReturnStmtTree = {}
    global tokenBuffer
    tokens = tokenBuffer
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.value == 'return':
        returnStmtTree['Return-Statement'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        astReturnStmtTree = {tokenToBeConsumed.value:[]}
        consume(tokenToBeConsumed,tokenBuffer)
        #breakpoint()
        exprTree,astExprTree = parseExpr(tokens)
        if exprTree['Expr'] != None:
            returnStmtTree['Return-Statement'].update(exprTree)
            astReturnStmtTree['return'].append(astExprTree)
            tokenToBeConsumed = tokenBuffer[0]
            if tokenToBeConsumed.type == 'END':
                returnStmtTree['Return-Statement'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
                consume(tokenToBeConsumed,tokenBuffer)
    return returnStmtTree, astReturnStmtTree

isFactorExpr = False
def parseExpr(tokens):
    """
    Description:
        Simulates the Expr productions from the grammar
    Args:
        tokenBuffer: tokens that have yet to be consumed
    Returns:
        exprTree: A nested dictionary object that contains all children resulting from Expr productions
    """ 
    #print("Entering Expr")
    #Initializes a dictionary object that will store the children of Expr
    exprTree = {'Expr':{}}
    astExprTree = {}
    global tokenBuffer
    tokens = tokenBuffer
    #parse Term
    term,astTerm = parseTerm(tokens)
    if term:
        exprTree['Expr'].update(term)
        astExprTree.update(astTerm)
    #breakpoint()
    exprPrime,astExprPrime = parseExprPrime(tokens)
    if exprPrime['ExprP']:
        exprTree['Expr'].update(exprPrime)
        #astExprTree.update(astExprPrime)
        #breakpoint()
        if astExprPrime != {}:
            
            #operator2 = list(list(astExprPrime[operator1])[0].keys())[0]    
            """
            operator2 = list(list(astExprPrime[operator1])[0].keys())[0]
            if operator2 in operations:
                print(operator1,operator2)
                op3 = list(astExprPrime[operator1][0][operator2][0].keys())[0]
                if op3 in operations:
                    op4 = list(astExprPrime[operator1][0][operator2][0][op3][0].keys())[0]
                    if op4 in operations:
                        astExprPrime[operator1][0][operator2][0][op3][0][op4].insert(0,astTerm)
                    else:    
                        astExprPrime[operator1][0][operator2][0][op3].insert(0,astTerm)
                else:           
                    astExprPrime[operator1][0][operator2].insert(0,astTerm)
            else:
                astExprPrime[operator1].insert(0,astTerm)
            """
            #breakpoint()
            global isFactorExpr
            #breakpoint()
            if isFactorExpr == True and tokenBuffer[0].type == 'END':
                isFactorExpr = False
            #breakpoint()
            global number_of_nodes
            number_of_nodes = totalNodes(astExprPrime)
            #breakpoint()
            inOrder(astExprPrime,astTerm,operations=['+','-'])
            #other_function(astExprPrime,astTerm,operations=['+','-'],isExprinParens=isFactorExpr)
            isFactorExpr = False
            #print("ok",astExprPrime)
            astExprTree.popitem()
            astExprTree.update(astExprPrime)
            
    return exprTree,astExprTree

def parseTerm(tokens):
    """
    Description:
        Simulates the Term productions from the grammar
    Args:
        tokenBuffer: tokens that have yet to be consumed
    Returns:
        termTree: A nested dictionary object that contains all children resulting from Term productions 
    """
    #print("Entering Term")
    #Initializes a dictionary object called termDict that has a key called Term 
    # and an empty dictionary as the value to store children
    termTree = {'Term':{}}
    astTermTree = {}
    global tokenBuffer
    tokens = tokenBuffer
    #Contains the tree for factor given the tokens that remain in the buffer
    factor,astFactor = parseFactor(tokens)
    #The value of factor will only be stored as a child of Term in Term dictionary if factor exists
    if factor:
        termTree['Term'].update(factor)
        astTermTree.update(astFactor)
    #Contains the tree for Term' given the tokens that remain in the buffer
    termPrime,astTermPrime = parseTermPrime(tokens)
    #The resulting Term' tree will ony be stored as a child of Term if termPrime exists
    if termPrime:
        termTree['Term'].update(termPrime)
    
    if astTermPrime != {}:
        #print(astTermPrime)
        #breakpoint()
        global isFactorExpr
        #breakpoint()
        
        if isFactorExpr == True and tokenBuffer[0].type == 'END':
            isFactorExpr = False
        #breakpoint()
        inOrder(astTermPrime,astFactor,operations=['*','/'])
        #other_function(astTermPrime,astFactor,operations=['*','/'],isExprinParens=isFactorExpr)
        isFactorExpr = False
        #print(astTermTree)
        astTermTree.popitem()
        astTermTree.update(astTermPrime)
    #print("Exiting Term")
    return termTree,astTermTree

def parseFactor(tokens):
    """
    Description:
        Simulates the Factor productions from the grammar
    Args:
        tokenBuffer: tokens that have yet to be consumed
    Returns:
        factorTree: A nested dictionary object that contains all children resulting from Factor productions
    """
    #print("Entering Factor")
    #Initalizes a dictionary object that stores the children resulting from a matching factor production
    factorTree = {'Factor':{}}
    astFactorTree = {}
    global tokenBuffer
    tokens = tokenBuffer
    #Checks to make sure there are tokens left in the token buffer, if not there must be an error
    if tokenBuffer:
        #the next token to be consumed will be set to the token that is next in the tokens buffer 
        tokenToBeConsumed = tokenBuffer[0]
    else:
        errorString = generateErrorString(tokens)
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
    #breakpoint()
    signs = ['+','-']
    sign = ''
    #breakpoint()
    if tokenToBeConsumed.value in signs:
        sign = copy.deepcopy(tokenToBeConsumed.value)
        consume(tokenToBeConsumed,tokenBuffer)
        tokenToBeConsumed = tokenBuffer[0] 
    leafNode = match(tokenToBeConsumed, terminalNodes,isFactor=True)
    # if a match exists, check to see if the type is a LPAREN
    #breakpoint()
    if leafNode:
        if leafNode.type == 'LPAREN':
            factorTree['Factor'].update({leafNode.type:leafNode.value})
            consume(tokenToBeConsumed,tokenBuffer)
            #breakpoint()
            expr,astExpr = parseExpr(tokens)
            if expr:
                factorTree['Factor'].update(expr)
                astFactorTree.update(astExpr)
            tokenToBeConsumed = tokenBuffer[0]
            leafNode = match(tokenToBeConsumed, terminalNodes,True)
            if leafNode:
                if leafNode.type == 'RPAREN':
                    factorTree['Factor'].update({leafNode.type:leafNode.value})
                    consume(tokenToBeConsumed,tokenBuffer)
                    #breakpoint()
                    global isFactorExpr
                    isFactorExpr = True
            else:
                errorString = generateErrorString(tokens)
                raise MissingRParenError(errorString,"Expected a Right Parenthesis",
                                 {'line': consumed[len(consumed)-1].line, 'column': consumed[len(consumed)-1].column+1})   
        else:
            if leafNode.type == 'RPAREN':
                errorString = generateErrorString(tokens)
                raise MissingFactorError(errorString,"Expected an Identifier or Number",
                                 {'line': consumed[len(consumed)-1].line, 'column': consumed[len(consumed)-1].column+1})             
            factorTree['Factor'].update({leafNode.type:sign+str(leafNode.value)})
            #astFactorTree.update({leafNode.type:sign+str(leafNode.value)})
            astFactorTree.update({leafNode.type:leafNode.value})
            consume(tokenToBeConsumed,tokenBuffer)
    else:
        errorString = generateErrorString(tokens)
        raise MissingFactorError(errorString,"Expected an Identifier or Number",
                                 {'line': consumed[len(consumed)-1].line, 'column': consumed[len(consumed)-1].column+1})
    #print("Exiting Factor")
    return factorTree, astFactorTree

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


def parseExprPrime(tokens):
    """
    Description:
        Simulates the Expr' productions from the grammar
    Args:
        tokenBuffer: the tokens that have yet to be consumed
    Returns:
        exprPrimeTree: A nested dictionary object that contains all children resulting from Expr' productions
    """
    #print("Entering Expr'")
    #Initalizes a dictionary object that stores the children resulting from a matching Expr' production
    exprPrimeTree = {'ExprP':'ε'}
    astExprPrimeTree = {}
    global tokenBuffer
    tokens = tokenBuffer
    #If tokens have yet to be consumed, match the value of the next token to be consumed to a '+' or '-' 
    if tokenBuffer:    
        tokenToBeConsumed = tokenBuffer[0]
        terminalNodes = {'+','-'}
        leafNode = match(tokenToBeConsumed, terminalNodes)
        if leafNode:
            exprPrimeTree = {'ExprP':{}} 
            exprPrimeTree['ExprP'].update({leafNode.type:leafNode.value})
            astExprPrimeTree = {leafNode.value:[]}
            consume(tokenToBeConsumed,tokenBuffer)
            term,astTerm = parseTerm(tokenBuffer)
            if term:
                exprPrimeTree['ExprP'].update(term)
                astExprPrimeTree[leafNode.value].append(astTerm)
                #print(astExprPrimeTree)
            #breakpoint()
            exprPrime,astExprPrime = parseExprPrime(tokenBuffer)
            if exprPrime:
                exprPrimeTree['ExprP'].update(exprPrime)
                #astExprPrimeTree[leafNode.value].append(astExprPrime)
            if astExprPrime != {}:
                if astExprPrimeTree != {}:
                    #breakpoint()
                    #print(astExprPrime,astExprPrimeTree)
                    #breakpoint()
                    #inOrder(astExprPrimeTree,astExprPrime,terminalNodes)
                    astExprPrimeTree = new_func(astExprPrimeTree, terminalNodes, astExprPrime)
                    astExprPrimeTree = astExprPrime
                    #other_function(astExprPrimeTree,astExprPrime,terminalNodes)
                else:
                    astExprPrimeTree[leafNode.value].append(astExprPrime)
                #print("AST ExprPrime",astExprPrimeTree)
    #print("Exiting Expr'")        
    return exprPrimeTree,astExprPrimeTree

def new_func(astExprPrimeTree, terminalNodes, astExprPrime):
    #breakpoint()
    #assuming key1 is always a '+' or '-'
    operator1 = list(astExprPrime.keys())[0]
    if astExprPrimeTree == astExprPrime:
        operator2 = list(list(astExprPrime[operator1])[0].keys())[0]
    else:
        operator2 = list(astExprPrimeTree.keys())[0]
  
    #print(operator1,operator2)
    #breakpoint()
    """
    if list(astExprPrime[operator1][0].keys())[0] == 'NUMBER' \
        or list(astExprPrime[operator1][0].keys())[0] == 'ID':
        astExprPrime[operator1].insert(0,astExprPrimeTree)
        astExprPrimeTree = astExprPrime
    """
    if len(astExprPrime[operator1]) == 1:
        #breakpoint()
        #key2 = list(astExprPrime[operator1][0].keys())[0]
        #print(key2)
        #breakpoint()    
        astExprPrime[operator1].insert(0,astExprPrimeTree)
        astExprPrimeTree = astExprPrime
    else:
        return new_func(astExprPrimeTree,terminalNodes,astExprPrime[operator1][0])
    return astExprPrimeTree

def other_function(astExprPrime,astTerm,operations,isExprinParens=False):
    #operations = ['+','-','*','/']
    operator1 = list(astExprPrime.keys())[0]
    if operator1 in operations:
        operator2 = list(astExprPrime[operator1][0].keys())[0]
        #breakpoint()
        if isExprinParens != True:
            #breakpoint()
            if operator2 in operations and len(astExprPrime[operator1][0][operator2])!=1:
                return other_function(astExprPrime[operator1][0],astTerm,operations,isExprinParens)
            else:
                if operator2 not in operations:
                    astExprPrime[operator1].insert(0,astTerm)
                else:
                    astExprPrime[operator1][0][operator2].insert(0,astTerm)
        else:
            if operator2 in operations and len(astExprPrime[operator1][0][operator2])!=2:
                return other_function(astExprPrime[operator1][0],astTerm,operations,isExprinParens)
            else:
                #breakpoint()
                astExprPrime[operator1].insert(0,astTerm)

visited_elements = []
def inOrder(root,node,operations):
    #internal_nodes = ['+','-','*','/']
    left = None
    right = None
    if root:
        root_key = list(root.keys())[0]
        if root_key in operations:
            children = root[root_key]
            left = children[0]
            if len(children) == 2:
                right = children[1]
            inOrder(left,node,operations)
            visited_elements.append(root_key)
            if right == None:
                root[root_key].insert(0,node)

            inOrder(right,node,operations)
            """
            if number_of_nodes == len(visited_elements):
                root[root_key].insert(0,node)     
            """
        else:
            visited_elements.append(root[root_key])
    
# from https://www.geeksforgeeks.org/count-number-of-nodes-in-a-complete-binary-tree/
# Function to get the count of nodes
# in complete binary tree
def totalNodes(root):
  # Base case
    internal_nodes = ['+','-','*','/']
    if(root == None):
        return 0
    # Find the left height and the
    # right heights
    root_type = list(root.keys())[0]
    if root_type not in internal_nodes:
        l = 0
        r = 0
    else:
        l = totalNodes(root[root_type][0])
        if len(root[root_type]) == 2:
            r = totalNodes(root[root_type][1])
        else:
            r = 0
 
    return 1 + l + r

def parseTermPrime(tokens):
    """
    Description: 
        Simulates the Term' productions from the grammar
    Args:
        tokenBuffer: tokens that have yet to be consumed
    Return:
        termPrimeTree: A nested dictionary object that contains all children resulting from Term' productions
    """
    #print("Entering Term'")
    termPrimeTree = {'TermP':'ε'}
    astTermPrimeTree = {}
    global tokenBuffer
    if tokenBuffer:
        tokenToBeConsumed = tokenBuffer[0]
        terminalNodes = {'*','/'}
        leafNode = match(tokenToBeConsumed, terminalNodes)
        if leafNode:
            termPrimeTree = {'TermP':{}}
            termPrimeTree['TermP'].update({leafNode.type:leafNode.value})
            astTermPrimeTree = {leafNode.value:[]}
            consume(tokenToBeConsumed,tokenBuffer)
            factor,astFactor = parseFactor(tokenBuffer)
            if factor:
                termPrimeTree['TermP'].update(factor)
                #astTermPrime
                astTermPrimeTree[leafNode.value].append(astFactor)
            #breakpoint()
            termPrime,astTermPrime = parseTermPrime(tokenBuffer)
            if termPrime:
                termPrimeTree['TermP'].update(termPrime)
            if astTermPrime != {}:
                if astTermPrimeTree != {}:
                    #breakpoint()        
                    #inOrder(astTermPrimeTree,astTermPrime,terminalNodes)
                    astTermPrimeTree = new_func(astTermPrimeTree,terminalNodes,astTermPrime)
                    astTermPrimeTree = astTermPrime
                else:
                    astTermPrimeTree[leafNode.value].append(astTermPrime)
    #print("Exiting Term'")
    return termPrimeTree, astTermPrimeTree

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

#ref https://datagy.io/python-nested-dictionary/
terminalNodes = []
def findTerminalNodes(dict_to_iterate):
    for key, value in dict_to_iterate.items():
        if type(value) == dict:
            #print(key)
            findTerminalNodes(value)
        else:
            #print(key + ":" + value)
            global terminalNodes
            terminalNodes.append(value)

def recursive_items(dictionary):
    for key, value in dictionary.items():
        if type(value) is dict:
            yield from recursive_items(value)
        else:
            yield (key, value)
def main():
    #tokens = [(), (), (), ()]    
    dict1 =  {'Conditional-Expression': {'Logical-OR-Expression': {'Logical-AND-Expression': {'Inclusive-OR-Expression': {'Exclusive-OR-Expression': {'AND-Expression': {'Equality-Expression': {'Relational-Expression': {'Shift-Expression': {'Additive-Expression': {'Multiplicative-Expression': {'Cast-Expression': {'Unary-Expression': {'Postfix-Expression': {'Primary-Expression': {'ID': 'b'}}}}, 'Multiplicative-Expression-Prime': {}}, 'Additive-Expression-Prime': {}}}}}}}}, 'Logical-AND-Expression-Prime': {}}, 'Logical-OR-Expression-Prime': {}}}}
    dict2 = {'Translation-Unit': {'External-Declaration': {'Function-Definition': {'Declaration-Specifiers': {'return-type': 'int'}, 'Declarator': {'Direct-Declarator': {'function-name': 'main', 'Direct-Declarator-Prime': {'LPAREN': '(', 'Parameter-Type-List': {'Parameter-List': {'Parameter-Declaration': {}}}, 'RPAREN': ')'}}}, 'Compound-Statement': {'LBRACE': '{', 'Block-Item-List': {'Block-Item': {'Statement': {'Jump-Statement': {'return': 'return', 'Expression': {'Assignment-Expression': {'Conditional-Expression': {'Logical-OR-Expression': {'Logical-AND-Expression': {'Inclusive-OR-Expression': {'Exclusive-OR-Expression': {'AND-Expression': {'Equality-Expression': {'Relational-Expression': {'Shift-Expression': {'Additive-Expression': {'Multiplicative-Expression': {'Cast-Expression': {'Unary-Expression': {'Postfix-Expression': {'Primary-Expression': {'NUMBER': 0}}}}}}}}}}}}}}}}}, 'END': ';'}}}}, 'RBRACE': '}'}}}}}
    dict3 = {'Translation-Unit': {'External-Declaration': {'Function-Definition': {'Declaration-Specifiers': {'return-type': 'int'}, 'Declarator': {'Direct-Declarator': {'function-name': 'main', 'Direct-Declarator-Prime': {'LPAREN': '(', 'Parameter-Type-List': {'Parameter-List': {'Parameter-Declaration': {'Declaration-Specifiers': {'type-specifier': 'int'}, 'Declarator': {'Direct-Declarator': {'ID': 'a'}}}, 'Parameter-List-Prime': {'COMMA': ',', 'Parameter-Declaration': {'Declaration-Specifiers': {'type-specifier': 'int'}, 'Declarator': {'Direct-Declarator': {'ID': 'b'}}}, 'Parameter-List-Prime': {'COMMA': ',', 'Parameter-Declaration': {'Declaration-Specifiers': {'type-specifier': 'int'}, 'Declarator': {'Direct-Declarator': {'ID': 'c'}}}}}}}, 'RPAREN': ')'}}}, 'Compound-Statement': {'LBRACE': '{', 'Block-Item-List': {'Block-Item': {'Declaration': {'Declaration-Specifiers': {'type-specifier': 'int'}, 'Init-Declarator-List': {'Init-Declarator': {'Declarator': {'Direct-Declarator': {'ID': 'x'}}, 'ASSIGN_OPS': '=', 'Initializer': {'Assignment-Expression': {'Conditional-Expression': {'Logical-OR-Expression': {'Logical-AND-Expression': {'Inclusive-OR-Expression': {'Exclusive-OR-Expression': {'AND-Expression': {'Equality-Expression': {'Relational-Expression': {'Shift-Expression': {'Additive-Expression': {'Multiplicative-Expression': {'Cast-Expression': {'Unary-Expression': {'Postfix-Expression': {'Primary-Expression': {'NUMBER': 4}}}}}}}}}}}}}}}}}}, 'Init-Declarator-List-Prime': {}}, 'END': ';'}}, 'Block-Item-List': {'Block-Item': {'Declaration': {'Declaration-Specifiers': {'type-specifier': 'int'}, 'Init-Declarator-List': {'Init-Declarator': {'Declarator': {'Direct-Declarator': {'ID': 'y'}}, 'ASSIGN_OPS': '=', 'Initializer': {'Assignment-Expression': {'Conditional-Expression': {'Logical-OR-Expression': {'Logical-AND-Expression': {'Inclusive-OR-Expression': {'Exclusive-OR-Expression': {'AND-Expression': {'Equality-Expression': {'Relational-Expression': {'Shift-Expression': {'Additive-Expression': {'Multiplicative-Expression': {'Cast-Expression': {'Unary-Expression': {'Postfix-Expression': {'Primary-Expression': {'ID': 'x'}}}}}, 'Additive-Expression-Prime': {'MATH_OP': '+', 'Cast-Expression': {'Unary-Expression': {'Postfix-Expression': {'Primary-Expression': {'NUMBER': 2}}}}}}}}}}}}}}}}}}, 'Init-Declarator-List-Prime': {}}, 'END': ';'}}, 'Block-Item-List': {'Block-Item': {'Declaration': {'Declaration-Specifiers': {'type-specifier': 'int'}, 'Init-Declarator-List': {'Init-Declarator': {'Declarator': {'Direct-Declarator': {'ID': 'd'}}, 'ASSIGN_OPS': '=', 'Initializer': {'Assignment-Expression': {'Conditional-Expression': {'Logical-OR-Expression': {'Logical-AND-Expression': {'Inclusive-OR-Expression': {'Exclusive-OR-Expression': {'AND-Expression': {'Equality-Expression': {'Relational-Expression': {'Shift-Expression': {'Additive-Expression': {'Multiplicative-Expression': {'Cast-Expression': {'Unary-Expression': {'Postfix-Expression': {'Primary-Expression': {'LPAREN': '(', 'Expression': {'Assignment-Expression': {'Conditional-Expression': {'Logical-OR-Expression': {'Logical-AND-Expression': {'Inclusive-OR-Expression': {'Exclusive-OR-Expression': {'AND-Expression': {'Equality-Expression': {'Relational-Expression': {'Shift-Expression': {'Additive-Expression': {'Multiplicative-Expression': {'Cast-Expression': {'Unary-Expression': {'Postfix-Expression': {'Primary-Expression': {'ID': 'c'}}}}}, 'Additive-Expression-Prime': {'MATH_OP': '+', 'Cast-Expression': {'Unary-Expression': {'Postfix-Expression': {'Primary-Expression': {'NUMBER': 8}}}}}}}}}}}}}}}}}, 'RPAREN': ')'}}}}, 'Multiplicative-Expression-Prime': {'MATH_OP': '/', 'Cast-Expression': {'Unary-Expression': {'Postfix-Expression': {'Primary-Expression': {'LPAREN': '(', 'Expression': {'Assignment-Expression': {'Conditional-Expression': {'Logical-OR-Expression': {'Logical-AND-Expression': {'Inclusive-OR-Expression': {'Exclusive-OR-Expression': {'AND-Expression': {'Equality-Expression': {'Relational-Expression': {'Shift-Expression': {'Additive-Expression': {'Multiplicative-Expression': {'Cast-Expression': {'Unary-Expression': {'Postfix-Expression': {'Primary-Expression': {'ID': 'y'}}}}}}}}}}}}}}}}}, 'RPAREN': ')'}}}}}}}}}}}}}}}}}}}, 'Init-Declarator-List-Prime': {}}, 'END': ';'}}, 'Block-Item-List': {'Block-Item': {'Statement': {'Jump-Statement': {'return': 'return', 'Expression': {'Assignment-Expression': {'Conditional-Expression': {'Logical-OR-Expression': {'Logical-AND-Expression': {'Inclusive-OR-Expression': {'Exclusive-OR-Expression': {'AND-Expression': {'Equality-Expression': {'Relational-Expression': {'Shift-Expression': {'Additive-Expression': {'Multiplicative-Expression': {'Cast-Expression': {'Unary-Expression': {'Postfix-Expression': {'Primary-Expression': {'ID': 'a'}}}}}}}}}}}}}}}}}, 'END': ';'}}}}}}}, 'RBRACE': '}'}}}}}
    dict4 = {'Translation-Unit': {'External-Declaration': {'Function-Definition': {'Declaration-Specifiers': {'return-type': 'int'}, 'Declarator': {'Direct-Declarator': {'function-name': 'main', 'Direct-Declarator-Prime': {'LPAREN': '(', 'Parameter-Type-List': {'Parameter-List': {'Parameter-Declaration': {'Declaration-Specifiers': {'type-specifier': 'int'}, 'Declarator': {'Direct-Declarator': {'ID': 'a'}}}, 'Parameter-List-Prime': {'COMMA': ',', 'Parameter-Declaration': {'Declaration-Specifiers': {'type-specifier': 'int'}, 'Declarator': {'Direct-Declarator': {'ID': 'b'}}}, 'Parameter-List-Prime': {'COMMA': ',', 'Parameter-Declaration': {'Declaration-Specifiers': {'type-specifier': 'int'}, 'Declarator': {'Direct-Declarator': {'ID': 'c'}}}}}}}, 'RPAREN': ')'}}}, 'Compound-Statement': {'LBRACE': '{', 'Block-Item-List': {'Block-Item': {'Declaration': {'Declaration-Specifiers': {'type-specifier': 'int'}, 'Init-Declarator-List': {'Init-Declarator': {'Declarator': {'Direct-Declarator': {'ID': 'x'}}, 'ASSIGN_OPS': '=', 'Initializer': {'Assignment-Expression': {'Conditional-Expression': {'Logical-OR-Expression': {'Logical-AND-Expression': {'Inclusive-OR-Expression': {'Exclusive-OR-Expression': {'AND-Expression': {'Equality-Expression': {'Relational-Expression': {'Shift-Expression': {'Additive-Expression': {'Multiplicative-Expression': {'Cast-Expression': {'Unary-Expression': {'Postfix-Expression': {'Primary-Expression': {'NUMBER': 4}}}}}}}}}}}}}}}}}}, 'Init-Declarator-List-Prime': {}}, 'END': ';'}}, 'Block-Item-List': {'Block-Item': {'Declaration': {'Declaration-Specifiers': {'type-specifier': 'int'}, 'Init-Declarator-List': {'Init-Declarator': {'Declarator': {'Direct-Declarator': {'ID': 'y'}}, 'ASSIGN_OPS': '=', 'Initializer': {'Assignment-Expression': {'Conditional-Expression': {'Logical-OR-Expression': {'Logical-AND-Expression': {'Inclusive-OR-Expression': {'Exclusive-OR-Expression': {'AND-Expression': {'Equality-Expression': {'Relational-Expression': {'Shift-Expression': {'Additive-Expression': {'Multiplicative-Expression': {'Cast-Expression': {'Unary-Expression': {'Postfix-Expression': {'Primary-Expression': {'ID': 'x'}}}}}, 'Additive-Expression-Prime': {'MATH_OP': '+', 'Cast-Expression': {'Unary-Expression': {'Postfix-Expression': {'Primary-Expression': {'NUMBER': 2}}}}}}}}}}}}}}}}}}, 'Init-Declarator-List-Prime': {}}, 'END': ';'}}, 'Block-Item-List': {'Block-Item': {'Declaration': {'Declaration-Specifiers': {'type-specifier': 'int'}, 'Init-Declarator-List': {'Init-Declarator': {'Declarator': {'Direct-Declarator': {'ID': 'd'}}, 'ASSIGN_OPS': '=', 'Initializer': {'Assignment-Expression': {'Conditional-Expression': {'Logical-OR-Expression': {'Logical-AND-Expression': {'Inclusive-OR-Expression': {'Exclusive-OR-Expression': {'AND-Expression': {'Equality-Expression': {'Relational-Expression': {'Shift-Expression': {'Additive-Expression': {'Multiplicative-Expression': {'Cast-Expression': {'Unary-Expression': {'Postfix-Expression': {'Primary-Expression': {'LPAREN': '(', 'Expression': {'Assignment-Expression': {'Conditional-Expression': {'Logical-OR-Expression': {'Logical-AND-Expression': {'Inclusive-OR-Expression': {'Exclusive-OR-Expression': {'AND-Expression': {'Equality-Expression': {'Relational-Expression': {'Shift-Expression': {'Additive-Expression': {'Multiplicative-Expression': {'Cast-Expression': {'Unary-Expression': {'Postfix-Expression': {'Primary-Expression': {'ID': 'c'}}}}}, 'Additive-Expression-Prime': {'MATH_OP': '+', 'Cast-Expression': {'Unary-Expression': {'Postfix-Expression': {'Primary-Expression': {'NUMBER': 8}}}}}}}}}}}}}}}}}, 'RPAREN': ')'}}}}, 'Multiplicative-Expression-Prime': {'MATH_OP': '/', 'Cast-Expression': {'Unary-Expression': {'Postfix-Expression': {'Primary-Expression': {'LPAREN': '(', 'Expression': {'Assignment-Expression': {'Conditional-Expression': {'Logical-OR-Expression': {'Logical-AND-Expression': {'Inclusive-OR-Expression': {'Exclusive-OR-Expression': {'AND-Expression': {'Equality-Expression': {'Relational-Expression': {'Shift-Expression': {'Additive-Expression': {'Multiplicative-Expression': {'Cast-Expression': {'Unary-Expression': {'Postfix-Expression': {'Primary-Expression': {'ID': 'y'}}}}}}}}}}}}}}}}}, 'RPAREN': ')'}}}}}}}}}}}}}}}}}}}, 'Init-Declarator-List-Prime': {}}, 'END': ';'}}, 'Block-Item-List': {'Block-Item': {'Statement': {'Jump-Statement': {'statement': 'return', 'Expression': {'Assignment-Expression': {'Conditional-Expression': {'Logical-OR-Expression': {'Logical-AND-Expression': {'Inclusive-OR-Expression': {'Exclusive-OR-Expression': {'AND-Expression': {'Equality-Expression': {'Relational-Expression': {'Shift-Expression': {'Additive-Expression': {'Multiplicative-Expression': {'Cast-Expression': {'Unary-Expression': {'Postfix-Expression': {'Primary-Expression': {'ID': 'a'}}}}}}}}}}}}}}}}}, 'END': ';'}}}}}}}, 'RBRACE': '}'}}}}}
    dict5 = {'Translation-Unit': {'External-Declaration': {'Function-Definition': {'Declaration-Specifiers': {'return-type': 'int'}, 'Declarator': {'Direct-Declarator': {'function-name': 'main', 'Direct-Declarator-Prime': {'LPAREN': '(', 'Parameter-Type-List': {'Parameter-List': {'Parameter-Declaration': {}}}, 'RPAREN': ')'}}}, 'Compound-Statement': {'LBRACE': '{', 'Block-Item-List': {'Block-Item': {'Statement': {'Jump-Statement': {'statement': 'return', 'Expression': {'Assignment-Expression': {'Conditional-Expression': {'Logical-OR-Expression': {'Logical-AND-Expression': {'Inclusive-OR-Expression': {'Exclusive-OR-Expression': {'AND-Expression': {'Equality-Expression': {'Relational-Expression': {'Shift-Expression': {'Additive-Expression': {'Multiplicative-Expression': {'Cast-Expression': {'Unary-Expression': {'Postfix-Expression': {'Primary-Expression': {'NUMBER': 0}}}}}}}}}}}}}}}}}, 'END': ';'}}}}, 'RBRACE': '}'}}}}}
    #{'main': {'LBRACE': '{', 'Declaration': [{'ID': 'd'}], 'Statement': [{'=': {'ID': 'd', 'NUMBER': 4}}, {'return': {'NUMBER': 0}}], 'RBRACE': '}'}}
    findTerminalNodes(dict2)
    #print(terminalNodes)
    """
    res = [] 
    for key, val in dict2.items():
        print("Val",val) 
        if(dict2[key].__contains__('function_name')):  
                res.append(key)       
            #print(dict2)
    print(res)
    """
    """
    astTree = {}
    keyTracker = []
    astKeyTracker = []
    function_name = 'main'
    for key, value in recursive_items(dict4):
        if key == 'function-name':
            astTree.update({value:{}})
            astKeyTracker.append(value)
        elif key == 'statement':
            astTree[astKeyTracker[-1]].update({value:{}})
            astKeyTracker.append(value)
        elif key == 'NUMBER':
            print("Key Tracker",keyTracker)
            print("Val Tracker", astKeyTracker)
            astTree[function_name].update({astKeyTracker[-1]:value})
            astKeyTracker
            
            if astKeyTracker[-1] == 'Statement':
                astTree['Statement'].update('')
            
        keyTracker.append(key)
        print(key,value)
    print(astTree)
    #print(key) 
    #print("key",key, '\n',"value",value,'\n')
    #astTree = getDictionaryItems(dict2)
    #print(astTree)
    """
if __name__ == '__main__':
    main()
