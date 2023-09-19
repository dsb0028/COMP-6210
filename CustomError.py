class MissingExprError(Exception):
    """ Exception raised for errors in the Factor Rule.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
        loc  -- dictionary object that provides the line and column number of the error
    """
    def __init__(self, expression, message, loc):
        self.expression = expression
        self.message = message
        self.loc = loc

class MissingRParenError(Exception):
    """ Exception raised when closed parenthesis is missing after expression. 

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
        loc  -- dictionary object that provides the line and column number of the error
    """
    def __init__(self, expression, message, loc):
        self.expression = expression
        self.message = message
        self.loc = loc

class MissingFactorError(Exception):
    """ Exception raised when factor is missing from ExprP rule. 

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
        loc  -- dictionary object that provides the line and column number of the error
    """
    def __init__(self, expression, message, loc):
        self.expression = expression
        self.message = message
        self.loc = loc
    
class NotAllTokensHaveBeenConsumedError(Exception):
    """ Exception raised when all tokens have not been consumed. 

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
        
    """
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
        
    
