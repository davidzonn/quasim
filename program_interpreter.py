from sympy import Symbol

import graphics.tools as tools

from gates.constants import *
from status_interpreter import normalize
from status_tree import Quantum_Status


class Quantum_Interpreter:

    step_number = 0

    bold = "\033[1m"
    end_bold = "\033[0;0m"

    def __init__(self, initial_status, associations, program):
        self.status = Quantum_Status(initial_status, associations)

        print Quantum_Interpreter.bold, "(Initial Status):", Quantum_Interpreter.end_bold, self.status
        # tools.print_graph(self.status.status, str(self.step_number) + "("+program.name+")")


        self.status.status = self.execute(program, self.status.status)


    #Analyse the AST instruction, according to it evolves the status.
    def execute(self, instruction, status):

        instruction_name = instruction.name

        if instruction_name == "sequence": #Is a sequence of commands
            new_status = status #Starts as the old status
            for step in instruction:
                new_status = self.execute_command(step, new_status) #Evolves

        else: #IS COMMAND
            new_status = self.execute_command(instruction, status)

        return new_status

    def execute_command(self, instruction, status):

        function_to_apply = instruction.name
        args = instruction.children

        if function_to_apply == 'if':  # If Statement
            new_status = self.ifthenelse(status, args[0], args[1], args[2])

        elif function_to_apply == 'skip':
            new_status = status

        else: #Is a Gate
            gate = Symbol(function_to_apply)
            if gate in self.status.associations:
                number_of_arguments = len(args)

                if number_of_arguments == 1:
                    new_status = self.status.apply_one_qubit_operator(gate, status, args[0])
                elif number_of_arguments == 2:
                    new_status = self.status.apply_two_qubit_operator(gate, status, args[0], args[1])

            else:
                print "WARNING: Unknown function \"" + function_to_apply + "\". Skipping. " \
                      + "Try with " + str([x for x in self.status.associations])
                new_status = status

            new_status = normalize(new_status)

        # self.status.status = new_status

        # self.status.status = self.status.calculate_new_status(instruction, self.status.status)

        print Quantum_Interpreter.bold, str(self.step_number) + ": ", instruction, "->", Quantum_Interpreter.end_bold, new_status

        pygraphviz_representation = tools.sympy_to_pygraphviz(new_status)
        tools.print_graph(pygraphviz_representation, str(self.step_number) + "("+instruction.name+")")
        self.step_number = self.step_number + 1

        return new_status

    def ifthenelse(self, status_tree, qubit, if_instructions, else_instructions):


        # true_status = self.status.apply_one_qubit_operator(True, status_tree, qubit)
        # false_status = self.status.apply_one_qubit_operator(False, status_tree, qubit)
        # true_application = self.execute(if_instructions, true_status)
        # false_application = self.execute(else_instructions, false_status)
        # return normalize(sympy.Add(true_application, false_application))



        true_status = normalize(self.status.apply_one_qubit_operator(True, status_tree, qubit))
        false_status = normalize(self.status.apply_one_qubit_operator(False, status_tree, qubit))
        # print "TRUE MEASSUREMENT ", true_status, ";\t\tFALSE MEASSUREMENT", false_status
        true_application = normalize(self.execute(if_instructions, true_status))
        false_application = normalize(self.execute(else_instructions, false_status))
        # print "TRUE APPLICATION ", true_application, "\t\tFALSE APPLICATION", false_application
        return normalize(sympy.Add(true_application, false_application))