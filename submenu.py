from tkinter import Tk, Button, messagebox, simpledialog, Canvas, font
from game import center_window
from game import BirdSortGame
from bfs import BirdSortBFS 
from dfs import BirdSortDFS
from a_star import BirdSortAStar 
from ids import BirdSortIDS 
from monte_carlo import BirdSortMonteCarlo #type:ignore
from greedy import BirdSortGreedy #type:ignore
from PIL import Image, ImageTk

class AiSubmenu:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Submenu")
        self.root.geometry("600x800")
        center_window(self.root)

        # Load background image
        image = Image.open("images/bkg_IA.png")  # Ensure this path is correct
        self.bg_image = ImageTk.PhotoImage(image)  # Convert for Tkinter use

        # Create Canvas for background
        self.canvas = Canvas(root, width=600, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
        
        options = ["DFS", "BFS", "IDS", "Greedy", "A*", "Monte Carlo", "Back to Menu"]
        self.buttons = []
        
        
        for i, option in enumerate(options):
            self.create_button(300, 200 + i * 80, option, "#86a340", self.select_option)

    def create_button(self, x, y, text, color, command):
        """Creates a styled button inside the Canvas."""
        btn_font = font.Font(family="Trebuchet MS", size=17, weight="bold")

        btn = Button(self.root, text=text, font=btn_font,
                     bg=color, fg="white",
                     activebackground=self.lighten_color(color), 
                     activeforeground="white",
                     borderwidth=3, relief="raised",
                     command=lambda: command(text))  # Pass button text as argument
        
        # Add button to canvas
        btn_window = self.canvas.create_window(x, y, window=btn, width=250, height=50)
        self.buttons.append(btn_window)

    def lighten_color(self, color, factor=30):
        """Lightens the given color slightly for hover effect."""
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        return f'#{min(r+factor, 255):02x}{min(g+factor, 255):02x}{min(b+factor, 255):02x}'


    def select_option(self, option):
        if option == "Back to Menu":
            self.root.destroy()
            from main_menu import MainMenu
            root = Tk()
            MainMenu(root)
            root.mainloop()
        else:
            difficulty = simpledialog.askinteger("Select Difficulty", "Enter difficulty level (1-19):", minvalue=1, maxvalue=19)
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
        elif algorithm == "GREEDY SEARCH":
            BirdSortGreedy(game_root, difficulty)
        elif algorithm == "MONTE CARLO TREE SEARCH":
            BirdSortMonteCarlo(game_root, difficulty)
        else:
            messagebox.showinfo("AI Mode", f"Selected AI: {algorithm}")
        
        game_root.mainloop()