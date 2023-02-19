import ply.lex as lex

# Name of tokens
tokens = (
    'PLUS', 'MINUS', 'DIVIDE', 'ASSIGN', 'TIMES', 'MOD', # arithmetic
    'INTEGER', 'IDENTIFIER', 'FLOAT', # data types
    'LPAREN','RPAREN', # parentheses
    'BIGGER', 'SMALLER', 'EQUAL', 'NOTEQUAL', 'BIGGEREQUAL', 'SMALLEREQUAL', # comparison
)

# Reserved keywords
reserved = {
    "and": "AND",
    "or": "OR",
    "not": "NOT",
    "if": "IF",
    "while": "WHILE",
    "else": "ELSE",
    "then": "THEN",
    "print": "PRINT",
    "do": "DO",
}
tokens += tuple(reserved.values())

# Definition of tokens
t_ignore = " \t"
t_PLUS = r'\+'
t_MINUS = r'-'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_TIMES = r'\*'
t_MOD = r'%'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_BIGGER = r'>'
t_SMALLER = r'<'
t_EQUAL = r'=='
t_NOTEQUAL = r'<>'
t_BIGGEREQUAL = r'>='
t_SMALLEREQUAL = r'<='

def t_DO(t):
    r'do'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_WHILE(t):
    r'while'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_PRINT(t):
    r'print'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_IF(t):
    r'if'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_THEN(t):
    r'then'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_ELSE(t):
    r'else'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_AND(t):
    r'and'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_OR(t):
    r'or'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_NOT(t):
    r'not'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

lexer = lex.lex()