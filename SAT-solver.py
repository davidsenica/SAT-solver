import random
import sys
import copy
import operator


class DPLL:
    def __init__(self, formula, all_diff_vars, counter):
        self.formula = formula
        self.all = all_diff_vars
        self.counter = counter
        self.var = set()

    def add_unit(self, clause):
        if abs(clause[0]) not in self.counter:
            self.counter.append(abs(clause[0]))
        self.all.add(clause[0])
        self.formula.append(clause)

    def clean_unit(self):
        cleaned = False
        for c in self.formula:
            if len(c) == 1:
                cleaned = True
                self.remove(c[0])
        return cleaned

    def clean_pure(self):
        cleaned = False
        for v in self.counter:
            if v in self.all and v > 0 and -v not in self.all:
                cleaned = True
                self.remove(v)
        return cleaned

    def remove(self, literal):
        if -literal in self.var:
            self.var.remove(-literal)
        self.var.add(literal)
        if literal in self.all:
            self.all.remove(literal)
        if -literal in self.all:
            self.all.remove(-literal)
        if abs(literal) in self.counter:
            self.counter.remove(abs(literal))
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
        new = DPLL(copy.deepcopy(self.formula), copy.deepcopy(self.all),
                   copy.deepcopy(self.counter))
        new.var = copy.deepcopy(self.var)
        return new


def read(filepath):
    with open(filepath, "r") as f:
        nbvar, nbclauses = -1, -1
        clauses = []  # Final array of Clauses
        counter = {}
        diff_vars = set()
        for line in f:
            row = line.strip()
            # Comments - ignore
            if row[0] == 'c':
                continue
            row = row.split()
            # If p -> save number of variables and clauses
            if row[0] == 'p':
                nbvar = int(row[2])
                nbclauses = int(row[3])
            # Else create clause and add it to result
            else:
                clause = []
                for r in row:
                    num = int(r)
                    if num == 0:
                        continue
                    clause.append(num)
                    diff_vars.add(num)
                    if num in counter:
                        counter[abs(num)] = counter[abs(num)] + 1
                    else:
                        counter[abs(num)] = 1
                clauses.append(clause)
    counter_sorted = [k for k, v in sorted(counter.items(), key=lambda item: item[1], reverse=True)]
    return DPLL(clauses, diff_vars, counter_sorted)


def write_file(filepath, vars):
    with open(filepath, 'w') as f:
        if vars is None:
            f.write('0')
        else:
            for num in vars:
                f.write(str(num) + ' ')


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
        l = curr.counter[0]
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


if __name__ == '__main__':
    import time
    start = time.time()
    dpll = read(sys.argv[1])
    truth, vars = solve_DPLL(dpll)
    print("Solver ran for %s s" % (time.time() - start))
    write_file(sys.argv[2], vars)
