import sys
import numpy

def read_file(file):
    with open(file) as f:
        line = f.readline().strip()
        return set(map(int, line.split(" ")))

def create_table(file, n):
    mnozica = read_file(file)
    t = numpy.zeros(n+1)
    for s in mnozica:
        if s < 0 :
            t[s * (-1)] = -1
        else :
            t[s] = 1
    return(t)

def check_solution(file1, file2):
    with open(file1) as fp:
        first = 0
        table = numpy.zeros(1);
        for line in fp :
            line2 = line.rstrip('\n').split(" ")
            if line2[0] != "c" and line2 != [""]:
                if first == 0:
                    line = line.rstrip('\n').split(" ")
                    n = int(line[2])
                    table = create_table(file2, n)
                    first = 1
                else:
                    check = 0;
                    line2 = list(filter(None,line2))
                    for l in line2:
                        lit = int(l)
                        if (lit < 0 and table[(-1) * lit]  < 0) or (lit > 0 and table[lit] > 0):
                            check = check + 1;
                    if check == 0:
                        return "false"
        return "true"

if __name__ == '__main__':
    
    solution = check_solution(sys.argv[1], sys.argv[2])
    print(solution)
