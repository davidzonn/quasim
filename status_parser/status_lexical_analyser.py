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
