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
        birds = self.bird_colors * 4  # 16 pássaros no total
        random.shuffle(birds)
        
        positions = [(50, 500), (50, 650), (450, 400), (450, 550), (450, 700)]  # 2 ramos à esquerda, 3 à direita
        for x, y in positions:
            branch = {"x": x, "y": y, "birds": []}
            self.branches.append(branch)
        
        index = 0
        while index < len(birds):
            for branch in self.branches:
                if index < len(birds) and len(branch["birds"]) < 4:
                    branch["birds"].append(birds[index])
                    index += 1
    
    def draw_game(self):
        self.canvas.delete("all")
        self.draw_background()
        
        for branch in self.branches:
            self.canvas.create_rectangle(branch["x"], branch["y"], branch["x"] + 120, branch["y"] + 20, fill="brown")
            for i, bird in enumerate(branch["birds"]):
                bird_x_offset = 10 + i * 25 if branch["x"] < 300 else 10 + i * 25
                self.canvas.create_oval(branch["x"] + bird_x_offset, branch["y"] - 30,
                                        branch["x"] + bird_x_offset + 25, branch["y"], fill=bird)
        
        self.canvas.create_text(500, 50, text=f"Score: {self.score}", font=("Arial", 16), fill="black")
    
    def draw_background(self):
        cloud_positions = [(100, 100), (300, 150), (500, 80)]
        for x, y in cloud_positions:
            self.canvas.create_oval(x, y, x + 80, y + 50, fill="white", outline="white")
            self.canvas.create_oval(x + 30, y - 20, x + 100, y + 30, fill="white", outline="white")
            self.canvas.create_oval(x - 30, y - 10, x + 50, y + 40, fill="white", outline="white")
    
    def on_click(self, event):
        for branch in self.branches:
            if branch["x"] < event.x < branch["x"] + 120 and branch["y"] < event.y < branch["y"] + 20:
                if self.selected_branch is None:
                    self.selected_branch = branch
                else:
                    if self.selected_branch != branch:
                        if self.selected_branch["birds"]:
                            # Verifica se o ramo de destino tem espaço
                            if len(branch["birds"]) < 4:
                                print(f"Moving bird from {self.selected_branch['x']},{self.selected_branch['y']} to {branch['x']},{branch['y']}")
                                # Move bird logic
                                if self.selected_branch["x"] < 300:  # Ramos da esquerda
                                    bird = self.selected_branch["birds"].pop()
                                else:
                                    bird = self.selected_branch["birds"].pop(0)
                                
                                if branch["x"] < 300:
                                    branch["birds"].append(bird)
                                else:
                                    branch["birds"].insert(0, bird)
                            else:
                                print(f"Ramo cheio! Não foi possível mover o pássaro.")
                    self.selected_branch = None
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
