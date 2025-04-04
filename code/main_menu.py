from tkinter import Tk, Label, Button, Canvas, font
from game import BirdSortGame
import tkinter as tk
from PIL import Image, ImageTk
from difficulty_manager import difficulty_level

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Menu")
        self.root.geometry("600x800")
        image = Image.open("../images/bkg.png")
        self.bg_image = ImageTk.PhotoImage(image)
        
        self.difficulty = difficulty_level
        self.canvas = tk.Canvas(root, width=600, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        # Menu Buttons to be displayed
        self.create_button(300, 350, "Play", "#86a340", self.start_game)
        self.create_button(300, 450, "AI", "#5a7547", self.open_ai_submenu)
        self.create_button(300, 550, "Quit", "#fbc182", self.root.quit)
        self.create_button(575, 675, "Info", "#6a3a03", self.open_info_page)
    
    def create_button(self, x, y, text, color, command):
        btn_font = font.Font(family="Trebuchet MS", size=17, weight="bold")

        if text == "Info": # Positioned over the sign we added in the background
            btn = tk.Button(self.root, text=text, font=btn_font,
                        bg=color, fg="white",
                        activebackground=self.lighten_color(color),
                        activeforeground="white",
                        borderwidth=0, relief="raised",
                        highlightthickness=0, command=command)
            btn.place(x=x - 100, y=y - 25, width=75, height=50)
        else:
            btn = tk.Button(self.root, text=text, font=btn_font,
                        bg=color, fg="white",
                        activebackground=self.lighten_color(color),
                        activeforeground="white",
                        borderwidth=3, relief="raised",
                        command=command)
            btn.place(x=x - 100, y=y - 25, width=200, height=50)

    # Used for Mouse Hovering Effect
    # - Makes the color lighter as the name implies
    def lighten_color(self, color, factor=30):
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        return f'#{min(r+factor, 255):02x}{min(g+factor, 255):02x}{min(b+factor, 255):02x}'

    # NAVIGATOR FUNCTION 1
    # - Enter Player Game (Human)
    def start_game(self):
        self.root.destroy()
        root = Tk()
        BirdSortGame(root)
        root.mainloop()
    
    # NAVIGATOR FUNCTION 2
    # - open AI Menu
    def open_ai_submenu(self):
        from submenu import AiSubmenu
        self.root.destroy()
        root = Tk()
        AiSubmenu(root)
        root.mainloop()

    # NAVIGATOR FUNCTION 3
    # - open About Us page
    def open_info_page(self):
        from info_page import InfoPage
        self.root.destroy()
        root = Tk()
        InfoPage(root)
        root.mainloop()

if __name__ == "__main__":
    root = Tk()
    MainMenu(root)
    root.mainloop()