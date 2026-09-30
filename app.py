from flask import Flask, request, jsonify, render_template
import random

app = Flask(__name__)

ROWS, COLS = 6, 7

# ─────────────────────────────
# Drop piece in column
# ─────────────────────────────
def drop(board, col, piece):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == 0:
            board[r][col] = piece
            return True
    return False

# ─────────────────────────────
# Check win
# ─────────────────────────────
def check_win(board, p):
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == p for i in range(4)):
                return True

    # Vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r+i][c] == p for i in range(4)):
                return True

    # Diagonal /
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r-i][c+i] == p for i in range(4)):
                return True

    # Diagonal \
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == p for i in range(4)):
                return True

    return False

# ─────────────────────────────
# Get valid columns
# ─────────────────────────────
def valid_cols(board):
    return [c for c in range(COLS) if board[0][c] == 0]

# ─────────────────────────────
# AI move (simple but smart enough)
# ─────────────────────────────
def ai_move(board):
    valid = valid_cols(board)

    # 1. Try winning move
    for c in valid:
        temp = [row[:] for row in board]
        drop(temp, c, 2)
        if check_win(temp, 2):
            return c

    # 2. Block player win
    for c in valid:
        temp = [row[:] for row in board]
        drop(temp, c, 1)
        if check_win(temp, 1):
            return c

    # 3. Prefer center
    if 3 in valid:
        return 3

    # 4. Otherwise random
    return random.choice(valid) if valid else None

# ─────────────────────────────
# Routes
# ─────────────────────────────

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    board = data['board']
    col = data['col']

    # Player move
    if col not in valid_cols(board):
        return jsonify({'board': board, 'winner': 0})

    drop(board, col, 1)

    if check_win(board, 1):
        return jsonify({'board': board, 'winner': 1})

    if not valid_cols(board):
        return jsonify({'board': board, 'winner': 0})

    # AI move
    ai_col = ai_move(board)
    if ai_col is not None:
        drop(board, ai_col, 2)

        if check_win(board, 2):
            return jsonify({'board': board, 'winner': 2})

    return jsonify({'board': board, 'winner': 0})

# ─────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)