def reduce_nq_sat (n):
    file = open('../rezultat.txt', 'w')
    stv = n*n
    stc = 0
    clauses = list()
    M = [[str((x+1)+y*4) for x in range(n)] for y in range(n)]
    #najvec ena kraljica v vrstici
    c1 = ''
    for i in range(0, n):
        for j in range(0, n):
            c1 = c1 + M[i][j] + ' '
        c1 = c1 + '0'
        stc = stc + 1
        clauses.append(c1)
        c1 = ''

    #za vsako vrstico najvec ena kraljica v vrstici
    #za vsak stolpec najvec ena kraljica v stolpcu
    for j in range(0, n-1):
        for k in range(j+1, n):
            for i in range(0, n): 
                clauses.append('-'+M[i][j] + ' ' + '-'+M[i][k] + ' 0')
                stc = stc + 1
                clauses.append('-'+M[j][i] + ' ' + '-'+M[k][i] + ' 0')
                stc = stc + 1

    #najvec en element na diagonali
    for i in range(0, n):
        for j in range(0, n):
            for k in range(0, n):
                for l in range(0, n):
                    if i-j == l-k and M[i][j]!=M[l][k]:
                        clauses.append('-'+M[i][j] + ' ' + '-'+M[l][k] + ' 0')
                        stc = stc + 1
                    if i+j == l+k and M[i][j]!=M[l][k]:
                        clauses.append('-'+M[i][j] + ' ' + '-'+M[l][k] + ' 0')
                        stc = stc + 1
           

    #printanje
    file.write( 'p cnf'+ ' ' + str(stv) +' ' +str(stc)+'\n')
    for i in range(0, len(clauses)):
        file.write(clauses[i]+'\n')
    

reduce_nq_sat(41)
