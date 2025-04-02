import tkinter as tk
from main_menu import MainMenu  # Import the MainMenu class

class InstructionsPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Instructions")
        self.root.geometry("600x800")
        
        # Create a label for the instructions
        instructions = (
            "\n\n"
        
            "Welcome to Bird Sort!\n\n"
            "Objective:\n"
            "Sort the birds into branches so that each branch contains birds of the same color.\n\n"
            "How to Play:\n"
            "- Branchs are numbered up to down and then left to right.\n"
            "- Click on a branch to select it.\n"
            "- Click on another branch to move the top group of birds to it.\n"
            "- A move is valid only if the destination branch has space and the top bird matches the color.\n\n"
            "Good luck and have fun!"
        )
        label = tk.Label(self.root, text=instructions, font=("Arial", 14), justify="left", wraplength=550)
        label.pack(pady=20, padx=20)

        # Add a "Back" button to return to the main menu
        back_button = tk.Button(self.root, text="Back", font=("Arial", 12),
                                bg="#5a7547", fg="white",
                                activebackground="#86a340", activeforeground="white",
                                command=self.back_to_main_menu)
        back_button.place(x=10, y=10, width=80, height=40)  # Position in the top-left corner

    def back_to_main_menu(self):
        """Returns to the Main Menu."""
        self.root.destroy()
        root = tk.Tk()
        MainMenu(root)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    InstructionsPage(root)
    root.mainloop()
