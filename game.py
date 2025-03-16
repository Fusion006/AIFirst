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
        
        self.bird_colors = ["red", "green", "blue", "yellow"]
        self.bird_images = {}  # Store images to prevent garbage collection issues

        # Load and resize bird images
        for color in self.bird_colors:
            img = Image.open(f"images/{color}_bird.png")  # Ensure you have images like "red_bird.png"
            img = img.resize((50, 50), Image.Resampling.LANCZOS)  # Resize to fit the branches
            self.bird_images[color] = ImageTk.PhotoImage(img)
            self.bird_images[color + "_flipped"] = ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT))  # Flipped

        self.branches = []
        self.selected_branch = None
        self.highlighted_branch = None
        self.score = 0
        
        self.init_branches()
        self.draw_game()
        self.create_back_button()
        
        self.root.bind("<Button-1>", self.on_click)

    def go_back_to_menu(self):
        """Returns to the main menu and closes the current game window."""
        self.root.destroy()  
        from main_menu import MainMenu  
        new_root = tk.Tk()  # Create a new root window
        MainMenu(new_root)  # Open the main menu
        new_root.mainloop()  # Start the event loop

    def create_back_button(self):
        self.back_button = tk.Button(self.root, text="← Go Back", font=("Arial", 12), command=self.go_back_to_menu, bg="lightgray", fg="black")
        self.back_button.place(x=10, y=10)  # Position at top-left

    def init_branches(self):
        self.branches.clear()

        positions = [(50, 200), (50, 350), (50, 500), (450, 250), (450, 400), (450, 550)]
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
            highlight_color = "darkgoldenrod" if branch == self.highlighted_branch else "brown"  # Highlight selection
            self.canvas.create_rectangle(branch["x"], branch["y"], branch["x"] + 120, branch["y"] + 20, fill=highlight_color)

            for i, bird in enumerate(branch["birds"]):
                if branch["x"] < 300:  # Left branches grow left-to-right
                    bird_x_offset = 10 + i * 25
                    bird_image = self.bird_images[bird + "_flipped"]  # Use normal image
                else:  # Right branches grow right-to-left
                    bird_x_offset = 85 - i * 25 
                    bird_image = self.bird_images[bird]  # Use flipped image

                # self.canvas.create_oval(branch["x"] + bird_x_offset, branch["y"] - 30,
                #                        branch["x"] + bird_x_offset + 25, branch["y"], fill=bird)
                # Place the image instead of drawing an oval
                self.canvas.create_image(branch["x"] + bird_x_offset, branch["y"] - 15, anchor=tk.NW, image=bird_image)


        self.canvas.create_text(530, 28, text=f"Score: {self.score}", font=("Arial", 16), fill="black")
                              # 500, 50 se quiserem meter como estava originalmente :)

    def draw_background(self):
        self.bg_image = ImageTk.PhotoImage(file="images/background.png")  # Load the background image
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)  # Draw it on the canvas
        
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
                    if branch["birds"]:
                        self.selected_branch = branch
                        self.highlighted_branch = branch  # Highlight it
                else:
                    if self.selected_branch != branch:
                        if self.selected_branch["birds"]:
                            moving_birds = self.get_top_group(self.selected_branch)
                            if self.can_move(moving_birds, branch):
                                print(f"Moving birds {moving_birds} from {self.selected_branch['x']},{self.selected_branch['y']} to {branch['x']},{branch['y']}")
                                
                                for _ in range(len(moving_birds)):
                                    branch["birds"].append(self.selected_branch["birds"].pop())  # Ensure order is preserved

                        self.selected_branch = None
                        self.highlighted_branch = None  # Remove highlight after move
                break

        self.draw_game()
        self.check_complete()
    
    def check_complete(self):
        new_branches = []
        for branch in self.branches:
            if len(branch["birds"]) == 4 and all(b == branch["birds"][0] for b in branch["birds"]):
                self.score += 100
            else:
                new_branches.append(branch)
        self.branches = new_branches

        self.draw_game()

        if self.is_game_won():
            self.show_win_popup()

    def is_game_won(self):
        """Checks if all non-empty branches contain uniform colors."""
        for branch in self.branches:
            if branch["birds"] and (len(branch["birds"]) != 4 or len(set(branch["birds"])) != 1):
                return False
        return True

    def show_win_popup(self):
        """Displays the win message and a button to return to the main menu."""
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
