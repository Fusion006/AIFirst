import tkinter as tk
import random
from PIL import Image, ImageTk
from difficulty_manager import increase_difficulty, reset_difficulty, get_difficulty, get_difficulty_settings
from hint import get_optimal_move
import os

# GETTER FUNCTION FOR HIGHSCORE
def get_highscore():
    highscore_file = "../results/highscore.txt"
    if os.path.exists(highscore_file):
        with open(highscore_file, "r") as f:
            return int(f.read().strip())
    return 0

# SETTER FUNCTION FOR HIGHSCORE
def save_highscore(new_score):
    highscore_file = "../results/highscore.txt"
    with open(highscore_file, "w") as f:
        f.write(str(new_score))

def center_window(root, width=600, height=800):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

class BirdSortGame:
    def __init__(self, root, difficulty=None):
        self.root = root
        self.root.title("Bird Sort Game")
        self.difficulty = difficulty if difficulty else get_difficulty()
        human_game = False if difficulty else True
        if human_game == False: # Since AI algorithms have labels at the top of the screen, we made the window bigger to fit the labels and the canvas
            width = 600
            height = 1000
            center_window(self.root, width, height)
            self.canvas = tk.Canvas(root, width=600, height=800, bg="#87CEFA")
        else:
            center_window(self.root)
            self.canvas = tk.Canvas(root, width=600, height=800, bg="#87CEFA")
        self.canvas.pack()
        
        num_colors, num_branches = get_difficulty_settings(self.difficulty)

        self.bird_colors = random.sample(["red", "green", "blue", "yellow", "orange", "purple", "pink", "white", "cyan", "brown"], num_colors)
        self.bird_images = {}
        
        self.branch_img = Image.open("../images/branch.png").resize((250, 30), Image.Resampling.LANCZOS)
        # Highlighted Branch is used whenever we click on a branch to improve the game's interface
        self.highlighted_branch_img = Image.open("../images/branch_highlighted.png").resize((250, 30), Image.Resampling.LANCZOS)

        # Images were all drawn facing left, so we simply flip them to face the right, so they can be used on the left side of the screen.
        # Thanks to this, all art pieces will be "facing" the middle of the screen.
        self.branch_img_left = self.branch_img.transpose(Image.FLIP_LEFT_RIGHT)
        self.highlighted_branch_img_left = self.highlighted_branch_img.transpose(Image.FLIP_LEFT_RIGHT)

        self.branch_img_tk = ImageTk.PhotoImage(self.branch_img)
        self.highlighted_branch_img_tk = ImageTk.PhotoImage(self.highlighted_branch_img)
        self.branch_img_left_tk = ImageTk.PhotoImage(self.branch_img_left)
        self.highlighted_branch_img_left_tk = ImageTk.PhotoImage(self.highlighted_branch_img_left)

        # Bird Scaler (they become bigger to improve interface)
        for color in self.bird_colors:
            img = Image.open(f"../images/{color}_bird.png").resize((75, 75), Image.Resampling.LANCZOS)  
            self.bird_images[color] = ImageTk.PhotoImage(img)
            self.bird_images[color + "_flipped"] = ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT))  
        
        self.branches = []
        self.selected_branch = None
        self.highlighted_branch = None
        self.score = 100
        self.highscore = get_highscore()
        self.init_branches(num_branches)     # Game Maker
        self.draw_game(human_game)           # Game Displayer
        self.create_back_button(difficulty)
        
        if human_game:
            self.create_hint_button()
        
        self.root.bind("<Button-1>", self.on_click)

    # Hint Button Maker
    # - Calls show_hint()
    def create_hint_button(self):
        self.hint_button = tk.Button(self.root, text="Hint", font=("Fixedsys", 12), command=self.show_hint, borderwidth=0, highlightthickness=0, bg="#48b9d7", fg="black")
        self.hint_button.place(x=530, y=15)

    # Updates labels for hints
    # - Important once branches start getting deleted, the labels must adjust to the quantity of branches per side
    def update_branch_labels(self):
        self.branch_labels = {}
        left_index = 1
        right_index = 1

        for idx, branch in enumerate(self.branches):
            if branch["x"] < 300:
                self.branch_labels[idx] = f"L{left_index}"
                left_index += 1
            else:
                self.branch_labels[idx] = f"R{right_index}"
                right_index += 1

    # Hint Displayer Function (two places)
    # - Suggests the most optimal move and prints it in the terminal
    # - Displays the hint in a text box on the screen for 4 seconds
    # - Messages are Displayed using LX for branches on the left (1 being highest) or RX for branches on the right (1 being highest)
    # For example, L2 to R4 | R3 to L5 | L4 to L2 | ...
    def show_hint(self):
        self.update_branch_labels() # <- Ensure label map is the current one

        branches_state = [branch["birds"] for branch in self.branches]
        optimal_move = get_optimal_move(branches_state)

        if optimal_move:
            src_idx, dst_idx = optimal_move
            src_label = self.branch_labels[src_idx]
            dst_label = self.branch_labels[dst_idx]
            print(f"Hint: Move birds from branch {src_label} to branch {dst_label}")
            hint_text = f"Move birds from branch {src_label} to branch {dst_label}"
        else:
            print("No valid moves available.")
            hint_text = "No valid moves available."

        hint_box = self.canvas.create_rectangle(125, 700, 475, 750, fill="#7cbd76", outline="black")
        hint_text_item = self.canvas.create_text(300, 725, text=hint_text, font=("Arial", 12, "bold"), fill="black")
        self.hint_after_id = self.root.after(4000, lambda: self.canvas.delete(hint_box, hint_text_item))
        
    # NAVIGATOR FUNCTION 1
    # - return to Main Menu
    def go_back_to_menu(self):
        if self.score >= self.highscore: # Save only if new highscore is achieved
            save_highscore(self.score)
        reset_difficulty() 
        if hasattr(self, "hint_after_id"):
            self.root.after_cancel(self.hint_after_id)
        self.root.destroy()  
        from main_menu import MainMenu  
        new_root = tk.Tk()  
        MainMenu(new_root) 
        new_root.mainloop()  

    # NAVIGATOR FUNCTION 2
    # - return to AI Menu
    def go_back_to_ai_menu(self):
        reset_difficulty()
        self.root.destroy()  
        from submenu import AiSubmenu 
        new_root = tk.Tk()  
        AiSubmenu(new_root)
        new_root.mainloop() 

    def create_back_button(self, difficulty=None):
        if difficulty: # this is for AI algorithms (only change is in bg color)
            self.back_button = tk.Button(self.root, text="←", font=("Fixedsys", 12, "bold"), command=self.go_back_to_ai_menu, borderwidth=0, highlightthickness=0, fg="black")
        else:
            self.back_button = tk.Button(self.root, text="←", font=("Fixedsys", 12, "bold"), command=self.go_back_to_menu, borderwidth=0, highlightthickness=0, bg="#48b9d7", fg="black")
        self.back_button.place(x=10, y=10) 

    # Game Maker
    # - This function is responsible for distributing the birds along the branches
    # - It creates solvable games (unsolvable are discarded and regenerated)
    def init_branches(self, num_branches):
        self.branches.clear()

        num_birds_per_branch = 4  
        self.num_per_side = num_branches // 2                                              
        self.num_left = num_branches // 2
        self.num_right = num_branches - self.num_left

        def generate_branch_positions():
            screen_height = 750 # Max height
            branch_spacing = 100 # Space between branches
            num_per_side = num_branches // 2                                              
            num_left = num_branches // 2
            num_right = num_branches - num_left

            # Calculate dynamic starting Y so branches are centered
            total_branch_height = (num_per_side - 1) * branch_spacing                       
            start_y1 = max(125, (screen_height - total_branch_height) // 2)                 
            start_y2 = start_y1 + random.choice([-10, -5, 10, 20]) # Slight offset for variation 

            # Generate positions
            y1_positions = [start_y1 + (i * branch_spacing) for i in range(num_left)]
            y2_positions = [start_y2 + (i * branch_spacing) for i in range(num_right)]
            print(num_per_side, num_left, num_right, total_branch_height)
            print(y1_positions, y2_positions)
            # Ensure branches don't exceed the bottom of the screen
            y1_positions = [y for y in y1_positions if y <= 800]
            y2_positions = [y for y in y2_positions if y <= 800]
            print(y1_positions, y2_positions)
            left_branches = [(0, y) for y in y1_positions]
            right_branches = [(350, y) for y in y2_positions]

            return left_branches + right_branches

        positions = generate_branch_positions()[:num_branches] # Adjust to required number of branches
        self.branches = [{"x": x, "y": y, "birds": []} for x, y in positions]

        birds = self.bird_colors * num_birds_per_branch  
        random.shuffle(birds)

        # Distribute birds randomly but evenly across branches
        index = 0
        while index < len(birds):
            for branch in self.branches:
                if index < len(birds) and len(branch["birds"]) < num_birds_per_branch:
                    branch["birds"].append(birds[index])
                    index += 1

        # Build label map once, based on initial layout (x-coordinates)
        # - This is used for hints
        self.branch_labels = {}
        left_index = 1
        right_index = 1

        for idx, branch in enumerate(self.branches):
            if branch["x"] < 300:  # Assume left side
                self.branch_labels[idx] = f"L{left_index}"
                left_index += 1
            else:  # Right side
                self.branch_labels[idx] = f"R{right_index}"
                right_index += 1

        # Ensure solvability 
        # - We discard any unsolvable games
        if not self.has_valid_move():
            self.init_branches(num_branches)

    # Checks if there is at least one valid move possible
    def has_valid_move(self):
        for src in self.branches:
            if not src["birds"]:
                continue 
            top_group = self.get_top_group(src)
            for dest in self.branches:
                if src != dest and self.can_move(top_group, dest):
                    return True
        return False

    # Game Displayer
    # - After the game was generated with the code above, we display it
    # - Left Side uses flipped art pieces while the Right side uses original ones
    # - Score, Difficulty, and Highscore are displayed at the top of the screen
    def draw_game(self, human_game):
        if self.score > self.highscore:
            self.highscore = self.score
        self.canvas.delete("all")
        self.draw_background()
        
        for branch in self.branches:
            # Left side:
            if branch["x"] < 300:  
                branch_img = self.highlighted_branch_img_left_tk if branch == self.highlighted_branch else self.branch_img_left_tk
            # Right side:
            else:  
                branch_img = self.highlighted_branch_img_tk if branch == self.highlighted_branch else self.branch_img_tk

            self.canvas.create_image(branch["x"], branch["y"], anchor=tk.NW, image=branch_img)

            for i, bird in enumerate(branch["birds"]):
                bird_x_offset = 5 + i * 50 if branch["x"] < 300 else 170 - i * 50
                bird_image = self.bird_images[bird + "_flipped"] if branch["x"] < 300 else self.bird_images[bird]
                self.canvas.create_image(branch["x"] + bird_x_offset, branch["y"] - 60, anchor=tk.NW, image=bird_image)

        if human_game:
            self.canvas.create_text(300, 28, text=f"Score: {self.score}", font=("Fixedsys", 16, "bold"), fill="black")
            self.canvas.create_text(300, 50, text=f"Difficulty: {get_difficulty()}", font=("Fixedsys", 14, "bold"), fill="black")
            self.canvas.create_text(300, 72, text=f"Highscore: {self.highscore}", font=("Fixedsys", 12, "bold"), fill="black")

    def draw_background(self):
        self.bg_image = ImageTk.PhotoImage(file="../images/background.png") 
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)  
        

    def get_top_group(self, branch):
        if not branch["birds"]:
            return []
        top_bird = branch["birds"][-1]  
        group = []
        for bird in reversed(branch["birds"]): 
            if bird == top_bird:
                group.append(bird)
            else:
                break
        return group

    # Validate the chosen move
    # - Branch must have space for single/group of birds
    # - The bird in the "outer" side of the branch must match the color of the moving birds
    def can_move(self, moving_birds, target_branch):
        if not moving_birds:
            return False

        if len(target_branch["birds"]) + len(moving_birds) > 4:
            return False # No space

        if not target_branch["birds"]: # Can move to an empty branch
            return True
        
        return target_branch["birds"][-1] == moving_birds[0] # Check color match

    # On Click, the branch becomes highlighted
    # - This function defines the hitbox for the branches (the area where the birds are is also clickable to improve gameplay)
    # - Dynamically modfies the highscore whenever score == highscore
    def on_click(self, event):
        if self.score > self.highscore:
            self.highscore = self.score

        for branch in self.branches:
            if branch["x"] < event.x < branch["x"] + 350 and branch["y"]-50 < event.y < branch["y"] + 30:
                if self.selected_branch is None:
                    if branch["birds"]:
                        self.selected_branch = branch
                        self.highlighted_branch = branch  
                else:
                    if self.selected_branch != branch:
                        if self.selected_branch["birds"]:
                            moving_birds = self.get_top_group(self.selected_branch)
                            if self.can_move(moving_birds, branch):
                                print(f"Moving birds {moving_birds} from {self.selected_branch['x']},{self.selected_branch['y']} to {branch['x']},{branch['y']}")
                                
                                for _ in range(len(moving_birds)):
                                    branch["birds"].append(self.selected_branch["birds"].pop()) # Ensure order is preserved
                                if (self.score - 5) > 0:
                                    self.score -= 5
                                else:
                                    self.score = 0
                        self.selected_branch = None
                        self.highlighted_branch = None # Remove highlight after move
                break
        
        self.draw_game(True)
        self.check_complete()
    
    # Check if the game is complete
    # - If so, display a Win popup
    def check_complete(self):
        new_branches = []
        for branch in self.branches:
            if len(branch["birds"]) == 4 and all(b == branch["birds"][0] for b in branch["birds"]):
                self.score += 50
            else:
                new_branches.append(branch)
        self.branches = new_branches

        self.draw_game(True)

        if self.is_game_won():
            self.show_win_popup()

    # WIN-CONDITION: All branches are empty
    def is_game_won(self):
        for branch in self.branches:
            if branch["birds"] and (len(branch["birds"]) != 4 or len(set(branch["birds"])) != 1):
                return False
        return True

    # Resets the game state and starts a new round with increased difficulty
    def reset_game(self):
        self.difficulty = get_difficulty() # Get updated difficulty
        
        num_colors, num_branches = get_difficulty_settings(self.difficulty)

        self.bird_colors = random.sample(["red", "green", "blue", "yellow", "orange", "purple", "pink", "white", "cyan", "brown"], num_colors)

        # Reload bird images
        self.bird_images.clear()
        for color in self.bird_colors:
            img = Image.open(f"../images/{color}_bird.png").resize((75, 75), Image.Resampling.LANCZOS)
            self.bird_images[color] = ImageTk.PhotoImage(img)
            self.bird_images[color + "_flipped"] = ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT))

        self.init_branches(num_branches) # Pass the calculated number of branches
        self.draw_game(True)

    # After winning, the player can either continue playing or go back to the menu
    def show_win_popup(self):
        popup = tk.Toplevel(self.root, background="#48b9d7")
        popup.title(" ")
        center_window(popup, 400, 200)

        tk.Label(popup, text="Congratulations!", fg="white", font=("Arial", 20, "bold"), background="#48b9d7").pack(pady=10)
        tk.Label(popup, text=f"Final Score: {self.score}", fg="white", font=("Arial", 16, "bold"), background="#48b9d7").pack(pady=5)

        def next_level():
            increase_difficulty() # Increase difficulty before restarting
            popup.destroy()
            self.reset_game() # Restart the game with new settings
            
        def return_to_menu():
            if self.score >= self.highscore: # Save only if new highscore is achieved
                save_highscore(self.score)
            reset_difficulty() 
            popup.destroy()
            self.root.destroy()
            from main_menu import MainMenu
            new_root = tk.Tk()
            MainMenu(new_root)
            new_root.mainloop()

        tk.Button(popup, text="Go to Next Level", font=("Arial", 14), background="white", borderwidth=0, highlightthickness=0, command=next_level).pack(pady=10)
        tk.Button(popup, text="Return to Main Menu", font=("Arial", 14), background="white", borderwidth=0, highlightthickness=0, command=return_to_menu).pack(pady=10)

        popup.transient(self.root)
        popup.after(10, lambda: popup.grab_set())
        self.root.wait_window(popup)
