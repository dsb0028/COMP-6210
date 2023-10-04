from CustomError import *
from symboltable import *
"""
Program -> Declarations

translation-unit:
    external-declaration translation-unit

external-declaration:
    declaration
    function-definition
    
declaration:
    declaration-specifiers init-declarator-list;
    epsilon

declaration-specifiers:
    type-specifier declaration-specifers'

declaration-specifiers':
    declaration-specifiers declaration-specifiers'
    epsilon
    
init-declarator-list:
    init-declarator init-declarator-list' 
    epsilon

init-declarator-list':
    , init-declarator-list init-declarator-list'
    epsilon  

init-declarator:
    declarator
    declarator = initializer

initializer:
    assignment-expression
    { initializer-list }
    { initializer-list, }    

initializer-list:
    designation initializer

designation:
    designation-list =
    epsilon

designator-list:
    designator
    desinator-list designator

designator:
    [ constant-expression ]
    . identifier

constant-expression:
    conditional-expression

assignment-expression:
    conditional-expression
    unary-expression assignment-operator assignment-expression

conditional-expression:
    logical-OR-expression

logical-OR-expression;
    logical-AND-expression

logical-AND-expression:
    inclusive-OR-expression

inclusive-OR-expression:
    exclusive-OR-expression

exclusive-OR-expression:
    AND-expression

AND-expression:
    equality-expression

equality-expression:
    relational-expression

relational-expression:
    shift-expression

shift-expression:
    additive-expression

additive-expression:
    multiplicative-expression additive-expression'
   
additive-expression':
    + multiplicative-expression additive-expression'
    - multiplicatice-expression additive-expression'
    epsilon
        
multiplicative-expression:
    cast-expression multiplicative-expresssion'
  
multiplicative-expresssion':
    * cast-expression multiplicative-expresssion'
    / cast-expression multiplicative-expresssion'
    % cast-expression multiplicative-expresssion'
    epsilon

cast-expression:
    unary-expression

expression:
    assignment-expression expression-list
    epsilon
    
expession-list:
    , expression expression-list
    epsilon

unary-expression:
    postfix-expression

postfix-expression:
    primary-expression

primary-expression:
    identifier
    constant
    string-literal
    ( expression )
    
declarator:
    pointer direct-declarator

pointer:
    epsilon

function-definition:
    declaration-specifiers declarator declaration-list compound-statement

compound-statement:
    { block-item-list }

block-item-list:
    block-item block-item-list
    epsilon

block-item:
    declaration
    statement

statement:
    compound-statement
    jump-statement

jump-statement:
    return expressionopt;
    
declaration-list:
    declaration declaration-list
    epsilon

direct-declarator:
    identifier
    (declarator)
    
Declarations => type id (args) compound-statement

args -> epsilon

compound-statement:
	{localDeclarations statements}

localDeclarations:
	type id assignment-expression; localDeclarations 
	type id; localDeclarations
    id assignment-expression; localDeclarations

    typeopt id assignment-expressionopt; localDeclarations
    epsilon

assignment-expression:
	= Expr
    epsilon

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
#internalNodeKeys = {'Expr', 'Term', 'TermP', 'Factor','ExprP'}
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
    return declarations,symTable
"""
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
    
    #print(astTree)
    #print(dictionaryItems)
"""    
# from https://stackoverflow.com/questions/39233973/get-all-keys-of-a-nested-dictionary
def getDictionaryItems(parseTree):
    for key, value in parseTree.items():
        if type(value) is dict:
            yield from getDictionaryItems(value)
        else:
            yield (key, value)
"""
translation-unit:
    external-declaration translation-unit
"""

def parseTranslationUnit(tokenBuffer):
    translationUnitTree = {'Translation Unit':{}}
    externalDeclaration = parseExternalDeclaration(tokenBuffer)
    if externalDeclaration != {}:
        translationUnitTree['Translation Unit'].update(externalDeclaration)
    translationUnit = parseTranslationUnit(tokenBuffer)
    if translationUnit != {}:
        translationUnitTree['Translation Unit'].update(translationUnit)
    return translationUnitTree 
"""
external-declaration:
    declaration
    function-definition
