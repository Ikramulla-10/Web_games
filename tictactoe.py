import tkinter as tk
import random

# --- Game State ---
board = ['' for _ in range(9)]
current_player = 'X'
game_over = False
mode = 'AI'  # 'AI' or '2P'
difficulty = 'Hard'  # Easy, Medium, Hard

# --- GUI ---
root = tk.Tk()
root.title("Tic Tac Toe - AI & 2 Player")
root.geometry("400x500")

buttons = []

win_conditions = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # cols
    [0, 4, 8], [2, 4, 6]              # diagonals
]

# --- Game Logic ---
def check_winner(brd):
    for line in win_conditions:
        if brd[line[0]] == brd[line[1]] == brd[line[2]] != '':
            return brd[line[0]]
    if '' not in brd:
        return 'Draw'
    return None

def minimax(brd, is_max):
    result = check_winner(brd)
    if result == 'O':
        return 1
    elif result == 'X':
        return -1
    elif result == 'Draw':
        return 0

    if is_max:
        best = -float('inf')
        for i in range(9):
            if brd[i] == '':
                brd[i] = 'O'
                score = minimax(brd, False)
                brd[i] = ''
                best = max(score, best)
        return best
    else:
        best = float('inf')
        for i in range(9):
            if brd[i] == '':
                brd[i] = 'X'
                score = minimax(brd, True)
                brd[i] = ''
                best = min(score, best)
        return best

def best_ai_move(level):
    empty_cells = [i for i in range(9) if board[i] == '']

    if level == 'Easy':
        return random.choice(empty_cells)

    elif level == 'Medium':
        # 50% smart, 50% random
        if random.random() < 0.5:
            return random.choice(empty_cells)
        # else do hard move

    # Hard: minimax
    best_score = -float('inf')
    move = None
    for i in range(9):
        if board[i] == '':
            board[i] = 'O'
            score = minimax(board, False)
            board[i] = ''
            if score > best_score:
                best_score = score
                move = i
    return move

def handle_click(i):
    global current_player, game_over

    if board[i] == '' and not game_over:
        board[i] = current_player
        update_buttons()

        result = check_winner(board)
        if result:
            end_game(result)
            return

        if mode == '2P':
            current_player = 'O' if current_player == 'X' else 'X'
            status_label.config(text=f"{current_player}'s turn")
        else:
            if current_player == 'X':
                ai_move = best_ai_move(difficulty)
                if ai_move is not None:
                    board[ai_move] = 'O'
                    update_buttons()
                    result = check_winner(board)
                    if result:
                        end_game(result)
                    else:
                        current_player = 'X'

def update_buttons():
    for i in range(9):
        buttons[i].config(text=board[i])

def end_game(winner):
    global game_over
    game_over = True
    if winner == 'Draw':
        status_label.config(text="It's a draw!")
    else:
        status_label.config(text=f"{winner} wins!")

def restart_game():
    global board, current_player, game_over
    board = ['' for _ in range(9)]
    game_over = False
    current_player = 'X'
    for btn in buttons:
        btn.config(text='', state='normal')
    status_label.config(text=f"{current_player}'s turn")

# Mode and Difficulty dropdowns
def update_mode(new_mode):
    global mode
    mode = new_mode
    restart_game()

def update_difficulty(new_level):
    global difficulty
    difficulty = new_level
    restart_game()

title_label = tk.Label(root, text="Tic Tac Toe", font=("Helvetica", 20))
title_label.pack(pady=10)

# Mode selection
mode_frame = tk.Frame(root)
mode_frame.pack()
tk.Label(mode_frame, text="Mode:").pack(side='left')
mode_var = tk.StringVar(value='AI')
tk.OptionMenu(mode_frame, mode_var, 'AI', '2P', command=update_mode).pack(side='left')

# Difficulty selection
difficulty_frame = tk.Frame(root)
difficulty_frame.pack()
tk.Label(difficulty_frame, text="Difficulty:").pack(side='left')
difficulty_var = tk.StringVar(value='Hard')
tk.OptionMenu(difficulty_frame, difficulty_var, 'Easy', 'Medium', 'Hard', command=update_difficulty).pack(side='left')

# Board buttons
frame = tk.Frame(root)
frame.pack(pady=10)
for i in range(9):
    btn = tk.Button(frame, text='', width=5, height=2, font=('Helvetica', 24),
                    command=lambda i=i: handle_click(i))
    btn.grid(row=i//3, column=i%3)
    buttons.append(btn)

# Status and Restart
status_label = tk.Label(root, text="X's turn", font=("Helvetica", 14))
status_label.pack(pady=10)

restart_button = tk.Button(root, text="🔁 Restart", command=restart_game, font=("Helvetica", 12))
restart_button.pack(pady=5)

restart_game()
root.mainloop()