# Wordle Solver

A Python program to help you solve the daily Wordle puzzle. This solver uses letter frequency analysis and logical deduction to narrow down possible words based on your guesses and the feedback from Wordle.

## Features

- Suggests optimal starting words based on letter frequency analysis
- Tracks feedback from each guess (green, yellow, gray letters)
- Updates possible word list after each guess
- Displays remaining possible words
- Handles complex letter pattern cases (like repeated letters)
- **Excludes words already used in past Wordle puzzles**
- **User-friendly graphical interface**

## Command Line Interface

To use the command-line version:

1. Run the program: `python wordle_solver.py`
2. The solver will suggest an initial guess
3. Enter that word in your Wordle game
4. Enter your guess into the solver when prompted
5. Enter the feedback from Wordle using:
   - `G` for Green (correct letter, correct position)
   - `Y` for Yellow (correct letter, wrong position)
   - `X` for Gray/Black (letter not in the word)
6. The solver will suggest your next guess
7. Repeat steps 3-6 until you solve the puzzle!

## Graphical User Interface

For a more intuitive experience, use the GUI version:

1. Run the graphical interface: `python wordle_solver_gui.py`
2. The app shows a suggested word at the top
3. Enter that word in your Wordle game
4. Type the same word in the "Enter your guess" field and click "Enter Guess"
5. Click on each letter box to toggle its color according to Wordle's feedback:
   - Gray (default) → Green → Yellow → back to Gray
6. Click "Submit Feedback" when all colors match Wordle's feedback
7. The app will suggest your next word and update the possible words list
8. Repeat steps 3-7 until you solve the puzzle!

![Wordle Solver GUI](https://i.imgur.com/example.png) *(Image placeholder)*

## Example (Command Line)

```
===== Welcome to Wordle Solver! =====
Loaded 967 past used Wordle words to exclude
Excluded 967 past used words
Successfully loaded 1348 possible words from words.txt
Loaded 1348 possible words.
(Excluding words already used in past Wordle puzzles)

How to use:
1. Make a guess in your Wordle game
2. Enter your guess when prompted
3. Enter the feedback using:
   G - Green (correct letter, correct position)
   Y - Yellow (correct letter, wrong position)
   X - Gray (letter not in the word)

Example: If you guessed 'CRANE' and got Green, Yellow, Gray, Gray, Yellow
You would enter: GYXXY


--- Guess 1/6 ---
Number of possible words: 1348
Suggested guess: CRANE

After playing your guess in the Wordle game:
Enter your 5-letter guess: crane

Enter the color feedback from Wordle:
G = Green (correct letter, correct position)
Y = Yellow (correct letter, wrong position)
X = Gray/Black (letter not in the word)
Feedback (GGYXX format): GYXXX
Recorded: C(G) R(Y) A(X) N(X) E(X)

--- Guess 2/6 ---
Number of possible words: 34
Known positions (Green): C _ _ _ _
Present letters (Yellow): R
Absent letters (A, E, N)
Suggested guess: CROST
...
```

## Files

- `words.txt` - A comprehensive list of 5-letter English words
- `past_used_words.txt` - A list of words that have already been used in past Wordle puzzles
  - This list can be updated as new puzzles are released
  - Words from this list won't be suggested, ensuring you only get viable answers
- `wordle_solver.py` - Command-line interface for the solver
- `wordle_solver_gui.py` - Graphical user interface for the solver (requires Tkinter)

## Requirements

- Python 3.6 or higher
- Tkinter (included with most Python installations) for the GUI version

## Technical Details

- Written in Python 3
- Uses letter frequency analysis and positional scoring for optimal suggestions
- Handles complex edge cases with duplicate letters
- Automatically excludes past Wordle answers to improve suggestion accuracy
- GUI built with Tkinter for cross-platform compatibility

## Tips

- The first guess is important! The solver suggests words that have common letters in diverse positions
- Words with duplicate letters (like 'SPEED') provide less information than words with 5 unique letters
- If the solver doesn't find a solution, check if you entered the feedback correctly
- For the best chance of success, always use the suggested guesses 