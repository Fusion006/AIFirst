import tkinter as tk
import random
from PIL import Image, ImageTk

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
        
        self.bird_colors = random.sample(["red", "green", "blue", "yellow", "orange", "purple"], 4)
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
            img = Image.open(f"images/{color}_bird.png") 
            img = img.resize((50, 50), Image.Resampling.LANCZOS)  
            self.bird_images[color] = ImageTk.PhotoImage(img)
            self.bird_images[color + "_flipped"] = ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT))  

        self.branches = []
        self.selected_branch = None
        self.highlighted_branch = None
        self.score = 100
        
        self.init_branches()
        self.draw_game()
        self.create_back_button()
        
        self.root.bind("<Button-1>", self.on_click)


    def go_back_to_menu(self):
        """Returns to the main menu and closes the current game window."""
        self.root.destroy()  
        from main_menu import MainMenu  
        new_root = tk.Tk()  
        MainMenu(new_root) 
        new_root.mainloop()  


    def create_back_button(self):
        self.back_button = tk.Button(self.root, text="← Go Back", font=("Arial", 12), command=self.go_back_to_menu, bg="lightgray", fg="black")
        self.back_button.place(x=10, y=10) 


    def init_branches(self):
        self.branches.clear()

        def generate_branch_positions():
            start_y1 = random.choice([150, 200, 250]) 
            start_y2 = random.choice([150, 200, 250]) 
            y1_positions = [start_y1, start_y1 + 150, start_y1 + 300] 
            y2_positions = [start_y2, start_y2 + 150, start_y2 + 300] 

            left_branches = [(0, y) for y in y1_positions]
            right_branches = [(400, 50+y) for y in y2_positions]

            return left_branches + right_branches

        positions = generate_branch_positions()

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
                if branch["x"] < 300:  # Left branches grow left-to-right
                    bird_x_offset = 10 + i * 35
                    bird_image = self.bird_images[bird + "_flipped"] 
                else:  # Right branches grow right-to-left
                    bird_x_offset = 140 - i * 35 
                    bird_image = self.bird_images[bird] 

                self.canvas.create_image(branch["x"] + bird_x_offset, branch["y"] - 35, anchor=tk.NW, image=bird_image)

        self.canvas.create_text(530, 28, text=f"Score: {self.score}", font=("Arial", 16), fill="black")


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
        for branch in self.branches:
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


    def show_win_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Game Over")
        center_window(popup, 400, 200)

        tk.Label(popup, text="🎉 Congratulations! 🎉", font=("Arial", 20)).pack(pady=10)
        tk.Label(popup, text=f"Final Score: {self.score}", font=("Arial", 16)).pack(pady=5)

        def return_to_menu():
            popup.destroy()
            self.root.destroy()
            from main_menu import MainMenu
            new_root = tk.Tk()
            MainMenu(new_root)
            new_root.mainloop()

        tk.Button(popup, text="Return to Main Menu", font=("Arial", 14), command=return_to_menu).pack(pady=20)

        popup.transient(self.root)
        popup.grab_set()
        self.root.wait_window(popup)
