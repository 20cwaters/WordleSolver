import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import random
from wordle_solver import load_past_words, load_words, filter_words, suggest_next_guess

class WordleSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordle Solver GUI")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.configure(bg="#f0f0f0")
        
        # Set up the solver variables
        self.past_words = load_past_words()
        self.exclude_past_words = tk.BooleanVar(value=True)  # Default: exclude past words
        self.all_words_with_past = None  # Will hold all words including past words
        self.all_words = None  # Will hold filtered words (or all if not excluding)
        self.load_word_lists()  # Initialize word lists
        
        self.possible_words = list(self.all_words)
        self.known_letters = [None] * 5
        self.present_letters = set()
        self.absent_letters = set()
        self.yellow_misplaced = [set() for _ in range(5)]
        self.tried_letters = set()
        self.guess_number = 1
        self.current_guess = ""
        self.current_feedback = ["X"] * 5
        
        # Color constants
        self.GREEN = "#6aaa64"  # Wordle green
        self.YELLOW = "#c9b458"  # Wordle yellow
        self.GRAY = "#787c7e"    # Wordle gray
        self.EMPTY = "#ffffff"   # White for empty
        self.BG_COLOR = "#f0f0f0"  # Light gray background
        
        # Main frame
        self.main_frame = tk.Frame(root, bg=self.BG_COLOR)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # Title
        self.title_label = tk.Label(
            self.main_frame, 
            text="Wordle Solver", 
            font=("Helvetica", 24, "bold"),
            bg=self.BG_COLOR
        )
        self.title_label.pack(pady=(0, 20))
        
        # Frame for word list options
        self.options_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        self.options_frame.pack(pady=(0, 10), fill=tk.X)
        
        # Checkbox to exclude past words
        self.exclude_past_checkbox = tk.Checkbutton(
            self.options_frame,
            text="Exclude past used Wordle words",
            variable=self.exclude_past_words,
            bg=self.BG_COLOR,
            command=self.toggle_exclude_past_words
        )
        self.exclude_past_checkbox.pack(side=tk.LEFT, padx=(0, 10))
        
        # Info about excluded words
        self.excluded_info = tk.Label(
            self.options_frame,
            text=self.get_word_count_text(),
            font=("Helvetica", 10),
            bg=self.BG_COLOR
        )
        self.excluded_info.pack(side=tk.LEFT)
        
        # Frame for suggested word
        self.suggestion_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        self.suggestion_frame.pack(pady=10, fill=tk.X)
        
        self.suggestion_label = tk.Label(
            self.suggestion_frame,
            text="Suggested word:",
            font=("Helvetica", 12),
            bg=self.BG_COLOR
        )
        self.suggestion_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.suggested_word = tk.StringVar()
        self.suggested_word_label = tk.Label(
            self.suggestion_frame,
            textvariable=self.suggested_word,
            font=("Helvetica", 16, "bold"),
            bg=self.BG_COLOR
        )
        self.suggested_word_label.pack(side=tk.LEFT)
        
        # Frame for guess input
        self.guess_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        self.guess_frame.pack(pady=10, fill=tk.X)
        
        self.guess_label = tk.Label(
            self.guess_frame,
            text="Enter your guess:",
            font=("Helvetica", 12),
            bg=self.BG_COLOR
        )
        self.guess_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.guess_var = tk.StringVar()
        self.guess_entry = tk.Entry(
            self.guess_frame,
            textvariable=self.guess_var,
            font=("Helvetica", 16),
            width=10
        )
        self.guess_entry.pack(side=tk.LEFT)
        
        # Frame for letter buttons
        self.letters_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        self.letters_frame.pack(pady=10)
        
        # Create letter boxes
        self.letter_boxes = []
        for i in range(5):
            box = tk.Label(
                self.letters_frame,
                text="",
                font=("Helvetica", 24, "bold"),
                width=2,
                height=1,
                relief=tk.RAISED,
                bg=self.EMPTY
            )
            box.pack(side=tk.LEFT, padx=5)
            box.bind("<Button-1>", lambda event, idx=i: self.toggle_letter_color(idx))
            self.letter_boxes.append(box)
        
        # Frame for submit button
        self.submit_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        self.submit_frame.pack(pady=10)
        
        self.enter_guess_btn = tk.Button(
            self.submit_frame,
            text="Enter Guess",
            font=("Helvetica", 12),
            command=self.enter_guess
        )
        self.enter_guess_btn.pack(side=tk.LEFT, padx=5)
        
        self.submit_btn = tk.Button(
            self.submit_frame,
            text="Submit Feedback",
            font=("Helvetica", 12),
            command=self.submit_feedback,
            state=tk.DISABLED
        )
        self.submit_btn.pack(side=tk.LEFT, padx=5)
        
        self.reset_btn = tk.Button(
            self.submit_frame,
            text="New Game",
            font=("Helvetica", 12),
            command=self.reset_game
        )
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Frame for game status
        self.status_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        self.status_frame.pack(pady=10, fill=tk.X)
        
        self.status_label = tk.Label(
            self.status_frame,
            text=f"Guess {self.guess_number}/6",
            font=("Helvetica", 12, "bold"),
            bg=self.BG_COLOR
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Create frame for known letters display
        self.known_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        self.known_frame.pack(pady=5, fill=tk.X)
        
        self.known_label = tk.Label(
            self.known_frame,
            text="Known positions (Green):",
            font=("Helvetica", 10),
            bg=self.BG_COLOR
        )
        self.known_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.known_var = tk.StringVar(value="_ _ _ _ _")
        self.known_value = tk.Label(
            self.known_frame,
            textvariable=self.known_var,
            font=("Helvetica", 10, "bold"),
            bg=self.BG_COLOR
        )
        self.known_value.pack(side=tk.LEFT)
        
        # Create frame for present letters
        self.present_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        self.present_frame.pack(pady=5, fill=tk.X)
        
        self.present_label = tk.Label(
            self.present_frame,
            text="Present letters (Yellow):",
            font=("Helvetica", 10),
            bg=self.BG_COLOR
        )
        self.present_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.present_var = tk.StringVar(value="None")
        self.present_value = tk.Label(
            self.present_frame,
            textvariable=self.present_var,
            font=("Helvetica", 10, "bold"),
            bg=self.BG_COLOR
        )
        self.present_value.pack(side=tk.LEFT)
        
        # Create frame for absent letters
        self.absent_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        self.absent_frame.pack(pady=5, fill=tk.X)
        
        self.absent_label = tk.Label(
            self.absent_frame,
            text="Absent letters (Gray):",
            font=("Helvetica", 10),
            bg=self.BG_COLOR
        )
        self.absent_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.absent_var = tk.StringVar(value="None")
        self.absent_value = tk.Label(
            self.absent_frame,
            textvariable=self.absent_var,
            font=("Helvetica", 10, "bold"),
            bg=self.BG_COLOR
        )
        self.absent_value.pack(side=tk.LEFT)
        
        # Create frame for possible words
        self.possible_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        self.possible_frame.pack(pady=5, fill=tk.BOTH, expand=True)
        
        self.possible_label = tk.Label(
            self.possible_frame,
            text=f"Possible words ({len(self.possible_words)}):",
            font=("Helvetica", 10),
            bg=self.BG_COLOR
        )
        self.possible_label.pack(anchor=tk.W)
        
        self.possible_words_text = scrolledtext.ScrolledText(
            self.possible_frame,
            width=40,
            height=5,
            font=("Helvetica", 10)
        )
        self.possible_words_text.pack(fill=tk.BOTH, expand=True)
        
        # Instructions frame
        self.instructions_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        self.instructions_frame.pack(pady=10, fill=tk.X)
        
        self.instructions_label = tk.Label(
            self.instructions_frame,
            text="Instructions: 1. Enter your guess. 2. Click on letters to toggle color (Green/Yellow/Gray). 3. Submit feedback.",
            font=("Helvetica", 10),
            bg=self.BG_COLOR
        )
        self.instructions_label.pack()
        
        # Initialize with a suggested word
        self.update_suggestion()
        self.update_possible_words_display()
    
    def load_word_lists(self):
        """Load word lists based on current settings"""
        # If we haven't loaded all words yet, do it now
        if self.all_words_with_past is None:
            # Load all 5-letter words
            try:
                with open("words.txt", 'r') as file:
                    self.all_words_with_past = [word.strip().lower() for word in file 
                                         if len(word.strip()) == 5 and word.strip().isalpha()]
            except FileNotFoundError:
                messagebox.showwarning("Warning", "words.txt not found. Using small sample list.")
                # Fallback to a small sample list
                self.all_words_with_past = [
                    "crane", "slate", "audio", "adieu", "trace", "roate", "raise", "soare", 
                    "alert", "alter", "later", "table", "ratio", "stare", "arise", "irate",
                    "learn", "noble", "media", "ocean", "ideal", "radio", "steam", "dream"
                ]
        
        # Filter based on exclude_past_words setting
        if self.exclude_past_words.get() and self.past_words:
            self.all_words = [word for word in self.all_words_with_past if word not in self.past_words]
        else:
            self.all_words = list(self.all_words_with_past)
    
    def get_word_count_text(self):
        """Get text describing the current word list status"""
        if self.exclude_past_words.get() and self.past_words:
            return f"Using {len(self.all_words)} words (excluding {len(self.past_words)} past puzzles)"
        else:
            return f"Using all {len(self.all_words_with_past)} possible words"
    
    def toggle_exclude_past_words(self):
        """Handle toggling the exclude past words option"""
        # Reload word lists
        self.load_word_lists()
        
        # Update info text
        self.excluded_info.config(text=self.get_word_count_text())
        
        # Ask if user wants to start a new game with the new word list
        if messagebox.askyesno("Word List Changed", 
                             "Word list has been updated. Do you want to start a new game?"):
            self.reset_game()
        else:
            # Just update the possible words
            self.possible_words = [word for word in self.possible_words if word in self.all_words]
            self.update_possible_words_display()
            self.update_suggestion()
        
    def toggle_letter_color(self, index):
        """Toggle letter color between green, yellow, and gray"""
        if not self.current_guess or len(self.current_guess) != 5:
            return
            
        current_color = self.letter_boxes[index].cget("bg")
        
        if current_color == self.GREEN or current_color == "#6aaa64":
            # Green -> Yellow
            self.letter_boxes[index].config(bg=self.YELLOW)
            self.current_feedback[index] = "Y"
        elif current_color == self.YELLOW or current_color == "#c9b458":
            # Yellow -> Gray
            self.letter_boxes[index].config(bg=self.GRAY)
            self.current_feedback[index] = "X"
        else:
            # Gray -> Green
            self.letter_boxes[index].config(bg=self.GREEN)
            self.current_feedback[index] = "G"
    
    def enter_guess(self):
        """Process the user's guess input"""
        guess = self.guess_var.get().lower().strip()
        
        if not guess:
            messagebox.showerror("Error", "Please enter a guess.")
            return
            
        if len(guess) != 5:
            messagebox.showerror("Error", "Guess must be 5 letters.")
            return
            
        if not guess.isalpha():
            messagebox.showerror("Error", "Guess must contain only letters.")
            return
        
        # Set current guess and update letter boxes
        self.current_guess = guess
        for i in range(5):
            self.letter_boxes[i].config(text=guess[i].upper(), bg=self.GRAY)
            self.current_feedback[i] = "X"  # Default to gray
        
        # Enable submit button
        self.submit_btn.config(state=tk.NORMAL)
        self.enter_guess_btn.config(state=tk.DISABLED)
    
    def submit_feedback(self):
        """Process the feedback and update the word list"""
        feedback = "".join(self.current_feedback)
        
        # Add to tried letters
        for letter in self.current_guess:
            self.tried_letters.add(letter)
        
        # Check if all green (win)
        if feedback == "GGGGG":
            messagebox.showinfo("Congratulations!", f"You found the word: {self.current_guess.upper()}")
            self.submit_btn.config(state=tk.DISABLED)
            return
            
        # Filter words based on feedback
        self.possible_words = filter_words(
            self.possible_words, 
            self.current_guess, 
            feedback, 
            self.known_letters, 
            self.present_letters, 
            self.absent_letters, 
            self.yellow_misplaced
        )
        
        # Check if we ran out of possible words
        if not self.possible_words:
            messagebox.showwarning("Warning", "No possible words left. Please check your feedback.")
            self.submit_btn.config(state=tk.DISABLED)
            return
        
        # Update the guess number
        self.guess_number += 1
        if self.guess_number > 6:
            messagebox.showinfo("Game Over", "You've used all 6 guesses.")
            self.submit_btn.config(state=tk.DISABLED)
            return
            
        self.status_label.config(text=f"Guess {self.guess_number}/6")
        
        # Update displays
        self.update_known_letters_display()
        self.update_present_letters_display()
        self.update_absent_letters_display()
        self.update_possible_words_display()
        self.update_suggestion()
        
        # Reset for next guess
        self.guess_var.set("")
        for box in self.letter_boxes:
            box.config(text="", bg=self.EMPTY)
        self.current_guess = ""
        self.current_feedback = ["X"] * 5
        
        # Reset button states
        self.submit_btn.config(state=tk.DISABLED)
        self.enter_guess_btn.config(state=tk.NORMAL)
    
    def update_suggestion(self):
        """Update the suggested word"""
        if len(self.possible_words) == 0:
            self.suggested_word.set("No words left")
            return
            
        # For first guess, use predefined starters
        if self.guess_number == 1:
            starters = ["crane", "slate", "soare", "adieu", "trace"]
            valid_starters = [s for s in starters if s in self.possible_words]
            if valid_starters:
                suggestion = random.choice(valid_starters)
            else:
                suggestion = suggest_next_guess(self.possible_words, self.tried_letters)
        else:
            suggestion = suggest_next_guess(self.possible_words, self.tried_letters)
            
        self.suggested_word.set(suggestion.upper() if suggestion else "No suggestion")
    
    def update_known_letters_display(self):
        """Update the display of known letter positions"""
        known_str = []
        for letter in self.known_letters:
            if letter:
                known_str.append(letter.upper())
            else:
                known_str.append('_')
        self.known_var.set(" ".join(known_str))
    
    def update_present_letters_display(self):
        """Update the display of present letters (yellow)"""
        if self.present_letters:
            present_str = ", ".join(sorted([l.upper() for l in self.present_letters]))
            self.present_var.set(present_str)
        else:
            self.present_var.set("None")
    
    def update_absent_letters_display(self):
        """Update the display of absent letters (gray)"""
        if self.absent_letters:
            absent_str = ", ".join(sorted([l.upper() for l in self.absent_letters]))
            self.absent_var.set(absent_str)
        else:
            self.absent_var.set("None")
    
    def update_possible_words_display(self):
        """Update the display of possible words"""
        self.possible_label.config(text=f"Possible words ({len(self.possible_words)}):")
        
        self.possible_words_text.delete(1.0, tk.END)
        
        # Only show all words if there are a reasonable number
        show_all = len(self.possible_words) <= 200
        
        if show_all:
            # Sort alphabetically
            words_to_show = sorted(self.possible_words)
            
            # Format into columns for easier reading
            columns = 8  # Number of columns for display
            rows = (len(words_to_show) + columns - 1) // columns  # Ceiling division
            
            for row in range(rows):
                line = ""
                for col in range(columns):
                    idx = col * rows + row
                    if idx < len(words_to_show):
                        line += f"{words_to_show[idx]:8} "  # Pad to 8 chars
                self.possible_words_text.insert(tk.END, line + "\n")
        else:
            self.possible_words_text.insert(tk.END, "Too many words to display. Keep guessing to narrow down.")
    
    def reset_game(self):
        """Reset the game state for a new game"""
        # Reset solver variables
        self.possible_words = list(self.all_words)
        self.known_letters = [None] * 5
        self.present_letters = set()
        self.absent_letters = set()
        self.yellow_misplaced = [set() for _ in range(5)]
        self.tried_letters = set()
        self.guess_number = 1
        self.current_guess = ""
        self.current_feedback = ["X"] * 5
        
        # Reset UI
        self.status_label.config(text=f"Guess {self.guess_number}/6")
        self.guess_var.set("")
        for box in self.letter_boxes:
            box.config(text="", bg=self.EMPTY)
        
        # Reset displays
        self.known_var.set("_ _ _ _ _")
        self.present_var.set("None")
        self.absent_var.set("None")
        
        # Reset button states
        self.submit_btn.config(state=tk.DISABLED)
        self.enter_guess_btn.config(state=tk.NORMAL)
        
        # Update suggestion and possible words
        self.update_suggestion()
        self.update_possible_words_display()
        
        messagebox.showinfo("New Game", "Game has been reset. Good luck!")

if __name__ == "__main__":
    root = tk.Tk()
    app = WordleSolverGUI(root)
    root.mainloop() 