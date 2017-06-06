
class AST:

    def __init__(self, name, *children):
        self.name = name
        self.children = children

    def __str__(self):
        # return self.name + str(map(str, self.children))
        ans = self.name + "{"
        for i, x in enumerate(self.children):
            ans += ("," if i else "") + str(x)
        ans += "}"
        return ans

    def __iter__(self):
        return iter(self.children)