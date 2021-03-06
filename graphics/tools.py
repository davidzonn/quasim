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


import pygraphviz as pg


from sympy import Pow
# from ...gates import constants
## Transforms from sympy into pygraphviz for easier graphical representation.

multiplication_representation = u"\u00D7"
addition_representation = u"\u002B"
tensor_product_representation = u"\u2297"
quality_dpi = 1000

def sympy_to_pygraphviz(sympy_tree):
    global quality_dpi
    pg_graph = pg.AGraph(directed=True, strict=False, dpi = quality_dpi)
    add_to_graph(pg_graph, sympy_tree)
    # print pg_graph
    return pg_graph



##Recursively add edges of sympy graph into pygraphviz one.

node_number = 0
def add_to_graph(pg_graph, node):

    global node_number, multiplication_representation, addition_representation

    u = node_number
    ulabel = node.func.__name__
    if hasattr(node, 'unicode_representation'):
        ulabel = node.unicode_representation
    if node.is_Add:
        ulabel = addition_representation
    if node.is_Mul:
        ulabel = multiplication_representation
    #
    # if node.is_Pow: #First child number, second child the exponent.
    #     ulabel = node.func.__name__
    #     vlabel =

    for child in node.args:

        node_number = node_number + 1
        v = node_number


        if child.is_Number: #Child is Leaf

            vlabel = str(child) #The string representation of the number.

            # ulabel = str(node.func)
            # vlabel = str(child.func)

            pg_graph.add_node(u, label=ulabel)
            pg_graph.add_node(v, label=vlabel)

            pg_graph.add_edge(u, v)

        elif child.is_Symbol: #Child is leaf

            # u = str(node)
            # v = str(child)

            vlabel = str(child) #The string representation of the number.



            # ulabel = str(node.func)
            # vlabel = str(child.func)

            pg_graph.add_node(u, label=ulabel)
            pg_graph.add_node(v, label=vlabel)

            pg_graph.add_edge(u, v)
            # counter = counter + 1


        else: #Child is intermediate node

            # u = str(node)
            # v = str(child)

            vlabel = child.func.__name__

            # ulabel = str(node.func)
            # vlabel = str(child.func)

            pg_graph.add_node(u, label=ulabel)
            pg_graph.add_node(v, label=vlabel)

            pg_graph.add_edge(u, v)
            add_to_graph(pg_graph, child) #Same for all children.

        node_number = node_number + 1

### Prints pygraphviz-represented graph into file_name file.
def print_graph(pg_graph, file_name):
    file_name = "img/" + file_name + ".png"
    pg_graph.draw(file_name, prog = 'dot')


def program_to_pygraphviz(quantum_program):
    global quality_dpi
    pg_graph = pg.AGraph(directed=True, strict=True, dpi = quality_dpi)
    return add_to_programpgraph(pg_graph, quantum_program)

counter = 0
def add_to_programpgraph(pg_graph, quantum_program):
    global counter
    if hasattr(quantum_program, "name"): #If not leaf

        # u = str(quantum_program)
        u = counter

        ulabel = quantum_program.name

        for child in quantum_program.children:

            counter = counter + 1
            v = counter

            if hasattr(child, "name"):
                # v = str(child)
                vlabel = child.name
            else: #Primitive type
                if isinstance(child, int):
                    vlabel = str(child + 1)
                else:
                    # v = counter
                    # counter = counter + 1
                    vlabel = str(child)

            pg_graph.add_node(u, label=ulabel)
            pg_graph.add_node(v, label=vlabel)
            pg_graph.add_edge(u, v)

            add_to_programpgraph(pg_graph, child)

    return pg_graph

