from typing import NamedTuple
import re
#got this code from https://docs.python.org/3/library/re.html#re.Match

class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int

def tokenize(code):
    types = {'int', 'double', 'float'}
    modifiers = {'unsigned', 'long', 'short'}
    itrs = {'if', 'for', 'while', 'switch', 'do','else'}
    controlStmts = {'return', 'break'}
    keywords = types.union(modifiers,itrs,controlStmts)
        
    token_specification = [
        ('NUMBER',   r'\d+(\.\d*)?'),  # Integer or floating point number
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
        ('ASSIGN_OPS', r"=|\+=|\-=|\*=|/=|%=|\^="), # Assignment operators
        ('PREFIX_OP', r"\+\+|\-\-"),      # Unary operators
        ('MATH_OP',  r'[+\-*/%]'),     # Arithmetic operators
        ('RELAT_OP', r"<=|>=|!=|>|<|=="), # Relational operators
        ('LOGICAL_OP', r"&&|!|\|\|"),          # Logical operators
        ('BITWISE_OP', r"&|\||<<|>>|~|\^"), # Bitwise operators
        ('TERNARY_OP', r'\?:'),        # Ternary operator
        ('NEWLINE',  r'\n'),           # Line endings
        ('SKIP',     r'[ \t]+'),       # Skip over spaces and tabs
        ('MISMATCH', r'.'),            # Any other character
    ]

    tokens = []
      
    code = re.sub('\//.*|\/\*.*\*\/'," ", code)
    #stores instances of strings
    strings = re.findall('\'.*\'|\".*\"', code)
    #print(strings)

    #remove all charcters after first single quote or first double quote
    code = re.sub('\'.*\'', "\'", code)
    code = re.sub('\".*\"', "\"", code)
    
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0

    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start + 1
        if kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif kind == 'ID' and value in keywords:
            kind = value
        elif kind == 'SQUOTE':
            kind = 'C_LITERAL' # character literal
            value = strings[0]
            strings.pop(0)
        elif kind == 'DQUOTE':
            kind = 'S_LITERAL' # string literal
            value = strings[0]
            strings.pop(0)
        elif kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        token =  Token(kind, value, line_num, column)
        tokens.append(token)
    return tokens

    