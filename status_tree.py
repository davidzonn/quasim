import sympy
from sympy import *
from collections import Sequence
from status_interpreter import normalize
from constants import *
from lexical_analyser import tokens




class Quantum_Status:

    def __init__(self, status_array, associations, if_associations):
        self.associations = associations
        self.status = self.fuse_qubits(status_array)
        self.status = normalize(self.status)
        self.associations.update(if_associations)

    def fuse_qubits(self, status_array):
        status = tensor_product(*status_array)
        return status

    def apply_step(self, step):
        if isinstance(step, Sequence) and 2 <= len(step) <= 3:
            gate_to_apply = step[0]
            qubit1 = step[1]
            if len(step) == 2: # one qubit
                self.status = self.apply_one_qubit_operator(gate_to_apply, self.status, qubit1)
            else: # two qubit
                qubit2 = step[2]
                self.status = self.apply_two_qubit_operator(gate_to_apply, self.status, qubit1, qubit2)
            self.status = normalize(self.status)
        elif isinstance(step, Sequence) and len(step) == 5 and step[0] == quantum_if:
            measurement_basis = step[1]
            qubit_to_measure = step[2]
            if_instructions = step[3]
            else_instructions = step[4]
            self.status = self.apply_measurement(measurement_basis, self.status, qubit_to_measure, if_instructions, else_instructions)
            self.status = normalize(self.status)
        else:
            print "Malformed Status. Expected (Gate, q1[, q2])* or (quantum_if, measurement_basis, qubit_to_measure, if_block, else_block). Received: ", step
        pass

    #Traverse recursively the tree Assumes tree is "normalized"
    def apply_one_qubit_operator(self, gate, status_tree, qubit1):
        if isinstance(status_tree, tensor_product):
            previous_children = status_tree.args
            previous_element = previous_children[qubit1]
            try:
                new_element = self.associations[gate][previous_element]
            except Exception:
                new_element = unknown_node # "Unknown" node if it gate or qubit association not in mapping
            if new_element == nought:
                new_children = previous_children[:qubit1] + previous_children[qubit1 + 1:]
            else:
                new_children = previous_children[:qubit1] + (new_element,) + previous_children[qubit1 + 1:]
            return tensor_product(*new_children)
        elif isinstance(status_tree, Mul) or isinstance(status_tree, Add):
            return status_tree.func(*[self.apply_one_qubit_operator(gate, x, qubit1) for x in status_tree.args]) #Apply to all children
        else:
            return status_tree # it was an end Symbol (ex, a number)


        # # print "Tree representation: ", srepr(status_before), " String Representation", status_before
        # default_symbol = sympy.Symbol("Unknown")
        #
        # if isinstance(status_before, Symbol):  # Is symbol leaf
        #     status_after = gate_associations.setdefault(status_before,
        #                                                 default_symbol)  # If the root is a symbol, apply operator
        # elif not status_before.args:  # No children, is leaf
        #     status_after = status_before
        # else:
        #     new_arguments = [calculate_one_qubit_evolution(gate_associations, x) for x in
        #                      status_before.args]  # Recursively apply to all children.
        #     status_after = status_before.func(*new_arguments)
        # return status_after

    #Traverse recursively the tree
    def apply_two_qubit_operator(self, gate, status_tree, qubit1, qubit2):
        if isinstance(status_tree, tensor_product):
            previous_children = status_tree.args
            previous_element_1 = previous_children[qubit1]
            previous_element_2 = previous_children[qubit2]

            try:
                new_elements = (self.associations[gate][(previous_element_1, previous_element_2)])
            except Exception:
                new_elements = (unknown_node, unknown_node) # "Unknown" node if it gate or qubit association not in mapping
            new_children = list(previous_children)
            new_children[qubit1] = new_elements[0]
            new_children[qubit2] = new_elements[1]
            return tensor_product(*new_children)
        elif isinstance(status_tree, Mul) or isinstance(status_tree, Add):
            recursive_apply = [self.apply_two_qubit_operator(gate, x, qubit1, qubit2) for x in status_tree.args]
            return status_tree.func(*recursive_apply) #Apply to all children
        else:
            return status_tree # it was an end Symbol (ex, a number)



    def apply_measurement(self, measurement_base, status_tree, qubit_to_measure, if_instructions, else_instructions):
        if isinstance(status_tree, tensor_product):
            previous_children = status_tree.args
            new_children = previous_children[:qubit_to_measure] + (measurement_base, ) + previous_children[qubit_to_measure + 1:]
            return tensor_product(*new_children)
        else:
            recursive_apply = [self.apply_measurement(measurement_base, x, qubit_to_measure, if_instructions, else_instructions) for x in status_tree.args]
            return status_tree.func(*recursive_apply)

    def __str__(self):
        return str(self.status)# + "\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t===TREE(" + srepr(self.status) + "==="

    def calculate_new_status(self, step, status):

        function_to_apply = step.name
        gate = Symbol(function_to_apply)
        args = step.children

        if function_to_apply == 'if':  # If Statement
            new_status = self.ifthenelse(status, args[0], args[1], args[2])
        elif function_to_apply == 'skip':
            new_status = status
        elif gate in self.associations:
            number_of_arguments = len(args)
            if number_of_arguments == 1:
                new_status = self.apply_one_qubit_operator(gate, status, args[0])
            elif number_of_arguments == 2:
                new_status = self.apply_two_qubit_operator(gate, status, args[0], args[1])
            new_status = normalize(new_status)
        else:
            print "WARNING: Unknown function " + function_to_apply + ". Skipping. " \
                  + "Try with " + str([x for x in self.associations])
            new_status = status
        return new_status

    def apply_AST_step(self, step):
        self.status = self.calculate_new_status(step, self.status)


    def ifthenelse(self, status_tree, qubit, if_instructions, else_instructions):
        true_status = normalize(self.apply_one_qubit_operator(True, status_tree, qubit))
        true_application = self.calculate_new_status(if_instructions, true_status)
        false_status = normalize(self.apply_one_qubit_operator(False, status_tree, qubit))
        false_application = self.calculate_new_status(else_instructions, false_status)
        print "TRUE MEASSUREMENT ", true_status, ";\t\tTRUE APPLICATION ", true_application, ";\t\tFALSE MEASSUREMENT", false_application, ";\t\tFALSE APPLICATION", false_application
        return sympy.Add(true_application,false_application)
