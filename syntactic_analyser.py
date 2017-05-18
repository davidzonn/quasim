#input: Tokens. Output: Tree A.K.A Parser

import ply.yacc
import lexical_analyser
from abstract_syntax_tree import AST

from lexical_analyser import tokens

def p_error(p):
    print("Syntax error in input!")


def p_command_skip (p):
    '''
        command : SKIP
    '''
    p[0] = p[1]

def p_command_multiplecommands (p):
    '''
        command : command ';' command
    '''
    p[0] = AST("Statement Sequence", p[1], p[3])

def p_command_gate (p):
    '''
        command : IDENTIFIER '(' args ')'
    '''
    p[0] = AST("Gate", p[1] , p[3])

def p_command_if (p):
    '''
        command : IF QUBITEXPRESSION THEN command ELSE command
    '''
    p[0] = AST(p[1])

def p_args_single (p):
    '''
        args : QUBITEXPRESSION 
    '''
    p[0] = p[1]

def p_args_list (p):
    '''
         args : QUBITEXPRESSION ',' args
    '''
    p[0] = (p[1], p[3])

def main():

    quantum_code = """
        H(q2); //End of line comment
        Cnot(q2, q3);
        Cnot(q1, q2);
        H(q1);
        if q1 then
            if q1 then skip else x(q3)
        else
            if q2 then z(q3) else y(q3)
    """


    lexical_analyser.lexer.input(quantum_code)
    # while True:
    #     tok = lexical_analyser.lexer.token()
    #     if not tok: break
    #     print tok.type


    parser = ply.yacc.yacc()
    parsed_tokens = parser.parse(quantum_code)
    print parsed_tokens


if __name__ == "__main__":
    main()