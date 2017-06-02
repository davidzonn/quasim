# gotessman knill algorithm
#http://docs.sympy.org/dev/tutorial/manipulation.html
#H, CNOT, because they transform Pauli operators into other Pauli operators, are Clifford
import ply.lex
import ply.yacc

import program_interpreter
import program_parser.program_syntactic_analyser as program_syntactic_analyser
import status_parser.status_lexical_analyser as status_lexical_analyser
import status_parser.status_syntactic_analyser as status_syntactic_analyser
# from project.gates.exact import *
from project.gates.approximate import *
from project.program_parser import program_lexical_analyser


def execute_compiler():


    unparsed_initial_status = """
        {X, (I + Z)/2, (I+Z)/2}
    """

    # unparsed_quantum_code = """
    #     H(q2);
    #     */
    #
    #     SOME CODE WITHIN MY COMMENTS:
    #     /*
    #
    #     CNot(q2, q3); */ and some weird /*
    #     */commends in
    #         random
    #         H(q1);
    #         places /*
    #
    #     CNot(q1, */even inbetween commands /* q2);
    #     //By the way, line commends should also be ignored
    #     H(q1);
    #     H(q1)
    # """


    # unparsed_quantum_code = """
    #     if q1 then
    #         X(q2)
    # """


    # initial_status = [x]
    # unparsed_quantum_code = """
    #     T(q1);
    #     T(q1)
    # """

    # initial_status = [(z+i)/2, (i+x)/2]
    #
    # unparsed_quantum_code = """
    #     if q1 then
    #         T(q2); T(q2)
    #     else
    #         skip; T(q2); X(q1); Y(q2); X(q1); X(q1)
    # """

    # initial_status = [(i+x)/2]
    #
    # unparsed_quantum_code = """
    #     if q1 then
    #         skip
    #     else
    #         skip
    # """

    # unparsed_quantum_code = """
    #     T(q1)
    # """

    unparsed_quantum_code = """
        H(q2);
        CNot(q2, q3);
        CNot(q1, q2);
        H(q1);
        if q1 then
            if q1 then skip else X(q3)
        else
            if q2 then Z(q3) else Y(q3)
    """

    program_lexer = ply.lex.lex(module=program_lexical_analyser)
    program_parser = ply.yacc.yacc(module=program_syntactic_analyser)

    status_lexer = ply.lex.lex(module=status_lexical_analyser)
    status_parser = ply.yacc.yacc(module=status_syntactic_analyser)

    parsed_initial_status = status_parser.parse(unparsed_initial_status, lexer=status_lexer)
    print parsed_initial_status

    parsed_program = program_parser.parse(unparsed_quantum_code, program_lexer)
    print parsed_program

    program_interpreter.Quantum_Interpreter(parsed_initial_status, associations, parsed_program)


# def execute_random_program():
#     #generation of a random initial configuration
#     number_of_qubits = 5
#     number_of_steps = 15
#
#     possible_initial_status = (x, y, z)
#     possible_initial_programs = chain(((h, i) for i in range(0, number_of_qubits)), ((t, i) for i in range(0, number_of_qubits)),
#                                    ((cnot, i, j) for i in range(0, number_of_qubits) for j in range(0, number_of_qubits) if i != j and abs(i-j) == 1))
#     random_status = list()
# #    print [(cnot, i, j) for i in range(0, number_of_qubits) for j in range(0, number_of_qubits) if i != j]
#     for i in range(0,number_of_qubits):
#         random_status.append(random.choice(possible_initial_status))
#     random_program = []
#     possible_initial_programs = list(possible_initial_programs)
#
#     for i in range(0,number_of_steps):
#         random_choice = random.choice(possible_initial_programs)
#         random_program.append(random_choice)
#     abstract_quantum.execute(random_status, associations, random_program)
#
#
# def execute_parsed_program():
#     initial_status = [x]
#     quantum_program = ((t, 0), (t, 0))
#     abstract_quantum.execute(initial_status, associations, quantum_program)

def main():
    pass
    # execute_parsed_program()
    execute_compiler()
    # execute_random_program()

if __name__ == "__main__":
    main()