"""

def parseExternalDeclaration(tokenBuffer):
    externalDeclarationTree = {'External Declaration':{}}
    declaration = parseDeclaration(tokenBuffer)
    if declaration != {}:
        externalDeclarationTree['External Declaration'].update(declaration)
    functionDef = parseFunctionDefinition(tokenBuffer)
    if functionDef != {}:
        externalDeclarationTree['External Declaration'].update(functionDef)
    return externalDeclarationTree

"""
declaration:
    declaration-specifiers init-declarator-list;
    epsilon
"""

def parseDeclaration(tokenBuffer):
    declarationTree = {'Declaration':{}}
    declarationSpecifiers = parseDeclarationSpecifiers(tokenBuffer)
    if declarationSpecifiers != {}:
        declarationTree['Declaration'].update(declarationSpecifiers)
    initDeclaratorList = parseInitDeclaratorList(tokenBuffer)
    if initDeclaratorList != {}:
        declarationTree['Declaration'].update(initDeclaratorList)
    return declarationTree
"""
declaration-specifiers:
    type-specifier declaration-specifers'
"""
def parseDeclarationSpecifiers(tokenBuffer):
    declarationSpecifiers = {'Declaration Specifiers':{}}
    tokenToBeConsumed = tokenBuffer[0]
    types = {'int', 'float','double'}
    #check if type-specifier is valid type
    if tokenToBeConsumed.type in types:
        declarationSpecifiers['Declaration Specifiers'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        tokenToBeConsumed = tokenBuffer[0]
        declarationSpecifiersP = parseDeclarationSpecifiersPrime(tokenBuffer)
        declarationSpecifiers['Declaration Specifiers'].update(declarationSpecifiersP)
    else:
        #raise an error
        pass
    return declarationSpecifiers
"""
declaration-specifiers':
    declaration-specifiers declaration-specifiers'
    epsilon
"""    
def parseDeclarationSpecifiersPrime(tokenBuffer):
    declarationSpecifiersPrimeDict = {'Declaration Specifiers Prime':{}}
    declarationSpecifers = parseDeclarationSpecifiers(tokenBuffer)
    declarationSpecifiersPrimeDict['Declaration Specifiers Prime'].update(declarationSpecifers)
    declarationSpecifersP = parseDeclarationSpecifiersPrime(tokenBuffer)
    declarationSpecifiersPrimeDict['Declaration Specifiers Prime'].update(declarationSpecifersP)
    return declarationSpecifiersPrimeDict
"""
init-declarator-list:
    init-declarator init-declarator-list' 
    epsilon
"""

def parseInitDeclaratorList(tokenBuffer):
    initDeclaratorListTree = {'Init Declarator List':{}} 
    initDeclarator = parseInitDeclarator(tokenBuffer)
    return initDeclaratorListTree
"""
init-declarator:
    declarator
    declarator = initializer
"""
def parseInitDeclarator(tokenBuffer):
    initDeclaratorTree = {'Init Declarator':{}}
    declarator = parseDeclarator(tokenBuffer)
    initDeclaratorTree['Init Declarator'].update(declarator)
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.value == '=':
        initDeclaratorTree['Init Declarator'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        initializer = parseInitializer(tokenBuffer)
        initDeclaratorTree['Init Declarator'].update(initializer)
    return initDeclaratorTree
"""
initializer:
    assignment-expression
    { initializer-list }
    { initializer-list, } 
"""
def parseInitializer(tokenBuffer):
    initializer = {'Initializer':{}}
    assignmentExpr = parseAssignmentExpression(tokenBuffer)
    return initializer
"""
assignment-expression:
    conditional-expression
    unary-expression assignment-operator assignment-expression
