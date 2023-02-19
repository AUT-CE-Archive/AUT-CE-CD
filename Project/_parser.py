# Standard imports
import ply.yacc as yacc

# Local imports
from _lexer import *
from tac import TAC, TACs


temp_counter = 0
def new_temp():
    global temp_counter
    temp_counter += 1
    return f"t{temp_counter}"

# dictionary of names
names = {}

# precedence rules
precedence = (
    ('left', 'PLUS', 'MINUS'),              # Addition and subtraction (left associative)
    ('left', 'TIMES', 'DIVIDE', 'MOD'),     # Multiplication and division (left associative)
    ('right','UMINUS'),                     # Unary minus operator (right associative)
    ('left', 'AND', 'OR'),                  # Logical operators (left associative)
)

def p_statement_assign(t):
    'statement : IDENTIFIER ASSIGN expression'
    names[t[1]] = t[3]
    TACs.append(TAC(t[2], t[1], t[3], new_temp()))


def p_statement_expr(t):
    'statement : expression'
    print(t[1])


def p_expression_arithmetics(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression DIVIDE expression
                  | expression TIMES expression
                  | expression MOD expression'''
    # type checking (both sides can be either int or float)
    if not ((type(t[1]) == int or type(t[1]) == float) and (type(t[3]) == int or type(t[3]) == float)):
        return print("Can only operate arithmetics on integers and floats")

    if t[2] == '+': t[0] = t[1] + t[3]
    elif t[2] == '-': t[0] = t[1] - t[3]
    elif t[2] == '*': t[0] = t[1] * t[3]
    elif t[2] == '/': t[0] = t[1] / t[3]
    elif t[2] == '%':
        if type(t[1]) == int and type(t[3]) == int:
            t[0] = t[1] % t[3]
        else:
            return print("Can only operate modulo on integers")
    TACs.append(TAC(t[2], t[1], t[3], new_temp()))


def p_expression_logical_not(t):
    'expression : NOT expression'
    # type checking (expression must only be boolean)
    if type(t[2]) != bool:
        return print("Can only operate logical not on booleans")

    t[0] = not t[2]
    TACs.append(TAC(t[1], t[2], None, new_temp()))


def p_expression_logical(t):
    '''expression : expression AND expression
                  | expression OR expression'''
    # type checking (both sides must be bools)
    if not (type(t[1]) == type(t[3]) == bool):
        return print("Can only operate comparison on booleans")

    if t[2] == 'and': t[0] = t[1] and t[3]
    elif t[2] == 'or': t[0] = t[1] or t[3]
    TACs.append(TAC(t[2], t[1], t[3], new_temp()))


def p_expression_comparison(t):
    '''expression : expression BIGGER expression
                  | expression SMALLER expression
                  | expression EQUAL expression
                  | expression NOTEQUAL expression
                  | expression BIGGEREQUAL expression
                  | expression SMALLEREQUAL expression'''
    # type checking (both sides must be either int or float)
    if not ((type(t[1]) == int or type(t[1]) == float) and (type(t[3]) == int or type(t[3]) == float)):
        return print("Can only operate comparison on integers and floats")

    if t[2] == '>': t[0] = t[1] > t[3]
    elif t[2] == '<': t[0] = t[1] < t[3]
    elif t[2] == '==': t[0] = t[1] == t[3]
    elif t[2] == '<>': t[0] = t[1] != t[3]
    elif t[2] == '>=': t[0] = t[1] >= t[3]
    elif t[2] == '<=': t[0] = t[1] <= t[3]
    TACs.append(TAC(t[2], t[1], t[3], new_temp()))


def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]
    TACs.append(TAC("uminus", t[2], None, new_temp()))


def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]
    TACs.append(TAC("group", t[2], None, new_temp()))


def p_expression_number(t):
    '''expression : INTEGER
                  | FLOAT'''
    t[0] = t[1]


def p_expression_name(t):
    'expression : IDENTIFIER'
    try: t[0] = names[t[1]]
    except LookupError: print(f"Undefined name '{t[1]}'")


def p_expression_if(t):
    'statement : IF expression THEN statement'
    TACs.append(TAC("if", t[2], t[4], new_temp()))


def p_expression_if_else(t):
    'statement : IF expression THEN statement ELSE statement'
    # TACs.append(TAC("if_else", t[2], t[4], new_temp()))
    pass


def p_expression_while(t):
    'statement : WHILE expression DO statement'
    TACs.append(TAC("while", t[2], t[4], new_temp()))


def p_expression_print(t):
    'statement : PRINT expression'
    TACs.append(TAC("print", t[2], None, new_temp()))


def p_error(t):
    print("Syntax error at '%s'" % t.value)

parser = yacc.yacc()

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    parser.parse(s, debug = False)
    
    for tac in TACs:
        print(tac.to_c_code())