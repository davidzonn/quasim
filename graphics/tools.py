import pygraphviz as pg

## Transforms from sympy into pygraphviz for easier graphical representation.
def sympy_to_pygraphviz(sympy_tree):
    pg_graph = pg.AGraph(directed=True, strict=False)
    add_to_graph(pg_graph, sympy_tree)
    # print pg_graph
    return pg_graph




##Recursively add edges of sympy graph into pygraphviz one.
def add_to_graph(pg_graph, node):

    for child in node.args:

        if child.is_Number or child.is_Symbol: #Is Leaf

            u = str(node)
            v = str(child)

            ulabel = node.func.__name__
            vlabel = str(child) #The string representation of the number.

            # ulabel = str(node.func)
            # vlabel = str(child.func)

            pg_graph.add_node(u, label=ulabel)
            pg_graph.add_node(v, label=vlabel)

            pg_graph.add_edge(u, v)

        else:

            u = str(node)
            v = str(child)

            ulabel = node.func.__name__
            vlabel = child.func.__name__

            # ulabel = str(node.func)
            # vlabel = str(child.func)

            pg_graph.add_node(u, label=ulabel)
            pg_graph.add_node(v, label=vlabel)

            pg_graph.add_edge(u, v)
            add_to_graph(pg_graph, child) #Same for all children.


### Prints pygraphviz-represented graph into file_name file.
def print_graph(pg_graph, file_name):
    file_name = "img/" + file_name + ".png"
    pg_graph.draw(file_name, prog = 'dot')
