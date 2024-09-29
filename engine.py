Here’s a detailed README in markdown format for your chess engine project, assuming the repository will be named "ChessAI-Engine":

```markdown
# ChessAI-Engine

This repository hosts a lightweight chess engine capable of evaluating board positions and selecting optimal moves using a combination of piece-square evaluation tables and the Alpha-Beta pruning algorithm. The engine is also equipped with a transposition table to optimize performance by caching previously evaluated positions.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Code Overview](#code-overview)
- [Future Enhancements](#future-enhancements)
- [License](#license)

## Introduction

**ChessAI-Engine** is a Python-based chess engine that simulates gameplay using intelligent board evaluation techniques. It integrates piece-square tables for position evaluation and employs the Alpha-Beta pruning algorithm for efficiently selecting the best moves. Additionally, a quiescence search is included to avoid common pitfalls, such as the horizon effect, and a transposition table is used to store previously computed evaluations, reducing redundant calculations.

## Features

- **Piece-Square Tables**: Predefined evaluation charts for different pieces are used to score board positions, enhancing the engine’s decision-making.
- **Alpha-Beta Pruning**: A classic algorithm used to optimize the search tree, speeding up move selection by eliminating branches that cannot influence the final decision.
- **Transposition Table**: A caching mechanism that saves the evaluations of previously encountered positions to improve performance.
- **Quiescence Search**: A technique that ensures better evaluation by searching deeper into captures and threats, preventing shallow tactical blunders.
- **Random Move Generator**: A simple method for generating random legal moves for testing or fun gameplay.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/Shashwat1729/ChessAI-Engine.git
    cd ChessAI-Engine
    ```

2. **Install Required Dependencies**:
    The engine relies on the `python-chess` library, which you can install via pip:
    ```bash
    pip install python-chess
    ```

3. **Optional**: To explore deeper optimizations or debugging features, you might want to install additional tools like `numpy` for faster matrix operations (not required for basic use).

## Usage

You can use the chess engine to play games, evaluate positions, or integrate it into your own projects.

1. **Run the Engine**:
    To start evaluating positions and make moves, instantiate the `group1` class with your chosen color:
    ```python
    import chess
    from engine import group1  # Assuming your main code is in a file named engine.py

    # Initialize a chess board
    board = chess.Board()

    # Create an AI engine instance for white
    engine = group1("white")

    # Get the engine's move
    move = engine.makemove(board)

    # Apply the move to the board
    board.push_uci(move)
    ```

2. **Board Evaluation**:
    You can also evaluate any board position by using the `evaluate_board` function:
    ```python
    eval_score = engine.evaluate_board(board)
    print(f"Board Evaluation Score: {eval_score}")
    ```

3. **Random Move Selection**:
    Use the `get_move` method to get a random move from the legal options on the board:
    ```python
    random_move = engine.get_move(board)
    print(f"Random Move: {random_move}")
    ```

## Project Structure

```plaintext
ChessAI-Engine/
│
├── engine.py           # Core chess engine code, including evaluation and move generation
├── README.md           # This readme file
├── LICENSE             # License file
└── requirements.txt    # Required libraries for the project
```

## Code Overview

### Piece Evaluation Charts

Each chess piece has an associated evaluation chart, which assigns different scores based on their positions on the board. These charts help the engine understand the relative value of a piece depending on its location.

Example: 
```python
pawn_chart = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    ...
]
```

### Transposition Table

To avoid redundant calculations, the engine implements a transposition table. It stores previously computed board evaluations, so positions that have already been analyzed can be quickly reused.

```python
class TranspositionTable:
    def __init__(self):
        self.table = {}

    def lookup(self, key):
        return self.table.get(key)

    def store(self, key, value):
        self.table[key] = value
```

### Alpha-Beta Pruning

Alpha-beta pruning optimizes the decision-making process by trimming branches in the game tree that won’t affect the outcome, reducing the number of board positions that need to be evaluated.

```python
def alphabeta(self, alpha, beta, depthleft, board):
    if depthleft == 0:
        return self.quiesce(alpha, beta, board)

    for move in board.legal_moves:
        board.push(move)
        score = -self.alphabeta(-beta, -alpha, depthleft - 1, board)
        board.pop()

        alpha = max(alpha, score)
        if alpha >= beta:
            return alpha  # Beta cutoff
    return alpha
```

### Quiescence Search

The quiescence search helps the engine avoid horizon effects by extending the search for unstable positions, such as those involving captures.

```python
def quiesce(self, alpha, beta, board):
    stand_pat = self.evaluate_board(board)
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -self.quiesce(-beta, -alpha, board)
            board.pop()

            alpha = max(alpha, score)
            if alpha >= beta:
                return alpha  # Beta cutoff
    return alpha
```

### Move Generation

The `select_move` function implements move selection based on the evaluation of the board after each legal move. The engine selects the move with the highest evaluation score.

```python
def select_move(self, board):
    best_move = None
    best_value = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    for move in board.legal_moves:
        board.push(move)
        board_value = -self.alphabeta(-beta, -alpha, 2, board)
        board.pop()

        if board_value > best_value:
            best_value = board_value
            best_move = move
        alpha = max(alpha, board_value)

    return best_move
```

## Future Enhancements

- **Search Depth Optimization**: Introduce iterative deepening to improve search depth dynamically based on the game state.
- **Endgame Knowledge**: Add specific endgame strategies for more accurate evaluation in the late game.
- **Multi-threading**: Optimize the engine to support parallel move evaluation for faster decision-making.
- **Opening Book**: Implement a predefined opening book for stronger initial moves.
- **GUI Integration**: Connect the engine to a graphical interface for more user-friendly gameplay.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

You can adjust the repository name and other project-specific details as needed. This README provides a comprehensive overview of the chess engine project, from installation to detailed explanations of core components.
