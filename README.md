# CS50 AI Crossword

Crossword generator that uses backtracking, forward checking, and constraint satisfaction algorithms to assign words to a crossword grid. It ensures that all words satisfy length and overlap constraints while avoiding repetition and maintaining consistency between intersecting words. 

## Contributions

`generate.py`:

`enforce_node_consistency`: Ensures each variable’s domain only includes words that match the required length, adhering to unary constraints.

`revise`: Makes variable x arc consistent with variable y by removing inconsistent values in x's domain based on overlaps between x and y.

`ac3`: Implements the AC3 algorithm to enforce arc consistency by iteratively revising arcs in the problem until all arcs are consistent or a domain becomes empty.

`assignment_complete`: Checks if every variable in the crossword puzzle has been assigned a value, confirming the assignment is complete.

`consistent`: Verifies that the current assignment satisfies all constraints: distinct values, correct word lengths, and no conflicts between overlapping variables.

`order_domain_values`: Orders the domain values of a variable based on the least-constraining value heuristic, which minimises the impact on neighboring variables.

`select_unassigned_variable`: Selects the next unassigned variable based on the minimum remaining values heuristic, and if tied, chooses the one with the largest degree.

`backtrack`: Performs backtracking search to find a complete, consistent assignment of words to variables, ensuring all constraints are satisfied.

### Testing

A test script (`test_generate.py`) has been developed to verify the correct operation of all listed functions.

### Technologies Used

- `Unittest`

### Usage

- main: `python3 generate.py structure words [output]`
- test: `python3 test_generate.py`