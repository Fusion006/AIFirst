import copy

def get_optimal_move(branches):
    """
    Suggests the most optimal move based on the current game state.
    The algorithm evaluates all possible moves and selects the one
    that minimizes the heuristic score of the resulting state.

    :param branches: List of branches representing the current game state.
    :return: A tuple (source_branch_index, target_branch_index) representing the optimal move.
    """
    def heuristic(state):
        """
        Heuristic function to evaluate the state.
        - Penalizes mixed colors in branches.
        - Rewards completed branches.
        - Penalizes scattered birds.
        """
        score = 0
        for branch in state:
            if not branch:
                continue

            colors = set(branch)
            if len(colors) > 1:
                score += len(colors) * 2  # Penalty for mixed colors

            if len(colors) == 1:
                score -= (len(branch) / 4) * 3  # Reward for nearly complete branches

            for color in colors:
                color_count = branch.count(color)
                if color_count < 4:
                    score += (4 - color_count)  # Penalty for scattered birds

        return score

    def get_possible_moves(state):
        """
        Generates all possible moves from the current state.

        :param state: List of branches representing the current game state.
        :return: A list of tuples (new_state, (source_index, target_index)).
        """
        moves = []
        for i, src in enumerate(state):
            if not src:
                continue

            bird_to_move = src[-1]
            move_group = 1
            while move_group < len(src) and src[-(move_group + 1)] == bird_to_move:
                move_group += 1

            for j, dst in enumerate(state):
                if i != j and len(dst) + move_group <= 4:
                    if not dst or dst[-1] == bird_to_move:
                        new_state = copy.deepcopy(state)
                        birds_moving = new_state[i][-move_group:]
                        new_state[i] = new_state[i][:-move_group]
                        new_state[j].extend(birds_moving)
                        moves.append((new_state, (i, j)))

        return moves

    # Evaluate all possible moves and select the one with the lowest heuristic score
    possible_moves = get_possible_moves(branches)
    if not possible_moves:
        return None  # No valid moves available

    optimal_move = min(possible_moves, key=lambda x: heuristic(x[0]))
    return optimal_move[1]  # Return the (source_index, target_index) of the optimal move