"""
def parseAssignmentExpression(tokenBuffer):
    assignmentExpressionTree = {'Assignment Expression':{}}
    conditionalExpr = parseConditionalExpression(tokenBuffer)
    if conditionalExpr:
        assignmentExpressionTree['Assignment Expression'].update(conditionalExpr)
    else:
        unaryExpr = parseUnaryExpression(tokenBuffer)
        if unaryExpr:
            assignmentExpressionTree['Assignment Expression'].update(unaryExpr)
        tokenToBeConsumed = tokenBuffer[0]
        assignmentOperators = {}
        if tokenToBeConsumed.value in assignmentOperators:
            assignmentExpressionTree['Assignment Expression'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
            assignExpr = parseAssignmentExpression(tokenBuffer)
            if assignExpr:
                assignmentExpressionTree['Assignment Expression'].update(assignExpr)
    return assignmentExpressionTree

"""
conditional-expression:
    logical-OR-expression
"""
def parseConditionalExpression(tokenBuffer):
    conditionalExprTree = {'Conditional Expression':{}}
    logicalOrExpression = parseLogicalOrExpression(tokenBuffer)
    if logicalOrExpression:
        conditionalExprTree['Conditional Expression'].update(logicalOrExpression)
    return conditionalExprTree

"""
logical-OR-expression;
    logical-AND-expression
"""
def parseLogicalOrExpression(tokenBuffer):
    logicalOrExpressionTree = {'Logical OR Expression':{}}
    logicalAndExpr = parseLogicalAndExpression(tokenBuffer)
    if logicalAndExpr:
        logicalOrExpressionTree['Logical OR Expression'].update(logicalAndExpr)
    return logicalOrExpressionTree

"""
logical-AND-expression:
    inclusive-OR-expression
"""
def parseLogicalAndExpression(tokenBuffer):
    logicalAndExprTree = {'Logical AND Expression':{}}
    inclusiveOrExpr = parseInclusiveOrExpression(tokenBuffer)
    if inclusiveOrExpr:
        logicalAndExprTree['Logical AND Expression'].update(inclusiveOrExpr)
    return logicalAndExprTree

"""
inclusive-OR-expression:
    exclusive-OR-expression
"""
def parseInclusiveOrExpression(tokenBuffer):
    inclusiveOrExprTree = {'Inclusive OR Expression':{}}
    exclusiveOrExpr = parseExclusiveOrExpression(tokenBuffer)
    if exclusiveOrExpr:
        inclusiveOrExprTree['Inclusive OR Expression'].update(exclusiveOrExpr)
    return inclusiveOrExprTree

"""
exclusive-OR-expression:
    AND-expression
"""
def parseExclusiveOrExpression(tokenBuffer):
    exclusiveOrExprTree = {'Exclusive OR Expression':{}}
    andExpression = parseAndExpression(tokenBuffer)
    if andExpression:
        exclusiveOrExprTree['Exclusive OR Expression'].update(andExpression)
    return exclusiveOrExprTree

"""
AND-expression:
    equality-expression
"""
def parseAndExpression(tokenBuffer):
    andExprTree = {'AND Expression':{}}
    equalityExpression = parseEqualityExpression(tokenBuffer)
    if equalityExpression:
        andExprTree['AND Expression'].update(equalityExpression)
    return andExprTree

"""
equality-expression:
    relational-expression
"""
def parseEqualityExpression(tokenBuffer):
    equalityExprTree = {'Equality Expression':{}}
    relationalExpression = parseRelationalExpression(tokenBuffer)
    if relationalExpression:
        equalityExprTree['Equality Expression'].update(relationalExpression)
    return equalityExprTree

"""
relational-expression:
    shift-expression
"""
def parseRelationalExpression(tokenBuffer):
    relationalExprTree = {'Relational Expression':{}}
    shiftExpression = parseShiftExpression(tokenBuffer)
    if shiftExpression:
        relationalExprTree['Relational Expression'].update(shiftExpression)
    return relationalExprTree

"""
shift-expression:
    additive-expression
