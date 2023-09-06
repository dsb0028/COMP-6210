from typing import NamedTuple
import re

class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int

def tokenize(code):
    types = {'int', 'double', 'float'}
    modifiers = {'unsigned', 'long', 'short'}
    itrs = {'if', 'for', 'while', 'switch', 'do'}
    bkStmts = {'return', 'break'}
    keywords = types.union(modifiers,itrs,bkStmts)
        
    token_specification = [
        ('NUMBER',   r'\d+(\.\d*)?'),  # Integer or decimal number
        ('ID',       r'[A-Za-z]+[\d]?'),  # Identifiers
        ('PERIOD',r"\."),              # period
        ('COMMA', r'\,'),              # Comma operator
        ('END',   r';'),            # Statement terminator
        ('HASH',r'#'),              # Hash
        ('LPAREN', r"\("),             # Left parenthesis
        ('RPAREN', r"\)"),             # Right parenthesis
        ('LBRACE', r"\{"),             # Left brace
        ('RBRACE', r"\}"),             # Right brace     
        ('LBRACK', r"\["),             # Left bracket
        ('RBRACK', r"\]"),             # Right bracket 
        ('SQUOTE', r"'"),              # Single quote
        ('DQUOTE', r"\""),             # Double quote
        ('BMULTLINCOMM', r"\/\*"),     # Beginning of multiline comment
        ('EMULTLINCOMM', r"\*/"),      # End of multiline comment
        ('SINGLINECOMM', r"\/\/"),     # represents beginning of single line comment
        ('ASSIGN_OPS', r"=|\+=|\-=|\*=|/=|%=|\^="), # Assignment operators
        ('PREFIX_OP', r"\++|\--"),      # Unary operators
        ('MATH_OP',  r'[+\-*/%]'),     # Arithmetic operators
        ('RELAT_OP', r"<=|>=|!=|>|<|=="), # Relational operators
        ('LOGICAL_OP', r"&&|!|'\||'"),          # Logical operators
        ('BITWISE_OP', r"&|\||<<|>>|~|\^"), # Bitwise operators
        ('TERNARY_OP', r'\?:'),        # Ternary operator
        ('NEWLINE',  r'\n'),           # Line endings
        ('SKIP',     r'[ \t]+'),       # Skip over spaces and tabs
        ('MISMATCH', r'.'),            # Any other character
    ]

    tokens = []
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif kind == 'ID' and value in keywords:
            kind = value
        elif kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        token =  Token(kind, value, line_num, column)
        #print("Token",token, '\n')
        tokens.append(token)
        #print(tokens)
    return tokens

    