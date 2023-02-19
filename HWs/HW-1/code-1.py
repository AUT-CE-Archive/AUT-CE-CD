import ply.lex as lex

# List of token names.   This is always required
tokens = (
   'ID',
#    'MULTI_LINE_COMMENT_1',
#    'MULTI_LINE_COMMENT_2',
    'MULTI_LINE_COMMENT',
    'SINGLE_LINE_COMMENT',
)

def t_ID(t):
    r'[a-zA-Z0-9]+'
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# /* comment */
def t_MULTI_LINE_COMMENT_1(t):
    r'\/\*(?:[\s\S])*\*\/'
    ncr = t.value.count("\n")
    t.lexer.lineno += ncr

# (* comment *)
def t_MULTI_LINE_COMMENT_2(t):
    r'\(\*(?:[\s\S])*\*\)'
    ncr = t.value.count("\n")
    t.lexer.lineno += ncr

def MULTI_LINE_COMMENT(t):
    r'(\/|\()\*(?:[\s\S])*\*(\/|\()'
    ncr = t.value.count("\n")
    t.lexer.lineno += ncr

# // comment
def t_SINGLE_LINE_COMMENT(t):
    r'(//.*?(\n|$))'
    t.lexer.lineno += 1

# Build the lexer
lexer = lex.lex(debug = False)

# Passed
no_comment = '''
Howdy lil fella
'''

# Passed
single_line_comment = '''
// I'm a Single Line Comment!
Howdy lil fella
'''

# Passed
single_line_complex_comment_1 = '''
/* Still Single! */
Howdy lil fella
'''

# Passed
single_line_complex_comment_2 = '''
(* Still Single! *)
Howdy lil fella
'''

# Passed
multi_line_comment_1 = '''
/*
    Not Single Anymore! Haha!
*/
Howdy lil fella
'''

# Passed
multi_line_comment_2 = '''
(*
    Not Single Anymore! Haha!
*)
Howdy lil fella
'''

# Passed
multi_line_nested_comment_1 = '''
/*
    /*
        Not Single Anymore! Haha!
    */
*/
Howdy lil fella
'''

# Passed
multi_line_nested_comment_2 = '''
(*
    (*
        Not Single Anymore! Haha!
    *)
*)
Howdy lil fella
'''

# Passed
multi_line_complex_nested_comment = '''
(*
  (* I'm a complex comment! *)
  (*
     (*
         I'm a very nested comment!
     *)
  *)
  /* I'm another complex comment! */
*)
Howdy lil fella
'''

# Passed
sample_test_1 = '''
hi1 2 /* good */
bye 7 (* bad /* inner */ *)
'''

# Passed
sample_test_2 = '''
/*
    comment in depth 1
    (*
        comment in depth 2
        /*
            /* comment in depth 3 */
        */
    *)
    another comment in depth 1
    /*
        another comment in depth 2
    */
*/
Howdy lil fella
'''

# Give the lexer some input
lexer.input(sample_test_1)

# Tokenize
n_tokens = 0
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok.type, tok.value, tok.lineno, tok.lexpos, sep = '\t')
    n_tokens += len(tok.value)
print('NUMBER OF TOKENS:', n_tokens)