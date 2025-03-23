from tkinter import Tk, Label, Button
from game import BirdSortGame, center_window

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Menu")
        center_window(self.root)
        
        from difficulty_manager import difficulty_level # type: ignore
        self.difficulty = difficulty_level

        Label(root, text="Bird Sort Game", font=("Arial", 24)).pack(pady=50)
        
        Button(root, text="Play (Human)", font=("Arial", 16), command=self.start_game).pack(pady=10)
        Button(root, text="Play (AI)", font=("Arial", 16), command=self.open_ai_submenu).pack(pady=10)
        Button(root, text="Quit", font=("Arial", 16), command=root.quit).pack(pady=10)
    
    def start_game(self):
        self.root.destroy()
        root = Tk()
        BirdSortGame(root)
        root.mainloop()
    
    def open_ai_submenu(self):
        from submenu import AiSubmenu # type: ignore
        self.root.destroy()
        root = Tk()
        AiSubmenu(root)
        root.mainloop()

if __name__ == "__main__":
    root = Tk()
    MainMenu(root)
    root.mainloop()