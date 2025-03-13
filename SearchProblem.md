
# Search Problem

## State Representation
A state represents the current configuration of birds on the branches.

Example State:
```
[
    ["red", "blue", "blue", "red"],
    ["yellow", "yellow", "red", "blue"],
    ["green", "green", "yellow", "yellow"],
    ["blue", "red", "green", "green"],
    []
]
```
Each inner list represents a branch with birds of different colors, stacked from bottom to top.
- The number of branches and birds per branches will depend on the difficulty level.
- An empty list represents an empty branch where birds can be moved.

## Initial State
When the game starts, the birds are randomly shuffled and distributed among the branches, according to the difficulty level.
> The exact distribution is defined in the functions `distribuir_facil()`, `distribuir_medio()`, and `distribuir_dificil()`.

## Goal State | Objective Test
- Each branch contains birds of only one color.
- Some branches may remain empty depending on the level configuration.

Example state:
```
[
    ["red", "red", "red", "red"],
    ["blue", "blue", "blue", "blue"],
    ["yellow", "yellow", "yellow", "yellow"],
    ["green", "green", "green", "green"],
    []
]
```
> Important Note: Every time a sequence of birds is complete, that branch becomes locked. In other words, that branch is "removed from the game".

## Operators
> Names, preconditions, effects, costs

### Move Bird from one branch to another
1. Move(`bird`, `source_branch`, `target_branch`)
2. Preconditions
   - `source_branch` is not empty.
   - `target_branch` is not full.
   - `target_branch` is either empty or the top bird in `target_branch` matches `bird`.
3. Effects
   - The top bird from `source_branch` is removed.
   - THe bird is added to `target_branch`.
4. Cost
   - We can assume that the cost of each move is 1 (uniform).

## Heuristics/Evaluation Function
To solve a puzzle at a given state, we can define a set of heuristics that will calculate how far we are from the goal.

**H1.** Number of misplaced birds
Counts the number of birds that are not in a uniform branch of the same color.

**H2.** - Number of incomplete branches
Counts the number of branches that do not contain only one color or are empty.

**H3.** - Moves needed to free a branch
Estimates the number of moves required to create at least one empty branch, which is useful for rearranging the birds.

**H4.** - A combination of the above
Example: H(state) = H1 + 0.5 * H2 to prioritize sorting while keeping track of incomplete branches.
