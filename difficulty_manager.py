difficulty_level = 1

def get_difficulty():
    global difficulty_level
    return difficulty_level

def increase_difficulty():
    global difficulty_level
    difficulty_level += 1
    print(f"Difficulty increased to: {difficulty_level}")

def reset_difficulty():
    global difficulty_level
    difficulty_level = 1
    print("Difficulty reset to 1")

def get_difficulty_settings(difficulty):
    difficulty_settings = {
            range(1, 4): (4, 6),      # Levels: 1 2 3      Birds: 4   Branches: 6
            range(4, 7): (5, 8),      # Levels: 4 5 6      Birds: 5   Branches: 8
            range(7, 10): (5, 7),     # Levels: 7 8 9      Birds: 5   Branches: 7
            range(10, 13): (6, 9),    # Levels: 10 11 12   Birds: 6   Branches: 9
            range(13, 16): (6, 8),    # Levels: 13 14 15   Birds: 6   Branches: 8
            range(16, 19): (7, 10),   # Levels: 16 17 18   Birds: 7   Branches: 10
            range(19, 22): (7, 9),    # Levels: 19 20 21   Birds: 7   Branches: 9
            range(22, 25): (8, 11),   # Levels: 22 23 24   Birds: 8   Branches: 11
            range(25, 28): (8, 10),   # Levels: 25 26 27   Birds: 8   Branches: 10
            range(28, 31): (9, 12),   # Levels: 28 29 30   Birds: 9   Branches: 12
            range(31, 34): (9, 11),   # Levels: 31 32 33   Birds: 9   Branches: 11
            range(34, 37): (10, 13),  # Levels: 34 35 36   Birds: 10  Branches: 13
            range(37, 999): (10, 12), # Levels:   >37      Birds: 10  Branches: 12
        }
    for key, value in difficulty_settings.items():
        if difficulty in key:
            return value
    return (4, 6) 

"""
White
Cyan
Brown
"""