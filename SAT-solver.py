import sys
import copy


class DPLL:
    def __init__(self, formula, all_diff_vars, counter):
        self.formula = formula
        self.all = all_diff_vars
        self.counter = counter
        self.var = set()

    def add_unit(self, clause):
        self.all.add(clause[0])
        self.formula.append(clause)

    def clean_unit(self):
        cleaned = False
        for c in self.formula:
            if len(c) == 1:
                cleaned = True
                self.remove(c[0])
                break
        return cleaned

    def clean_pure(self):
        cleaned = False
        for v in self.counter:
            if v < 0:
                continue
            if -v not in self.all:
                cleaned = True
                self.remove(v)
                break
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
    stack = []
    curr = alg_DPLL.copy()
    while True:
        cleaned_unit = True
        cleaned_pure = True
        while cleaned_unit or cleaned_pure:
            cleaned_unit = curr.clean_unit()
            cleaned_pure = curr.clean_pure()
        if not curr.formula:
            return True, curr.var
        else:
            c = []
            if c in curr.formula:  # Check if this ok
                if len(stack) == 0:
                    return False, None
                l = stack.pop()
                curr = l[1]
                curr.add_unit([-l[0]])
                continue

            l = None
            for i in range(len(curr.counter)):
                l = curr.counter[i]
                if l in curr.all or -l in curr.all:
                    break
                else:
                    curr.counter.remove(l)

            stack.append((l, curr.copy()))
            curr.add_unit([l])


if __name__ == '__main__':
    import time
    start = time.time()
    dpll = read(sys.argv[1])
    truth, vars = solve_DPLL(dpll)
    print("Solver ran for %s s" % (time.time() - start))
    write_file(sys.argv[2], vars)
