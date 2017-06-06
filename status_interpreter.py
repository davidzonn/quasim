##TODO##, semantic analyser
import sympy as sympy

from gates import constants


##returns a flag indicating if any modification was made and the modified tree.
def apply_transformation(tree):
    modifications = False
    if not tree.args: #Is a leaf
        pass
    else: #is a function
        if isinstance(tree, constants.tensor_product):
            children = tree.args
            i = 0
            for child in children:

                if isinstance (child, sympy.Mul):
                    tree_children = list()
                    numerical_children = list()
                    for child_child in child.args:
                        if child_child.is_Number or child_child.is_Pow:
                            numerical_children.append(child_child)
                        else:
                            tree_children.append(child_child)
                    tensor_children = children[:i] + tuple(tree_children) + children[i+1:]
                    tensor_child = constants.tensor_product(*tensor_children)
                    tree = sympy.Mul(tensor_child, *numerical_children)
                    modifications = True
                    break

                if isinstance (child, sympy.Add):
                    trees_left = children[:i] + (child.args[0],) + children[i+1:]
                    trees_right = children[:i] + child.args[1:] + children[i+1:]
                    tree_left = constants.tensor_product(*trees_left)
                    tree = sympy.Add(constants.tensor_product(*trees_left), constants.tensor_product(*trees_right))
                    modifications = True
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
    transformed_status = list(apply_transformation(tree))
    while (transformed_status[0]): #A change was made
        transformed_status = list(apply_transformation(transformed_status[1]))
    # print "TRANSFORMATION AFTER: ", transformed_status[1]
    #print "BEFORE SYMPY", transformed_status[1]
    transformed_status[1] = sympy.simplify(transformed_status[1])
    #print "AFTER SYMPY", transformed_status[1]
    return sympy.expand(transformed_status[1])

