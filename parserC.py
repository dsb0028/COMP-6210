from CustomError import *
from symboltable import *
from collections import defaultdict
import copy
import ast
"""
Program:
    translation-unit

translation-unit:
    external-declaration external-declaration'

external-declaration:
    declaration
    function-definition

external-declaration':
    external-declaration external-declaration'
    epsilon
    
declaration:
    declaration-specifiers init-declarator-list;
    ID initital-declarator;
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
  
assignment-expression:
    conditional-expression
    unary-expression assignment-operator assignment-expression

conditional-expression:
    logical-OR-expression

logical-OR-expression:
    logical-AND-expression
    logical-OR-expression || logical-AND-expression

logical-OR-expression:
    logical-AND-expression logical-OR-expression'
logical-OR-expression':
    || logical-AND-expression

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
    shift-expression relational-expression'

relational-expression':
    < shift-expression
    > shift-expression
    <= shift-expression
    >= shift-expression
    epsilon 


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
    assignment-expression 
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
    identifer direct-declarator'
    (declarator) direct-declarator'

direct-declarator':
    (parameter-type-list)
    (identifer-list)
    epsilon

parameter-type-list:
    parameter-list
    parameter-list, ...

parameter-list:
    parameter-declaration parameter-list'

parameter-declaration:
    declaration-specifers declarator

identifier-list:
    identifier identifier-list'

identifer-list':
    , identifer identifier-list'
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
"""  
# from https://stackoverflow.com/questions/39233973/get-all-keys-of-a-nested-dictionary
def getDictionaryItems(parseTree):
    dictItems = []
    for key,value in parseTree.items():
        
        if type(value) is dict:
            yield from getDictionaryItems(value)
        else:
            dictItems.append([key,value])
    return dictItems
"""
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
    externalDeclaration, astExternalDecl = parseExternalDeclaration(tokens)
    #Updating the translatationUnitTree with the externalDeclation subtree
    if externalDeclaration:
        translationUnitTree['Translation-Unit'].update(externalDeclaration)
        astTranslUnitTree.update(astExternalDecl)
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
    declaration, astDeclaration = parseDeclaration(tokens)
    if declaration['Declaration'].get('END') != None:
        externalDeclarationTree['External-Declaration'].update(declaration)
        astExternalDeclarationTree.update(astDeclaration)
    else:
        global tokenBuffer
        tokenBuffer = consumed + tokenBuffer
        astDeclarationTree.clear()
        consumed.clear()
        functionDef, astFunctionDef = parseFunctionDefinition(tokenBuffer)
        if functionDef['Function-Definition'] != {}:
            externalDeclarationTree['External-Declaration'].update(functionDef)
            astExternalDeclarationTree.update(astFunctionDef)
    return externalDeclarationTree, astExternalDeclarationTree

"""
external-declaration':
    external-declaration external-declaration'
    epsilon
"""

def parseExternalDeclarationPrime(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    externalDeclarationPrimeTree = {'External-Declaration-Prime':{}}
    if tokenBuffer:
        externalDeclaration = parseExternalDeclaration(tokenBuffer)
        if externalDeclaration:
            externalDeclarationPrimeTree['External-Declaration-Prime'].update(externalDeclaration)
            externalDeclarationPrime = parseExternalDeclarationPrime(tokenBuffer)
            if externalDeclarationPrime:
                externalDeclarationPrimeTree['External-Declaration-Prime'].update(externalDeclarationPrime)
    return externalDeclarationPrimeTree
"""
declaration:
    declaration-specifiers init-declarator-list;
    epsilon
