import ply.lex
import ply.yacc

reserved = {
            'if': 'IF',
            'then': 'THEN',
            'else': 'ELSE',
            'skip': 'SKIP'
            }

tokens = [
            'GATE',
            'NO_INSTRUCTION',
            'EQUAL',
            'IDENTIFIER'
          ] + list(reserved.values())

t_ignore = ' \t' #Ignore Tab or space
literals = ['+', '-', '/', '*', ',', ';', '(', ')'] #Returned with no modification

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

    quantum_code = """
        H(q2); //End of line comment
        Cnot(q2, q3);
        Cnot(q1, q2);
        H(q1)
        if (q1) then
            if (q1) then skip else x(q3)
        else
            if (q2) then z(q3) else y(q3)

    """

    lexer = ply.lex.lex()
    lexer.input(quantum_code)
    #parser = ply.yacc.yacc()
    while True:
        tok = lexer.token()
        if not tok: break
        print tok

if __name__ == "__main__":
    main()