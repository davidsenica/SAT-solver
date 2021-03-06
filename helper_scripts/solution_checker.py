import sys


def read_file(file):
    with open(file) as f:
        line = f.readline().strip()
        return set(map(int, line.split(" ")))


def check_file(file1, file2):
    set1 = read_file(file1)
    set2 = read_file(file2)
    set1.difference(set2)
    d1 = set1.difference(set2)
    d2 = set2.difference(set1)
    if d1 != set():
        print(d1)
    elif d2 != set():
        print(d2)
    else:
        print('Solutions are identical')


if __name__ == '__main__':
    check_file(sys.argv[1], sys.argv[2])
