import tkinter as tk
import random
from PIL import Image, ImageTk
from difficulty_manager import increase_difficulty, reset_difficulty, get_difficulty, get_difficulty_settings
from hint import get_optimal_move # type: ignore

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
        center_window(self.root)
        
        self.canvas = tk.Canvas(root, width=600, height=800, bg="#87CEFA")
        self.canvas.pack()
    
        num_colors, num_branches = get_difficulty_settings(self.difficulty)

        self.bird_colors = random.sample(["red", "green", "blue", "yellow", "orange", "purple", "pink", "white", "cyan", "brown"], num_colors)
        self.bird_images = {}  # Store images to prevent garbage collection issues

        # Load branch images 
        self.branch_img = Image.open("images/branch.png").resize((250, 30), Image.Resampling.LANCZOS)
        self.highlighted_branch_img = Image.open("images/branch_highlighted.png").resize((250, 30), Image.Resampling.LANCZOS)

        # Flip branch images for left side
        self.branch_img_left = self.branch_img.transpose(Image.FLIP_LEFT_RIGHT)
        self.highlighted_branch_img_left = self.highlighted_branch_img.transpose(Image.FLIP_LEFT_RIGHT)

        # Convert images to Tkinter PhotoImage
        self.branch_img_tk = ImageTk.PhotoImage(self.branch_img)
        self.highlighted_branch_img_tk = ImageTk.PhotoImage(self.highlighted_branch_img)
        self.branch_img_left_tk = ImageTk.PhotoImage(self.branch_img_left)
        self.highlighted_branch_img_left_tk = ImageTk.PhotoImage(self.highlighted_branch_img_left)

        # Load and resize bird images
        for color in self.bird_colors:
            img = Image.open(f"images/{color}_bird.png").resize((75, 75), Image.Resampling.LANCZOS)  
            self.bird_images[color] = ImageTk.PhotoImage(img)
            self.bird_images[color + "_flipped"] = ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT))  
        
        
        self.branches = []
        self.selected_branch = None
        self.highlighted_branch = None
        self.score = 100
        self.init_branches(num_branches)
        self.draw_game(human_game)
        self.create_back_button(difficulty)
        
        if human_game:
            self.create_hint_button()
        
        self.root.bind("<Button-1>", self.on_click)

    def create_hint_button(self):
        """Creates a 'Hint' button in the top-right corner."""
        self.hint_button = tk.Button(self.root, text="Hint", font=("Fixedsys", 12), command=self.show_hint, borderwidth=0, highlightthickness=0, bg="#48b9d7", fg="black")
        self.hint_button.place(x=530, y=15)  # Position the button in the top-right corner

    def show_hint(self):
        """Suggests the most optimal move and prints it in the terminal."""
        """Displays the hint in a text box on the screen for 4 seconds."""
        branches_state = [branch["birds"] for branch in self.branches]
        optimal_move = get_optimal_move(branches_state)

        if optimal_move:
            src_idx, dst_idx = optimal_move
            branch_labels = {1: "L1", 2: "L2", 3: "L3", 4: "R1", 5: "R2", 6: "R3"}
            src_label = branch_labels[src_idx+1]
            dst_label = branch_labels[dst_idx+1]
            print(f"Hint: Move birds from branch {src_label} to branch {dst_label}")
            hint_text = f"Move birds from branch {src_label} to branch {dst_label}"
        else:
            print("No valid moves available.")
            hint_text = "No valid moves available."

        hint_box = self.canvas.create_rectangle(125, 700, 475, 750, fill="#7cbd76", outline="black")
        hint_text_item = self.canvas.create_text(300, 725, text=hint_text, font=("Arial", 12, "bold"), fill="black")

        self.root.after(4000, lambda: self.canvas.delete(hint_box, hint_text_item))

    def go_back_to_menu(self):
        reset_difficulty() 
        self.root.destroy()  
        from main_menu import MainMenu  
        new_root = tk.Tk()  
        MainMenu(new_root) 
        new_root.mainloop()  

    def go_back_to_ai_menu(self):
        reset_difficulty() 
        self.root.destroy()  
        from submenu import AiSubmenu 
        new_root = tk.Tk()  
        AiSubmenu(new_root)
        new_root.mainloop() 

    def create_back_button(self, difficulty=None):
        if difficulty:
            self.back_button = tk.Button(self.root, text="←", font=("Fixedsys", 12, "bold"), command=self.go_back_to_ai_menu, borderwidth=0, highlightthickness=0, fg="black")
        else:
            self.back_button = tk.Button(self.root, text="←", font=("Fixedsys", 12, "bold"), command=self.go_back_to_menu, borderwidth=0, highlightthickness=0, bg="#48b9d7", fg="black")
        self.back_button.place(x=10, y=10) 


    def init_branches(self, num_branches):
        self.branches.clear()

        num_birds_per_branch = 4  # Each branch holds 4 birds

        # Generate positions based on the new number of branches
        def generate_branch_positions():
            screen_height = 750  # Max height
            branch_spacing = 100  # Space between branches
            num_per_side = num_branches // 2
            num_left = num_branches // 2
            num_right = num_branches - num_left

            # Calculate dynamic starting Y so branches are centered
            total_branch_height = (num_per_side - 1) * branch_spacing
            start_y1 = max(150, (screen_height - total_branch_height) // 2)
            start_y2 = start_y1 + random.choice([-20, 20])  # Slight offset for variation

            # Generate positions
            y1_positions = [start_y1 + (i * branch_spacing) for i in range(num_left)]
            y2_positions = [start_y2 + (i * branch_spacing) for i in range(num_right)]

            # Ensure branches don't exceed the bottom of the screen
            y1_positions = [y for y in y1_positions if y + branch_spacing <= screen_height]
            y2_positions = [y for y in y2_positions if y + branch_spacing <= screen_height]

            left_branches = [(0, y) for y in y1_positions]
            right_branches = [(350, y) for y in y2_positions]

            return left_branches + right_branches


        positions = generate_branch_positions()[:num_branches]  # Adjust to required number of branches
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

        # Ensure solvability
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

    
    def draw_game(self, human_game):
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

    def draw_background(self):
        self.bg_image = ImageTk.PhotoImage(file="images/background.png") 
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)  
        

    def get_top_group(self, branch):
        if not branch["birds"]:
            return []
        
        top_bird = branch["birds"][-1]  
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
        #print("Branches:", self.branches)
        for branch in self.branches:
            #print(f"Branch at ({branch['x']}, {branch['y']}) with birds: {branch['birds']}")
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
                                    branch["birds"].append(self.selected_branch["birds"].pop())  # Ensure order is preserved
                                if (self.score - 5) > 0:
                                    self.score -= 5
                                else:
                                    self.score = 0
                        self.selected_branch = None
                        self.highlighted_branch = None  # Remove highlight after move
                break

        self.draw_game(True)
        self.check_complete()
    

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


    def is_game_won(self):
        for branch in self.branches:
            if branch["birds"] and (len(branch["birds"]) != 4 or len(set(branch["birds"])) != 1):
                return False
        return True


    def reset_game(self):
        """Resets the game state and starts a new round with increased difficulty."""
        self.difficulty = get_difficulty()  # Get updated difficulty
        
        num_colors, num_branches = get_difficulty_settings(self.difficulty)

        self.bird_colors = random.sample(["red", "green", "blue", "yellow", "orange", "purple", "pink"], num_colors)

        # Reload bird images
        self.bird_images.clear()
        for color in self.bird_colors:
            img = Image.open(f"images/{color}_bird.png").resize((75, 75), Image.Resampling.LANCZOS)
            self.bird_images[color] = ImageTk.PhotoImage(img)
            self.bird_images[color + "_flipped"] = ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT))

        self.init_branches(num_branches)  # Pass the calculated number of branches
        self.draw_game(True)


    def show_win_popup(self):
        popup = tk.Toplevel(self.root, background="#48b9d7")
        popup.title(" ")
        center_window(popup, 400, 200)

        tk.Label(popup, text="🎉 Congratulations! 🎉", fg="white", font=("Arial", 20, "bold"), background="#48b9d7").pack(pady=10)
        tk.Label(popup, text=f"Final Score: {self.score}", fg="white", font=("Arial", 16, "bold"), background="#48b9d7").pack(pady=5)

        def next_level():
            increase_difficulty()  # Increase difficulty before restarting
            popup.destroy()
            self.reset_game()  # Restart the game with new settings
            
        def return_to_menu():
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
