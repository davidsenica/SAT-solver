# SAT-solver
This is an implementation of SAT solver done for homework
in course Logic in computer science

## Instruction
The code is written purely in python and 
doesn't use any kind of external libraries.
It implements DPLL algorithm.

Run the program with command:

`python SAT-solver.py input.txt output.txt`

where input.txt is location of a file in Dimacs format 
and output.txt is location of output file.

Example run

`python SAT-solver.py example\ solution.txt`

### Improvement
For next decision literal we select the one with highest occurrence.