"""
def parseShiftExpression(tokenBuffer):
    shiftExprTree = {'Shift Expression':{}}
    additiveExpression = parseAdditiveExpression(tokenBuffer)
    if additiveExpression:
        shiftExprTree['Shift Expression'].update(additiveExpression)
    return shiftExprTree

"""
additive-expression:
    multiplicative-expression additive-expression'
"""
def parseAdditiveExpression(tokenBuffer):
    additiveExpressionTree = {'Additive Expression':{}}
    multiplicativeExpr = parseMultiplicativeExpression(tokenBuffer)
    additiveExpressionTree['Additive Expression'].update(multiplicativeExpr)
    additiveExpressionPrime = parseAdditiveExpressionPrime(tokenBuffer)
    additiveExpressionTree['Additive Expression'].update(additiveExpressionPrime)
    return additiveExpressionTree

"""   
additive-expression':
    + multiplicative-expression additive-expression'
    - multiplicatice-expression additive-expression'
    epsilon
"""       
def parseAdditiveExpressionPrime(tokenBuffer):
    additiveExpressionPrimeTree = {'Additive Expression Prime':{}}
    pass

""" 
multiplicative-expression:
    cast-expression multiplicative-expresssion'
"""
def parseMultiplicativeExpression(tokenBuffer):
    multiplicativeExprTree = {'Multiplicative Expression':{}}
    castExpr = parseCastExpression(tokenBuffer)
    multiplicativeExprTree['Multiplicative Expression'].update(castExpr)
    multiplicativeExprPrime = parseMultiplicativeExpressionPrime(tokenBuffer)
    multiplicativeExprTree['Multiplicative Expression'].update(multiplicativeExprPrime)
    return multiplicativeExprTree

"""  
multiplicative-expresssion':
    * cast-expression multiplicative-expresssion'
    / cast-expression multiplicative-expresssion'
    % cast-expression multiplicative-expresssion'
    epsilon
"""
def parseMultiplicativeExpressionPrime(tokenBuffer):
    pass

"""
cast-expression:
    unary-expression
"""
def parseCastExpression(tokenBuffer):
    castExpressionTree = {'Cast Expression':{}}
    unaryExpression = parseUnaryExpression(tokenBuffer)
    if unaryExpression:
        castExpressionTree['Cast Expression'].update(unaryExpression)
    return castExpressionTree

"""
expression:
    assignment-expression expression-list
    epsilon
"""
def parseExpression(tokenBuffer):
    exprTree = {'Expression':{}}
    assignmentExpr = parseAssignmentExpression(tokenBuffer)
    if assignmentExpr != {}:
        exprTree['Expression'].update(assignmentExpr)
    expressionList = parseExpressionList(tokenBuffer)
    if expressionList != {}:
        exprTree['Expression'].update(expressionList)
    return exprTree

"""    
expession-list:
    , expression expression-list
    epsilon
"""
def parseExpressionList(tokenBuffer):
    expressionListTree = {'Expression List':{}}
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.type == 'COMMA':
        expressionListTree['Expression List'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        expression = parseExpression(tokenBuffer)
        if expression:
            expressionListTree['Expression List'].update(expression)
            expressionList = parseExpressionList(tokenBuffer)
            if expressionList:
                expressionListTree['Expression List'].update(expressionList)
    return expressionListTree

"""
unary-expression:
    postfix-expression
"""
def parseUnaryExpression(tokenBuffer):
    unaryExpressionTree = {'Unary Expression':{}}
    postfixExpression = parsePostfixExpression(tokenBuffer)
    if postfixExpression:
        unaryExpressionTree.update(postfixExpression)
    return unaryExpressionTree

"""
postfix-expression:
    primary-expression
"""
def parsePostfixExpression(tokenBuffer):
    postfixExpressionTree = {'Postfix Expression':{}}
    primaryExpression = parsePrimaryExpression(tokenBuffer)
    if primaryExpression:
        postfixExpressionTree['Postfix Expression'].update(primaryExpression)
    return postfixExpressionTree

"""
primary-expression:
    identifier
    constant
    string-literal
    ( expression )
