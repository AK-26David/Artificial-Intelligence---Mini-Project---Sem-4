import time
import tkinter as tk
from random import randint
from tkinter import messagebox

from PIL import ImageGrab

from generator import _gen
from isvalid import is_num_valid, is_valid_sudoku


# Test
class SudokuSolver:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku Solver")
        self.master.resizable(False, False)
        self.grid = [[None for _ in range(9)] for _ in range(9)]
        self.difficulty = "Easy"
        self.generated_list = []
        self.default_color = "#c1cdcd"
        self.grid_clicked_color = "#98fb98"
        self.grid_affected_color = "#98fb98"
        self.grid_unaffected_color = "#c1cdcd"
        self.generated_color = "#c1cdcd"
        self.fg_white = "white"
        self.fg_black = "black"
        self.grid_clicked = None
        self.buttons_can_be_clicked = True
        self._create_grid()
        self._create_menu()
        self._buttons()
        self._bindings()

    def _create_grid(self):
        # Create the grid
        self.grid = []
        for i in range(9):
            row = []
            for j in range(9):
                entry = tk.Entry(
                    width=3,
                    font=("Courier", 30),
                    justify="center",
                    bd=1,
                    relief=tk.RIDGE,
                )
                entry.grid(row=i, column=j, padx=1, pady=1)
                row.append(entry)
                entry.config(bg=self.default_color)
                entry.config(fg=self.fg_black)
                entry.bind("<Button-1>", self._grid_clicked)
            self.grid.append(row)

    def _grid_clicked(self, event):
        # Highlight the clicked cell, row, column and the 3x3 sub-grid
        # Get the row and column of the clicked cell
        row = event.widget.grid_info()["row"]
        col = event.widget.grid_info()["column"]
        self.grid_clicked = event.widget
        self._unhighlight(row, col)

        # Highlight the clicked cell's row and column
        for i in range(9):
            self.grid[row][i].config(bg=self.grid_affected_color)
            self.grid[i][col].config(bg=self.grid_affected_color)

        # Highlight the clicked cell's 3x3 sub-grid
        for i in range(3):
            for j in range(3):
                self.grid[(row // 3) * 3 + i][(col // 3) * 3 + j].config(
                    bg=self.grid_affected_color
                )

        # Highlight the clicked cell after its focused
        event.widget.config(bg=self.grid_clicked_color)

    def _unhighlight(self, row, col):
        # Unhighlight the entire grid
        for i in range(9):
            for j in range(9):
                self.grid[i][j].config(bg=self.grid_unaffected_color)

        # Unhighlight the clicked cell
        self.grid_clicked.config(bg=self.grid_unaffected_color)

        # Unhighlight the clicked cell's row and column
        for i in range(9):
            self.grid[row][i].config(bg=self.grid_unaffected_color)
            self.grid[i][col].config(bg=self.grid_unaffected_color)

    def _clickable_buttons(self):
        self.buttons_can_be_clicked = True

        # Make the buttons clickable
        self.solve_button.config(state=tk.NORMAL)
        self.generate_button.config(state=tk.NORMAL)
        self.clear_button.config(state=tk.NORMAL)

    def _unclickable_buttons(self):
        self.buttons_can_be_clicked = False
        
        # Make the buttons unclickable
        self.solve_button.config(state=tk.DISABLED)
        self.generate_button.config(state=tk.DISABLED)
        self.clear_button.config(state=tk.DISABLED)

    def _menu_unclickable(self):
        self.file_menu.entryconfig("Exit(E)", state=tk.DISABLED)
        self.puzzle_menu.entryconfig("Solve(S)", state=tk.DISABLED)
        self.puzzle_menu.entryconfig("Generate(G)", state=tk.DISABLED)
        self.puzzle_menu.entryconfig("Clear(C)", state=tk.DISABLED)

    def _menu_clickable(self):
        self.file_menu.entryconfig("Exit(E)", state=tk.NORMAL)
        self.puzzle_menu.entryconfig("Solve(S)", state=tk.NORMAL)
        self.puzzle_menu.entryconfig("Generate(G)", state=tk.NORMAL)
        self.puzzle_menu.entryconfig("Clear(C)", state=tk.NORMAL)

    def _toggle_buttons(self):
        if self.buttons_can_be_clicked:
            self._unclickable_buttons()
            self._menu_unclickable()
        else:
            self._clickable_buttons()
            self._menu_clickable()

    def _create_menu(self):
        
        # Create a menu
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        
        # File menu
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        
        # Difficulty dropdown menu
        self.difficulty_menu = tk.Menu(self.file_menu, tearoff=0)
        self.file_menu.add_cascade(label="Difficulty", menu=self.difficulty_menu)
        self.difficulty_menu.add_command(
            label="Easy", command=lambda: self._toggle_difficulty("Easy")
        )
        self.difficulty_menu.add_command(
            label="Medium", command=lambda: self._toggle_difficulty("Medium")
        )
        self.difficulty_menu.add_command(
            label="Hard", command=lambda: self._toggle_difficulty("Hard")
        )
        self.file_menu.add_command(label="Exit(E)", command=self.master.destroy)

        # Puzzle Menu
        self.puzzle_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Puzzle", menu=self.puzzle_menu)
        self.puzzle_menu.add_command(label="Solve(S)", command=self.solve)
        self.puzzle_menu.add_command(
            label="Generate(G)", command=lambda: self.generate("Easy")
        )
        self.puzzle_menu.add_command(label="Clear(C)", command=self.clear)

        # About Menu
        self.about_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_command(label="About", command=self._about)

    def _about(self):
        messagebox.showinfo(
            "About",
            "Sudoku Solver\n"
            "   - GUI version\n"
            "   - Uses backtracking algorithm\n"
            "   - Able to generate and solve puzzles\n"
            "   - Able to change difficulty levels\n"
            "\n"
            "Created by: \n"
            "    - Arnav Karnik\n"
            "    - Yashas S\n"
            "    - Nikhil Nair\n"
            "    - Krishanu Banerjee\n",
        )

    def _buttons(self):
        
        # Solve button
        self.solve_button = tk.Button(
            self.master,
            text="Solve",
            command=self.solve,
            bg="green2",
            fg="white",
            width=14,
            font=('Helvetica','11','bold')
        )
        self.solve_button.grid(row=9, column=0, columnspan=2)

        # Generate button
        self.generate_button = tk.Button(
            self.master,
            text="Generate",
            command=lambda: self.generate(self.difficulty),
            bg="royalblue1",
            fg="white",
            width=13,
            font=('Helvetica','11','bold')
        )
        self.generate_button.grid(row=9, column=2, columnspan=2)

        # Difficulty button
        self.difficulty_button = tk.Menubutton(
            self.master
        )
        self.difficulty_button.grid(row=9, column=5, columnspan=2)
        self.difficulty_menu = tk.Menu(self.difficulty_button, tearoff=0)

        self.difficulty_menu.add_command(
            label="Easy", command=lambda: self._toggle_difficulty("Easy")
        )
        self.difficulty_menu.add_command(
            label="Medium", command=lambda: self._toggle_difficulty("Medium")
        )
        self.difficulty_menu.add_command(
            label="Hard", command=lambda: self._toggle_difficulty("Hard")
        )
        self.difficulty_button["menu"] = self.difficulty_menu

        # Clear button
        self.clear_button = tk.Button(
            self.master,
            text="Clear",
            command=self.clear,
            bg="red2",
            fg="white",
            width=12,
            font=('Helvetica','11','bold')
        )
        self.clear_button.grid(row=9, column=7, columnspan=2)

    def _bindings(self):

        # Type S to solve the puzzle
        self.master.bind(
            "s", lambda event: self.solve() if self.buttons_can_be_clicked else None
        )
        self.master.bind(
            "S", lambda event: self.solve() if self.buttons_can_be_clicked else None
        )

        # Type G to generate a puzzle
        self.master.bind(
            "g",
            lambda event: self.generate(self.difficulty)
            if self.buttons_can_be_clicked
            else None,
        )
        self.master.bind(
            "G",
            lambda event: self.generate(self.difficulty)
            if self.buttons_can_be_clicked
            else None,
        )

        # Type C to clear the puzzle
        self.master.bind(
            "c", lambda event: self.clear() if self.buttons_can_be_clicked else None
        )
        self.master.bind(
            "C", lambda event: self.clear() if self.buttons_can_be_clicked else None
        )

        # Type E to exit the program
        self.master.bind("e", lambda event: self.master.destroy())
        self.master.bind("E", lambda event: self.master.destroy())

    def _toggle_difficulty(self, difficulty):
        self.difficulty = difficulty

    def solve(self):
        # Make the other buttons unclickable
        self._toggle_buttons()

        puzzle = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                try:
                    puzzle[i][j] = int(self.grid[i][j].get())
                except ValueError:
                    pass
        # print(puzzle)
        if is_valid_sudoku(puzzle):
            if self.backtrack(puzzle):
                for i in range(9):
                    for j in range(9):
                        self.grid[i][j].delete(0, tk.END)
                        self.grid[i][j].insert(0, puzzle[i][j])
                        # sleep for 0.05 seconds
                        time.sleep(randint(1, 10) / 100)
                        self.master.update()
            else:
                messagebox.showerror("Error", "No solution exists")
        else:
            messagebox.showerror("Error", "Invalid Sudoku")

        # make the other buttons clickable
        self._toggle_buttons()

    def backtrack(self, puzzle):
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] == 0:
                    for num in range(1, 10):
                        if is_num_valid(puzzle, i, j, num):
                            puzzle[i][j] = num
                            if self.backtrack(puzzle):
                                return True
                            puzzle[i][j] = 0
                    return False
        return True

    def generate(self, difficulty):
        board = _gen()
        for i in range(9):
            for j in range(9):
                self.grid[i][j].delete(0, tk.END)
                self.grid[i][j].insert(0, board[i][j])
                self.grid[i][j].config(bg="white")
        if difficulty == "Easy":
            for i in range(9):
                for j in range(9):
                    if randint(0, 1) != 1:
                        self.grid[i][j].delete(0, tk.END)
                        self.grid[i][j].config(bg=self.generated_color)
                        self.generated_list.append((i, j))
        elif difficulty == "Medium":
            for i in range(9):
                for j in range(9):
                    if randint(0, 3) != 1:
                        self.grid[i][j].delete(0, tk.END)
                        self.grid[i][j].config(bg=self.generated_color)
                        self.generated_list.append((i, j))
        elif difficulty == "Hard":
            for i in range(9):
                for j in range(9):
                    if randint(0, 5) != 1:
                        self.grid[i][j].delete(0, tk.END)
                        self.grid[i][j].config(bg=self.generated_color)
                        self.generated_list.append((i, j))

    def clear(self):
        for i in range(9):
            for j in range(9):
                self.grid[i][j].delete(0, tk.END)
                self.grid[i][j].config(bg=self.default_color)


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolver(root)
    root.mainloop()
