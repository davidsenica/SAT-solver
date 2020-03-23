import sys
from file_reader import read, write_file
from classes import Clause


class DPLL:
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
                return c[0]
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
        new = DPLL([])
        new.formula = self.formula.copy()
        new.var = self.var.copy()
        return new


def solve_DPLL(alg_DPLL, depth, vars):
    curr = alg_DPLL.copy()
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
        c = []
        if c in curr.formula or depth == len(vars):  # Check if this ok
            return False, None
        c1 = curr.copy()
        c1.add_unit([(vars[depth], True)])
        truth1, evaluation1 = solve_DPLL(c1, depth + 1, vars)

        c2 = curr.copy()
        c2.add_unit([(vars[depth], False)])
        truth2, evaluation2 = solve_DPLL(c2, depth + 1, vars)

        t = truth1 or truth2
        if truth1:
            eval = evaluation1
        else:
            eval = evaluation2

        return t, eval


def solve(cnf):
    d = DPLL(cnf)
    result = solve_DPLL(d, 0, list(d.var.keys()))
    #
    # if result[0]:
    #     for k in result[1].keys():
    #         if result[1][k] is None:
    #             result[1][k] = True
    return result


if __name__ == '__main__':
    cnf,_ ,_ = read(sys.argv[1])
    import time
    start = time.time()
    truth, vars = solve(cnf)
    print("Program ran for %s s" % (time.time() - start))
    write_file('solution.txt', vars)
    print(vars)
