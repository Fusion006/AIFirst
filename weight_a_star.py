import tkinter as tk
import copy
import time
import heapq
from game import BirdSortGame, center_window
from difficulty_manager import get_difficulty_settings
from tkinter import messagebox

class BirdSortWeightedAStar:
    def __init__(self, root, difficulty, weight=2.0):
        self.root = root
        self.root.title("Bird Sort Weighted A* Solution")
        center_window(self.root)
        
        self.weight = weight
        self.difficulty = difficulty
        self.create_controls()
        self.game = BirdSortGame(root, difficulty)
        self.game.root.unbind("<Button-1>")  # Disable manual play

        self.branches = [list(branch["birds"]) for branch in self.game.branches]
        self.solution = []
        self.current_step = 0

        self.solve()

    def solve(self):
        print("Starting Weighted A* search...")
        start_state = copy.deepcopy(self.branches)
        start_node = (0, 0, start_state, [])  # (f_score, node_count, state, moves)
        visited = set()
        heap = [start_node]
        node_count = 1
        max_iterations = 10000000
        iterations = 0
        max_queue_size = 1
        start_time = time.perf_counter()
        timeout_seconds = 60  # Stop after a minute
        timed_out = False  # Track whether timeout occurred

        while heap and iterations < max_iterations:

            if time.perf_counter() - start_time > timeout_seconds:
                timed_out = True
                break

            max_queue_size = max(max_queue_size, len(heap))
            _, _, current_state, moves = heapq.heappop(heap)
            state_tuple = tuple(tuple(branch) for branch in current_state)

            if state_tuple in visited:
                continue

            visited.add(state_tuple)
            iterations += 1

            if self.is_solved(current_state):
                end_time = time.perf_counter()
                self.elapsed_time = end_time - start_time
                self.solution = moves + [None]
                self.final_state = copy.deepcopy(current_state)
                self.total_moves = len(moves)
                self.states_explored = iterations
                self.max_queue_size = max_queue_size
                print(f"Solution found in {iterations} iterations and {self.elapsed_time:.3f} seconds!")
                self.update_step_counter()
                self.update_stats_display()
                return

            for new_state, move in self.get_possible_moves(current_state):
                if tuple(tuple(branch) for branch in new_state) not in visited:
                    g_score = len(moves) + 1
                    h_score = self.heuristic(new_state)
                    # Key difference: weighted f_score calculation
                    f_score = g_score + self.weight * h_score
                    node_count += 1
                    heapq.heappush(heap, (f_score, node_count, new_state, moves + [move]))

        self.solution = None
        if timed_out:
            print(f"Search timed out after {iterations} iterations.")
            self.show_no_solution_popup(iterations, timed_out=True)
        else:
            print(f"No solution found after {iterations} iterations.")
            self.show_no_solution_popup(iterations, timed_out=False)

    def show_no_solution_popup(self, iterations, timed_out=False):
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

    def update_game_info(self):
        num_colors, num_branches = get_difficulty_settings(self.difficulty)
        info_text = f"Algorithm: Weighted A* (w={self.weight}), Difficulty: {self.difficulty}, Colors: {num_colors}, Branches: {num_branches}"
        self.game_info_label.config(text=info_text)

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

        result_data = f"""Algorithm: Weighted A*
Difficulty: {self.difficulty}             
Colors: {num_colors}
Branches: {num_branches}
Time Taken: {self.elapsed_time:.6f}s
States Explored: {self.states_explored}
Max Queue Size: {self.max_queue_size}
Solution Steps:
""" + "\n".join(f"{i+1}. {step}" for i, step in enumerate(self.solution))
        
        filename = f"game/results/astar_weighted/ASTARWEIGHTED_difficulty={self.difficulty}_exectime={self.elapsed_time:.5f}.txt"
        with open(filename, "w") as file:
            file.write(result_data)
        messagebox.showinfo("Saved", f"Results saved to {filename}")

    def heuristic(self, state):
        score = 0
        for branch in state:
            if not branch:
                continue
            
            # Penalize mixed colors in a branch
            colors = set(branch)
            if len(colors) > 1:
                score += len(colors) * 2
            
            # Reward nearly complete branches
            if len(colors) == 1:
                score -= (len(branch) / 4) * 3
                
            # Penalize scattered same-color birds
            for color in colors:
                color_count = branch.count(color)
                if color_count < 4:
                    score += (4 - color_count)
                    
        return score

    def is_solved(self, state):
        return all(len(branch) == 0 for branch in state)

    def is_branch_complete(self, branch):
        return len(branch) == 4 and all(bird == branch[0] for bird in branch)

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

    def draw_state(self, state):
        self.game.canvas.delete("all")
        self.game.draw_background()

        for index, branch in enumerate(state):
            x, y = self.game.branches[index]["x"], self.game.branches[index]["y"]
            
            if x < 300:
                branch_img = self.game.branch_img_left_tk
            else:
                branch_img = self.game.branch_img_tk

            self.game.canvas.create_image(x, y, anchor=tk.NW, image=branch_img)

            for i, bird in enumerate(branch):
                if x < 300:
                    bird_x_offset = 5 + i * 50
                    bird_image = self.game.bird_images[bird + "_flipped"]
                else:
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
