from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

difficulty = "hard"  # default


# ---------------- GAME LOGIC ----------------
def check_winner_for_board(b):
    winning_combinations = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for combo in winning_combinations:
        a, b1, c = combo
        if b[a] == b[b1] == b[c] and b[a] != "":
            return b[a]
    if "" not in b:
        return "Draw"
    return None


# ---------- MINIMAX ----------
def minimax(b, is_maximizing):
    result = check_winner_for_board(b)

    if result == "O":
        return 1
    elif result == "X":
        return -1
    elif result == "Draw":
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(9):
            if b[i] == "":
                b[i] = "O"
                score = minimax(b, False)
                b[i] = ""
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(9):
            if b[i] == "":
                b[i] = "X"
                score = minimax(b, True)
                b[i] = ""
                best_score = min(score, best_score)
        return best_score


def best_move_for_board(board):
    best_score = -float("inf")
    move = None

    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(board, False)
            board[i] = ""

            if score > best_score:
                best_score = score
                move = i

    return move


# ---------- EASY ----------
def random_move_for_board(board):
    empty = [i for i, v in enumerate(board) if v == ""]
    return random.choice(empty) if empty else None


# ---------- MEDIUM ----------
def medium_move_for_board(board):
    if random.random() < 0.5:
        return best_move_for_board(board)
    else:
        return random_move_for_board(board)


# ---------- DIFFICULTY SWITCH ----------
def get_computer_move_for_board(board):
    if difficulty == "easy":
        return random_move_for_board(board)
    elif difficulty == "medium":
        return medium_move_for_board(board)
    else:
        return best_move_for_board(board)


# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/tic-tac-toe")
def tic_tac_toe():
    return render_template("index.html")


@app.route("/set_difficulty", methods=["POST"])
def set_difficulty():
    global difficulty
    data = request.json
    difficulty = data.get("level", "hard")
    return jsonify({"message": f"Difficulty set to {difficulty}"})


# 🎮 Move API (STATELESS)
@app.route("/move", methods=["POST"])
def move():
    data = request.json
    board = data["board"]   # ✅ get board from frontend
    position = data["position"]

    if board[position] == "":
        board[position] = "X"

        winner = check_winner_for_board(board)
        if winner:
            return jsonify({"status": "win", "winner": winner, "board": board})

        comp_pos = get_computer_move_for_board(board)
        if comp_pos is not None:
            board[comp_pos] = "O"

        winner = check_winner_for_board(board)
        if winner:
            return jsonify({"status": "win", "winner": winner, "board": board})

    return jsonify({"status": "continue", "board": board})


# 🔄 Reset (now optional, frontend handles it)
@app.route("/reset", methods=["POST"])
def reset():
    return jsonify({"board": [""] * 9})


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)