"""    
def parsePrimaryExpression(tokenBuffer):
    primaryExpressionTree = {'Primary Expression':{}}
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.type == 'ID':
        primaryExpressionTree['Primary Expression'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        tokenToBeConsumed = tokenBuffer[0]
    elif tokenToBeConsumed.type == 'NUMBER':
        primaryExpressionTree['Primary Expression'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        tokenToBeConsumed = tokenBuffer[0]
    elif tokenToBeConsumed.type == 'S_LITERAL':
        primaryExpressionTree['Primary Expression'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        tokenToBeConsumed = tokenBuffer[0]
    elif tokenToBeConsumed.type == 'LPAREN':
        primaryExpressionTree['Primary Expression'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        expression = parseExpression(tokenBuffer)
        if expression:
            primaryExpressionTree['Primary Expression'].update(expression)
        tokenToBeConsumed = tokenBuffer[0]
        if tokenToBeConsumed.type == 'RPAREN':
            primaryExpressionTree['Primary Expression'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
            consume(tokenToBeConsumed,tokenBuffer)
    return primaryExpressionTree


"""
init-declarator-list':
    , init-declarator-list init-declarator-list'
    epsilon  
"""
def parseInitDeclaratorListPrime(tokenBuffer):
    initDeclaratorListPrimeTree = {'Init Declarator List Prime':{}}
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.type == 'COMMA':
        initDeclaratorList = parseInitDeclaratorList(tokenBuffer)
        if initDeclaratorList:
            initDeclaratorListPrimeTree['Init Declarator List Prime'].update(initDeclaratorList)
            initDeclaratorListPrime = parseInitDeclaratorListPrime(tokenBuffer)
            if initDeclaratorListPrime:
                initDeclaratorListPrimeTree['Init Declarator List Prime'].update(initDeclaratorListPrime)
    return initDeclaratorListPrimeTree
    
"""
function-definition:
    declaration-specifiers declarator declaration-list compound-statement
"""    

def parseFunctionDefinition(tokenBuffer):
    functionDefTree = {'Function Definition':{}}
    declarationSpecifiers = parseDeclarationSpecifiers(tokenBuffer)
    if declarationSpecifiers:
        functionDefTree['Function Definition'].update(declarationSpecifiers)
        declarator = parseDeclarator(tokenBuffer)
        if declarator:
            functionDefTree['Function Definition'].update(declarator)
            declarationList = parseDeclarationList
            if declarationList:
                functionDefTree['Function Definition'].update(declarationList)
                compoundStatement = parseCompoundStatement(tokenBuffer)
                if compoundStatement:
                    functionDefTree['Function Definition'].update(compoundStatement)
    return functionDefTree

"""
declarator:
    pointer direct-declarator
"""
def parseDeclarator(tokenBuffer):
    declaratorTree = {'Declarator':{}}
    pointer = parsePointer(tokenBuffer)
    if pointer:
        declaratorTree['Declarator'].update(pointer)        
    directDeclarator = parseDirectDeclarator(tokenBuffer)
    if directDeclarator:
        declaratorTree['Declarator'].update(directDeclarator)
    return declaratorTree

"""
pointer:
    epsilon
"""
def parsePointer(tokenBuffer):
    pointerTree = {'Pointer':{}}
    return pointerTree

"""
direct-declarator:
    identifier
    (declarator)
"""
def parseDirectDeclarator(tokenBuffer):
    #if current token is identifier:
    #    .......
    #elif current token is (
    #   declarator = parseDeclarator(tokenBuffer)
    #   if current token is ):
    #       .....
    #   else:
    #       error message
    pass

"""
declaration-list:
    declaration declaration-list
    epsilon
