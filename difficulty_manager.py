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
            range(1, 5): (4, 6),
            range(5, 10): (5, 8),
            range(10, 15): (6, 9),
            range(15, 20): (7, 10),
            range(20, 25): (8, 12),
            range(25, 30): (9, 13),
        }
    for key, value in difficulty_settings.items():
        if difficulty in key:
            return value
    return (4, 6) 