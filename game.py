import tkinter as tk
import random

def center_window(root, width=600, height=800):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

class BirdSortGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Bird Sort Game")
        center_window(self.root)
        
        self.canvas = tk.Canvas(root, width=600, height=800, bg="#87CEFA")
        self.canvas.pack()
        
        self.bird_colors = ["red", "green", "blue", "yellow"]
        self.branches = []
        self.selected_branch = None
        self.score = 0
        
        self.init_branches()
        self.draw_game()
        
        self.root.bind("<Button-1>", self.on_click)
        
    def init_branches(self):
        self.branches.clear()

        positions = [(50, 350), (50, 500), (50, 650), (450, 400), (450, 550), (450, 700)]
        self.branches = [{"x": x, "y": y, "birds": []} for x, y in positions]

        # 4 colors, 4 birds each (16 total)
        birds = self.bird_colors * 4
        random.shuffle(birds)

        # Distribute birds randomly but evenly across branches
        index = 0
        while index < len(birds):
            for branch in self.branches:
                if index < len(birds) and len(branch["birds"]) < 4:
                    branch["birds"].append(birds[index])
                    index += 1

        # Make random swaps to ensure solvability
        for _ in range(50):  # Perform 50 random swaps
            src, dest = random.sample(self.branches, 2)
            if src["birds"] and len(dest["birds"]) < 4:
                bird = src["birds"].pop()
                dest["birds"].append(bird)
        
        # Ensure there's at least one valid move
        if not self.has_valid_move():
            self.init_branches()  # Retry if no valid move exists

    def has_valid_move(self):
        """Checks if there is at least one valid move possible"""
        for src in self.branches:
            if not src["birds"]:
                continue  # Ignore empty branches
            top_group = self.get_top_group(src)
            for dest in self.branches:
                if src != dest and self.can_move(top_group, dest):
                    return True  # At least one move is possible
        return False

    
    def draw_game(self):
        self.canvas.delete("all")
        self.draw_background()
        
        for branch in self.branches:
            self.canvas.create_rectangle(branch["x"], branch["y"], branch["x"] + 120, branch["y"] + 20, fill="brown")
            num_birds = len(branch["birds"])
            
            for i, bird in enumerate(branch["birds"]):
                if branch["x"] < 300:  # Left branches grow left-to-right
                    bird_x_offset = 10 + i * 25
                else:  # Right branches grow right-to-left
                    bird_x_offset = 85 - i * 25  # Start from right side

                self.canvas.create_oval(branch["x"] + bird_x_offset, branch["y"] - 30,
                                        branch["x"] + bird_x_offset + 25, branch["y"], fill=bird)

        self.canvas.create_text(500, 50, text=f"Score: {self.score}", font=("Arial", 16), fill="black")


    
    def draw_background(self):
        cloud_positions = [(100, 100), (300, 150), (500, 80)]
        for x, y in cloud_positions:
            self.canvas.create_oval(x, y, x + 80, y + 50, fill="white", outline="white")
            self.canvas.create_oval(x + 30, y - 20, x + 100, y + 30, fill="white", outline="white")
            self.canvas.create_oval(x - 30, y - 10, x + 50, y + 40, fill="white", outline="white")
    
    def get_top_group(self, branch):
        if not branch["birds"]:
            return []
        
        top_bird = branch["birds"][-1]  # The topmost bird
        group = []

        for bird in reversed(branch["birds"]):  # Check from top to bottom
            if bird == top_bird:
                group.append(bird)
            else:
                break

        return group

    def can_move(self, moving_birds, target_branch):
        if not moving_birds:
            return False

        if len(target_branch["birds"]) + len(moving_birds) > 4:
            return False  # No space

        if not target_branch["birds"]:  # Can move to an empty branch
            return True
        
        return target_branch["birds"][-1] == moving_birds[0]  # Check color match


    def on_click(self, event):
        for branch in self.branches:
            if branch["x"] < event.x < branch["x"] + 120 and branch["y"] < event.y < branch["y"] + 20:
                if self.selected_branch is None:
                    if branch["birds"]:  # Only select if there are birds to move
                        self.selected_branch = branch
                else:
                    if self.selected_branch != branch:
                        if self.selected_branch["birds"]:
                            # Identify the birds that should move as a group
                            moving_birds = self.get_top_group(self.selected_branch)

                            # Check if move is valid
                            if self.can_move(moving_birds, branch):
                                print(f"Moving birds {moving_birds} from {self.selected_branch['x']},{self.selected_branch['y']} to {branch['x']},{branch['y']}")
                                
                                for bird in moving_birds:
                                    self.selected_branch["birds"].remove(bird)  # Remove from original branch
                                    branch["birds"].append(bird)  # Add to target branch

                        self.selected_branch = None  # Deselect after the move
                break

        self.check_complete()
        self.draw_game()

    
    def check_complete(self):
        new_branches = []
        for branch in self.branches:
            if len(branch["birds"]) == 4 and all(b == branch["birds"][0] for b in branch["birds"]):
                self.score += 10
            else:
                new_branches.append(branch)
        self.branches = new_branches
