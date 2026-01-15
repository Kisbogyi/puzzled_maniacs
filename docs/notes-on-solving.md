# Notes on sudoku solving
One can ask why is it important how we can solve a sudoku if our purpose is to
create one. Most sudoku generators utilize a sudoku solver in order to generate
a solved sudoku, and them remove numbers from it or just to validate if the sudoku
is solvable or not.

## Approach
There are several approaches to sudoku solvers. Sudokus can be solved algorithmically 
by backtracking, constraint programming, Knuth's algorithm X. 

The backtracking approach uses depth first search (DFS) to find an empty cell and 
then try every number from 1-9 and check if the resulting sudoku is still valid.
If it exhausts all options it backtracks and goes back to a previously known valid
state. This algorithm is slow, because we brute force the solution to the sudoku.

With the constraint programming approach the code tries to narrow the possible 
solutions of some equations. This either has a solution (sudoku is solvable) do
not have a solution (sudoku is unsolvable) or have multiple solutions (sudoku has 
multiple solutions). The interesting part of this approach is that it is not
sequential it is declarative. The programmer declares how the output should look
like, and the program outputs one(or more) solutions for it. Prolog uses this 
approach, but we can use SAT solvers to achieve the same results in other
programming languages.

The Knuth's Algorithm X (Dancing Links) is considered to be the fastest sudoku 
solver algorithm. The algorithm converts the board into an Exact Cover matrix and
it select rows in a way that each column has exactly one "1". Moreover Knuth’s
"Dancing Links" (DLX) technique uses a circular doubly linked list to make the
backtracking process incredibly fast by efficiently "covering" and "uncovering" constraints.

Our choice was the constraint programming approach, because of it's simplicity. 
We "only" had to give the equations that describes how sudoku works. Moreover 
this approach seemed to be the most extendable one, we could easily add multiple 
constraints in order to create the variants. The only downside is that it can be 
a little slow sometimes. The solver uses the [z3-prover](https://github.com/Z3Prover/z3) in python.

## Variants
Sudoku has multiple variants:
- Anti-Knight: each number in a square should also consider the move that a knight could make
in a game of Chess;
- Windoku: there are four additional coloured 3x3 squares that must also be filled with only
unique digits;
- Nonconsecutive: no two horizontally or vertically adjacent numbers can be consecutive;
- Center Dot: each traditional 3x3 square has a coloured middle square that must also all have
unique values.

These variants has the same rules as default sudoku with some additional rules.
Which means that they are some extensions that we have to add to our constraints 
if we want to solve them. If we want to be a little bit spicy we can solve a sudoku 
with multiple variants. There can exist a 'Anti-Knight+Nonconsecutive+Center Dot' 
sudoku because the rules are not exclusive. Sadly a 'Anti-Knight+Nonconsecutive+Center Dot
+Windoku' is not possible.
