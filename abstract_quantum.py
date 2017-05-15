import sympy
from sympy import *
from status_tree import Quantum_Status

def calculate_one_qubit_evolution(gate_associations, status_before):
    #print "Tree representation: ", srepr(status_before), " String Representation", status_before
    default_symbol = sympy.Symbol("Unknown")

    if isinstance(status_before, Symbol): #Is symbol leaf
        status_after = gate_associations.setdefault(status_before, default_symbol) #If the root is a symbol, apply operator
    elif not status_before.args: #No children, is leaf
        status_after = status_before
    else:
        new_arguments = [calculate_one_qubit_evolution(gate_associations, x) for x in status_before.args]#Recursively apply to all children.
        status_after = status_before.func(*new_arguments)
    return status_after


def calculate_two_qubit_evolution(gate_associations, status_qubit1, status_qubit2):
    default_symbol = sympy.Symbol("Unknown")
    new_status = gate_associations.setdefault((status_qubit1, status_qubit2), (default_symbol, default_symbol))
    return new_status[0], new_status[1]


def apply_step(step, status, asociations):
    gate_to_apply = step[0]
    first_qubit_afected = step[1]
    is_one_qubit = True if len(step) == 2 else False
    is_two_qubit = True if len(step) == 3 else False
    if is_one_qubit:
        status[first_qubit_afected] = calculate_one_qubit_evolution(asociations.get(gate_to_apply), status[first_qubit_afected])
    elif is_two_qubit:
        second_qubit_afected = step[2]
        status[first_qubit_afected], status[second_qubit_afected] = \
            calculate_two_qubit_evolution(asociations.get(gate_to_apply), status[first_qubit_afected], status[second_qubit_afected])
    else:
        print "Malformed Status"


def execute(initial_status, associations, quantum_program):
    status_count = 0
    status = Quantum_Status(initial_status, associations)
    print "Initial Status:", status
    for step in quantum_program:
        status.apply_step(step)
        print step, "->", status
    # status = initial_status
    # print "Status ", status_count, ":", status
    # for step in quantum_program:
    #     apply_step(step, status, associations)
    #     status_count += 1
    #     print "Status ", status_count,step,":", status
