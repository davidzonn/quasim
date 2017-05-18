# gotessman knill algorithm
#http://docs.sympy.org/dev/tutorial/manipulation.html
#H, CNOT, because they transform Pauli operators into other Pauli operators, are Clifford
import random
import abstract_quantum
import sympy
from itertools import chain
import constants

# Declaraion of valid status (exc. mixed)
x = sympy.Symbol('X')
y = sympy.Symbol('Y')
z = sympy.Symbol('Z')
i = sympy.Symbol('I')
skip = sympy.Symbol("Skip")

# Declaration of valid gates
h = sympy.Symbol('H')
t = sympy.Symbol('T')
cnot = sympy.Symbol('CNOT')

# The quantum abstract domain associations
associations = {
    t: {
        x: (x + y) / constants.sqrt2,
        y: (y - x),
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
    },
    y: {
        x: -x,
        y: y,
        z: -z
    },
    z: {
        x: -x,
        y: -y,
        z: z
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


def execute_random_program():
    #generation of a random initial configuration
    number_of_qubits = 5
    number_of_steps = 15

    possible_initial_status = (x, y, z)
    possible_initial_programs = chain(((h, i) for i in range(0, number_of_qubits)), ((t, i) for i in range(0, number_of_qubits)),
                                   ((cnot, i, j) for i in range(0, number_of_qubits) for j in range(0, number_of_qubits) if i != j and abs(i-j) == 1))
    random_status = list()
#    print [(cnot, i, j) for i in range(0, number_of_qubits) for j in range(0, number_of_qubits) if i != j]
    for i in range(0,number_of_qubits):
        random_status.append(random.choice(possible_initial_status))
    random_program = []
    possible_initial_programs = list(possible_initial_programs)
    for i in range(0,number_of_steps):
        random_choice = random.choice(possible_initial_programs)
        random_program.append(random_choice)
    abstract_quantum.execute(random_status, associations, random_program)


def main():

    #The initial configuration of our qubits
    initial_status = [x]


    #The Program to be executed over our qubits (right first)
    quantum_program = ((t, 0), (t, 0))
    abstract_quantum.execute(initial_status, associations, quantum_program)

    ###### THE SAME BEING DONE WITH A COMPILER #####
    #Now, end of statements semicolon. Why not by new line?
    initial_status_string = "i, -y, i"

    quantum_code = """
        H(q2);
        CNot(q2, q3);
        Cnot(q1, q2);
        H(q1);
        if (q1) then
            if (q1) then skip; else x(q3);
        else
            if (q2) then z(q3) else y(q3);
    """

    execute_random_program()

if __name__ == "__main__":
    main()