from CustomError import *
from symboltable import *

"""
Program:
    translation-unit

translation-unit:
    external-declaration translation-unit'

translation-unit':
    translation-unit translation-unit'
    epsilon

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
    direct-declarator(parameter-type-list)
    direct-declarator(identifier-listopt)
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
    #declarations = parseDeclarations(tokenBuffer)
    translationUnit = parseTranslationUnit(tokenBuffer)
    #checks to make sure that all tokens have been consumed, i.e token buffer should be empty
    # if all tokens have not been consumed yet, then we need to throw an error message

    
    if not set(tokenBuffer).issubset(set(consumed)):
        #Convert the values of all the consumed tokens into string format
        #errorString = generateErrorString(tokenBuffer, isParseTreeGenerated=True)
        #raise NotAllTokensHaveBeenConsumedError(errorString,"Invalid expression")
        raise SyntaxError("Oh No")
    return translationUnit,symTable
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
    externalDeclaration = parseExternalDeclaration(tokenBuffer)
    #Updating the translatationUnitTree with the externalDeclation subtree
    translationUnitTree['Translation-Unit'].update(externalDeclaration)
    #if externalDeclaration:
    #    translationUnitTree['Translation-Unit'].update(externalDeclaration)
    #    print(tokenBuffer)
    return translationUnitTree 
"""
translation-unit':
    translation-unit translation-unit'
    epsilon
"""

def parseTranslationUnitPrime(tokenBuffer):
    """
    Descripton:
    Arguments:
    Returns:
    """
    #Initializes a dictionary object that will store the children of translation-unit-prime
    translationUnitPrimeTree = {'Translation-Unit-Prime':{}}
    if tokenBuffer:
        translationUnit = parseTranslationUnit(tokenBuffer)
        if translationUnit:
            translationUnitPrimeTree['Translation-Unit-Prime'].update(translationUnit)
    return translationUnitPrimeTree
"""
external-declaration:
    declaration
    function-definition
"""

def parseExternalDeclaration(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    
    """
    externalDeclarationTree = {'External-Declaration':{}}
    declaration = parseDeclaration(tokenBuffer)
    if declaration['Declaration'].get('END') != None:
        externalDeclarationTree['External-Declaration'].update(declaration)
    else:
        tokenBuffer = consumed + tokenBuffer
        functionDef = parseFunctionDefinition(tokenBuffer)
        if functionDef['Function-Definition'] != {}:
            externalDeclarationTree['External-Declaration'].update(functionDef)
            print(tokenBuffer)
    return externalDeclarationTree

"""
declaration:
    declaration-specifiers init-declarator-list;
    ID initital-declarator;
    epsilon
"""

