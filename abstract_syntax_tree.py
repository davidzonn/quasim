class AST:

    def __init__(self, name, *children):
        self.name = name
        self.children = children

    def __str__(self):
        return self.name + str([x.name for x in self.children])

    def __iter__(self):
        return iter(self.children)