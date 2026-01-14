# Notes on Sudoku generation
Intuitively, a sure-fire way to create a Sudoku is to take a solved Sudoku and remove numbers such that the solution would remain unique.

Naive method: set some upper-lower bounds for how many digits to remove/keep, then remove the set amount. Doesn't really get into depth regarding actual difficulty, but more filled Sudokus give the impression of an easier puzzle.
Examples: "easy" removes 36, "medium" 48, "hard" 56.7 (https://github.com/BaseMax/sudoku_plus AI slop warning). Another (no link) I think had upper bounds 31, 51, 81 for removal.


More advanced: evaluate how disjoint the set of starting cells is. The more disjoint, the more difficult.
Examples: https://github.com/BaseMax/sudoku_plus.


Rather advanced, upper limit for us: considering the techniques. Naked/hidden signles, naked pairs/triplets, locked candidate, XY-Wing, Unique Rectangle. Example: https://github.com/unmade/dokusan, which is based on a 2011 article https://dlbeer.co.nz/articles/sudoku.html. Includes a "rank" system.


## Special variants
Miracle sudoku generator https://github.com/Dan-LB/miracle_sudoku with all rules separately defined with boolean variables.


## Cell reduction methods
Mostly based on https://github.com/RutledgePaulV/sudoku-generator/blob/master/Sudoku/Generator.py
Once again, the first naive-but-simple way:
- some cells can only have one unique value due to naive constraints. Those cells can be removed.
- randomly choosing a cell to remove and checks for uniqueness.

Promotion-heavy material on sudoku difficulty rankings explained in human language https://sudoku.coach/en/learn/sudoku-difficulty. From that article, the main points to use for this project wrt difficulty level:
Difficulty can be expressed in two general ways: difficulty (eg. SE rating) and work (eg. HoDoKu rating). SE rating is essentially $\max (difficulty_i)$, HoDoKu is more akin to $\Sigma_i^n difficulty_i$. It's "complexity" vs "time spent".

Hodoku can be downloaded from the website https://hodoku.sourceforge.net/en/docs_cre.php (link directs to docs, has .jar Download).

The above methods are fun n' all, but I think we will be sufficiently happy with semi-random removals and uniqueness checks.


# Actual implementation notes
I will start with the very basic naive impelemtation:
- get the list of constraints
- get a puzzle
- remove a piece
- check for uniqueness
- rinse and repeat

If a backtracking solution was used, it could lookahead restore the "state" at which the sudoku was last unique.