"""

astDeclarationTree = defaultdict(list)
def parseDeclaration(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    
    """
    
    declarationTree = {'Declaration':{}}
    declarationSpecifiers, astDeclSpecs = parseDeclarationSpecifiers(tokenBuffer)
    if declarationSpecifiers['Declaration-Specifiers'] != {}:
        declarationTree['Declaration'].update(declarationSpecifiers)
        initDeclaratorList, astInitDeclaratorList = parseInitDeclaratorList(tokenBuffer)
        if initDeclaratorList:
            declarationTree['Declaration'].update(initDeclaratorList)
            #astDeclarationTree['Declaration'].append(astInitDeclaratorList)
            tokenToBeConsumed = tokenBuffer[0]
            if tokenToBeConsumed.type == 'END':
                #print(declarationSpecifiers)
                typeOfVar = declarationSpecifiers['Declaration-Specifiers']['type-specifier']
                nameOfVar = initDeclaratorList['Init-Declarator-List']['Init-Declarator']['Declarator']['Direct-Declarator']['ID']
                #print(initDeclaratorList)
                if function_name != None:
                    global symTable
                    symTable.addAVariable(nameOfVar,typeOfVar,function_name)
                declarationTree['Declaration'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
                #astDeclarationTree.update({tokenToBeConsumed.type:tokenToBeConsumed.value})
                consume(tokenToBeConsumed,tokenBuffer)
    return declarationTree, astDeclarationTree
"""
declaration-specifiers:
    type-specifier declaration-specifers'
"""
return_type = None
def parseDeclarationSpecifiers(tokenBuffer,isInFunction = False):
    """
    Description:
    Arguments:
    Returns:
    """
    declarationSpecifiers = {'Declaration-Specifiers':{}}
    astDeclSpecTree = {}
    tokenToBeConsumed = tokenBuffer[0]
    types = {'int', 'float','double'}
    #check if type-specifier is valid type
    if tokenToBeConsumed.type in types:
        if isInFunction != True:
            declarationSpecifiers['Declaration-Specifiers'].update({'type-specifier':tokenToBeConsumed.value})
        else:
            declarationSpecifiers['Declaration-Specifiers'].update({'return-type':tokenToBeConsumed.value})
            global return_type
            return_type = tokenToBeConsumed.value
        consume(tokenToBeConsumed,tokenBuffer)
        declarationSpecifiersP = parseDeclarationSpecifiersPrime(tokenBuffer)
        if declarationSpecifiersP['Declaration-Specifiers-Prime'] != {}:
            declarationSpecifiers['Declaration-Specifiers'].update(declarationSpecifiersP)
    return declarationSpecifiers, astDeclSpecTree
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
    declarationSpecifers, astDeclSpecs = parseDeclarationSpecifiers(tokenBuffer)
    if declarationSpecifers != {'Declaration-Specifiers':{}}:
        declarationSpecifiersPrimeDict['Declaration-Specifiers-Prime'].update(declarationSpecifers)
        declarationSpecifersP = parseDeclarationSpecifiersPrime(tokenBuffer)
        if declarationSpecifersP['Declaration-Specifiers-Prime'] != {}:
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
    astInitDeclaratorListTree = {}
    initDeclarator, astInitDeclarator = parseInitDeclarator(tokenBuffer)
    #print(initDeclarator)
    if initDeclarator:
        initDeclaratorListTree['Init-Declarator-List'].update(initDeclarator)
        astInitDeclaratorListTree.update(astInitDeclarator)
        initDeclaratorListPrime = parseInitDeclaratorListPrime(tokenBuffer)
        if initDeclaratorListPrime:
            initDeclaratorListTree['Init-Declarator-List'].update(initDeclaratorListPrime)
    return initDeclaratorListTree, astInitDeclaratorListTree
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
    astInitDeclaratorTree = {}
    declarator, astDeclarator = parseDeclarator(tokenBuffer)
    initDeclaratorTree['Init-Declarator'].update(declarator)
    #astInitDeclaratorTree.update(astDeclarator)
    #print(declarator,astDeclarator)
    tokenToBeConsumed = tokenBuffer[0]
    #print(declarator)
    if tokenToBeConsumed.value == '=':
        initDeclaratorTree['Init-Declarator'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        astInitDeclaratorTree.update({tokenToBeConsumed.value:{}})
        consume(tokenToBeConsumed,tokenBuffer)
        initializer, astInitializer = parseInitializer(tokenBuffer)
        initDeclaratorTree['Init-Declarator'].update(initializer)
        astInitDeclaratorTree['='].update(astDeclarator)
        astInitDeclaratorTree['='].update(astInitializer)
    else:
        astInitDeclaratorTree.update(astDeclarator)
    return initDeclaratorTree, astInitDeclaratorTree
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
    astInitalizerTree = {}
    assignmentExpr, astAssignExpr = parseAssignmentExpression(tokenBuffer)
    if assignmentExpr:
        initializer['Initializer'].update(assignmentExpr)
        astInitalizerTree.update(astAssignExpr)
    return initializer, astInitalizerTree
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
    astAssignExprTree = {}
    conditionalExpr, astCondExpr = parseConditionalExpression(tokenBuffer)
    tokenToBeConsumed = tokenBuffer[0]
    #checking to make sure that the next token to be consumed is not an assignmentOperator
    assignmentOperator = {'=', '*=', '/=','%=', '+=', '-=', '<<=', '>>=', '&=', '^=', '|='}
    if conditionalExpr['Conditional-Expression'] != {} and tokenToBeConsumed.value not in assignmentOperator:
        assignmentExpressionTree['Assignment-Expression'].update(conditionalExpr)
        #print(astCondExpr)
        if astAssignExprTree.get('='):
            astAssignExprTree['='].update(astCondExpr)
        else:
            astAssignExprTree.update(astCondExpr)
    else:
        if tokenToBeConsumed.value in assignmentOperator:
            findTerminalNodes(conditionalExpr)
            tokenBuffer.insert(0,consumed[-1])
            consumed.pop(-1)
            #print(assignmentExpressionTree)
        #backtracking is necessary
        unaryExpr, astUnaryExpr = parseUnaryExpression(tokenBuffer)
        if unaryExpr['Unary-Expression'] != {}:
            assignmentExpressionTree['Assignment-Expression'].update(unaryExpr)
            #astAssignExprTree.update(astUnaryExpr)
        else:
            #error handling
            pass
        tokenToBeConsumed = tokenBuffer[0]
        #assignmentOperator = {'=', '*=', '/=','%=', '+=', '-=', '<<=', '>>=', '&=', '^=', '|='}
        if tokenToBeConsumed.value in assignmentOperator:
            assignmentExpressionTree['Assignment-Expression'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
            astAssignExprTree.update({tokenToBeConsumed.value:{}})
            consume(tokenToBeConsumed,tokenBuffer)
            assignExpr, astAssignExpr = parseAssignmentExpression(tokenBuffer)
            if assignExpr['Assignment-Expression'] != {}:
                assignmentExpressionTree['Assignment-Expression'].update(assignExpr)
                astAssignExprTree['='].update(astUnaryExpr)
                astAssignExprTree['='].update(astAssignExpr)
                
            else:
                #error handling
                pass
        else:
            #error handling
            pass
    return assignmentExpressionTree, astAssignExprTree

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
    astConditionalExprTree = {}
    logicalOrExpression, astOrExpr = parseLogicalOrExpression(tokenBuffer)
    if logicalOrExpression['Logical-OR-Expression'] != {}:
        conditionalExprTree['Conditional-Expression'].update(logicalOrExpression)
        astConditionalExprTree.update(astOrExpr)
    return conditionalExprTree, astConditionalExprTree



"""
logical-OR-expression:
    logical-AND-expression logical-OR-expression'
"""
def parseLogicalOrExpression(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    logicalOrExpressionTree = {'Logical-OR-Expression':{}}
    astLogicalOrExpressionTree = {}
    logicalAndExpr, astLogicalAndExpr = parseLogicalAndExpression(tokenBuffer)
    if logicalAndExpr['Logical-AND-Expression'] != {}:
        logicalOrExpressionTree['Logical-OR-Expression'].update(logicalAndExpr)
        astLogicalOrExpressionTree.update(astLogicalAndExpr)
        logicalOrExprPrime, astLogicalOrExprPrime = parseLogicalOrExpressionPrime(tokenBuffer)
        if logicalOrExprPrime['Logical-OR-Expression-Prime'] != {}:
            logicalOrExpressionTree['Logical-OR-Expression'].update(logicalOrExprPrime)
            astLogicalOrExpressionTree.update(astLogicalOrExprPrime)
    return logicalOrExpressionTree, astLogicalOrExpressionTree

"""
logical-OR-expression':
    || logical-AND-expression logical-OR-expression'
    epsilon
"""
def parseLogicalOrExpressionPrime(tokenBuffer):
    """
    Description:
    Arguments:
        tokenBuffer: tokens that have yet to be consumed
    Returns:
        logicalOrExpressionPrimeTree
    """
    logicalOrExpressionPrimeTree = {'Logical-OR-Expression-Prime':{}}
    astLogicalOrExpressionPrimeTree = {}
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.value == '||':
        logicalOrExpressionPrimeTree['Logical-OR-Expression-Prime'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        logicalAndExpr = parseLogicalAndExpression(tokenBuffer)
        if logicalAndExpr['Logical-AND-Expression'] != {}:
            logicalOrExpressionPrimeTree['Logical-OR-Expression-Prime'].update(logicalAndExpr)
            logicalOrExprPrime = parseLogicalOrExpressionPrime(tokenBuffer)
            if logicalOrExprPrime['Logical-OR-Expression-Prime'] != {}:
                logicalOrExpressionPrimeTree['Logical-OR-Expression-Prime'].update(logicalOrExprPrime)
    return logicalOrExpressionPrimeTree, astLogicalOrExpressionPrimeTree

"""
logical-AND-expression:
    inclusive-OR-expression logical-AND-expression'
"""
def parseLogicalAndExpression(tokenBuffer):
    """
    Descripton:
    Arguments:
    Returns:
    """
    logicalAndExprTree = {'Logical-AND-Expression':{}}
    astLogicalAndExprTree = {}
    inclusiveOrExpr, astInclOrExpr = parseInclusiveOrExpression(tokenBuffer)
    if inclusiveOrExpr['Inclusive-OR-Expression'] != {}:
        logicalAndExprTree['Logical-AND-Expression'].update(inclusiveOrExpr)
        astLogicalAndExprTree.update(astInclOrExpr)
        logicalAndExprPrime, astLogicalAndExprPrime = parseLogicalAndExpressionPrime(tokenBuffer)
        if logicalAndExprPrime['Logical-AND-Expression-Prime'] != {}:
            logicalAndExprTree['Logical-AND-Expression'].update(logicalAndExprPrime)
            astLogicalAndExprTree.update(astLogicalAndExprPrime)
    return logicalAndExprTree, astLogicalAndExprTree

"""
logical-AND-expression':
    && inclusive-OR-expression logical-AND-expression'
"""
def parseLogicalAndExpressionPrime(tokenBuffer):
    """
    Definition:
    Arguments:
        tokenBuffer: tokens that have yet to be consumed
    Returns:
    
    """
    logicalAndExpressionPrimeTree = {'Logical-AND-Expression-Prime':{}}
    astLogicalAndExpressionPrimeTree = {}
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.value == '&&':
        logicalAndExpressionPrimeTree['Logical-AND-Expression-Prime'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        inclusiveOrExpr = parseInclusiveOrExpression(tokenBuffer)
        if inclusiveOrExpr['Inclusive-OR-Expression'] != {}:
            logicalAndExpressionPrimeTree['Logical-AND-Expression-Prime'].update(inclusiveOrExpr)
            logicalAndExprPrime = parseLogicalAndExpressionPrime(tokenBuffer)
            if logicalAndExprPrime['Logical-AND-Expression-Prime'] != {}:
                logicalAndExpressionPrimeTree['Logical-AND-Expression-Prime'].update(logicalAndExprPrime)
    return logicalAndExpressionPrimeTree, astLogicalAndExpressionPrimeTree
    pass
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
    astInclusiveOrExprTree = {}
    exclusiveOrExpr, astExclOrExpr = parseExclusiveOrExpression(tokenBuffer)
    if exclusiveOrExpr['Exclusive-OR-Expression'] != {}:
        inclusiveOrExprTree['Inclusive-OR-Expression'].update(exclusiveOrExpr)
        astInclusiveOrExprTree.update(astExclOrExpr)
    return inclusiveOrExprTree, astInclusiveOrExprTree

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
    astExclusiveOrExprTree = {}
    andExpression, astAndExpr = parseAndExpression(tokenBuffer)
    if andExpression['AND-Expression'] != {}:
        exclusiveOrExprTree['Exclusive-OR-Expression'].update(andExpression)
        astExclusiveOrExprTree.update(astAndExpr)
    return exclusiveOrExprTree, astExclusiveOrExprTree

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
    astAndExpr = {}
    equalityExpression, astEqualExpr = parseEqualityExpression(tokenBuffer)
    if equalityExpression['Equality-Expression'] != {}:
        andExprTree['AND-Expression'].update(equalityExpression)
        astAndExpr.update(astEqualExpr)
    return andExprTree, astAndExpr

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
    astEqualityExprTree = {}
    relationalExpression, astRelatExpr = parseRelationalExpression(tokenBuffer)
    if relationalExpression['Relational-Expression'] != {}:
        equalityExprTree['Equality-Expression'].update(relationalExpression)
        astEqualityExprTree.update(astRelatExpr)
    return equalityExprTree, astEqualityExprTree

"""
relational-expression:
    shift-expression relational-expression'
"""

def parseRelationalExpression(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    relationalExprTree = {'Relational-Expression':{}}
    astRelationalExprTree = {}
    shiftExpression, astShiftExpr = parseShiftExpression(tokenBuffer)
    if shiftExpression['Shift-Expression'] != {}:
        relationalExprTree['Relational-Expression'].update(shiftExpression) 
        astRelationalExprTree.update(astShiftExpr)
        relationalExpressionPrime, astRelationalExpressionPrime = parseRelationalExpressionPrime(tokenBuffer)
        if relationalExpressionPrime['Relational-Expression-Prime']:
            relationalExprTree['Relational-Expression'].update(relationalExpressionPrime)
            astRelationalExprTree.update(astRelationalExpressionPrime)
    return relationalExprTree, astRelationalExprTree

"""
relational-expression':
    < shift-expression
    > shift-expression
    <= shift-expression
    >= shift-expression
    epsilon

"""

def parseRelationalExpressionPrime(tokenBuffer):
    """
    Description:
    Arguments:
        tokenBuffer: tokens that have yet to be consumed
    Returns:
        relationalExpessionPrimeTree:
    """
    relationalExpressionPrimeTree = {'Relational-Expression-Prime':{}}
    astRelationalExpressionPrimeTree = {}
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.value == '<':
        relationalExpressionPrimeTree['Relational-Expression-Prime'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        astRelationalExpressionPrimeTree.update({tokenToBeConsumed.value:{}})
        consume(tokenToBeConsumed,tokenBuffer)
        shiftExpression = parseShiftExpression(tokenBuffer)
        if shiftExpression['Shift-Expression'] != {}:
            relationalExpressionPrimeTree['Relational-Expression-Prime'].update(shiftExpression)
    elif tokenToBeConsumed.value == '>':
        relationalExpressionPrimeTree['Relational-Expression-Prime'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        shiftExpression = parseShiftExpression(tokenBuffer)
        if shiftExpression['Shift-Expression'] != {}:
            relationalExpressionPrimeTree['Relational-Expression-Prime'].update(shiftExpression)
    elif tokenToBeConsumed.value == '>=':
        relationalExpressionPrimeTree['Relational-Expression-Prime'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        shiftExpression = parseShiftExpression(tokenBuffer)
        if shiftExpression['Shift-Expression'] != {}:
            relationalExpressionPrimeTree['Relational-Expression-Prime'].update(shiftExpression)
    elif tokenToBeConsumed.value == '<=':
        relationalExpressionPrimeTree['Relational-Expression-Prime'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        shiftExpression = parseShiftExpression(tokenBuffer)
        if shiftExpression['Shift-Expression'] != {}:
            relationalExpressionPrimeTree['Relational-Expression-Prime'].update(shiftExpression)
    return relationalExpressionPrimeTree, astRelationalExpressionPrimeTree


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
    astShiftExprTree = {}
    additiveExpression, astAddExpr = parseAdditiveExpression(tokenBuffer)
    if additiveExpression['Additive-Expression'] != {}:
        shiftExprTree['Shift-Expression'].update(additiveExpression)
        astShiftExprTree.update(astAddExpr)
        #print("Shift",astShiftExprTree)
    return shiftExprTree, astShiftExprTree

"""
additive-expression:
    multiplicative-expression additive-expression'
"""
#math_op = None
def parseAdditiveExpression(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    additiveExpressionTree = {'Additive-Expression':{}}
    #Initalzize a dictionary object to store children of additive-expression
    astAdditiveExpressionTree = {}
    #operands = []
    operators = ['+','-']
    #math_op = None
    #returns the resulting mutliplicative expression for full parse tree and ast
    multiplicativeExpr, astMultExpr = parseMultiplicativeExpression(tokenBuffer)
    #if there is a mutliplicatice expression, update the parse tree
    if multiplicativeExpr['Multiplicative-Expression'] != {}:
        additiveExpressionTree['Additive-Expression'].update(multiplicativeExpr)
        astAdditiveExpressionTree.update(astMultExpr)
        #print("MULT",astMultExpr)
        #print(math_op)
        if tokenBuffer[0].value in operators:
            #math_op = tokenBuffer[0].value
            #print("wow",math_op)
            pass
        additiveExpressionPrime, astAdditiveExpressionPrime = parseAdditiveExpressionPrime(tokenBuffer)
        if additiveExpressionPrime['Additive-Expression-Prime'] != {}:
            additiveExpressionTree['Additive-Expression'].update(additiveExpressionPrime)
            print(astAdditiveExpressionPrime)
            astAdditiveExpressionTree.update(astAdditiveExpressionPrime)         
    return additiveExpressionTree, astAdditiveExpressionTree

"""   
additive-expression':
    + multiplicative-expression additive-expression'
    - multiplicatice-expression additive-expression'
    epsilon
"""       


#astAdditiveExpressionPrimeTree = defaultdict(list)
#math_op = None
def parseAdditiveExpressionPrime(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    additiveExpressionPrimeTree = {'Additive-Expression-Prime':{}}
    astAdditiveExpressionPrimeTree = {}
    if tokenBuffer:
        tokenToBeConsumed = tokenBuffer[0]
        if tokenToBeConsumed.value in ['+','-']:
            math_op = tokenToBeConsumed.value
        if tokenToBeConsumed.value == '+':
            operands = []
            additiveExpressionPrimeTree['Additive-Expression-Prime'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
            astAdditiveExpressionPrimeTree.update({tokenToBeConsumed.value:[]})
            #print(astAdditiveExpressionPrimeTree)
            consume(tokenToBeConsumed, tokenBuffer)
            multiplicativeExprTree, astMultExprTree = parseMultiplicativeExpression(tokenBuffer)
            
            if multiplicativeExprTree['Multiplicative-Expression'] != {}:
                additiveExpressionPrimeTree['Additive-Expression-Prime'].update(multiplicativeExprTree)
                astAdditiveExpressionPrimeTree[tokenToBeConsumed.value].append(astMultExprTree)
                #operators.append(astMultExprTree)
                #print(astMultExprTree)
                additiveExprPrime, astAddPrime = parseAdditiveExpressionPrime(tokenBuffer)
                #print(math_op)
                if additiveExprPrime['Additive-Expression-Prime'] != {}:
                    additiveExpressionPrimeTree['Additive-Expression-Prime'].update(additiveExprPrime)
                    astAdditiveExpressionPrimeTree[tokenToBeConsumed.value].append(astAddPrime)
        elif tokenToBeConsumed.value == '-':
                additiveExpressionPrimeTree['Additive-Expression-Prime'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
                astAdditiveExpressionPrimeTree.update({tokenToBeConsumed.value:[]})
                consume(tokenToBeConsumed, tokenBuffer)
                multiplicativeExprTree, astMultExprTree = parseMultiplicativeExpression(tokenBuffer)
                if multiplicativeExprTree['Multiplicative-Expression'] != {}:
                    additiveExpressionPrimeTree['Additive-Expression-Prime'].update(multiplicativeExprTree)
                    astAdditiveExpressionPrimeTree[tokenToBeConsumed.value].append(astMultExprTree)
                    additiveExprPrime, astAddPrime = parseAdditiveExpressionPrime(tokenBuffer)
                    if additiveExprPrime['Additive-Expression-Prime'] != {}:
                        additiveExpressionPrimeTree['Additive-Expression-Prime'].update(additiveExprPrime)
                        astAdditiveExpressionPrimeTree[tokenToBeConsumed.value].append(astAddPrime)
    return additiveExpressionPrimeTree, astAdditiveExpressionPrimeTree

""" 
multiplicative-expression:
    cast-expression multiplicative-expresssion'
"""
#math_op = None
def parseMultiplicativeExpression(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    multiplicativeExprTree = {'Multiplicative-Expression':{}}
    astMultiplicativeExprTree = {}
    castExpr, astCastExpr = parseCastExpression(tokenBuffer)
    if tokenBuffer[0].value in ['+','-','*','/','%']:
        #global math_op
        #math_op = tokenBuffer[0].value
        pass
    if castExpr['Cast-Expression'] != {}:
        multiplicativeExprTree['Multiplicative-Expression'].update(castExpr)
        astMultiplicativeExprTree.update(astCastExpr)
        multiplicativeExprPrime, astMultiplicativeExprPrime = parseMultiplicativeExpressionPrime(tokenBuffer)
        if multiplicativeExprPrime['Multiplicative-Expression-Prime'] != {}:
            multiplicativeExprTree['Multiplicative-Expression'].update(multiplicativeExprPrime)
            astMultiplicativeExprTree.update(astMultiplicativeExprPrime)
    return multiplicativeExprTree, astMultiplicativeExprTree

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
    astMultiplicativeExprPrimeTree = {}
    if tokenBuffer:
        tokenToBeConsumed = tokenBuffer[0]
        if tokenToBeConsumed.value == '*':
            multiplicativeExprPrimeTree['Multiplicative-Expression-Prime'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
            astMultiplicativeExprPrimeTree.update({tokenToBeConsumed.value:[]})
            consume(tokenToBeConsumed, tokenBuffer)
            castExpression, astCastExpr = parseCastExpression(tokenBuffer)
            if castExpression['Cast-Expression'] != {}:
                multiplicativeExprPrimeTree['Multiplicative-Expression-Prime'].update(castExpression)
                astMultiplicativeExprPrimeTree[tokenToBeConsumed.value].append(astCastExpr)
                multiplicativeExprPrime, astMultiplicativeExprPrime = parseMultiplicativeExpressionPrime(tokenBuffer)
                if multiplicativeExprPrime['Multiplicative-Expression-Prime'] != {}:
                    multiplicativeExprPrimeTree['Multiplicative-Expression-Prime'].update(multiplicativeExprPrime)
                    astMultiplicativeExprPrimeTree[tokenToBeConsumed.value].append(astMultiplicativeExprPrime)
        elif tokenToBeConsumed.value == '/':
            multiplicativeExprPrimeTree['Multiplicative-Expression-Prime'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
            astMultiplicativeExprPrimeTree.update({tokenToBeConsumed.value:[]})
            consume(tokenToBeConsumed, tokenBuffer)
            castExpression,astCastExpr = parseCastExpression(tokenBuffer)
            if castExpression['Cast-Expression'] != {}:
                multiplicativeExprPrimeTree['Multiplicative-Expression-Prime'].update(castExpression)
                astMultiplicativeExprPrimeTree[tokenToBeConsumed.value].append(astCastExpr)
                multiplicativeExprPrime, astMultiplicativeExprPrime = parseMultiplicativeExpressionPrime(tokenBuffer)
                if multiplicativeExprPrime['Multiplicative-Expression-Prime'] != {}:
                    multiplicativeExprPrimeTree['Multiplicative-Expression-Prime'].update(multiplicativeExprPrime)
                    astMultiplicativeExprPrimeTree[tokenToBeConsumed.value].append(astMultiplicativeExprPrime)
        elif tokenToBeConsumed.value == '%':
            multiplicativeExprPrimeTree['Multiplicative-Expression-Prime'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
            consume(tokenToBeConsumed, tokenBuffer)
            castExpression = parseCastExpression(tokenBuffer)
            if castExpression['Cast-Expression'] != {}:
                multiplicativeExprPrimeTree['Multiplicative-Expression-Prime'].update(castExpression)
                multiplicativeExprPrime = parseMultiplicativeExpressionPrime(tokenBuffer)
                if multiplicativeExprPrime['Multiplicative-Expression-Prime'] != {}:
                    multiplicativeExprPrimeTree['Multiplicative-Expression-Prime'].update(multiplicativeExprPrime)
    return multiplicativeExprPrimeTree, astMultiplicativeExprPrimeTree

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
    astCastExpressionTree = {}
    unaryExpression, astUnaryExpr = parseUnaryExpression(tokenBuffer)
    if unaryExpression['Unary-Expression'] != {}:
        castExpressionTree['Cast-Expression'].update(unaryExpression)
        astCastExpressionTree.update(astUnaryExpr) 
    return castExpressionTree, astCastExpressionTree

"""
expression:
    assignment-expression
    epsilon
"""
def parseExpression(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    exprTree = {'Expression':{}}
    astExprTree = {}
    assignmentExpr, astAssignExpr = parseAssignmentExpression(tokenBuffer)
    if assignmentExpr['Assignment-Expression'] != {}:
        exprTree['Expression'].update(assignmentExpr)
        astExprTree.update(astAssignExpr)
    return exprTree, astExprTree

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
    astUnaryExpressionTree = {}
    postfixExpression, astPostfixExpr = parsePostfixExpression(tokenBuffer)
    if postfixExpression['Postfix-Expression'] != {}:
        unaryExpressionTree['Unary-Expression'].update(postfixExpression)
        astUnaryExpressionTree.update(astPostfixExpr)
    return unaryExpressionTree, astUnaryExpressionTree

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
    astPostfixExpressionTree = {}
    primaryExpression, astPrimExpr = parsePrimaryExpression(tokenBuffer)
    if primaryExpression['Primary-Expression'] != {}:
        postfixExpressionTree['Postfix-Expression'].update(primaryExpression)
        astPostfixExpressionTree.update(astPrimExpr)
    return postfixExpressionTree, astPostfixExpressionTree

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
    astPrimExprTree = {}
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.type == 'ID':
        primaryExpressionTree['Primary-Expression'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        astPrimExprTree.update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        tokenToBeConsumed = tokenBuffer[0]
    elif tokenToBeConsumed.type == 'NUMBER':
        primaryExpressionTree['Primary-Expression'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        astPrimExprTree.update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        tokenToBeConsumed = tokenBuffer[0]
    elif tokenToBeConsumed.type == 'S_LITERAL':
        primaryExpressionTree['Primary-Expression'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        tokenToBeConsumed = tokenBuffer[0]
    elif tokenToBeConsumed.type == 'LPAREN':
        primaryExpressionTree['Primary-Expression'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        expression,astExpr = parseExpression(tokenBuffer)
        if expression:
            primaryExpressionTree['Primary-Expression'].update(expression)
            astPrimExprTree.update(astExpr)
        tokenToBeConsumed = tokenBuffer[0]
        if tokenToBeConsumed.type == 'RPAREN':
            primaryExpressionTree['Primary-Expression'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
            consume(tokenToBeConsumed,tokenBuffer)
    return primaryExpressionTree, astPrimExprTree


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
function_name = None
def parseFunctionDefinition(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    functionDefTree = {'Function-Definition':{}}
    astFunctionDefTree = {}
    declarationSpecifiers, declSpecs = parseDeclarationSpecifiers(tokenBuffer,isInFunction = True)
    if declarationSpecifiers:
        functionDefTree['Function-Definition'].update(declarationSpecifiers)
        #astFunctionDefTree.update(declSpecs)
        declarator, astDeclarator = parseDeclarator(tokenBuffer,definedInFunctionDef = True)
        if declarator:
            #function = declarator['Declarator']['Direct-Declarator']['ID']
            #return_type = declarationSpecifiers['Declaration-Specifiers']['type-specifier']
            #global symTable
            #symTable.addAFunction(function,return_type)
            #findTerminalNodes(declarator)
            #print(terminalNodes)
            """
            if declarator['Declarator']['Direct-Declarator']['Direct-Declarator-Prime'].get('Parameter-Type-List'):
                if declarator['Declarator']['Direct-Declarator']['Direct-Declarator-Prime']['Parameter-Type-List']['Parameter-List']['Parameter-Declaration'].get('Declaration-Specifiers') != None:
                    varTypeToAddToSymbolTable = declarator['Declarator']['Direct-Declarator']['Direct-Declarator-Prime']['Parameter-Type-List']['Parameter-List']['Parameter-Declaration']['Declaration-Specifiers']['type-specifier']
                    varValueToAddToSymbolTable = declarator['Declarator']['Direct-Declarator']['Direct-Declarator-Prime']['Parameter-Type-List']['Parameter-List']['Parameter-Declaration']['Declarator']['Direct-Declarator']['ID']
                    #global symTable
                    symTable.addAVariable(varValueToAddToSymbolTable,varTypeToAddToSymbolTable,function)
            """        
            #terminalNodes.pop(0)
            #terminalNodes.pop(0)
            #print(terminalNodes)    
            functionDefTree['Function-Definition'].update(declarator)
            astFunctionDefTree = {function_name:astDeclarator}
            declarationList = parseDeclarationList(tokenBuffer)
            if declarationList['Declaration-List'] != {}:
                functionDefTree['Function-Definition'].update(declarationList)
            compoundStatement, astCompStmt = parseCompoundStatement(tokenBuffer)
            if compoundStatement:
                functionDefTree['Function-Definition'].update(compoundStatement)
                astFunctionDefTree[function_name].update(astCompStmt)
    return functionDefTree, astFunctionDefTree

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
    astDeclaratorTree = {}   
    pointer = parsePointer(tokenBuffer)
    if pointer['Pointer'] != {}:
        declaratorTree['Declarator'].update(pointer)        
    directDeclarator, astDirectDeclarator = parseDirectDeclarator(tokenBuffer,definedInFunctionDef)
    if directDeclarator['Direct-Declarator'] != {}:
        declaratorTree['Declarator'].update(directDeclarator)
        astDeclaratorTree.update(astDirectDeclarator)
    return declaratorTree, astDeclaratorTree

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
    identifer direct-declarator'
    (declarator) direct-declarator'

"""
function_name = None
def parseDirectDeclarator(tokenBuffer, definedInFunctionDef = False):
    """
    Description:
    Arguments:
        tokenBuffer: tokensToBeConsumed
        definedInFunctionDef: determines whether the direct-declarator is being defined in a function definition or not
    Returns:
    """
    directDeclaratorTree = {'Direct-Declarator':{}}
    astDirectDeclarator = {}
    tokenToBeConsumed = tokenBuffer[0]
    if definedInFunctionDef == False:
        if tokenToBeConsumed.type == 'LPAREN':
            directDeclaratorTree['Direct-Declarator'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
            consume(tokenToBeConsumed,tokenBuffer)
            declarator = parseDeclarator(tokenBuffer)
            if declarator['Declarator'] != {}:
                directDeclaratorTree['Direct-Declarator'].update(declarator)
                tokenToBeConsumed = tokenBuffer[0]
                if tokenToBeConsumed.type == 'RPAREN':
                    directDeclaratorTree['Direct-Declarator'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
                    consume(tokenToBeConsumed,tokenBuffer)
                    directDeclaratorP = parseDirectDeclaratorPrime(tokenBuffer,definedInFunctionDef)
                    if directDeclaratorP['Direct-Declarator-Prime'] != {}:
                        directDeclaratorTree['Direct-Declarator'].update(directDeclaratorP)        
                else:
                    #error handling
                    pass
        elif tokenToBeConsumed.type == 'ID':
                directDeclaratorTree['Direct-Declarator'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
                astDirectDeclarator.update({tokenToBeConsumed.type:tokenToBeConsumed.value})
                consume(tokenToBeConsumed,tokenBuffer)
                directDeclaratorP, astDirectDeclaratorPrime = parseDirectDeclaratorPrime(tokenBuffer,definedInFunctionDef)
                if directDeclaratorP['Direct-Declarator-Prime'] != {}:
                    directDeclaratorTree['Direct-Declarator'].update(directDeclaratorP)
                    astDirectDeclarator.update(astDirectDeclaratorPrime)      
    else:
        if tokenToBeConsumed.type == 'ID':
            directDeclaratorTree['Direct-Declarator'].update({'function-name':tokenToBeConsumed.value})
            if return_type != None:
                global function_name
                function_name = tokenToBeConsumed.value
                #astDirectDeclarator.update({function_name:{}})
                global symTable
                symTable.addAFunction(function_name,return_type)
            consume(tokenToBeConsumed,tokenBuffer)
            directDeclaratorP, astDirectDeclaratorPrime = parseDirectDeclaratorPrime(tokenBuffer,definedInFunctionDef)
            if directDeclaratorP['Direct-Declarator-Prime'] != {}:
                directDeclaratorTree['Direct-Declarator'].update(directDeclaratorP)
                #print("Function_Name", astDirectDeclarator[function_name])
                astDirectDeclarator.update(astDirectDeclaratorPrime)
    return directDeclaratorTree, astDirectDeclarator

"""
direct-declarator':
    (parameter-type-list)
    (identifer-list)
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
    directDeclaratorPrimeTree = {'Direct-Declarator-Prime':{}}
    astDirectDeclaratorPrimeTree = {}
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.type == 'LPAREN':
        directDeclaratorPrimeTree['Direct-Declarator-Prime'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        parameterTypeList, astParameterTypeList = parseParameterTypeList(tokenBuffer)
        if parameterTypeList['Parameter-Type-List']['Parameter-List']['Parameter-Declaration'].get('Declaration-Specifiers') == None:
            if parameterTypeList['Parameter-Type-List']['Parameter-List']['Parameter-Declaration'].get('Declarator') != None:
                identifierList = parseIdentifierList(tokenBuffer)
                if identifierList['Identifier-List']:
                    directDeclaratorPrimeTree['Direct-Declarator-Prime'].update(identifierList)
                    tokenToBeConsumed = tokenBuffer[0]
                    if tokenToBeConsumed.type == 'RPAREN':
                        directDeclaratorPrimeTree['Direct-Declarator-Prime'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
                        consume(tokenToBeConsumed,tokenBuffer)
                    else:
                        #error handling
                        pass
            else:
                directDeclaratorPrimeTree['Direct-Declarator-Prime'].update(parameterTypeList)
                tokenToBeConsumed = tokenBuffer[0]
                if tokenToBeConsumed.type == 'RPAREN':
                    directDeclaratorPrimeTree['Direct-Declarator-Prime'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
                    consume(tokenToBeConsumed,tokenBuffer)
        else:
            directDeclaratorPrimeTree['Direct-Declarator-Prime'].update(parameterTypeList)
            astDirectDeclaratorPrimeTree.update(astParameterTypeList)
            tokenToBeConsumed = tokenBuffer[0]
            if tokenToBeConsumed.type == 'RPAREN':
                    directDeclaratorPrimeTree['Direct-Declarator-Prime'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
                    consume(tokenToBeConsumed,tokenBuffer)
            else:
                #error handling
                pass
    else:
        #error handling 
        pass
    return directDeclaratorPrimeTree, astDirectDeclaratorPrimeTree

"""
if the list terminates with an ellipsis (, ...),
no information about the number or types
of the parameters after the comma is supplied.

parameter-type-list:
    parameter-list
    parameter-list, ...
"""

def parseParameterTypeList(tokenBuffer):
    """
    Description:
    Arguments:
        tokenBuffer: tokens that have yet to be consumed
    Returns:
        parameterTypeListTree: dict object that contains the children resulting from parameter-type-list productions
    """
    parameterTypeListTree = {'Parameter-Type-List':{}}
    astParameterTypeListTree = {}
    parameterList, astParameterList = parseParameterList(tokenBuffer)
    if parameterList:
        parameterTypeListTree['Parameter-Type-List'].update(parameterList)
        astParameterTypeListTree.update(astParameterList)
    return parameterTypeListTree, astParameterTypeListTree

"""
parameter-list:
    parameter-declaration parameter-list'
"""

def parseParameterList(tokenBuffer):
    """
    Description:
    Arguments:
        tokenBuffer: tokens that have yet to be consumed
    Returns:
        parameterListTree: dict object that contains the children resulting from parameter-list productions
    """
    parameterListTree = {'Parameter-List':{}}
    astParameterListTree = {}
    parameterDeclaration, astParamDeclTree = parseParameterDeclaration(tokenBuffer)
    if parameterDeclaration:
        #print(parameterDeclaration)
        parameterListTree['Parameter-List'].update(parameterDeclaration)
        astParameterListTree.update(astParamDeclTree)
        parameterListPrime = parseParameterListPrime(tokenBuffer)
        if parameterListPrime['Parameter-List-Prime'] != {}:
            parameterListTree['Parameter-List'].update(parameterListPrime)
    return parameterListTree, astParameterListTree


"""
parameter-list':
    , parameter-declaration parameter-list'
    epsilon
"""

def parseParameterListPrime(tokenBuffer):
    """
    Description:
    Arguments:
        tokenBuffer: tokens that have yet to be consumed
    Returns:
        parameterListPrimeTree: dict object that contains the children resulting from parameter-list' productions
    """
    parameterListPrimeTree = {'Parameter-List-Prime':{}}
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.type == 'COMMA':
        parameterListPrimeTree['Parameter-List-Prime'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        parameterDeclaration = parseParameterDeclaration(tokenBuffer)
        if parameterDeclaration:
            parameterListPrimeTree['Parameter-List-Prime'].update(parameterDeclaration)
            parameterListPrime = parseParameterListPrime(tokenBuffer)
            if parameterListPrime['Parameter-List-Prime'] != {}:
                parameterListPrimeTree['Parameter-List-Prime'].update(parameterListPrime)
    return parameterListPrimeTree

"""
parameter-declaration:
    declaration-specifers declarator
"""
def parseParameterDeclaration(tokenBuffer):
    """
    Description:
    Arguments:
        tokenBuffer: tokens that have yet to be consumed
    Returns:
        parameterDeclarationTree: dict object that contains the children resulting from parameter-declaration productions
    """
    parameterDeclarationTree = {'Parameter-Declaration':{}}
    astParameterDeclarationTree = {}
    declarationSpecifiers, astDeclSpecs = parseDeclarationSpecifiers(tokenBuffer)
    if declarationSpecifiers['Declaration-Specifiers'] != {}:
        parameterDeclarationTree['Parameter-Declaration'].update(declarationSpecifiers)
        astParameterDeclarationTree.update(astDeclSpecs)
        declarator = parseDeclarator(tokenBuffer)
        if declarator['Declarator'] != {}:   
            parameterDeclarationTree['Parameter-Declaration'].update(declarator)
            varTypeToAddToSymbolTable = declarationSpecifiers['Declaration-Specifiers']['type-specifier']
            varValueToAddToSymbolTable = declarator['Declarator']['Direct-Declarator']['ID']
            global symTable
            if function_name != None:
                symTable.addAVariable(varValueToAddToSymbolTable,varTypeToAddToSymbolTable,function_name)
    return parameterDeclarationTree, astParameterDeclarationTree
"""
identifier-list:
    identifier identifier-list'
"""

def parseIdentifierList(tokenBuffer):
    """
    Description:
    Arguments:
        tokenBuffer: tokens that havce yet to be consumed
    Returns:
        identifierListTree: dict object that contains the children resulting from identifier-list productions
    """
    identifierListTree = {'Identifier-List':{}}
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.type == 'ID':
        identifierListTree['Identifier-List'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        identifierListPrime = parseIdentifierListPrime(tokenBuffer)
        if identifierListPrime:
            identifierListTree['Identifier-List'].update(identifierListPrime)
    return identifierListTree

"""
identifer-list':
    , identifer identifier-list'
"""
def parseIdentifierListPrime(tokenBuffer):
    """
    Description:
    Arguments:
        tokenBuffer: tokens that have yet to be consumed
    Returns:
        identifierListPrimeTree: dict object that contains the children resulting from identifier-list-prime productions
    """
    identifierListPrimeTree = {'Identifier-List-Prime':{}}
    tokenToBeConsumed = tokenBuffer[0] 
    if tokenToBeConsumed.type == 'COMMA':
        identifierListPrimeTree['Identifier-List-Prime'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed, tokenBuffer)
        tokenToBeConsumed = tokenBuffer[0]
        if tokenToBeConsumed.type == 'ID':
            identifierListPrimeTree['Identifier-List-Prime'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
            consume(tokenToBeConsumed,tokenBuffer)
            identifierListPrime = parseIdentifierListPrime(tokenBuffer)
            if identifierListPrime:
                identifierListPrimeTree['Identifier-List-Prime'].update(identifierListPrime)
    return identifierListPrimeTree

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
    declaration, astDeclaration = parseDeclaration(tokenBuffer)
    tokenToBeConsumed = tokenBuffer[0]
    if declaration['Declaration'].get('END') != None:
        declarationListTree['Declaration-List'].update(declaration)
        tokenToBeConsumed = tokenBuffer[0]
        if tokenToBeConsumed.type != 'LBRACE':
            declarationList = parseDeclarationList(tokenBuffer)
            if declarationList['Declaration-List'] != {}:
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
    astCompoundStatementTree = {}
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.type == 'LBRACE':
        compoundStatementTree['Compound-Statement'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        astCompoundStatementTree.update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
        blockItemList, astBlockItemList = parseBlockItemList(tokenBuffer)
        if blockItemList['Block-Item-List'] != {}:
            compoundStatementTree['Compound-Statement'].update(blockItemList)
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
def parseBlockItemList(tokenBuffer):
    blockItemListTree = {'Block-Item-List':{}}
    #astBlockItemListTree = {}
    astBlockItemListTree = defaultdict(list)
    if tokenBuffer[0].type != 'RBRACE':
        blockItem, astBlockItem = parseBlockItem(tokenBuffer)
        if blockItem['Block-Item'] != {}:
            blockItemListTree['Block-Item-List'].update(blockItem)
            astBlockItemListTree.update(astBlockItem)
            blockItemList, astBlockItemList = parseBlockItemList(tokenBuffer)
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
def parseBlockItem(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    blockItemTree = {'Block-Item':{}}
    astBlockItemTree = {}
    declaration, astDeclaration = parseDeclaration(tokenBuffer)
    if declaration['Declaration'].get('END') == None:
        statement,astStmt = parseStatement(tokenBuffer)
        if statement:
            blockItemTree['Block-Item'].update(statement)
            astBlockItemTree.update(astStmt)
    else:
        #print(declaration)
        blockItemTree['Block-Item'].update(declaration)
        astBlockItemTree.update(astDeclaration)
    return blockItemTree, astBlockItemTree

"""
statement:
    compound-statement
    jump-statement
    expression-statement
    selection-statement
"""

astStmtTree = defaultdict(list)
def parseStatement(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    """
    statementTree = {'Statement':{}}
    #astStmtTree = defaultdict(list)
    compoundStatement, astCompoundStmt = parseCompoundStatement(tokenBuffer)
    if compoundStatement['Compound-Statement'] != {}:
        statementTree['Statement'].update(compoundStatement)
        global astStmtTree
        astStmtTree['Statement'].append(astCompoundStmt)
    else:    
        jumpStatement, astJumpStmt = parseJumpStatement(tokenBuffer) 
        if jumpStatement['Jump-Statement'] != {}:
            statementTree['Statement'].update(jumpStatement)
            astStmtTree['Statement'].append(astJumpStmt)
        else:
            exprStmt,astExprStmt = parseExpressionStatement(tokenBuffer)
            if exprStmt['Expression-Statement'] != {}:
                statementTree['Statement'].update(exprStmt)
                #astStmtTree.setdefault('Expression-Statement', []).append(astExprStmt)
                astStmtTree['Statement'].append(astExprStmt)
                #print("EXPR",astExprStmt)
            else:
                selectionStatement = parseSelectionStatement(tokenBuffer)
                if selectionStatement['Selection-Statement'] != {}:
                    statementTree['Statement'].update(selectionStatement)
                    astStmtTree.update(selectionStatement)
    return statementTree, astStmtTree

"""
expression-statement:
    expressionopt;
"""
def parseExpressionStatement(tokenBuffer):
    exprStmtTree = {'Expression-Statement':{}}
    astExprStmt = {}
    expression,astExpr = parseExpression(tokenBuffer)
    if expression['Expression'] != {}:
        exprStmtTree['Expression-Statement'].update(expression)
        #astExprStmt.setdefault('Expression-Statement', []).append(astExpr)
        astExprStmt.update(astExpr)
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.type == 'END':
        exprStmtTree['Expression-Statement'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        consume(tokenToBeConsumed,tokenBuffer)
    return exprStmtTree, astExprStmt

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
   
    jumpStatementTree = {'Jump-Statement':{}}
    astJumpStmtTree = {}
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.type == 'return':
        jumpStatementTree['Jump-Statement'].update({'statement':tokenToBeConsumed.value})
        #astJumpStmtTree['Jump-Statement'].append({tokenToBeConsumed.type:{}})
        consume(tokenToBeConsumed,tokenBuffer)
        tokenToBeConsumed = tokenBuffer[0]
        if tokenToBeConsumed.type != 'END':
            expression,exprAst = parseExpression(tokenBuffer)
            if expression:
                findTerminalNodes(expression)
                for terminalNode in terminalNodes:
                    type_1 = symTable.lookUpVariable(terminalNode,function_name)
                    if type_1 != None:
                        if type_1 != return_type and type(terminalNode) == str:
                            raise RuntimeError("type of variable being returned does not match return_type of function")
                jumpStatementTree['Jump-Statement'].update(expression)
                astJumpStmtTree.update({'return':exprAst})
                tokenToBeConsumed = tokenBuffer[0]
                if tokenToBeConsumed.type == 'END':
                    jumpStatementTree['Jump-Statement'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
                    consume(tokenToBeConsumed,tokenBuffer)
                else:
                    raise SyntaxError("Expected a semicolon at end of statement")
        else:
            jumpStatementTree['Jump-Statement'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
            consume(tokenToBeConsumed,tokenBuffer)
    return jumpStatementTree, astJumpStmtTree

"""
selection-statement:
    if ( expression ) statement
    if ( expression ) statement else statement
"""

def parseSelectionStatement(tokenBuffer):
    """
    Description:
    Arguments:
    Returns:
    
    """
    selectionStmtTree = {'Selection-Statement':{}}
    astSelectionStmtTree = {}
    tokenToBeConsumed = tokenBuffer[0]
    if tokenToBeConsumed.type == 'if':
        selectionStmtTree['Selection-Statement'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
        astSelectionStmtTree.update({tokenToBeConsumed.value:{}})
        consume(tokenToBeConsumed,tokenBuffer)
        tokenToBeConsumed = tokenBuffer[0]
        if tokenToBeConsumed.type == 'LPAREN':
            selectionStmtTree['Selection-Statement'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
            consume(tokenToBeConsumed,tokenBuffer)
            expression,exprAst = parseExpression(tokenBuffer)
            if expression:
                selectionStmtTree['Selection-Statement'].update(expression)
                astSelectionStmtTree['if'].update(exprAst)
                tokenToBeConsumed = tokenBuffer[0]
                if tokenToBeConsumed.type == 'RPAREN':
                    selectionStmtTree['Selection-Statement'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
                    consume(tokenToBeConsumed,tokenBuffer)
                    statement,astStmt = parseStatement(tokenBuffer)
                    statement['Statement-1'] = statement.pop('Statement')
                    if statement['Statement-1']:
                        selectionStmtTree['Selection-Statement'].update(statement)
                        astSelectionStmtTree.update(astStmt)
                        tokenToBeConsumed = tokenBuffer[0]
                        if tokenToBeConsumed.type == 'else':
                            selectionStmtTree['Selection-Statement'].update({tokenToBeConsumed.type:tokenToBeConsumed.value})
                            consume(tokenToBeConsumed, tokenBuffer)
                            statement,astStmt = parseStatement(tokenBuffer)
                            statement['Statement-2'] = statement.pop('Statement')
                            if statement:
                                selectionStmtTree['Selection-Statement'].update(statement)         
    return selectionStmtTree


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
"""
def getDictionaryItems(dict_to_iterate):
    astTree = []
    for key, value in dict_to_iterate.items():
        if type(value) == dict and len(value) != 0:
            astTree = value.popitem()
            getDictionaryItems(dict_to_iterate)
    return astTree
"""

def getDictionaryItems(dict_to_iterate):
    

    pass

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
