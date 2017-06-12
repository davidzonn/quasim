import pygraphviz as pg
from sympy import Pow

## Transforms from sympy into pygraphviz for easier graphical representation.
def sympy_to_pygraphviz(sympy_tree):
    pg_graph = pg.AGraph(directed=True, strict=False)
    add_to_graph(pg_graph, sympy_tree)
    # print pg_graph
    return pg_graph




##Recursively add edges of sympy graph into pygraphviz one.

node_number = 0
def add_to_graph(pg_graph, node):

    global node_number

    u = node_number
    ulabel = node.func.__name__

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
    pg_graph = pg.AGraph(directed=True, strict=True)
    return add_to_programpgraph(pg_graph, quantum_program)

counter = 0

def add_to_programpgraph(pg_graph, quantum_program):
    global counter
    if hasattr(quantum_program, "name"): #If not leaf

        ulabel = quantum_program.name
        u = str(quantum_program)

        for child in quantum_program.children:
            if hasattr(child, "name"):
                v = str(child)
                vlabel = child.name
            else: #Primitive type
                v = counter
                counter = counter + 1
                vlabel = str(child)

            pg_graph.add_node(u, label=ulabel)
            pg_graph.add_node(v, label=vlabel)
            pg_graph.add_edge(u, v)

            add_to_programpgraph(pg_graph, child)

    return pg_graph

