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
