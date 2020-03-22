import numpy as np

from classes import Clause, Literal


def read(filepath):
    with open(filepath, "r") as f:
        nbvar, nbclauses = -1, -1
        clauses = []  # Final array of Clauses

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
                row = list(map(int, row))
                row.remove(0)

                clause = Clause([Literal(int(np.cbrt(nbvar)), abs(num), num > 0) for num in row])
                clauses.append(clause)

    return clauses, nbvar, nbclauses


def write(filepath, literals):
    """
    :param literals: List of Literal objects, returned by DPLL
    """
    with open(filepath, "w") as f:
        for l in literals:
            number = (l.base ** 2) * (l.x - 1) + l.base * (l.y - 1) + l.z
            if not l.orientation:
                number *= -1
            f.write(str(number) + " ")


if __name__ == '__main__':
    data, num_vars, num_claueses = read("tests/sudoku_mini.txt")
    for d in data:
        print(d)

    # Write test
    # write("test.txt", [data[10].clause[0], data[10].clause[1]])
