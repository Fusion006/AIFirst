from tkinter import Tk, Button, messagebox, simpledialog, Canvas, font
from game import center_window
import tkinter
from game import BirdSortGame
from bfs import BirdSortBFS 
from dfs import BirdSortDFS
from a_star import BirdSortAStar 
from ids import BirdSortIDS 
from weight_a_star import BirdSortWeightedAStar #type:ignore
from greedy import BirdSortGreedy #type:ignore
from PIL import Image, ImageTk

class AiSubmenu:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Submenu")
        self.root.geometry("600x800")
        center_window(self.root)
        image = Image.open("../images/bkg_IA.png") 
        self.bg_image = ImageTk.PhotoImage(image)

        self.canvas = Canvas(root, width=600, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
        
        # Options for:
        # - the 6 Algorithms
        # - Return to Main Menu
        # - Open AI Info Page
        options = ["DFS", "BFS", "IDS", "Greedy", "A*", "Weighted A*", "Go Back", "AI Info"]
        self.buttons = []
        
        for i, option in enumerate(options):
            if option == "AI Info":
                self.create_button(560, 675, option, "#6a3a03", self.select_option)
            else:
                self.create_button(300, 210 + i * 80, option, "#86a340", self.select_option)
        
    # NAVIGATOR FUNCTION 1
    # - open Main Menu
    def go_back_to_menu(self):
        self.root.destroy()  
        from main_menu import MainMenu  
        new_root = tkinter.Tk()  
        MainMenu(new_root) 
        new_root.mainloop()  

    def create_button(self, x, y, text, color, command):
        btn_font = font.Font(family="Trebuchet MS", size=17, weight="bold")

        if text == "AI Info": # Positioned over the sign we added in the background
            btn = Button(self.root, text=text, font=btn_font,
                        bg=color, fg="white",
                        activebackground=self.lighten_color(color),
                        activeforeground="white", 
                        borderwidth=0, relief="raised",
                        highlightthickness=0, command=lambda: command(text))
            btn.place(x=x - 100, y=y - 25, width=100, height=50)
        else: 
            btn = Button(self.root, text=text, font=btn_font,
                        bg=color, fg="white",
                        activebackground=self.lighten_color(color), 
                        activeforeground="white",
                        borderwidth=3, relief="raised",
                        command=lambda: command(text))
            
            btn_window = self.canvas.create_window(x, y, window=btn, width=190, height=50)
            self.buttons.append(btn_window)

    # Used for Mouse Hovering Effect
    # - Makes the color lighter as the name implies
    def lighten_color(self, color, factor=30):
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        return f'#{min(r+factor, 255):02x}{min(g+factor, 255):02x}{min(b+factor, 255):02x}'

    # Used to create Difficulty Popup
    # - Asks for input (difficulty must be between 1 and 35)
    # - The function includes input validation as error messages
    def custom_difficulty_popup(self, callback):
        popup = tkinter.Toplevel(self.root, background="#48b9d7")
        popup.title(" ")

        width, height = 400, 200  # Define popup size
        center_window(popup, width, height)  # Center the popup

        tkinter.Label(popup, text="Select Difficulty", fg="white", font=("Arial", 20, "bold"), background="#48b9d7").pack(pady=10)
        tkinter.Label(popup, text="Enter difficulty level (1-35):", fg="white", font=("Arial", 14), background="#48b9d7").pack(pady=5)
        entry = tkinter.Entry(popup, font=("Arial", 14))
        entry.pack(pady=10)
        error_label = tkinter.Label(popup, text="", fg="red", font=("Arial", 12, "bold"), background="#48b9d7")
        error_label.pack(pady=1)
        
        # Validates input
        def submit():
            try:
                difficulty = int(entry.get())
                if 1 <= difficulty <= 35:
                    popup.destroy()
                    callback(difficulty)
                else:
                    error_label.config(text="⚠️ Enter a number between 1 and 35!")
            except ValueError:
                error_label.config(text="⚠️ Invalid input! Please enter a number.")

        tkinter.Button(popup, text="Confirm", font=("Arial", 14), background="white", borderwidth=0, highlightthickness=0, command=submit).pack(pady=5)
        popup.transient(self.root)
        popup.after(10, lambda: popup.grab_set())
        self.root.wait_window(popup)
        
    # Simple Navigator Function
    # - Go Back to Main Menu
    # - Open AI Info Page
    # - Enter Algorithm Execution
    def select_option(self, option):
        if option == "Go Back":
            self.root.destroy()
            from main_menu import MainMenu
            root = Tk()
            MainMenu(root)
            root.mainloop()
        if option == "AI Info":
            self.root.destroy()
            from info_page_ai import InfoPage_AI
            root = Tk()
            InfoPage_AI(root)
            root.mainloop()
        else:
            def start_with_difficulty(difficulty):
                self.start_ai(option, difficulty)
            self.custom_difficulty_popup(start_with_difficulty)

    # Called from Navigator Function Above
    # - calls each algorithm class
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
        elif algorithm == "Greedy":
            BirdSortGreedy(game_root, difficulty)
        elif algorithm == "Weighted A*":
            BirdSortWeightedAStar(game_root, difficulty)
        else:
            messagebox.showinfo("AI Mode", f"Selected AI: {algorithm}")
        
        game_root.mainloop()