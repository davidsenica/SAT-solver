import sys
from file_reader import read
from classes import Clause


class DDLL:
    def __init__(self, formula):
        self.formula = formula
        self.var = {}
        for c in formula:
            for i in c:
                self.var[i[0]] = None

    def add_unit(self, clause):
        self.formula.append(clause)

    def find_first_unit(self):
        for c in self.formula:
            if len(c) == 1:
                return c.clause[0]
        return None

    def find_pure(self):
        for v in self.var.keys():
            is_pure = True
            is_in_formula = False
            for c in self.formula:
                for l in c:
                    if l[0] == v and l[1]:
                        is_in_formula = True
                    if l[0] == v and not l[1]:
                        is_pure = False
                        break
                if not is_pure:
                    break
            if is_pure and is_in_formula:
                return v
        return None

    def remove(self, literal):
        self.var[literal[0]] = literal[1]
        modified = self.formula.copy()
        for clause in self.formula:
            if literal in clause:
                modified.remove(clause)
            elif (literal[0], not literal[1]) in clause:
                modified.remove(clause)
                tmp = clause.copy()
                tmp.remove((literal[0], not literal[1]))
                modified.append(tmp)
        self.formula = modified

    def copy(self):
        new = DDLL([])
        new.formula = self.formula.copy()
        new.var = self.var.copy()
        return new


def solve_DDLL(alg_DDLL, depth, vars):
    curr = alg_DDLL.copy()
    while True:
        unit = curr.find_first_unit()
        if unit is not None:
            curr.remove(unit)
            continue
        pure = curr.find_pure()
        if pure is not None:
            curr.remove((pure, True))
        else:
            break
    if not curr.formula:
        return True, curr.var
    else:
        c = Clause([()])
        if c in curr.formula or depth == len(vars):  # Check if this ok
            return False, None
        c1 = curr.copy()
        c1.add_unit((vars[depth], True))
        truth, evaluation = solve_DDLL(c1, depth + 1, vars)
        if truth:
            return True, evaluation
        c2 = curr.copy()
        c2.add_unit((vars[depth], False))
        truth, evaluation = solve_DDLL(c2, depth + 1, vars)
        if not truth:
            return False, None


def solve(cnf):
    d = DDLL(cnf)
    result = solve_DDLL(d, 0, list(d.var.keys()))
    #
    # if result[0]:
    #     for k in result[1].keys():
    #         if result[1][k] is None:
    #             result[1][k] = True
    return result


if __name__ == '__main__':
    cnf,_,_ = read(sys.argv[1])
    print(solve(cnf))
