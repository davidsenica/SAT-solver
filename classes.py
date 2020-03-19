class Clause:
    def __init__(self, clause):
        self.clause = clause

    def __str__(self):
        output = ''
        for c in self.clause:
            if c[1]:
                output += c[0]
            else:
                output += '¬' + c[0]
            output += ' ∨ '
        return output[:-3]

    def __len__(self):
        return len(self.clause)

    def drop_remove(self, item):
        c = (item[0], not item[1])
        self.clause.remove(c)
        return item in self.clause  # return True if we need to remove literal

