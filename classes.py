class Clause:
    def __init__(self, clause):
        self.clause = clause

    def __str__(self):
        output = ''
        for literal in self.clause:
            output += str(literal)
            output += ' ∨ '
        return output[:-3]

    def __len__(self):
        return len(self.clause)

    def drop_remove(self, item):
        c = (item[0], not item[1])
        self.clause.remove(c)
        return item in self.clause  # return True if we need to remove literal


class Literal:
    def __init__(self, base, number, orientation):
        self.base = base

        if number % (self.base ** 2) != 0:
            self.x = int(number / (self.base ** 2)) + 1  # row x
            number = number % (self.base ** 2)
        else:
            self.x = int(number / (self.base ** 2))
            number = self.base ** 2

        if number % self.base != 0:
            self.y = int(number / self.base) + 1  # column y
            number = number % self.base
        else:
            self.y = int(number / self.base)
            number = self.base
        self.z = number  # contains z

        self.orientation = orientation  # Positive/negative

    def __str__(self):
        output = ''
        if not self.orientation:
            output += '¬'
        output += 'P_' + str(self.x) + str(self.y) + str(self.z)
        return output