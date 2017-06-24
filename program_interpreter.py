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
from sympy import Symbol
from sympy import Mul
from sympy import Add

import graphics.tools as tools

from gates.constants import *
from status_interpreter import normalize
from status_tree import Quantum_Status
from gates.constants import tensor_product

from program_parser.abstract_syntax_tree import AST


class Quantum_Interpreter:

    generate_graphical_output = False #Requires dot program

    step_number = 1

    bold = "\033[1m"
    end_bold = "\033[0;0m"

    def __init__(self, initial_status, associations, program):
        self.status = Quantum_Status(initial_status, associations)

        self.generate_status_output("Initial Status", self.status.status)
        self.generate_program_output(program)
        self.generate_transformations_output()

        self.status.status = self.execute(program, self.status.status)


    def generate_transformations_output(self):
        if self.generate_graphical_output:
            kron = tensor_product.unicode_representation
            tree = AST("T")
            tree1 = AST("T1")
            tree2 = AST("T2")
            tree3 = AST("T3")
            tree4 = AST("T4")
            trees = AST("T*")
            trees1 = AST("T*1")
            trees2 = AST("T*2")
            trees3 = AST("T*3")
            trees4 = AST("T*4")
            number = AST("NumExpr")
            number1 = AST("NumExpr 1")
            number2 = AST("NumExpr 2")
            mul = tools.multiplication_representation
            add = tools.addition_representation

            T1L = AST(kron, trees1, AST(mul, trees2, number, trees3), trees4)
            T1R = AST(mul, AST(kron, trees1, AST(mul, trees2, trees3), trees4), number) #Mult by Scalar

            # T2L = AST(kron, trees1, AST(mul, trees2, number, trees3), trees4)
            # T2R = AST(mul, AST(kron, trees1, trees2, trees3, trees4), number) #Tensor of Mult.

            T2L = AST(kron, trees1, AST(add, trees2, trees3), trees4)
            T2R = AST(add, AST(kron, trees1, trees2, trees4), AST(kron, trees1, trees3, trees4)) #Dist. Tensor

            T3L = AST(mul, trees1, AST(add, trees2, trees3), trees4)
            T3R = AST(add, AST(mul, trees1, trees2, trees4), AST(mul, trees1, trees3, trees4)) #Dist. Mult.

            T4L = AST(add, trees1, AST(mul, trees2, number1), trees3, AST(mul, trees2, number2), trees4)
            T4R = AST(add, trees1, AST(mul, trees2, AST(number1.name + " + \n" + number2.name)),trees3, trees4) #Similar terms

            T5L = AST(mul, trees1, AST(mul, trees2), trees3)
            T5R = AST(mul, trees1, trees2, trees3)#mult. fusioning

            T6L = AST(add, trees1, AST(add, trees2), trees3)
            T6R = AST(add, trees1, trees2, trees3)#add. fusioning

            transformations = {"T1L": T1L,  "T1R": T1R, "T2L": T2L, "T2R": T2R, "T3L": T3L,"T3R": T3R,
                               "T4L": T4L,"T4R": T4R, "T5L": T5L,"T5R": T5R, "T6L": T6L,"T6R": T6R}

            for key in transformations.keys():
                name = key
                program = transformations[key]
                pygraphviz_representation = tools.program_to_pygraphviz(program)
                tools.print_graph(pygraphviz_representation, name)


            pygraphviz_representation = tools.program_to_pygraphviz(T1R)
            tools.print_graph(pygraphviz_representation, "T1R")



    def generate_program_output(self, program):
        if self.generate_graphical_output:
            pygraphviz_representation = tools.program_to_pygraphviz(program)
            tools.print_graph(pygraphviz_representation, "Quantum Program")


    def generate_status_output(self, label, sympy_status):

        print Quantum_Interpreter.bold, str(self.step_number) + ": ", label, "->", Quantum_Interpreter.end_bold, sympy_status

        if self.generate_graphical_output:
            pygraphviz_representation = tools.sympy_to_pygraphviz(sympy_status)
            tools.print_graph(pygraphviz_representation, str(self.step_number) + "("+label+")")
            self.step_number = self.step_number + 1


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

        self.generate_status_output(str(instruction), new_status)

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