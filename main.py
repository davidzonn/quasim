# gotessman knill algorithm
#http://docs.sympy.org/dev/tutorial/manipulation.html
#H, CNOT, because they transform Pauli operators into other Pauli operators, are Clifford
import random
from abstract_quantum import *
from sympy import *
from itertools import chain

def main():
    #Declaraion of valid status (exc. mixed)
    x = sympy.Symbol('X')
    y = sympy.Symbol('Y')
    z = sympy.Symbol('Z')
    i = sympy.Symbol('I')
    ifz = sympy.Symbol('IfZ')
    skip = sympy.Symbol("Skip")

    #Declaration of valid gates
    h = sympy.Symbol('H')
    t = sympy.Symbol('T')
    cnot = sympy.Symbol('CNOT')

    #Declaration of mathematical constants to be interpreted as symbols
    sqrt2 = sympy.sqrt(2)

    #The quantum abstract domain associations
    associations = {
        t: {
            x: (x + y)/sqrt2,
            y: (y - x)/sqrt2,
            z: z,
            i: i
        },
        h: {
            x: z,
            y: -y,
            z: x,
            i: i
        },
        cnot: {
            (x,x):(x,i),
            (x,y):(y,z),
            (x,z):(-y,y),
            (y,x):(y,i),
            (y,y):(-x,z),
            (y,z):(x,y),
            (z,x):(z,x),
            (z,y):(i,y),
            (z,z):(i,z),
            (i,x):(i,x),
            (i,y):(z,y),
            (i,z):(z,z),
            (x,i):(x,x),
            (y,i):(y,x),
            (z,i):(z,i),
            (i,i):(i,i),
        }
    }


    #The initial configuration of our qubits
    initial_status = [i, y, i]


    #The Program to be executed over our qubits (right first)
    quantum_program = ((h, 1), (cnot,0,1), (cnot,2, 1), (h,1))
    # execute(initial_status, associations, quantum_program)

    ###### THE SAME BEING DONE WITH A COMPILER #####
    #End of statements by new line
    initial_status_string = "i, -y, i"
    quantum_code = """
        initial_status = "i, -y, i"
    """

    #generation of a random initial configuration
    number_of_qubits = 5
    number_of_steps = 15

    possible_initial_status = (x, y, z)
    possible_initial_programs = chain(((h, i) for i in range(0, number_of_qubits)), ((t, i) for i in range(0, number_of_qubits)),
                                   ((cnot, i, j) for i in range(0, number_of_qubits) for j in range(0, number_of_qubits) if i != j))
    random_status = list()
#    print [(cnot, i, j) for i in range(0, number_of_qubits) for j in range(0, number_of_qubits) if i != j]
    for i in range(0,number_of_qubits):
        random_status.append(random.choice(possible_initial_status))
    random_program = []
    possible_initial_programs = list(possible_initial_programs)
    for i in range(0,number_of_steps):
        random_choice = random.choice(possible_initial_programs)
        random_program.append(random_choice)
    execute(random_status, associations, random_program)

if __name__ == "__main__":
    main()