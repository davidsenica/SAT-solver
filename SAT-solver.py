import random
import sys
from file_reader import read, write_file
import copy
from classes import Clause


class DPLL:
    def __init__(self, formula):
        self.formula = formula
        tmp = set()
        self.all = set()
        for c in formula:
            for i in c:
                tmp.add(abs(i))
                self.all.add(i)
        self.diff = list(tmp)
        self.var = []

    def add_unit(self, clause):
        self.all.add(clause[0])
        self.formula.append(clause)

    def clean_unit(self):
        cleaned = False
        for c in self.formula:
            if len(c) == 1:
                cleaned = True
                self.remove(c[0])
        return cleaned

    def find_first_unit(self):
        for c in self.formula:
            if len(c) == 1:
                return c[0]
        return None

    def find_pure(self):
        for v in self.diff:
            if v in self.all and v > 0 and -v not in self.all:
                return v
        # for v in self.var:
        #     is_pure = True
        #     is_in_formula = False
        #     for c in self.formula:
        #         for l in c:
        #             if abs(l) == abs(v):
        #                 if l > 0:
        #                     is_in_formula = True
        #                 else:
        #                     is_pure = False
        #                     break
        #         if not is_pure:
        #             break
        #     if is_pure and is_in_formula:
        #         return v
        return None

    def clean_pure(self):
        cleaned = False
        for v in self.diff:
            if v in self.all and v > 0 and -v not in self.all:
                cleaned = True
                self.remove(v)
        return cleaned

    def remove(self, literal):
        if -literal in self.var:
            self.var.remove(-literal)
        self.var.append(literal)
        if literal in self.all:
            self.all.remove(literal)
        if -literal in self.all:
            self.all.remove(-literal)
        modified = []
        for clause in self.formula:
            if literal in clause:
                continue
            elif -literal in clause:
                tmp = clause.copy()
                tmp.remove(-literal)
                modified.append(tmp)
            else:
                modified.append(clause)
        self.formula = modified

    def copy(self):
        new = DPLL([])
        new.formula = copy.deepcopy(self.formula)
        new.var = copy.deepcopy(self.var)
        new.all = copy.deepcopy(self.all)
        new.diff = copy.deepcopy(self.diff)
        return new


def solve_DPLL(alg_DPLL):
    curr = alg_DPLL.copy()
    while True:
        cleaned_unit = curr.clean_unit()
        cleaned_pure = curr.clean_pure()
        if not cleaned_unit and not cleaned_pure:
            break
    if not curr.formula:
        return True, curr.var
    else:
        c = []
        if c in curr.formula:  # Check if this ok
            return False, None
        l = abs(random.sample(curr.all, 1)[0])
        c1 = curr.copy()
        c1.add_unit([l])
        truth1, evaluation1 = solve_DPLL(c1)

        c2 = curr.copy()
        c2.add_unit([-l])
        truth2, evaluation2 = solve_DPLL(c2)

        t = truth1 or truth2
        if truth1:
            eval = evaluation1
        else:
            eval = evaluation2

        return t, eval


def solve(cnf):
    d = DPLL(cnf)
    result = solve_DPLL(d)
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
