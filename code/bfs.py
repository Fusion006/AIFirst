import tkinter as tk
import copy
import time
from collections import deque
from game import BirdSortGame, center_window
from difficulty_manager import get_difficulty_settings
from tkinter import messagebox

class BirdSortBFS:
    def __init__(self, root, difficulty):
        self.root = root
        self.root.title("Bird Sort BFS Solution")
        center_window(self.root)

        self.difficulty = difficulty
        self.create_controls()
        self.game = BirdSortGame(root, difficulty)
        self.game.root.unbind("<Button-1>")  # Disable manual play

        self.branches = [list(branch["birds"]) for branch in self.game.branches]  # Start with mutable lists
        self.solution = []
        self.current_step = 0

        self.solve()

    # CONTROLS:
    # - Previous -> Go a step back (works by Button or Left Arrow Key)
    # - Next -> Go a step ahead (works by Button or Right Arrow Key)
    # - Save -> Save Algorithm Execution to a .txt file (works by Button)
    # - Dynamically changes game statistics
    def create_controls(self):
        control_frame = tk.Frame(self.root, bg="lightgray")
        control_frame.pack(side=tk.TOP, pady=10)

        self.step_label = tk.Label(control_frame, text="Step: 0/0", font=("Arial", 14))
        self.step_label.pack(side=tk.LEFT, padx=10)

        prev_button = tk.Button(control_frame, text="← Previous", font=("Arial", 12), command=self.previous_step)
        next_button = tk.Button(control_frame, text="Next →", font=("Arial", 12), command=self.next_step)
        save_button = tk.Button(control_frame, text="Save", font=("Arial", 12), command=self.save_result)

        prev_button.pack(side=tk.LEFT, padx=5)
        next_button.pack(side=tk.LEFT, padx=5)
        save_button.pack(side=tk.RIGHT, padx=5)

        self.stats_label = tk.Label(self.root, text="Empty Branches = 0, States Explored = 0, Max Queue Size = 0", font=("Arial", 12))
        self.stats_label.pack(pady=5)

        self.game_info_label = tk.Label(self.root, text="", font=("Arial", 10))
        self.game_info_label.pack(pady=5)
        self.elapsed_time = 0
        self.update_game_info()

        self.root.bind("<Left>", lambda e: self.previous_step())
        self.root.bind("<Right>", lambda e: self.next_step())
        self.root.bind("<space>", lambda e: self.next_step())

    # Saves results to a .txt file
    # - The result data is specific to the algorithm
    def save_result(self):
        num_colors, num_branches = get_difficulty_settings(self.difficulty) 

        # !!! NAO MEXER NA INDENTAÇÃO DESTA FUNÇÃO POR FAVOR

        result_data = f"""Algorithm: BFS
Difficulty: {self.difficulty}             
Colors: {num_colors}
Branches: {num_branches}
Time Taken: {self.elapsed_time:.6f}s
States Explored: {self.states_explored}
Max Queue Size: {self.max_queue_size}
Solution Steps:
""" + "\n".join(f"{i+1}. {step}" for i, step in enumerate(self.solution))
        
        filename = f"../results/bfs/BFS_difficulty={self.difficulty}_exectime={self.elapsed_time:.5f}.txt"
        with open(filename, "w") as file:
            file.write(result_data)
        messagebox.showinfo("Saved", f"Results saved to {filename}")

    # Main Algorithm Function
    # - Checks for Solution -> Saves collected information in variables
    # - If no solution was found, a Popup displays a warning message
    # - If the algorithm doesn't find a solution after a minute, it displays a Popup with a warning
    def solve(self):
        print("Starting BFS...")
        queue = deque([(copy.deepcopy(self.branches), [])])
        visited = set()
        max_iterations = 10000000
        iterations = 0
        max_queue_size = 1
        start_time = time.perf_counter()
        timeout_seconds = 60  # Algorithm stops running if a minute passes
        timed_out = False

        while queue and iterations < max_iterations:

            if time.perf_counter() - start_time > timeout_seconds:
                timed_out = True
                break

            max_queue_size = max(max_queue_size, len(queue)) 
            state, moves = queue.popleft()  # BFS -> FIFO
            state_tuple = tuple(tuple(branch) for branch in state)  # Hashable state

            if state_tuple in visited:
                continue

            visited.add(state_tuple)
            iterations += 1

            if self.is_solved(state):
                end_time = time.perf_counter()
                self.elapsed_time = end_time - start_time
                self.solution = moves + [None] 
                self.final_state = copy.deepcopy(state) 
                self.total_moves = len(moves) 
                self.states_explored = iterations
                self.max_queue_size = max_queue_size 
                print(f"Solution found in {iterations} iterations and {self.elapsed_time:.3f} seconds!")
                self.update_step_counter()
                self.update_stats_display()
                return

            for new_state, move in self.get_possible_moves(state):
                new_state_tuple = tuple(tuple(branch) for branch in new_state)
                if new_state_tuple not in visited:
                    queue.append((new_state, moves + [move]))

        self.solution = None
        if timed_out:
            print(f"Search timed out after {iterations} iterations.")
            self.show_no_solution_popup(iterations, timed_out=True)
        else:
            print(f"No solution found after {iterations} iterations.")
            self.show_no_solution_popup(iterations, timed_out=False)

    # No Solution Popup (two cases)
    # 1. Solution doesn't exist with this algorithm
    # 2. 60 second timeout after no solution was found
    def show_no_solution_popup(self, iterations, timed_out=False):
        popup = tk.Toplevel(self.root)
        popup.title("No Solution Found")
        popup.configure(bg="red")
        popup.geometry("280x100")
        popup.transient(self.root) 
        popup.grab_set()
        
        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (280 // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (100 // 2)
        popup.geometry(f"280x100+{x}+{y}")
        
        if timed_out:
            label = tk.Label(popup, text=f"Search timed out after {iterations} iterations.", 
                         font=("Arial", 12, "bold"), bg="red", fg="white", wraplength=260)
        else:
            label = tk.Label(popup, text=f"No solution found after {iterations} iterations.", 
                         font=("Arial", 12, "bold"), bg="red", fg="white", wraplength=260)
        label.pack(pady=10, padx=10)

        close_button = tk.Button(popup, text="OK", font=("Arial", 10), command=popup.destroy, 
                                 bg="white", fg="black")
        close_button.pack(pady=5)
        
        popup.lift()  # Raise popup above other windows
        popup.attributes('-topmost', True)  # Force popup to stay on top

    # Check if a branch has exactly 4 birds of the same color
    def is_branch_complete(self, branch):
        return len(branch) == 4 and all(bird == branch[0] for bird in branch)

    # Remove complete branches from game state (Note: they remain visible)
    def eliminate_complete_branches(self, state):
        new_state = []
        for branch in state:
            if not self.is_branch_complete(branch):
                new_state.append(branch)
            else:
                new_state.append([]) 
        return new_state

    def get_possible_moves(self, state):
        moves = []
        state = [list(branch) for branch in state] 
        
        state = self.eliminate_complete_branches(state)

        for i, src in enumerate(state):
            if not src:
                continue

            bird_to_move = src[-1]
            move_group = 1
            while move_group < len(src) and src[-(move_group + 1)] == bird_to_move:
                move_group += 1 
                
            for j, dst in enumerate(state):
                if i != j and len(dst) + move_group <= 4: 
                    if not dst or dst[-1] == bird_to_move:
                        new_state = copy.deepcopy(state)
                        birds_moving = new_state[i][-move_group:]
                        new_state[i] = new_state[i][:-move_group] 
                        new_state[j].extend(birds_moving)
                        
                        new_state = self.eliminate_complete_branches(new_state)
                        moves.append((new_state, (i, j)))

        return moves

    # Considers all empty branches as solved
    def is_solved(self, state):
        return all(len(branch) == 0 for branch in state)

    def draw_state(self, state):
        self.game.canvas.delete("all")
        self.game.draw_background()

        for index, branch in enumerate(state):
            x, y = self.game.branches[index]["x"], self.game.branches[index]["y"]
            
            # Choose the correct branch image based on position
            if x < 300: # Left side
                branch_img = self.game.branch_img_left_tk
            else: # Right side
                branch_img = self.game.branch_img_tk

            self.game.canvas.create_image(x, y, anchor=tk.NW, image=branch_img)

            for i, bird in enumerate(branch):
                if x < 300: # Left branches grow left-to-right
                    bird_x_offset = 5 + i * 50
                    bird_image = self.game.bird_images[bird + "_flipped"] 
                else: # Right branches grow right-to-left
                    bird_x_offset = 170 - i * 50
                    bird_image = self.game.bird_images[bird]

                self.game.canvas.create_image(x + bird_x_offset, y - 60, anchor=tk.NW, image=bird_image)

    # INTERFACE CONTROLS - "Go back a step button" is pressed
    def previous_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.rebuild_state(self.current_step)

    # INTERFACE CONTROLS - "Go step ahead button" is pressed
    def next_step(self):
        if self.solution and self.current_step < (len(self.solution)-1):
            self.current_step += 1
            self.rebuild_state(self.current_step)

    # Dynamically updates labels at the top of the screen and redraws the game to match current state
    def rebuild_state(self, step):
        if step == len(self.solution):  
            self.draw_state(self.final_state)
        else:
            current_state = copy.deepcopy(self.branches)

            for i in range(step):
                src_idx, dst_idx = self.solution[i]

                bird_to_move = current_state[src_idx][-1]
                move_group = 1
                while move_group < len(current_state[src_idx]) and current_state[src_idx][-move_group - 1] == bird_to_move:
                    move_group += 1

                birds_moving = current_state[src_idx][-move_group:]
                current_state[src_idx] = current_state[src_idx][:-move_group]
                current_state[dst_idx].extend(birds_moving)
                
                current_state = self.eliminate_complete_branches(current_state)

            self.draw_state(current_state)

        self.update_step_counter()
        self.update_stats_display()

    def update_step_counter(self):
        if self.solution:
            self.step_label.config(text=f"Step: {self.current_step}/{len(self.solution)-1}")

    # Dynamic Statistics Label  
    def update_stats_display(self):
        if self.current_step == len(self.solution):
            current_state = self.final_state
        else:
            current_state = copy.deepcopy(self.branches)
            for i in range(self.current_step):
                src_idx, dst_idx = self.solution[i]

                bird_to_move = current_state[src_idx][-1]
                move_group = 1
                while move_group < len(current_state[src_idx]) and current_state[src_idx][-move_group - 1] == bird_to_move:
                    move_group += 1

                birds_moving = current_state[src_idx][-move_group:]
                current_state[src_idx] = current_state[src_idx][:-move_group]
                current_state[dst_idx].extend(birds_moving)
                current_state = self.eliminate_complete_branches(current_state) 

        empty_branches = sum(1 for branch in current_state if len(branch) == 0)
        stats_text = (
            f"Time: {self.elapsed_time:.3f}s, "
            f"Empty Branches: {empty_branches}, "
            f"States Explored: {self.states_explored}, "
            f"Max Queue Size: {self.max_queue_size}"
        )
        self.stats_label.config(text=stats_text)

    # These remain the same for all states
    def update_game_info(self):
        num_colors, num_branches = get_difficulty_settings(self.difficulty) 

        info_text = f"BFS, Difficulty: {self.difficulty}, Colors: {num_colors}, Branches: {num_branches}"
        self.game_info_label.config(text=info_text)