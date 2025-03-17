import tkinter as tk
import random
from PIL import Image, ImageTk
from difficulty_manager import increase_difficulty
from difficulty_manager import reset_difficulty
from difficulty_manager import get_difficulty

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
        self.difficulty = get_difficulty()
        center_window(self.root)
        
        self.canvas = tk.Canvas(root, width=600, height=800, bg="#87CEFA")
        self.canvas.pack()
        
        difficulty_settings = {
            range(1, 5): (4, 6),
            range(5, 10): (5, 8),
            range(10, 15): (6, 9),
            range(15, 20): (7, 10),
            range(20, 25): (8, 12),
            range(25, 30): (9, 13),
        }
        def get_difficulty_settings(difficulty):
            for key, value in difficulty_settings.items():
                if difficulty in key:
                    return value
            return (4, 6) 
    
        num_colors, num_branches = get_difficulty_settings(self.difficulty)

        self.bird_colors = random.sample(["red", "green", "blue", "yellow", "orange", "purple", "pink"], num_colors)
        self.bird_images = {}  # Store images to prevent garbage collection issues

        # Load branch images 
        self.branch_img = Image.open("images/branch.png").resize((200, 30), Image.Resampling.LANCZOS)
        self.highlighted_branch_img = Image.open("images/branch_highlighted.png").resize((200, 30), Image.Resampling.LANCZOS)

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
            img = Image.open(f"images/{color}_bird.png").resize((50, 50), Image.Resampling.LANCZOS)  
            self.bird_images[color] = ImageTk.PhotoImage(img)
            self.bird_images[color + "_flipped"] = ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT))  

        self.branches = []
        self.selected_branch = None
        self.highlighted_branch = None
        self.score = 100
        self.init_branches(num_branches)
        self.draw_game()
        self.create_back_button()
        
        self.root.bind("<Button-1>", self.on_click)

    
    def go_back_to_menu(self):
        """Returns to the main menu and closes the current game window."""
        reset_difficulty() 
        self.root.destroy()  
        from main_menu import MainMenu  
        new_root = tk.Tk()  
        MainMenu(new_root) 
        new_root.mainloop()  


    def create_back_button(self):
        self.back_button = tk.Button(self.root, text="← Go Back", font=("Arial", 12), command=self.go_back_to_menu, bg="lightgray", fg="black")
        self.back_button.place(x=10, y=10) 


    def init_branches(self, num_branches):
        self.branches.clear()

        num_birds_per_branch = 4  # Each branch holds 4 birds

        # Generate positions based on the new number of branches
        def generate_branch_positions():
            screen_height = 750  # Max height
            branch_spacing = 80  # Space between branches
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
            right_branches = [(400, y) for y in y2_positions]

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

    
    def draw_game(self):
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
                bird_x_offset = 10 + i * 35 if branch["x"] < 300 else 140 - i * 35
                bird_image = self.bird_images[bird + "_flipped"] if branch["x"] < 300 else self.bird_images[bird]
                self.canvas.create_image(branch["x"] + bird_x_offset, branch["y"] - 35, anchor=tk.NW, image=bird_image)

        self.canvas.create_text(530, 28, text=f"Score: {self.score}", font=("Arial", 16), fill="black")
        self.canvas.create_text(530, 50, text=f"Difficulty: {get_difficulty()}", font=("Arial", 14), fill="black")

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
            if branch["x"] < event.x < branch["x"] + 200 and branch["y"] < event.y < branch["y"] + 30:
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
                                self.score -= 5
                        self.selected_branch = None
                        self.highlighted_branch = None  # Remove highlight after move
                break

        self.draw_game()
        self.check_complete()
    

    def check_complete(self):
        new_branches = []
        for branch in self.branches:
            if len(branch["birds"]) == 4 and all(b == branch["birds"][0] for b in branch["birds"]):
                self.score += 50
            else:
                new_branches.append(branch)
        self.branches = new_branches

        self.draw_game()

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

        difficulty_settings = {
            range(1, 5): (4, 6),
            range(5, 10): (5, 8),
            range(10, 15): (6, 9),
            range(15, 20): (7, 10),
            range(20, 25): (8, 12),
            range(25, 30): (9, 13),
        }
        def get_difficulty_settings(difficulty):
            for key, value in difficulty_settings.items():
                if difficulty in key:
                    return value
            return (4, 6) 
        
        num_colors, num_branches = get_difficulty_settings(self.difficulty)

        self.bird_colors = random.sample(["red", "green", "blue", "yellow", "orange", "purple", "pink"], num_colors)

        # Reload bird images
        self.bird_images.clear()
        for color in self.bird_colors:
            img = Image.open(f"images/{color}_bird.png").resize((50, 50), Image.Resampling.LANCZOS)
            self.bird_images[color] = ImageTk.PhotoImage(img)
            self.bird_images[color + "_flipped"] = ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT))

        self.init_branches(num_branches)  # Pass the calculated number of branches
        self.draw_game()


    def show_win_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Game Over")
        center_window(popup, 400, 200)

        tk.Label(popup, text="🎉 Congratulations! 🎉", font=("Arial", 20)).pack(pady=10)
        tk.Label(popup, text=f"Final Score: {self.score}", font=("Arial", 16)).pack(pady=5)

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

        tk.Button(popup, text="Go to Next Level", font=("Arial", 14), command=next_level).pack(pady=10)
        tk.Button(popup, text="Return to Main Menu", font=("Arial", 14), command=return_to_menu).pack(pady=10)

        popup.transient(self.root)
        popup.after(10, lambda: popup.grab_set())
        self.root.wait_window(popup)
