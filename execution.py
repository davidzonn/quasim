import ply.lex
import ply.yacc

import program_interpreter
import program_parser.program_syntactic_analyser as program_syntactic_analyser
import status_parser.status_lexical_analyser as status_lexical_analyser
import status_parser.status_syntactic_analyser as status_syntactic_analyser
from program_parser import program_lexical_analyser

def execute (program_string, status_string, associations):
    program_lexer = ply.lex.lex(module=program_lexical_analyser)
    program_parser = ply.yacc.yacc(module=program_syntactic_analyser)

    status_lexer = ply.lex.lex(module=status_lexical_analyser)
    status_parser = ply.yacc.yacc(module=status_syntactic_analyser)

    parsed_initial_status = status_parser.parse(status_string, lexer=status_lexer)
    print parsed_initial_status

    parsed_program = program_parser.parse(program_string, program_lexer)
    print parsed_program

    program_interpreter.Quantum_Interpreter(parsed_initial_status, associations, parsed_program)