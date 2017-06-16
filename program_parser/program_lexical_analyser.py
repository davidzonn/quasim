import ply.lex
import ply.yacc

reserved = {
            'if': 'IF',
            'then': 'THEN',
            'else': 'ELSE',
            'skip': 'SKIP'
            }

tokens = [
            'IDENTIFIER',
            'QUBITEXPRESSION'
          ] + list(reserved.values())

t_ignore = ' \t' #Ignore Tab or space
literals = ['+', '-', '/', '*', ',', ';', '(', ')'] #Returned with no modification

def t_QUBITEXPRESSION(t):
    # r'q\d+' #One 'q' followed by a number.
    r'q[1-9][0-9]*'
    t.value = int(t.value[1]) - 1 #Remove the q for the program, standarize by removing one.
    return t


def t_MULTILINE_COMMENT(t):
    r'\*\/(.|\n)*?\/\*' #no return, it gets ignored, higher priority than single line comments


def t_COMMENT(t):
    r'\/\/.*' #no return, it gets ignored


def t_newline(t):
    r'\n+' #maybe use new line for end of statement instead of ;"?"
    t.lexer.lineno += len(t.value)

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_error(t):
    print("Warning: Illegal character '%s' skipped" % t.value[0])
    t.lexer.skip(1)





def main():
    lexer = ply.lex.lex()

    quantum_code = """
        H(q2);
        CNot(q2, q3);
        CNot(q1, q2);
        H(q1);
        if q1 then
            if q1 then skip else X(q3)
        else
            if q2 then Z(q3) else Y(q3)
    """

    lexer.input(quantum_code)
    while True:
        tok = lexer.token()
        if not tok: break
        print tok

if __name__ == "__main__":
    main()
