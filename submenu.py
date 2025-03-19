from tkinter import Tk, Label, Button, messagebox
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
        elif option == "BFS":
            self.start_bfs_ai()
        elif option == "DFS":
            self.start_dfs_ai()
        elif option == "A*":
            self.start_astar_ai()
        elif option == "IDS":
            self.start_ids_ai()
        else:
            messagebox.showinfo("AI Mode", f"Selected AI: {option}")

    def start_bfs_ai(self):
        print("Initializing BFS AI...")
        self.root.destroy()
        game_root = Tk()
        BirdSortBFS(game_root)
        game_root.mainloop()
    
    def start_dfs_ai(self):
        print("Initializing DFS AI...")
        self.root.destroy()
        game_root = Tk()
        BirdSortDFS(game_root)
        game_root.mainloop()
    
    def start_ids_ai(self):
        print("Initializing IDS AI...")
        self.root.destroy()
        game_root = Tk()
        BirdSortIDS(game_root)
        game_root.mainloop()
    
    def start_astar_ai(self):
        print("Initializing A* AI...")
        self.root.destroy()
        game_root = Tk()
        BirdSortAStar(game_root)
        game_root.mainloop()
