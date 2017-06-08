import sympy
def sympy_to_graphviz(sympy_graph):
    graph = sympy._dict_from_expr(sympy_graph)
    print graph