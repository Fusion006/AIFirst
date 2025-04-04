import os
import random

difficulty_levels = {
    range(1, 4): (4, 6),
    range(4, 7): (5, 8),
    range(7, 10): (5, 7),  
    range(10, 13): (6, 9), 
    range(13, 16): (6, 8), 
    range(16, 19): (7, 10),
    range(19, 22): (7, 9), 
    range(22, 25): (8, 11),  
    range(25, 28): (8, 10),   
    range(28, 31): (9, 12), 
    range(31, 34): (9, 11),  
    range(34, 999): (10, 14),
}

bird_colors = ["red", "green", "blue", "yellow", "orange", "purple", "pink", "white", "cyan", "brown"]

os.makedirs("game/initial_states", exist_ok=True)
os.makedirs("game/mid_states", exist_ok=True)

# Solvable Initial State Generator
# - Follows similar logic as the normal level maker
def generate_initial_state(num_colors, num_branches):
    selected_colors = random.sample(bird_colors, num_colors)
    birds = selected_colors * 4
    random.shuffle(birds)
    branches = [[] for _ in range(num_branches)]
    for i, bird in enumerate(birds):
        branches[i % num_branches].append(bird)
    return branches

# Mid State Generator
# - Modifies initial states
def generate_mid_state(initial_state):
    modified_state = [list(branch) for branch in initial_state]
    # 50% chance to create a partially solved state
    if random.random() < 0.5:
        for branch in modified_state:
            if branch and random.random() < 0.4:  # 40% chance to sort a branch
                branch.sort()
    # 50% chance to remove some birds (simulate missing colors)
    else:
        for branch in modified_state:
            if branch and random.random() < 0.3:  # 30% chance to remove some birds
                branch.pop()
    return modified_state

# File Maker
# - Will take states created above and save them on text files (/game dir)
for i, (level_range, (num_colors, num_branches)) in enumerate(difficulty_levels.items(), start=1):
    initial_state = generate_initial_state(num_colors, num_branches)
    mid_state = generate_mid_state(initial_state)
    with open(f"game/initial_states/{i}.txt", "w") as f:
        for branch in initial_state:
            f.write(" ".join(branch) + "\n")
    with open(f"game/mid_states/{i}.txt", "w") as f:
        for branch in mid_state:
            f.write(" ".join(branch) + "\n")

