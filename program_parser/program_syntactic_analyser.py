#input: Tokens. Output: Tree A.K.A Parser

import ply.yacc
import program_lexical_analyser
from project.abstract_syntax_tree import AST

from program_lexical_analyser import tokens


def p_error(p):
    print("Syntax error in input!") #Could maybe be a bit more... descriptive?


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

def p_command_ifthenelse (p):
    '''
        command : IF QUBITEXPRESSION THEN command ELSE command
    '''
    p[0] = AST(p[1], p[2], p[4], p[6])

def p_command_if(p):
    '''
        command : IF QUBITEXPRESSION THEN command
    '''
    p[0] = AST(p[1], p[2], p[4], AST("skip"))


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



def main():
    program_parser = ply.yacc.yacc()

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

    parsing_result =  program_parser.parse(quantum_code)
    print parsing_result
    #lexical_analyser.lexer.input(quantum_code)
    # while True:
    #     tok = lexical_analyser.lexer.token()
    #     if not tok: break
    #     print tok.type




if __name__ == "__main__":
    main()