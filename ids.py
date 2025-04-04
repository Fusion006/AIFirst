import tkinter as tk
import copy
import time
from game import BirdSortGame, center_window
from difficulty_manager import get_difficulty_settings
from tkinter import messagebox

class BirdSortIDS:
    def __init__(self, root, difficulty):
        self.root = root
        self.root.title("Bird Sort IDS Solution")
        center_window(self.root)

        self.difficulty = difficulty
        self.create_controls()
        self.game = BirdSortGame(root, difficulty)
        self.game.root.unbind("<Button-1>")  # Disable manual play

        self.branches = [list(branch["birds"]) for branch in self.game.branches]
        self.solution = []
        self.current_step = 0

        self.solve()

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

        self.stats_label = tk.Label(self.root, text="Empty Branches = 0, States Explored = 0, Nodes Generated = 0", font=("Arial", 12))
        self.stats_label.pack(pady=5)

        self.game_info_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.game_info_label.pack(pady=5)
        self.elapsed_time = 0
        self.update_game_info()

        self.root.bind("<Left>", lambda e: self.previous_step())
        self.root.bind("<Right>", lambda e: self.next_step())
        self.root.bind("<space>", lambda e: self.next_step())

    def save_result(self):
        num_colors, num_branches = get_difficulty_settings(self.difficulty) 

        # NAO MEXER NA INDENTAÇÃO DESTA FUNÇÃO POR FAVOR

        result_data = f"""Algorithm: IDS
Difficulty: {self.difficulty}             
Colors: {num_colors}
Branches: {num_branches}
Time Taken: {self.elapsed_time:.6f}s
States Explored: {self.states_explored}
Depth Limit: {self.depth_limit}
Nodes Generated: {self.nodes_generated}
Solution Steps:
""" + "\n".join(f"{i+1}. {step}" for i, step in enumerate(self.solution))
        
        filename = f"game_states/results/ids/IDS_difficulty={self.difficulty}_exectime={self.elapsed_time:.5f}.txt"
        with open(filename, "w") as file:
            file.write(result_data)
        messagebox.showinfo("Saved", f"Results saved to {filename}")

    def dls(self, state, depth, max_depth, moves, visited, total_nodes_generated):
        """Depth-limited search helper function"""
        if depth > max_depth:
            return None

        state_tuple = tuple(tuple(branch) for branch in state)
        if state_tuple in visited:
            return None

        visited.add(state_tuple)

        total_nodes_generated[0] += 1 

        if self.is_solved(state):
            return moves

        if depth == max_depth:
            return None

        for new_state, move in self.get_possible_moves(state):
            new_state_tuple = tuple(tuple(branch) for branch in new_state)
            if new_state_tuple not in visited:
                result = self.dls(new_state, depth + 1, max_depth, moves + [move], visited, total_nodes_generated)
                if result is not None:
                    return result

        return None

    def solve(self):
        print("Starting IDS...")
        max_depth = 1
        max_iterations = 10000
        iterations = 0
        total_nodes_generated = [0]
        start_time = time.perf_counter()

        while iterations < max_iterations:
            print(f"Trying depth limit: {max_depth}")
            visited = set()
            result = self.dls(copy.deepcopy(self.branches), 0, max_depth, [], visited, total_nodes_generated)
            
            if result is not None:
                end_time = time.perf_counter()
                self.elapsed_time = end_time - start_time
                self.solution = result + [None]  # Append None for final state
                self.final_state = self.get_final_state(result)
                self.states_explored = iterations
                self.depth_limit = max_depth
                self.nodes_generated = total_nodes_generated[0]  # Store final nodes generated count
                print(f"Solution found at depth {max_depth}!")
                self.update_step_counter()
                self.update_stats_display()
                return
            
            max_depth += 1
            iterations += 1

        self.solution = None
        print(f"No solution found within {max_iterations} depth iterations.")
        self.show_no_solution_popup(iterations)

    def show_no_solution_popup(self, iterations):
        popup = tk.Toplevel(self.root)
        popup.title("No Solution Found")
        popup.configure(bg="red")
        popup.geometry("280x100")
        popup.transient(self.root)  # Make popup modal
        popup.grab_set()  # Ensure popup is focused
        
        # Center the popup relative to the main window
        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (280 // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (100 // 2)
        popup.geometry(f"280x100+{x}+{y}")
        
        label = tk.Label(popup, text=f"No solution found after {iterations} iterations.", 
                         font=("Arial", 12, "bold"), bg="red", fg="white", wraplength=260)
        label.pack(pady=10, padx=10)

        close_button = tk.Button(popup, text="OK", font=("Arial", 10), command=popup.destroy, 
                                 bg="white", fg="black")
        close_button.pack(pady=5)
        
        popup.lift()  # Raise popup above other windows
        popup.attributes('-topmost', True)  # Force popup to stay on top

    def get_final_state(self, moves):
        """Reconstruct final state from moves"""
        state = copy.deepcopy(self.branches)
        for src_idx, dst_idx in moves:
            bird_to_move = state[src_idx][-1]
            move_group = 1
            while move_group < len(state[src_idx]) and state[src_idx][-move_group - 1] == bird_to_move:
                move_group += 1

            birds_moving = state[src_idx][-move_group:]
            state[src_idx] = state[src_idx][:-move_group]
            state[dst_idx].extend(birds_moving)
            state = self.eliminate_complete_branches(state)
        return state

    def is_solved(self, state):
        """Modified to consider empty branches as solved"""
        return all(len(branch) == 0 for branch in state)

    def is_branch_complete(self, branch):
        """Check if a branch has exactly 4 birds of the same color"""
        return len(branch) == 4 and all(bird == branch[0] for bird in branch)

    def eliminate_complete_branches(self, state):
        """Remove complete branches from game state"""
        new_state = []
        for branch in state:
            if not self.is_branch_complete(branch):
                new_state.append(branch)
            else:
                new_state.append([])  # Replace complete branch with empty branch
        return new_state
    
    def get_possible_moves(self, state):
        moves = []
        state = [list(branch) for branch in state]  # Convert to mutable lists
        
        # First eliminate any complete branches
        state = self.eliminate_complete_branches(state)

        for i, src in enumerate(state):
            if not src:
                continue  # Skip empty branches

            bird_to_move = src[-1]
            move_group = 1
            while move_group < len(src) and src[-(move_group + 1)] == bird_to_move:
                move_group += 1  # Count consecutive birds of the same color

            for j, dst in enumerate(state):
                if i != j and len(dst) + move_group <= 4:  # Check 4-bird limit
                    if not dst or dst[-1] == bird_to_move:
                        new_state = copy.deepcopy(state)  # Copy before modifying
                        birds_moving = new_state[i][-move_group:]  # Take the group
                        new_state[i] = new_state[i][:-move_group]  # Remove from source
                        new_state[j].extend(birds_moving)  # Add to destination
                        
                        # Check if the move created a complete branch
                        new_state = self.eliminate_complete_branches(new_state)
                        moves.append((new_state, (i, j)))

        return moves
    
    def draw_state(self, state):
        self.game.canvas.delete("all")
        self.game.draw_background()

        for index, branch in enumerate(state):
            x, y = self.game.branches[index]["x"], self.game.branches[index]["y"]
            
            # Choose the correct branch image based on position
            if x < 300:  # Left side
                branch_img = self.game.branch_img_left_tk
            else:  # Right side
                branch_img = self.game.branch_img_tk

            # Draw the branch
            self.game.canvas.create_image(x, y, anchor=tk.NW, image=branch_img)

            for i, bird in enumerate(branch):
                if x < 300:  # Left branches grow left-to-right
                    bird_x_offset = 5 + i * 50
                    bird_image = self.game.bird_images[bird + "_flipped"]  # Use flipped version
                else:  # Right branches grow right-to-left
                    bird_x_offset = 170 - i * 50
                    bird_image = self.game.bird_images[bird]

                self.game.canvas.create_image(x + bird_x_offset, y - 60, anchor=tk.NW, image=bird_image)
    
    def previous_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.rebuild_state(self.current_step)

    def next_step(self):
        if self.solution and self.current_step < (len(self.solution)-1):
            self.current_step += 1
            self.rebuild_state(self.current_step)

    def rebuild_state(self, step):
        if step == len(self.solution):  
            # If at the final step, just display the solved state
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
        self.update_game_info()

    def update_step_counter(self):
        if self.solution:
            self.step_label.config(text=f"Step: {self.current_step}/{len(self.solution)-1}")

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
                current_state = self.eliminate_complete_branches(current_state)  # Update for eliminated branches

        empty_branches = sum(1 for branch in current_state if len(branch) == 0)
        stats_text = (
            f"Time: {self.elapsed_time:.3f}s, "
            f"Empty Branches: {empty_branches}, "
            f"Depth Limit: {self.depth_limit}, "
            f"Nodes Generated: {self.nodes_generated}"
        )
        self.stats_label.config(text=stats_text)

    def update_game_info(self):
        num_colors, num_branches = get_difficulty_settings(self.difficulty)  # Get values from function

        info_text = f"Algorithm: IDS, Difficulty: {self.difficulty}, Colors: {num_colors}, Branches: {num_branches}"
        self.game_info_label.config(text=info_text)