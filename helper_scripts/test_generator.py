import random

# n: number of variables
# m: number of clauses
def randomtest(n, m):

    #create file
    f= open("input.txt","w")
    
    #write first line
    f.write("p cnf " + str(n) + " " + str(m) + "\n")
    
    # create list of all possible variables
    variables = list(range(1, n+1))

    # for each clause select its random lenght (clength) and random variables in it
    for i in range(1, m+1):
        
        #choose random length of clause
        clength = random.randint(1, n)
        
        #choose clenght varibales
        randvar = random.sample(variables, clength)
        
        #negate some variables
        randvar = [var * random.choice([-1, 1]) for var in randvar]

        #write clause in file
        f.write(" ".join(str(item) for item in randvar) + " 0\n")
              

    #close file
    f.close()
        
randomtest(3, 3)
