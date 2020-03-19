import sys
from file_reader import read
from classes import Clause


def DDLL(cnf):
    pass


def solve(cnf):
    pass


if __name__ == '__main__':
    cnf = read(sys.argv[1])
    for c in cnf:
        print(c)
    solve(cnf)