def parseDeclaration(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    
    """
    
    declarationTree = {'Declaration':{}}
    declarationSpecifiers = parseDeclarationSpecifiers(tokenBuffer)
    if declarationSpecifiers['Declaration-Specifiers'] != {}:
        declarationTree['Declaration'].update(declarationSpecifiers)
        initDeclaratorList = parseInitDeclaratorList(tokenBuffer)
        if initDeclaratorList:
            declarationTree['Declaration'].update(initDeclaratorList)
            tokenToBeConsumed = tokenBuffer[0]
            if tokenToBeConsumed.type == 'END':
                declarationTree['Declaration'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
                consume(tokenToBeConsumed,tokenBuffer)
    else:
        tokenToBeConsumed = tokenBuffer[0]
        if tokenToBeConsumed.type == 'ID':
            initDecl = parseInitDeclarator(tokenBuffer)
            declarationTree['Declaration'].update(initDecl)
            tokenToBeConsumed = tokenBuffer[0]
            if tokenToBeConsumed.type == 'END':
                declarationTree['Declaration'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
                consume(tokenToBeConsumed,tokenBuffer)
    return declarationTree
"""
declaration-specifiers:
    type-specifier declaration-specifers'
"""
def parseDeclarationSpecifiers(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    declarationSpecifiers = {'Declaration-Specifiers':{}}
    tokenToBeConsumed = tokenBuffer[0]
    types = {'int', 'float','double'}
    #check if type-specifier is valid type
    if tokenToBeConsumed.type in types:
        declarationSpecifiers['Declaration-Specifiers'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        declarationSpecifiersP = parseDeclarationSpecifiersPrime(tokenBuffer)
        if declarationSpecifiersP:
            declarationSpecifiers['Declaration-Specifiers'].update(declarationSpecifiersP)
    return declarationSpecifiers
"""
declaration-specifiers':
    declaration-specifiers declaration-specifiers'
    epsilon
"""    
def parseDeclarationSpecifiersPrime(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    declarationSpecifiersPrimeDict = {'Declaration-Specifiers-Prime':{}}
    declarationSpecifers = parseDeclarationSpecifiers(tokenBuffer)
    if declarationSpecifers != {'Declaration-Specifiers':{}}:
        declarationSpecifiersPrimeDict['Declaration-Specifiers-Prime'].update(declarationSpecifers)
        declarationSpecifersP = parseDeclarationSpecifiersPrime(tokenBuffer)
        if declarationSpecifersP:
            declarationSpecifiersPrimeDict['Declaration-Specifiers-Prime'].update(declarationSpecifersP)
    return declarationSpecifiersPrimeDict
"""
init-declarator-list:
    init-declarator init-declarator-list' 
    epsilon
"""

def parseInitDeclaratorList(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    initDeclaratorListTree = {'Init-Declarator-List':{}} 
    initDeclarator = parseInitDeclarator(tokenBuffer)
    if initDeclarator:
        initDeclaratorListTree['Init-Declarator-List'].update(initDeclarator)
        initDeclaratorListPrime = parseInitDeclaratorListPrime(tokenBuffer)
        if initDeclaratorListPrime:
            initDeclaratorListTree['Init-Declarator-List'].update(initDeclaratorListPrime)
    return initDeclaratorListTree
"""
init-declarator:
    declarator
    declarator = initializer
"""
def parseInitDeclarator(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    initDeclaratorTree = {'Init-Declarator':{}}
    declarator = parseDeclarator(tokenBuffer)
    initDeclaratorTree['Init-Declarator'].update(declarator)
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.value == '=':
        initDeclaratorTree['Init-Declarator'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        initializer = parseInitializer(tokenBuffer)
        initDeclaratorTree['Init-Declarator'].update(initializer)
    return initDeclaratorTree
"""
initializer:
    assignment-expression
    { initializer-list }
    { initializer-list, } 
"""
def parseInitializer(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    initializer = {'Initializer':{}}
    assignmentExpr = parseAssignmentExpression(tokenBuffer)
    if assignmentExpr:
        initializer['Initializer'].update(assignmentExpr)
    return initializer
"""
assignment-expression:
    conditional-expression
    unary-expression assignment-operator assignment-expression
"""
def parseAssignmentExpression(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    
    """
    assignmentExpressionTree = {'Assignment-Expression':{}}
    conditionalExpr = parseConditionalExpression(tokenBuffer)
    if conditionalExpr['Conditional-Expression'] != {}:
        assignmentExpressionTree['Assignment-Expression'].update(conditionalExpr)
    else:
        unaryExpr = parseUnaryExpression(tokenBuffer)
        if unaryExpr['Unary-Expression'] != {}:
            assignmentExpressionTree['Assignment-Expression'].update(unaryExpr)
        else:
            #error handling
            pass
        tokenToBeConsumed = tokenBuffer[0]
        assignmentOperator = {'=', '*=', '/=','%=', '+=', '-=', '<<=', '>>=', '&=', '^=', '|='}
        if tokenToBeConsumed.value in assignmentOperator:
            assignmentExpressionTree['Assignment-Expression'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
            assignExpr = parseAssignmentExpression(tokenBuffer)
            if assignExpr['Assignment-Expression'] != {}:
                assignmentExpressionTree['Assignment-Expression'].update(assignExpr)
            else:
                #error handling
                pass
        else:
            #error handling
            pass
    return assignmentExpressionTree

"""
conditional-expression:
    logical-OR-expression
"""
def parseConditionalExpression(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    conditionalExprTree = {'Conditional-Expression':{}}
    logicalOrExpression = parseLogicalOrExpression(tokenBuffer)
    if logicalOrExpression:
        conditionalExprTree['Conditional-Expression'].update(logicalOrExpression)
    return conditionalExprTree

"""
logical-OR-expression;
    logical-AND-expression
"""
def parseLogicalOrExpression(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    logicalOrExpressionTree = {'Logical-OR-Expression':{}}
    logicalAndExpr = parseLogicalAndExpression(tokenBuffer)
    if logicalAndExpr:
        logicalOrExpressionTree['Logical-OR-Expression'].update(logicalAndExpr)
    return logicalOrExpressionTree

"""
logical-AND-expression:
    inclusive-OR-expression
"""
def parseLogicalAndExpression(tokenBuffer):
    """
    Descripton:
    Arguments:
    Returns:
    """
    logicalAndExprTree = {'Logical-AND-Expression':{}}
    inclusiveOrExpr = parseInclusiveOrExpression(tokenBuffer)
    if inclusiveOrExpr['Inclusive-OR-Expression'] != {}:
        logicalAndExprTree['Logical-AND-Expression'].update(inclusiveOrExpr)
    return logicalAndExprTree

"""
inclusive-OR-expression:
    exclusive-OR-expression
"""
def parseInclusiveOrExpression(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    inclusiveOrExprTree = {'Inclusive-OR-Expression':{}}
    exclusiveOrExpr = parseExclusiveOrExpression(tokenBuffer)
    if exclusiveOrExpr['Exclusive-OR-Expression'] != {}:
        inclusiveOrExprTree['Inclusive-OR-Expression'].update(exclusiveOrExpr)
    return inclusiveOrExprTree

"""
exclusive-OR-expression:
    AND-expression
"""
def parseExclusiveOrExpression(tokenBuffer):
    """
    Descripton:
    Arguments:
    Returns:
    """
    exclusiveOrExprTree = {'Exclusive-OR-Expression':{}}
    andExpression = parseAndExpression(tokenBuffer)
    if andExpression['AND-Expression'] != {}:
        exclusiveOrExprTree['Exclusive-OR-Expression'].update(andExpression)
    return exclusiveOrExprTree

"""
AND-expression:
    equality-expression
"""
def parseAndExpression(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    andExprTree = {'AND-Expression':{}}
    equalityExpression = parseEqualityExpression(tokenBuffer)
    if equalityExpression['Equality-Expression'] != {}:
        andExprTree['AND-Expression'].update(equalityExpression)
    return andExprTree

"""
equality-expression:
    relational-expression
"""
def parseEqualityExpression(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    
    """
    equalityExprTree = {'Equality-Expression':{}}
    relationalExpression = parseRelationalExpression(tokenBuffer)
    if relationalExpression['Relational-Expression'] != {}:
        equalityExprTree['Equality-Expression'].update(relationalExpression)
    return equalityExprTree

"""
relational-expression:
    shift-expression
"""
def parseRelationalExpression(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    relationalExprTree = {'Relational-Expression':{}}
    shiftExpression = parseShiftExpression(tokenBuffer)
    if shiftExpression['Shift-Expression'] != {}:
        relationalExprTree['Relational-Expression'].update(shiftExpression)
    return relationalExprTree

"""
shift-expression:
    additive-expression
"""
def parseShiftExpression(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    shiftExprTree = {'Shift-Expression':{}}
    additiveExpression = parseAdditiveExpression(tokenBuffer)
    if additiveExpression['Additive-Expression'] != {}:
        shiftExprTree['Shift-Expression'].update(additiveExpression)
    return shiftExprTree

"""
additive-expression:
    multiplicative-expression additive-expression'
"""
def parseAdditiveExpression(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    additiveExpressionTree = {'Additive-Expression':{}}
    multiplicativeExpr = parseMultiplicativeExpression(tokenBuffer)
    if multiplicativeExpr['Multiplicative-Expression'] != {}:
        additiveExpressionTree['Additive-Expression'].update(multiplicativeExpr)
        additiveExpressionPrime = parseAdditiveExpressionPrime(tokenBuffer)
        additiveExpressionTree['Additive-Expression'].update(additiveExpressionPrime)
    return additiveExpressionTree

"""   
additive-expression':
    + multiplicative-expression additive-expression'
    - multiplicatice-expression additive-expression'
    epsilon
"""       
def parseAdditiveExpressionPrime(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    additiveExpressionPrimeTree = {'Additive-Expression-Prime':{}}
    if tokenBuffer:
        tokenToBeConsumed = tokenBuffer[0]
        if tokenToBeConsumed.value == '+':
            additiveExpressionPrimeTree['Additive-Expression-Prime'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
            consume(tokenToBeConsumed, tokenBuffer)
            castExpression = parseCastExpression(tokenBuffer)
            if castExpression['Cast-Expression'] != {}:
                additiveExpressionPrimeTree['Additive-Expression-Prime'].update(castExpression)
                additiveExprPrime = parseAdditiveExpressionPrime(tokenBuffer)
                if additiveExprPrime != None:
                    additiveExpressionPrimeTree['Additive-Expression-Prime'].update(additiveExprPrime)
        elif tokenToBeConsumed.value == '-':
            additiveExpressionPrimeTree['Additive-Expression-Prime'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
            consume(tokenToBeConsumed, tokenBuffer)
            castExpression = parseCastExpression(tokenBuffer)
            if castExpression['Cast-Expression'] != {}:
                additiveExpressionPrimeTree['Additive-Expression-Prime'].update(castExpression)
                additiveExprPrime = parseAdditiveExpressionPrime(tokenBuffer)
                if additiveExprPrime != None:
                    additiveExpressionPrimeTree['Additive-Expression-Prime'].update(additiveExprPrime)
    return additiveExpressionPrimeTree

""" 
multiplicative-expression:
    cast-expression multiplicative-expresssion'
"""
def parseMultiplicativeExpression(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    multiplicativeExprTree = {'Multiplicative-Expression':{}}
    castExpr = parseCastExpression(tokenBuffer)
    if castExpr['Cast-Expression'] != {}:
        multiplicativeExprTree['Multiplicative-Expression'].update(castExpr)
    multiplicativeExprPrime = parseMultiplicativeExpressionPrime(tokenBuffer)
    if multiplicativeExprPrime != None:
        multiplicativeExprTree['Multiplicative-Expression'].update(multiplicativeExprPrime)
    return multiplicativeExprTree

"""  
multiplicative-expresssion':
    * cast-expression multiplicative-expresssion'
    / cast-expression multiplicative-expresssion'
    % cast-expression multiplicative-expresssion'
    epsilon
"""
def parseMultiplicativeExpressionPrime(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    multiplicativeExprPrimeTree = {'Multiplicative-Expression-Prime':{}}
    if tokenBuffer:
        tokenToBeConsumed = tokenBuffer[0]
        if tokenToBeConsumed.value == '*':
            multiplicativeExprPrimeTree['Multiplicative-Expression-Prime'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
            consume(tokenToBeConsumed, tokenBuffer)
            castExpression = parseCastExpression(tokenBuffer)
            if castExpression:
                multiplicativeExprPrimeTree['Multiplicative-Expression-Prime'].update(castExpression)
                multiplicativeExprPrime = parseMultiplicativeExpressionPrime(tokenBuffer)
                if multiplicativeExprPrime != None:
                    multiplicativeExprPrimeTree['Multiplicative-Expression-Prime'].update(multiplicativeExprPrime)
        elif tokenToBeConsumed.value == '/':
            multiplicativeExprPrimeTree['Multiplicative-Expression-Prime'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
            consume(tokenToBeConsumed, tokenBuffer)
            castExpression = parseCastExpression(tokenBuffer)
            if castExpression['Cast-Expression'] != {}:
                multiplicativeExprPrimeTree['Multiplicative Expression Prime'].update(castExpression)
                multiplicativeExprPrime = parseMultiplicativeExpressionPrime(tokenBuffer)
                if multiplicativeExprPrime != None:
                    multiplicativeExprPrimeTree['Multiplicative-Expression-Prime'].update(multiplicativeExprPrime)
        elif tokenToBeConsumed.value == '%':
            multiplicativeExprPrimeTree['Multiplicative-Expression-Prime'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
            consume(tokenToBeConsumed, tokenBuffer)
            castExpression = parseCastExpression(tokenBuffer)
            if castExpression['Cast-Expression'] != {}:
                multiplicativeExprPrimeTree['Multiplicative-Expression-Prime'].update(castExpression)
                multiplicativeExprPrime = parseMultiplicativeExpressionPrime(tokenBuffer)
                if multiplicativeExprPrime != None:
                    multiplicativeExprPrimeTree['Multiplicative-Expression-Prime'].update(multiplicativeExprPrime)
    return multiplicativeExprPrimeTree

"""
cast-expression:
    unary-expression
"""
def parseCastExpression(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    castExpressionTree = {'Cast-Expression':{}}
    unaryExpression = parseUnaryExpression(tokenBuffer)
    if unaryExpression:
        castExpressionTree['Cast-Expression'].update(unaryExpression)
    return castExpressionTree

"""
expression:
    assignment-expression expression-list
    epsilon
"""
def parseExpression(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    exprTree = {'Expression':{}}
    assignmentExpr = parseAssignmentExpression(tokenBuffer)
    if assignmentExpr['Assignment-Expression'] != {}:
        exprTree['Expression'].update(assignmentExpr)
    expressionList = parseExpressionList(tokenBuffer)
    if expressionList['Expression-List'] != {}:
        exprTree['Expression'].update(expressionList)
    return exprTree

"""    
expession-list:
    , expression expression-list
    epsilon
"""
def parseExpressionList(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    expressionListTree = {'Expression-List':{}}
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.type == 'COMMA':
        expressionListTree['Expression-List'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        expression = parseExpression(tokenBuffer)
        if expression:
            expressionListTree['Expression-List'].update(expression)
            expressionList = parseExpressionList(tokenBuffer)
            if expressionList:
                expressionListTree['Expression-List'].update(expressionList)
    return expressionListTree

"""
unary-expression:
    postfix-expression
"""
def parseUnaryExpression(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    unaryExpressionTree = {'Unary-Expression':{}}
    postfixExpression = parsePostfixExpression(tokenBuffer)
    if postfixExpression:
        unaryExpressionTree.update(postfixExpression)
    return unaryExpressionTree

"""
postfix-expression:
    primary-expression
"""
def parsePostfixExpression(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    postfixExpressionTree = {'Postfix-Expression':{}}
    primaryExpression = parsePrimaryExpression(tokenBuffer)
    if primaryExpression:
        postfixExpressionTree['Postfix-Expression'].update(primaryExpression)
    return postfixExpressionTree

"""
primary-expression:
    identifier
    constant
    string-literal
    ( expression )
"""    
def parsePrimaryExpression(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    primaryExpressionTree = {'Primary-Expression':{}}
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.type == 'ID':
        primaryExpressionTree['Primary-Expression'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        tokenToBeConsumed = tokenBuffer[0]
    elif tokenToBeConsumed.type == 'NUMBER':
        primaryExpressionTree['Primary-Expression'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        tokenToBeConsumed = tokenBuffer[0]
    elif tokenToBeConsumed.type == 'S_LITERAL':
        primaryExpressionTree['Primary-Expression'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        tokenToBeConsumed = tokenBuffer[0]
    elif tokenToBeConsumed.type == 'LPAREN':
        primaryExpressionTree['Primary-Expression'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        expression = parseExpression(tokenBuffer)
        if expression:
            primaryExpressionTree['Primary-Expression'].update(expression)
        tokenToBeConsumed = tokenBuffer[0]
        if tokenToBeConsumed.type == 'RPAREN':
            primaryExpressionTree['Primary-Expression'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
            consume(tokenToBeConsumed,tokenBuffer)
    return primaryExpressionTree


"""
init-declarator-list':
    , init-declarator-list init-declarator-list'
    epsilon  
"""
def parseInitDeclaratorListPrime(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    initDeclaratorListPrimeTree = {'Init-Declarator-List-Prime':{}}
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.type == 'COMMA':
        initDeclaratorList = parseInitDeclaratorList(tokenBuffer)
        if initDeclaratorList:
            initDeclaratorListPrimeTree['Init-Declarator-List-Prime'].update(initDeclaratorList)
            initDeclaratorListPrime = parseInitDeclaratorListPrime(tokenBuffer)
            if initDeclaratorListPrime:
                initDeclaratorListPrimeTree['Init-Declarator-List-Prime'].update(initDeclaratorListPrime)
    return initDeclaratorListPrimeTree
    
"""
function-definition:
    declaration-specifiers declarator declaration-list compound-statement
"""    

def parseFunctionDefinition(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    functionDefTree = {'Function-Definition':{}}
    declarationSpecifiers = parseDeclarationSpecifiers(tokenBuffer)
    if declarationSpecifiers:
        functionDefTree['Function-Definition'].update(declarationSpecifiers)
        isAFunction = True
        declarator = parseDeclarator(tokenBuffer)
        if declarator:
            functionDefTree['Function-Definition'].update(declarator)
            declarationList = parseDeclarationList(tokenBuffer)
            if declarationList:
                functionDefTree['Function-Definition'].update(declarationList)
                compoundStatement = parseCompoundStatement(tokenBuffer)
                if compoundStatement:
                    functionDefTree['Function-Definition'].update(compoundStatement)
    return functionDefTree

"""
declarator:
    pointer direct-declarator
"""
def parseDeclarator(tokenBuffer,definedInFunctionDef = False):
    """
    Description:
    Arguments:
        tokenBuffer: tokens that have yet to be consumed
        definedInFunctionDef: determines whether declarator is being defined in a function definition or not
    Returns:
    """
    declaratorTree = {'Declarator':{}}
    pointer = parsePointer(tokenBuffer)
    if pointer:
        declaratorTree['Declarator'].update(pointer)        
        directDeclarator = parseDirectDeclarator(tokenBuffer,definedInFunctionDef)
        if directDeclarator:
            declaratorTree['Declarator'].update(directDeclarator)
    return declaratorTree

"""
pointer:
    epsilon
"""
def parsePointer(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    pointerTree = {'Pointer':{}}
    return pointerTree

"""
direct-declarator:
    identifier 
    (declarator)
    direct-declarator(parameter-type-list)
    direct-declarator(identifier-type-listopt)
"""
"""
direct-declarator:
    identifer direct-declarator'
    (declarator) direct-declarator'

"""

def parseDirectDeclarator(tokenBuffer, definedInFunctionDef = False):
    """
    Description:
    Arguments:
        tokenBuffer: tokensToBeConsumed
        definedInFunctionDef: determines whether the direct-declarator is being defined in a function definition or not
    Returns:
    """
    #if current token is identifier:
    #    .......
    #elif current token is (
    #   declarator = parseDeclarator(tokenBuffer)
    #   if current token is ):
    #       .....
    #   else:
    #       error message
    directDeclaratorTree = {'Direct-Declarator':{}}
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.type == 'ID':
        directDeclaratorTree['Direct-Declarator'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.type == 'LPAREN':
        directDeclaratorTree['Direct-Declarator'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        declarator = parseDeclarator(tokenBuffer)
        if declarator:
            directDeclaratorTree['Direct-Declarator'].update(declarator)
            tokenToBeConsumed = tokenBuffer[0]
            if tokenToBeConsumed.type == 'RPAREN':
                directDeclaratorTree['Direct-Declarator'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
                consume(tokenToBeConsumed,tokenBuffer)
    return directDeclaratorTree

"""
direct-declarator':
    (parameter-type-list)
    (identifer-type-list)
    epsilon
"""
def parseDirectDeclaratorPrime(tokenBuffer, isInFunDef = False):
    """
    Description:
    Arguments:
        tokenBuffer: tokens that have yet to be consumed
        isInFunDef: determines if rule is being defined in function defintion or not
    Returns:    
        directDeclaratorPrimeTree: dict that stores children resulting from its productions
    """
    pass

"""
declaration-list:
    declaration declaration-list
    epsilon
"""
def parseDeclarationList(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    declarationListTree = {'Declaration-List':{}}
    declaration = parseDeclaration(tokenBuffer)
    tokenToBeConsumed = tokenBuffer[0]
    if declaration['Declaration'].get('END') != None:
        declarationListTree['Declaration-List'].update(declaration)
        tokenToBeConsumed = tokenBuffer[0]
        if tokenToBeConsumed.type != 'LBRACE':
            declarationList = parseDeclarationList(tokenBuffer)
            if declarationList:
                declarationListTree['Declaration-List'].update(declarationList)
    return declarationListTree

"""     
compound-statement:
    { block-item-list }
"""
def parseCompoundStatement(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    compoundStatementTree = {'Compound-Statement':{}}
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.type == 'LBRACE':
        compoundStatementTree['Compound-Statement'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        blockItemList = parseBlockItemList(tokenBuffer)
        if blockItemList['Block-Item-List'] != {}:
            compoundStatementTree['Compound-Statement'].update(blockItemList)
            tokenToBeConsumed = tokenBuffer[0]
            if tokenToBeConsumed.type == 'RBRACE':
                compoundStatementTree['Compound-Statement'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
                consume(tokenToBeConsumed,tokenBuffer)
    return compoundStatementTree

"""
block-item-list:
    block-item block-item-list
    epsilon
"""
def parseBlockItemList(tokenBuffer):
    blockItemListTree = {'Block-Item-List':{}}
    if tokenBuffer[0].type != 'RBRACE':
        blockItem = parseBlockItem(tokenBuffer)
        if blockItem['Block-Item'] != {}:
            blockItemListTree['Block-Item-List'].update(blockItem)
            blockItemList = parseBlockItemList(tokenBuffer)
            if blockItemList:
                blockItemListTree['Block-Item-List'].update(blockItemList)
    return blockItemListTree

"""
block-item:
    declaration
    statement
"""
def parseBlockItem(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    blockItemTree = {'Block-Item':{}}
    declaration = parseDeclaration(tokenBuffer)
    if declaration['Declaration'].get('END') == None:
        #backtracking
        statement = parseStatement(tokenBuffer)
        if statement:
            blockItemTree['Block-Item'].update(statement)
    else:
        blockItemTree['Block-Item'].update(declaration)
    return blockItemTree

"""
statement:
    compound-statement
    jump-statement
"""
def parseStatement(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    statementTree = {'Statement':{}}

    compoundStatement = parseCompoundStatement(tokenBuffer)
    if compoundStatement['Compound-Statement'] != {}:
        statementTree['Statement'].update(compoundStatement)
    else:    
        jumpStatement = parseJumpStatement(tokenBuffer) 
        if jumpStatement['Jump-Statement'] != {}:
            statementTree['Statement'].update(jumpStatement)
    return statementTree

"""
jump-statement:
    return expressionopt;
"""
def parseJumpStatement(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    #if currToken is return:
    #   expression = parseExpression(tokenBuffer)
    #   if currToken is ;:
    #       ......
    #   else:
    #       error message is returned    
    
    jumpStatementTree = {'Jump-Statement':{}}
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.type == 'return':
        jumpStatementTree['Jump-Statement'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        tokenToBeConsumed = tokenBuffer[0]
        if tokenToBeConsumed.type != 'END':
            expression = parseExpression(tokenBuffer)
            if expression:
                jumpStatementTree['Jump-Statement'].update(expression)
                tokenToBeConsumed = tokenBuffer[0]
                if tokenToBeConsumed.type == 'END':
                    jumpStatementTree['Jump-Statement'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
                    consume(tokenToBeConsumed,tokenBuffer)
                else:
                    raise SyntaxError("Expected a semicolon at end of statement")
        else:
            jumpStatementTree['Jump-Statement'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
            consume(tokenToBeConsumed,tokenBuffer)
        
    return jumpStatementTree

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
