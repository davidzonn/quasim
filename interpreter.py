##TODO##, semantic analyser
from sympy import *
from constants import *

##returns a flag indicating if any modification was made and the modified tree.
def apply_transformation(tree):
    modifications = false
    if not tree.args: #Is a leaf
        pass
    else: #is a function
        if isinstance(tree, tensor_product):
            children = tree.args
            i = 0
            for child in children:
                if isinstance (child, Mul):
                    tree_children = list()
                    numerical_children = list()
                    for child_child in child.args:
                        if child_child.is_Number or child_child.is_Pow:
                            numerical_children.append(child_child)
                        else:
                            tree_children.append(child_child)
                    tensor_children = children[:i] + tuple(tree_children) + children[i+1:]
                    tensor_child = tensor_product(*tensor_children)
                    tree = Mul(tensor_child, *numerical_children)
                    modifications = true
                    break

                if isinstance (child, Add):
                    trees_left = children[:i] + (child.args[0],) + children[i+1:]
                    trees_right = children[:i] + child.args[1:] + children[i+1:]
                    tree_left = tensor_product(*trees_left)
                    tree = Add(tensor_product(*trees_left), tensor_product(*trees_right))
                    modifications = true
                i += 1

            #If one children is mult apply transf 1.
            #If one children is add
        else:
            new_subtrees = []
            for subtree in tree.args:
                answer_subtree = apply_transformation(subtree)
                modifications = modifications or answer_subtree[0]
                new_subtrees.append(answer_subtree[1])
            tree = tree.func(*new_subtrees)
    return modifications, tree


def normalize(tree):
    # print "TRANSFORMATION BEFORE: ", tree
    transformed_status = apply_transformation(tree)
    while (transformed_status[0]): #A change was made
        transformed_status = apply_transformation(transformed_status[1])
    # print "TRANSFORMATION AFTER: ", transformed_status[1]
    return transformed_status[1]
