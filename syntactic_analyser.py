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
    p[0] = AST(p[1])

def p_command_multiplecommands (p):
    '''
        command : command ';' command
    '''
    command_name = "sequence"
    if (p[3].name == command_name):
        p[0] = AST(command_name, p[1], *p[3])
    else:
        p[0] = AST(command_name, p[1], p[3])

def p_command_gate (p):
    '''
        command : IDENTIFIER '(' args ')'
    '''
    p[0] = AST(p[1] , *p[3])

def p_command_if (p):
    '''
        command : IF QUBITEXPRESSION THEN command ELSE command
    '''
    p[0] = AST(p[1], p[2], p[4], p[6])

def p_args_single (p):
    '''
        args : QUBITEXPRESSION 
    '''
    p[0] = [p[1]]

def p_args_list (p):
    '''
         args : QUBITEXPRESSION ',' args
    '''
    p[0] = [p[1]] + p[3]

quantum_parser = ply.yacc.yacc()

def main():

    quantum_code = """
        H(q2);
        CNot(q2, q3);
        Cnot(q1, q2);
        H(q1);
        if q1 then
            if q1 then skip else x(q3)
        else
            if q2 then z(q3) else y(q3)
    """

    parsing_result =  quantum_parser.parse(quantum_code)
    print parsing_result
    #lexical_analyser.lexer.input(quantum_code)
    # while True:
    #     tok = lexical_analyser.lexer.token()
    #     if not tok: break
    #     print tok.type




if __name__ == "__main__":
    main()