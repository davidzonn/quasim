# Copyright 2017 David A. Zonneveld Michel
# This file is part of Quasim.
#
# Quasim is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Quasim is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>

import ply.yacc
import sympy

import status_lexical_analyser

from status_lexical_analyser import tokens

def p_error(p):
    print("Syntax error in input!") #Could maybe be a bit more... descriptive?


def p_status(p):
    '''
        status : '{' expressionlist '}'
                | '[' expressionlist ']'
    '''
    p[0] = p[2]


def p_expressionlist_single(p):
    '''
        expressionlist : expression
    '''
    p[0] = [p[1]]


def p_expressionlist_multiple(p):
    '''
        expressionlist : expression ',' expressionlist
    '''
    p[0] = [p[1]] + p[3]


def p_expression_parenthesis(p):
    '''
        expression : '(' expression ')'
    '''
    p[0] = p[2]


def p_expression_sqrt(p):
    '''
        expression : SQRT '(' NUMBER ')'
    '''
    p[0] = sympy.sqrt(int(p[3]))


def p_expression_number(p):
    '''
        expression : NUMBER
    '''
    p[0] = p[1]


def p_expression_identifier(p):
    '''
        expression : IDENTIFIER
    '''
    p[0] = sympy.Symbol(p[1])


def p_expression_div(p):
    '''
        expression : expression '/' expression
    '''
    p[0] = sympy.Mul(p[1], sympy.Pow(p[3], sympy.Integer(-1)), evaluate=False)
    #p[0] = p[1] / p[3]

def p_expression_mult(p):
    '''
        expression : expression '*' expression        
    '''
    p[0] = p[1] * p[3]

def p_expression_add(p):
    '''
        expression : expression '+' expression
    '''
    p[0] = p[1] + p[3]



def main():
    status_parser = ply.yacc.yacc()

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


    quantum_status = """
        {x, (i + z)/sqrt(2), (i+z)/2}
        //{x/2}
    """

    status_lexical_analyser.lexer.input(quantum_status)
    while True:
        tok = status_lexical_analyser.lexer.token()
        if not tok: break
        print tok
    parsing_result =  status_parser.parse(quantum_status)
    print parsing_result
    #lexical_analyser.lexer.input(quantum_code)
    # while True:
    #     tok = lexical_analyser.lexer.token()
    #     if not tok: break
    #     print tok.type




if __name__ == "__main__":
    main()