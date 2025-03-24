from tkinter import Tk, Label, Button, messagebox, simpledialog
from game import center_window
from game import BirdSortGame
from bfs import BirdSortBFS 
from dfs import BirdSortDFS
from a_star import BirdSortAStar # type: ignore
from ids import BirdSortIDS  # type: ignore

class AiSubmenu:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Submenu")
        center_window(self.root)
        
        Label(root, text="Select AI Algorithm", font=("Arial", 20)).pack(pady=50)
        
        options = ["DFS", "BFS", "IDS", "GREEDY SEARCH", "A*", "MONTE CARLO TREE SEARCH", "Back to Main Menu"]
        for option in options:
            Button(root, text=option, font=("Arial", 16), command=lambda opt=option: self.select_option(opt)).pack(pady=10)
    
    def select_option(self, option):
        if option == "Back to Main Menu":
            self.root.destroy()
            from main_menu import MainMenu
            root = Tk()
            MainMenu(root)
            root.mainloop()
        else:
            difficulty = simpledialog.askinteger("Select Difficulty", "Enter difficulty level (1-999):", minvalue=1, maxvalue=999)
            if difficulty:
                self.start_ai(option, difficulty)

    def start_ai(self, algorithm, difficulty):
        self.root.destroy()
        game_root = Tk()
        
        if algorithm == "BFS":
            BirdSortBFS(game_root, difficulty)
        elif algorithm == "DFS":
            BirdSortDFS(game_root, difficulty)
        elif algorithm == "A*":
            BirdSortAStar(game_root, difficulty)
        elif algorithm == "IDS":
            BirdSortIDS(game_root, difficulty)
        else:
            messagebox.showinfo("AI Mode", f"Selected AI: {algorithm}")
        
        game_root.mainloop()