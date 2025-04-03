from tkinter import Tk, Label, Button, Canvas, font
from game import BirdSortGame
import tkinter as tk
from PIL import Image, ImageTk

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Menu")
        self.root.geometry("600x800")
        
        # Load background image
        image = Image.open("images/bkg.png")  # Ensure this path is correct
        self.bg_image = ImageTk.PhotoImage(image) # Replace with your image

        from difficulty_manager import difficulty_level # type: ignore
        self.difficulty = difficulty_level
        
        # Create Canvas for background
        self.canvas = tk.Canvas(root, width=600, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        # Create styled buttons
        self.create_button(300, 350, "Play", "#86a340", self.start_game)
        self.create_button(300, 450, "AI", "#5a7547", self.open_ai_submenu)
        self.create_button(300, 550, "Quit", "#fbc182", self.root.quit)
        self.create_button(575, 675, "Info", "#6a3a03", self.open_instructions)
    
    def create_button(self, x, y, text, color, command):
        btn_font = font.Font(family="Trebuchet MS", size=17, weight="bold")
    
        # Place button properly in the window~
        if text == "Info":
            btn = tk.Button(self.root, text=text, font=btn_font,
                        bg=color, fg="white",
                        activebackground=self.lighten_color(color),  # Prevents gray hover effect
                        activeforeground="white",  # Keeps text white when hovered
                        borderwidth=0, relief="raised",  # Ridge effect
                        highlightthickness=0, command=command)
            btn.place(x=x - 100, y=y - 25, width=75, height=50)
        else:
            btn = tk.Button(self.root, text=text, font=btn_font,
                        bg=color, fg="white",
                        activebackground=self.lighten_color(color),  # Prevents gray hover effect
                        activeforeground="white",  # Keeps text white when hovered
                        borderwidth=3, relief="raised",  # Ridge effect
                        command=command)
            btn.place(x=x - 100, y=y - 25, width=200, height=50)

    def lighten_color(self, color, factor=30):
        """Lightens the given color slightly."""
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        return f'#{min(r+factor, 255):02x}{min(g+factor, 255):02x}{min(b+factor, 255):02x}'

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

    def open_instructions(self):
        from instructions_menu import InstructionsPage
        self.root.destroy()
        root = Tk()
        InstructionsPage(root)
        root.mainloop()

if __name__ == "__main__":
    root = Tk()
    MainMenu(root)
    root.mainloop()