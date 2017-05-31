# gotessman knill algorithm
#http://docs.sympy.org/dev/tutorial/manipulation.html
#H, CNOT, because they transform Pauli operators into other Pauli operators, are Clifford
import random
import program_interpreter
import abstract_quantum
import sympy
from itertools import chain
import constants
from constants import sqrt2
from syntactic_analyser import quantum_parser

# Declaraion of valid status (exc. mixed)
x = sympy.Symbol('X')
y = sympy.Symbol('Y')
z = sympy.Symbol('Z')
i = sympy.Symbol('I')
skip = sympy.Symbol("Skip")

# Declaration of valid gates
h = sympy.Symbol('H')
t = sympy.Symbol('T')
cnot = sympy.Symbol('CNot')

# The quantum abstract domain associations
associations = {
    t: {
        x: (x + y) / sqrt2,
        y: (y - x) / sqrt2,
        z: z,
        i: i
    },
    h: {
        x: z,
        y: -y,
        z: x,
        i: i
    },
    x: {
        x: x,
        y: -y,
        z: -z,
        i: i
    },
    y: {
        x: -x,
        y: y,
        z: -z,
        i: i
    },
    z: {
        x: -x,
        y: -y,
        z: z,
        i: i
    },
    cnot: {
        (x, x): (x, i),
        (x, y): (y, z),
        (x, z): (-y, y),
        (y, x): (y, i),
        (y, y): (-x, z),
        (y, z): (x, y),
        (z, x): (z, x),
        (z, y): (i, y),
        (z, z): (i, z),
        (i, x): (i, x),
        (i, y): (z, y),
        (i, z): (z, z),
        (x, i): (x, x),
        (y, i): (y, x),
        (z, i): (z, i),
        (i, i): (i, i),
    }
}

if_associations = {
    True: {
        i: (i + z)/2,
        x: constants.measured,
        y: constants.measured,
        z: (i + z)/2
    },
    False: {
        i: (i - z)/2,
        x: constants.measured,
        y: constants.measured,
        z: (z - i)/2
    }
}


def execute_compiler():

    # initial_status = [x, z, z]

    initial_status = [x, (i + z)/2, (i + z)/2] #CREATE BNF OF STATUS AND ADD TO COMPILER / SEPARATE COMPILER?

    quantum_code = """
        H(q2);
        CNot(q2, q3);
        CNot(q1, q2);
        H(q1);
        if q1 then
            if q2 then skip else X(q3)
    """

    # quantum_code = """
    #     if q1 then
    #         X(q2)
    # """


    # initial_status = [x]
    # quantum_code = """
    #     T(q1);
    #     T(q1)
    # """

    # initial_status = [(z+i)/2, (i+x)/2]
    #
    # quantum_code = """
    #     if q1 then
    #         T(q2); T(q2)
    #     else
    #         skip; T(q2); X(q1); Y(q2); X(q1); X(q1)
    # """

    # initial_status = [(i+x)/2]
    #
    # quantum_code = """
    #     if q1 then
    #         skip
    #     else
    #         skip
    # """

    # quantum_code = """
    #     T(q1)
    # """
    parsed_input = quantum_parser.parse(quantum_code)
    print "PARSED: ", parsed_input
    print parsed_input

    program_interpreter.Quantum_Interpreter(initial_status, associations, parsed_input, if_associations)


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

    # execute_parsed_program()
    execute_compiler()
    # execute_random_program()

if __name__ == "__main__":
    main()