difficulty_level = 1

# Each of these functions is used to manipulate or collect the current set difficulty

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

# According to the difficulty passed as a parameter, 
# returns the number of birds and branches as a tuple
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
            range(34, 999): (10, 14), # Levels:   >34      Birds: 10  Branches: 14
            "Init1": (4, 6),          # Levels: 1 2 3      Birds: 4   Branches: 6
            "Init2": (5, 8),          # Levels: 4 5 6      Birds: 5   Branches: 8
            "Init3": (5, 7),          # Levels: 7 8 9      Birds: 5   Branches: 7
            "Init4": (6, 9),          # Levels: 10 11 12   Birds: 6   Branches: 9
            "Init5": (6, 8),          # Levels: 13 14 15   Birds: 6   Branches: 8
            "Init6": (7, 10),         # Levels: 16 17 18   Birds: 7   Branches: 10
            "Init7": (7, 9),          # Levels: 19 20 21   Birds: 7   Branches: 9
            "Init8": (8, 11),         # Levels: 22 23 24   Birds: 8   Branches: 11
            "Init9": (8, 10),         # Levels: 25 26 27   Birds: 8   Branches: 10
            "Init10": (9, 12),        # Levels: 28 29 30   Birds: 9   Branches: 12
            "Init11": (9, 11),        # Levels: 31 32 33   Birds: 9   Branches: 11
            "Init12": (10, 14),       # Levels:   >34      Birds: 10  Branches: 14
            "Mid1": (4, 6),           # Levels: 1 2 3      Birds: 4   Branches: 6
            "Mid2": (5, 8),           # Levels: 4 5 6      Birds: 5   Branches: 8
            "Mid3": (5, 7),           # Levels: 7 8 9      Birds: 5   Branches: 7
            "Mid4": (6, 9),           # Levels: 10 11 12   Birds: 6   Branches: 9
            "Mid5": (6, 8),           # Levels: 13 14 15   Birds: 6   Branches: 8
            "Mid6": (7, 10),          # Levels: 16 17 18   Birds: 7   Branches: 10
            "Mid7": (7, 9),           # Levels: 19 20 21   Birds: 7   Branches: 9
            "Mid8": (8, 11),          # Levels: 22 23 24   Birds: 8   Branches: 11
            "Mid9": (8, 10),          # Levels: 25 26 27   Birds: 8   Branches: 10
            "Mid10": (9, 12),         # Levels: 28 29 30   Birds: 9   Branches: 12
            "Mid11": (9, 11),         # Levels: 31 32 33   Birds: 9   Branches: 11
            "Mid12": (10, 14)         # Levels:   >34      Birds: 10  Branches: 14
        }
    for key, value in difficulty_settings.items():
        if difficulty in key:
            return value
    return (4, 6) 