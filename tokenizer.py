import re
#tokens

WHITESPACE = ""
#DATATYPES
#RESERVEDWORDS
#OPERATORS  


def tokenize(s):
    
    token_specfication = [
        ('TTAIL')
    ]
    
    #tokens = [s[i] for i,j in range(0,len(s))]
    #tokens = [str(tok) for tok in tokenblocks]
    WHITESPACE = re.findall("\S+", s[0])
    #print(WHITESPACE)
    #DATATYPES =  re.findall("int|num",s[0])
    
    
    tokens = []
    for line in s:
        for char in line:
            tokens.append(char)    
    return tokens