"""
def parseDeclarationList(tokenBuffer):
    declarationListTree = {'Declaration List':{}}
    declaration = parseDeclaration(tokenBuffer)
    if declaration:
        declarationListTree['Declaration List'].update(declaration)
        if declarationList:
            declarationList = parseDeclarationList(tokenBuffer)
            declarationListTree['Declaration List'].update(declarationList)
    return declarationListTree

"""     
compound-statement:
    { block-item-list }
"""
def parseCompoundStatement(tokenBuffer):
    compoundStatementTree = {'Compound Statement':{}}
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.type == 'LBRACE':
        compoundStatementTree['Compound Statement'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        blockItemList = parseBlockItemList(tokenBuffer)
        if blockItemList:
            compoundStatementTree['Compound Statement'].update({blockItemList})
            consume(tokenToBeConsumed,tokenBuffer)
            tokenToBeConsumed = tokenBuffer[0]
            if tokenToBeConsumed.type == 'RBRACE':
                compoundStatementTree['Compound Statement'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
                consume(tokenToBeConsumed,tokenBuffer)
    return compoundStatementTree

"""
block-item-list:
    block-item block-item-list
    epsilon
"""
def parseBlockItemList(tokenBuffer):
    blockItemListTree = {'Block Item List':{}}
    blockItem = parseBlockItem(tokenBuffer)
    if blockItem:
        blockItemListTree['Block Item List'].update(blockItem)
        blockItemList = parseBlockItemList(tokenBuffer)
        if blockItemList:
            blockItemListTree['Block Item List'].update(blockItemList)
    return blockItemListTree

"""
block-item:
    declaration
    statement
"""
def parseBlockItem(tokenBuffer):
    blockItemTree = {'Block Item':{}}
    declaration = parseDeclaration(tokenBuffer)
    if declaration == {}:
        #backtracking
        statement = parseStatement(tokenBuffer)
        if statement:
            blockItemTree['Block Item'].update(statement)
    else:
        blockItemTree['Block Item'].update(declaration)
    return blockItemTree

"""
statement:
    compound-statement
    jump-statement
"""
def parseStatement(tokenBuffer):
    statementTree = {'Statement':{}}
    compoundStatement = parseCompoundStatement(tokenBuffer)
    if compoundStatement != {}:
        statementTree['Statement'].update(compoundStatement)
    else:
        #backtracking    
        jumpStatement = parseJumpStatement(tokenBuffer) 
        if jumpStatement:
            statementTree['Statement'].update(jumpStatement)
    return statementTree

"""
jump-statement:
    return expressionopt;
"""
def parseJumpStatement(tokenBuffer):
    #if currToken is return:
    #   expression = parseExpression(tokenBuffer)
    #   if currToken is ;:
    #       ......
    #   else:
    #       error message is returned    
    
    jumpStatementTree = {'Jump Statement':{}}
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.type == 'return':
        jumpStatementTree['Jump Statement'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        expression = parseExpression(tokenBuffer)
        if expression:
            jumpStatementTree['Jump Statement'].update(expression)
            tokenToBeConsumed = tokenBuffer[0]
            if tokenToBeConsumed.type == 'END':
                jumpStatementTree['Jump Statement'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
                consume(tokenToBeConsumed,tokenBuffer)
            else:
                raise SyntaxError("Expected a semicolon at end of statement")
    return jumpStatementTree

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
            symTable.addAFunction(tokenToBeConsumed.value)
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
            symTable.addAVariable(tokenToBeConsumed.value,consumed[-1].value,'main')
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
            localDecls = parseLocalDeclarations(tokenBuffer)
            if localDecls != {}:
                localDeclsTree['Local Declarations'].update(localDecls)
    else:
        print(tokenToBeConsumed.value)
        if tokenToBeConsumed.type == 'ID':
            localDeclsTree['Local Declarations'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
            symTable.addAVariable(tokenToBeConsumed.value,consumed[-1].value, 'main')
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
            localDecls = parseLocalDeclarations(tokenBuffer)
            if localDecls != {}:
                localDeclsTree['Local Declarations'].update(localDecls)

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
