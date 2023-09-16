grammar CGrammar;
    Expr: Term ExprP;
    
    ExprP: ('+' | '-') Term ExprP |;
    
    Term : Factor TermP;
    
    TermP: ('*'|'/') Factor TermP |;
    
    Factor:  '(' Expr ')' | NUMBER | ID;

    fragment NUMBER: INT | FLOAT;
    fragment INT: [0-9]+;
    fragment FLOAT: [0-9]+.[0-9]+;
    fragment ID: [A-Za-z]+[NUMBER]*;