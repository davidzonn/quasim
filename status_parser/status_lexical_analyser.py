import ply.lex
import ply.yacc

reserved = {
            'sqrt': 'SQRT'
            }

tokens = [
            'IDENTIFIER',
            'NUMBER'
          ] + list(reserved.values())

t_ignore = ' \t' #Ignore Tab or space
literals = ['+', '-', '/', '*', ',', ';', '(', ')', '{', '}'] #Returned with no modification


def t_MULTILINE_COMMENT(t):
    r'\*\/(.|\n)*?\/\*' #no return, it gets ignored, higher priority than single line comments


def t_COMMENT(t):
    r'\/\/.*' #no return, it gets ignored


def t_newline(t):
    r'\n+' #maybe use new line for end of statement instead of ;"?"
    t.lexer.lineno += len(t.value)

def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_error(t):
    print("Warning: Illegal character '%s' skipped" % t.value[0])
    t.lexer.skip(1)


def main():
    lexer = ply.lex.lex()
    quantum_status = """
        {x, (i + z)/sqrt(2), (i+z)/2}
    """

    lexer.input(quantum_status)
    while True:
        tok = lexer.token()
        if not tok: break
        print tok

if __name__ == "__main__":
    main()
