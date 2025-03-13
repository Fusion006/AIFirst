import copy
import tkinter as tk
from game import BirdSortGame, center_window

class BirdSortBFS:
    def __init__(self, root):
        self.root = root
        self.root.title("Bird Sort AI Solution")
        center_window(self.root)
        
        # Initialize game instance but don't bind click events
        self.game = BirdSortGame(root)
        self.game.root.unbind("<Button-1>")  # Disable click events
        
        # Store initial state
        self.branches = copy.deepcopy(self.game.branches)
        self.solution = []
        self.current_step = 0
        
        # Create controls
        self.create_controls()
        
        # Start solving
        self.solve()
        
    def create_controls(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)
        
        self.step_label = tk.Label(
            control_frame, 
            text="Step: 0/0", 
            font=("Arial", 14)
        )
        self.step_label.pack(side=tk.LEFT, padx=10)
        
        prev_button = tk.Button(
            control_frame, 
            text="← Previous", 
            font=("Arial", 12), 
            command=self.previous_step
        )
        next_button = tk.Button(
            control_frame, 
            text="Next →", 
            font=("Arial", 12), 
            command=self.next_step
        )
        
        prev_button.pack(side=tk.LEFT, padx=5)
        next_button.pack(side=tk.LEFT, padx=5)
        
        # Keyboard shortcuts
        self.root.bind("<Left>", lambda e: self.previous_step())
        self.root.bind("<Right>", lambda e: self.next_step())
        self.root.bind("<space>", lambda e: self.next_step())
    
    def solve(self):
        print("Starting BFS...")
        queue = [(self.branches, [])]
        visited = set()
        max_iterations = 100000
        iterations = 0
        
        while queue and iterations < max_iterations:
            state, moves = queue.pop(0)
            state_tuple = tuple(tuple(branch["birds"]) for branch in state)
            
            if state_tuple in visited:
                continue
                
            visited.add(state_tuple)
            iterations += 1
            
            if self.is_solved(state):
                self.solution = moves
                print(f"Solution found in {iterations} iterations!")
                self.update_step_counter()
                return
            
            for new_state, move in self.get_possible_moves(state):
                new_state_tuple = tuple(tuple(branch["birds"]) for branch in new_state)
                if new_state_tuple not in visited:
                    queue.append((new_state, moves + [move]))
        
        self.solution = None
        print(f"No solution found after {iterations} iterations.")

    def is_solved(self, state):
        for branch in state:
            if len(branch["birds"]) > 0:
                first_bird = branch["birds"][0]
                if any(bird != first_bird for bird in branch["birds"]):
                    return False
        return True

    def get_possible_moves(self, state):
        moves = []
        for i, src in enumerate(state):
            if not src["birds"]:
                continue
            
            for j, dst in enumerate(state):
                if i != j and len(dst["birds"]) < 4:
                    bird_to_move = src["birds"][-1]
                    if len(dst["birds"]) == 0 or dst["birds"][-1] == bird_to_move:
                        new_state = copy.deepcopy(state)
                        bird = new_state[i]["birds"].pop()
                        new_state[j]["birds"].append(bird)
                        moves.append((new_state, (i, j)))
        return moves

    def draw_state(self, state):
        self.game.canvas.delete("all")
        self.game.draw_background()
        
        # Draw branches and birds using game's visual style
        for branch in state:
            self.game.canvas.create_rectangle(
                branch["x"], branch["y"], 
                branch["x"] + 120, branch["y"] + 20, 
                fill="brown"
            )
            for i, bird in enumerate(branch["birds"]):
                bird_x_offset = 10 + i * 25
                self.game.canvas.create_oval(
                    branch["x"] + bird_x_offset, branch["y"] - 30,
                    branch["x"] + bird_x_offset + 25, branch["y"], 
                    fill=bird
                )

    def previous_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            current_state = copy.deepcopy(self.branches)
            
            # Replay moves up to current step
            for i in range(self.current_step):
                src_idx, dst_idx = self.solution[i]
                bird = current_state[src_idx]["birds"].pop()
                current_state[dst_idx]["birds"].append(bird)
            
            self.draw_state(current_state)
            self.update_step_counter()

    def next_step(self):
        if self.solution and self.current_step < len(self.solution):
            current_state = copy.deepcopy(self.branches)
            
            # Replay moves up to next step
            for i in range(self.current_step + 1):
                src_idx, dst_idx = self.solution[i]
                bird = current_state[src_idx]["birds"].pop()
                current_state[dst_idx]["birds"].append(bird)
            
            self.current_step += 1
            self.draw_state(current_state)
            self.update_step_counter()
            print(f"Step {self.current_step}: Move from branch {src_idx} to branch {dst_idx}")

    def update_step_counter(self):
        if self.solution:
            self.step_label.config(text=f"Step: {self.current_step}/{len(self.solution)}")